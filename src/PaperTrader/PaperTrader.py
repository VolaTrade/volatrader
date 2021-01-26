import os
import sys
import time
import datetime
from Helpers.Logger import logToSlack, logDebugToFile, logErrorToFile, MessageType, Channel
from Trader.TradeSession import TradeSession
from Helpers.Constants.Enums import Pair, Candle, SessionType, Time, Market
from DataBasePY.DBReader import DBReader
from DataBasePY.DBwriter import DBwriter
from Strategies import Strategies
from Helpers.DataOperators import fetchCandleData, convertCandlesToDict
from Helpers.API.MarketFunctions import getCurrentBinancePrice
import ccxt
import re
import uuid
import json
from typing import Dict, List, Tuple, Union
import traceback
from Telegram import messages 

float_format = lambda number: float("{:.2f}".format(number))

class PaperTrader:

    def __init__(self, pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: int, takeProfitPercent: int,
              principle: int, timeToRun: Time, uid):
        
        self.writer = DBwriter()
        self.reader = DBReader()
        self.stratName = strategy
        self.strategy = Strategies.getStrat(self.stratName)(pair, candleSize, principle)
        self.strategy.initialize()
        self.timeStep: int = int(re.sub("[^0-9]", "", candleSize.value))
        self.pair = pair
        self.candleSize = candleSize
        self.takeProfitPercent = f"0{takeProfitPercent}" if takeProfitPercent - 10 <= 0 else f"{takeProfitPercent}"  #TODO there's gotta be a better way of doing this 
        self.stopLossPercent = stopLossPercent
        self.sessionid = uid
        self.tradingSession = TradeSession(pair, self.candleSize, self.strategy, takeProfitPercent,
                                           self.stopLossPercent, self.stratName,
                                           SessionType.PAPERTRADE, sessionid=self.sessionid)
        self.currentPrice: float  = None

        self.principle = principle
        self.timeToRun = timeToRun
        self.isTimeToUpdate = lambda minute: minute % self.timeStep == 0 or minute == 0
        self.isProfitUpdate = lambda  minute: (minute % 2 == 0 or minute == 0) and self.currentPrice is not None
        self.getEndTime =  lambda timeToRun: datetime.datetime.now() + datetime.timedelta(hours=timeToRun)
        self.startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.isMegna = False 
        
    def getResults(self) -> str:
        return self.tradingSession.getResults()

    def writeUpdate(self) -> Union[None, Exception]:
        
        if self.currentPrice is not None:
            current_pnl = self.tradingSession.getCurrentPnl(self.currentPrice)
            print("Current profit net loss ----------_>", current_pnl)


        else:
            print("Current price ....", self.currentPrice)
            current_pnl = 0
        with open(f"{self.sessionid}.json", "w") as file_write:
            json.dump({"session_id": self.sessionid,"session_start_time": self.startTime, "strategy": self.stratName, "running_on": os.environ.get("DATABASE_NAME"), "pair": self.pair.value, "candle": self.candleSize.value, "total_pnl": current_pnl, "principle": self.principle}, file_write)
            

           
    def preinstall(self, candles: list, stratUpdate) -> None:

       
        for candle in candles:
            logDebugToFile(candle, sessionId=self.sessionid)
            stratUpdate(candle)
        logDebugToFile("Preinstall successfull")

          

    def profitUpdate(self, minute: int, bought: bool):
        
        if self.isProfitUpdate(minute):
            currentpnl = self.tradingSession.getCurrentPnl(self.currentPrice)
            logDebugToFile(f'PNL being written ---- > {currentpnl}{type(currentpnl)}', sessionId=self.sessionid)
            print(f"principle --------> {self.principle}")

            try:
                self.writer.writeTotalPnl(float_format(currentpnl), self.principle, self.sessionid)
                logDebugToFile("PNL written", self.sessionid)

            except Exception as e:
                logToSlack(f"[{e}]{traceback.format_exc()}", messageType=MessageType.ERROR)


    def writeTransactionData(self):
        self.writer.writeTransactionData(self.tradingSession.results, self.sessionid)

        
    def initialize(self) -> None:
        print("strategy intitialization limit ----------------------------------------->", int(self.strategy.candleLimit))
        try:
            candles: List[Dict[str, Union[str, float, int]]] = convertCandlesToDict(
                fetchCandleData(
                    ccxt.binance(),
                    self.pair,
                    self.candleSize,
                    limit = int(self.strategy.candleLimit)
                )
            )
            logDebugToFile(
            f"starting preinstall for {self.stratName} with {self.pair}/{self.candleSize} & candle-limit = {self.strategy.candleLimit}", sessionId=self.sessionid)
            self.preinstall(candles, self.tradingSession.STRATEGY.interValUpdate)

        except Exception as e:
            logErrorToFile(e)

    def writeStart(self) -> None:
        try:
            logDebugToFile(f"Writing data to db for paper trader session {self.sessionid}")
            self.writer.writePaperTradeStart(
                self.sessionid,
                datetime.datetime.now(),
                self.stratName,
                self.pair,
                self.candleSize,
                self.principle,
                self.stopLossPercent,
                self.takeProfitPercent
            )
        except Exception as e:
            logErrorToFile(f"[{self.sessionid}]Error writing to postgres")
            raise e

  

    def fetchMostRecentCandle(self) -> dict: #both methods are fortunately unit tested
        return convertCandlesToDict(fetchCandleData(ccxt.binance(), self.pair, self.candleSize, 1))[0]
        
    def buyUpdate(self, minute: int, trade_session,  fetch_candle, logToSlack=logToSlack, logDebugToFile=logDebugToFile, time=time, test=False) -> bool:

        try:
            candle: Dict[str, Union[str, float, int]] =  fetch_candle()
        except Exception as e:
            logToSlack(f"[{e}]{traceback.format_exc()}", messageType=MessageType.ERROR)
            return None 

        logDebugToFile(f"Interval update with {candle}")
        bought = trade_session.update(candle, True)
        logDebugToFile(f"bought status ->{bought}", sessionId=self.sessionid)

        if bought and not test:
            self.tradingSession.calculateTakeProfit()
            sl = self.tradingSession.sellStrat.slValFunc(self.tradingSession.buyPrice)
            messages.wrapMessage(self.pair, self.candleSize, Market.BINANCE, sl, self.tradingSession.takeProfitValue, self.sessionid)

        return bought

    def sellUpdate(self, session, getCurrentBinancePrice=getCurrentBinancePrice, logToSlack=logToSlack, logDebugToFile=logDebugToFile, time=time) -> bool:
        try:
            price, _ = getCurrentBinancePrice(self.pair)
            print("PRICE ", price)
            assert isinstance(price, float)
        
        except Exception as e:
            logToSlack(f"[{self.sessionid}][{e}]{traceback.format_exc()}", messageType=MessageType.ERROR)
            return None
        self.currentPrice = price
        print(self.currentPrice)
        ts = datetime.datetime.now()
        logDebugToFile(f"Checking for sell w/ {self.pair} @ {self.currentPrice}", sessionId=self.sessionid)
        dummyCandle = {"close": self.currentPrice, "timestamp": ts}
        logDebugToFile(dummyCandle) 
        return session.update(dummyCandle, False)


    def run(self) -> None:
        try:
            first: bool = True
            bought: bool = None
            end_time = self.getEndTime(self.timeToRun)

            logToSlack(
                f"[PAPERTRADER][{self.sessionid}] Starting Paper Trader for {self.pair.value}/{self.candleSize.value} \nstrat: {self.stratName}\n takeprofit: %{float(self.takeProfitPercent)}\n stoploss: %{float(self.stopLossPercent)}\n Finishing on {end_time}",
                channel=Channel.PAPERTRADER)
            
            self.writeUpdate()

            while datetime.datetime.now() < end_time:

                if self.isMegna:
                    raise Exception("I have been megna'd")

                minute: int = datetime.datetime.now().minute 
                if first:
                    first = False
                    self.initialize()
                    self.writeStart()

                if self.isTimeToUpdate(minute) and(bought is False or bought is None):
                    bought = self.buyUpdate(
                                        minute,
                                        self.tradingSession, 
                                        self.fetchMostRecentCandle, 
                                        )

                if bought:
                    update = self.sellUpdate(self.tradingSession)

                    if update is not None:
                        bought = update

                    if bought is False:  #just sold, time to write the finished transaction data 

                        tracked_users = self.reader.getTrackingUsers(self.sessionid)
                        print(tracked_users)
                        print("sending exit notifs")
                        messages.sendTradeExit(tracked_users, self.sessionid)
                        self.writeTransactionData()
                        self.profitUpdate(minute, bought)


                    self.writeUpdate()



            logToSlack(f"[{self.sessionid}] I HAVE COMPLETED")
       
            
        except Exception as e:
            logToSlack(f"[{e}][{self.sessionid}]{traceback.format_exc()}", messageType=MessageType.ERROR)
            self.writer.writePaperTradeEnd(self.sessionid)
            raise e
        except KeyboardInterrupt:
            self.writer.writePaperTradeEnd(self.sessionid)
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
