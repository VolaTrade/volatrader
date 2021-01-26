import os
from enum import Enum
import time
import datetime
from termcolor import colored
from Helpers.Constants.Enums import SessionType, Pair, Candle
from Trader.SellLogic import Instance
from Helpers.Logger import logDebugToFile, logToSlack, Channel, logErrorToFile
from Helpers.TimeHelpers import convertNumericTimeToString, getTimeStampOfDayBefore
from DataBasePY.DBwriter import DBwriter
from Strategies.Strategies import strategy
from typing import Dict, List, Union, Tuple


class TradeSession:
    """  
    Class to hold buying and selling logic and execute each accordingly to price updates
    """

    def __init__(self, pair: Pair, candleSize: Candle, buyStrategy: strategy, takeProfit: float, slValue: float,
                 stratString: str, sessionType=SessionType.BACKTEST, principle=1000, sessionid=None, console=True):
        self.pair: Pair = pair
        self.candleSize: Candle = candleSize
        self.sellStrat: Instance = Instance()
        self.sl: int = slValue
        self.sellStrat.setStopLossPercent(slValue)
        self.profitlosses: list = []
        self.stratString: str = stratString
        self.bought: bool = False
        self.buyPrice: int = None
        self.buyTime: int = None
        self.sellTime: int = None
        self.takeProfit: float = takeProfit  #percent 
        self.takeProfitScalar: float = self.getTakeProfitScalar(self.takeProfit)  #what we multiply by 
        self.sellPrice: float = None
        self.profitLoss: float = None
        self.quantity: float = None
        self.STRATEGY: strategy = buyStrategy
        self.results: List[Dict[str, str]] = []
        self.positiveTrades: int = 0
        self.NegativeTrades: int = 0
        self.type: SessionType = sessionType
        self.prevcandle: Dict[str, Union[float, int, str]]  = None
        self.fee: float = .1 / 100
        self.calcWithFee = lambda price: price * float(1 - self.fee)
        self.totalFees: List[float] = []
        self.principle: float = principle
        self.principleOverTime: List[float] = []
        self.writer = DBwriter()
        self.sessionid: Union[str, None] = sessionid
        self.startTime: str = None
        self.finishTime: str = None
        self.dailyCloses: Dict[str, float]  = {}
        self.day: str = None 
        self.console: bool = console
        self.openClose: dict = {}
        self.takeProfitValue = 0 

    def getTotalFees(self) -> float:
        return sum(self.totalFees)

    def checkDailyPriceCloseChange(self, candle: Dict[str, Union[str, int, float, datetime.datetime]]) -> None:
        assert isinstance(candle['timestamp'], int) or isinstance(candle['timestamp'], datetime.datetime), "Timestamp is not of integer type"

        if isinstance(candle['timestamp'], datetime.datetime):
            day = str(candle['timestamp'].date())
        else:
            day = datetime.datetime.fromtimestamp(candle['timestamp']/1000).strftime('%Y-%m-%d')

        if self.day is None:
            self.day = day
            return

        if day != self.day:
            self.dailyCloses[self.day] = candle['close']
            self.day = day


    def getAccuracy(self) -> float:
        return self.positiveTrades / self.getTotalTrades()

    def getCurrentPnl(self, currentPrice: float) -> float:
        allPnl = self.profitlosses.copy()
        print("PNL LIST --->", allPnl)
        print("Buy Price --->", self.buyPrice)
        print("Current Price --> ", currentPrice)
        if self.buyPrice != 0:
            currentPnl = 100 * (currentPrice - self.buyPrice) / self.buyPrice
            allPnl.append(currentPnl)

        try:
            return sum(allPnl)

        except Exception as e:
            logErrorToFile(e)

    def getStopLossPercent(self) -> int:
        """
        :returns: Percent stop loss
        """
        return self.sellStrat.percentStopLoss

    def getTakeProfitPercent(self) -> int:
        """
        :returns: percent take profit
        """
        return self.takeProfit

    def getTradeData(self) -> Tuple[int, int]:
        """
        @returns # of winning and # of losing trades
        """
        return self.positiveTrades, self.NegativeTrades

    def addResult(self) -> None:
        """
        Adds trade result to results list
        updates winning and losing trade counts
        @:returns None
        """
        if self.type is SessionType.LIVETRADE:
            return
        self.results.append({"buytime": convertNumericTimeToString(self.buyTime), "buyprice": self.buyPrice,
                             "selltime": convertNumericTimeToString(self.sellTime),
                             "sellprice": self.sellPrice, "profitloss": self.profitLoss})

        if self.profitLoss > 0:
            self.positiveTrades += 1
        else:
            self.NegativeTrades += 1

    def reset(self) -> None:
        """
        reset function to reset class members after selling
        """
        self.addResult()
        self.sellStrat.reset()
        self.bought = False
        self.buyPrice = 0
        self.sellPrice = 0
        self.profitLoss = None
        self.quantity = 0

    def calcPL(self) -> None:
        """
        Calculate profit loss function
        @:returns None
        """
        self.profitLoss = (100 - (100 * (self.buyPrice / self.sellPrice))) if self.sellPrice > self.buyPrice else -(
                100 - (100 * (self.sellPrice / self.buyPrice)))


    def toString(self) -> str:
        """
        toString method
        @:returns toString representation of Session instance
        """

        return f"Buy Price {self.buyPrice} Buy Time: {(self.buyTime)} \nSell Price {self.sellPrice} Sell time: {self.sellTime}\nProfit Loss: {self.profitLoss}\n"

    def getTotalPL(self) -> float:
        """
        @:returns total profit-loss percentage after running strategy
        """
        return sum(self.profitlosses)

    def CHECK_STOPLOSS(self, candle: Dict[str, Union[str, int, float]]) -> bool:
        return self.sellStrat.run(float(candle['close']))

    def CHECK_TAKEPROFIT(self, candle: Dict[str, Union[str, int, float]]) -> bool:
        return self.takeProfitValue <= float(candle['close'])

    def buyUpdate(self, candle: Dict[str, Union[str, int, float]]) -> None:
        """
        updates session w/ buy data
        """
        self.bought = True
        self.buyPrice, self.buyTime = candle['close'], candle['timestamp']
        self.quantity = self.principle / self.buyPrice
        self.totalFees.append(self.fee * self.principle)

        if self.type is not SessionType.BACKTEST:
            typ = "[PAPERTRADE]" if self.type is SessionType.PAPERTRADE else "[LIVETRADE]"
            id = f"{typ}[{self.stratString}/{self.candleSize.value}/{self.pair.value}][{self.sessionid}] "
            msg = f"{id}\nBuying at price: {self.buyPrice}"
            print(msg)

    def sellUpdate(self, candle: Dict[str, Union[str, int, float]]) -> None:
        """
        updates session w/ sell data
        """
        self.sellPrice, self.sellTime = float(candle['close']), candle['timestamp']
        self.totalFees.append(self.fee * self.principle)
        self.calcPL()
        if self.type is not SessionType.BACKTEST:
            logToSlack(f"TRADE COMPLETE [{self.stratString}][{self.pair.value}][{self.stratString}] \nResults:\n{self.toString()}", channel=Channel.PAPERTRADER)

        else:
            if self.console:
                print(colored("--------------------------\n" + self.toString() + "--------------------------",
                            'green') if self.profitLoss > 0 else colored(
                    "--------------------------\n" + self.toString() + "--------------------------", 'red'))
        self.profitlosses.append(self.profitLoss)
        self.reset()
        if self.type is SessionType.PAPERTRADE:
            # write new transaction to
            results = self.getResults()["tradeResults"]
            logDebugToFile(f"results {results}")
            self.writer.writeTransactionData(results, self.sessionid)

    def checkBuy(self, candle: Dict[str, Union[str, int, float]]) -> bool:
        self.principleOverTime.append(self.principle)
        if self.prevcandle is None or self.prevcandle['timestamp'] != candle['timestamp']:
            return self.STRATEGY.checkBuy(candle)

        return None

    def calculateTakeProfit(self) -> None:
        self.takeProfitValue = float(self.buyPrice) * self.takeProfitScalar
 
    def checkSell(self, candle: Dict[str, Union[str, int, float]]) -> bool:
        self.calculateTakeProfit()
        self.principle = self.calcWithFee(candle['close']) * self.quantity
        self.principleOverTime.append(self.principle)
        sl, tp, cs = self.CHECK_STOPLOSS(candle), self.CHECK_TAKEPROFIT(candle), self.STRATEGY.checkSell(candle)
        return  sl or tp or cs

    def update(self, candle: Dict[str, Union[str, int, float]], update: bool=True) -> bool:
        """
        main function
        @:param candle
        takes in @:param candle and makes buy/sell or do-nothing decisions accordingly
        @:returns None
        """

        self.checkTimeUpdate(candle)
        if self.startTime is None:
            self.startTime = candle['timestamp']
        self.finishTime = candle['timestamp']

        self.checkDailyPriceCloseChange(candle)

        if update:
            if self.STRATEGY.interValUpdate(candle) is False:
                return None 

        takeprofit_scalar, sl_scalar = self.STRATEGY.checkTakeProfitScale(), self.STRATEGY.checkStopLossScale()

        if takeprofit_scalar is not False:
            self.takeProfitScalar = takeprofit_scalar * self.takeProfitScalar
            self.calculateTakeProfit()

        if sl_scalar is not False:
            self.sl = sl_scalar * self.sl
            self.sellStrat.setStopLossPercent(self.sl)

        if not self.bought:  # not bought
            if self.checkBuy(candle):
                self.prevcandle = candle
                self.buyUpdate(candle)
                return True

        else:  # is bought

            if self.checkSell(candle): #Time to sell
                self.prevcandle = candle
                self.sellUpdate(candle)
                return False

        self.prevcandle = candle
        return None

    def getTotalTrades(self) -> int:
        """
        @:returns count of total trades
        """
        return len(self.profitlosses)

    def getPrincipleList(self) -> list:
        return self.principleOverTime

    def getResults(self) -> dict:
        """
        @:returns results in a dictionary that hold buytime, buyprice, selltime, sellprice, profitloss
        """
        return {
            "pair": self.pair.value,
            "tradeResults": self.results
        }

    def getDailyCloses(self) -> Dict[str, float]:
        return self.dailyCloses

    def checkTimeUpdate(self, candle):

        ts = convertNumericTimeToString(candle['timestamp'])
        date, time = ts[0 : 10], ts[11 : len(ts)]

        if time == "12:00:00":
            self.openClose[date] = {"open": candle['close'], "close": None}

        elif time == "00:00:00":

            prior_day = getTimeStampOfDayBefore(candle['timestamp'])[0 : 10]

            if prior_day in self.openClose.keys():
                print("prior day ---> ", prior_day)
                self.openClose[prior_day]['close'] = candle['close']

    def getTakeProfitScalar(self, takeProfit: Union[float, int]) -> Union[float, int]:
        
        takeProfit = float(takeProfit)
        if takeProfit < 10:
            takeProfit = str(takeProfit).replace(".", "")
            return float(f"1.0{takeProfit}")

        else:
            takeProfit = str(takeProfit).replace(".", "")
            return float(f"1.{takeProfit}")
    