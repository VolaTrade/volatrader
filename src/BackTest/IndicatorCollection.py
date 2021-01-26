import os 
import sys
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
import re
import copy 
import datetime
from Helpers.TimeHelpers import convertNumericTimeToString
from Trader.TradeSession import TradeSession
from Strategies import Strategies
import subprocess
from Helpers.Constants.Enums import Pair, Candle, Time, Market, Indicator
from Helpers.ArgParser import getParser
from Helpers.DataOperators import printLogo
from Helpers import TimeHelpers
from Helpers import DataOperators
from Strategies.Strategies import strategy 

class INDICATOR_COLLECTOR(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.SMA, Indicator.MOM, Indicator.FIBBOLINGER]
        self.values = []

    def checkBuy(self, candle):
        self.values.append(self.indicators)
        return BUY 
        
    def checkSell(self, candle):
        self.values.append(self.indicators)
        return HOLD 



def IndicatorCollectedBacktest(pair: Pair, candleSize: Candle, timeStart: Time, collector,  market=Market.BINANCE, candle_getter = DataOperators.getCandlesFromTime):


    strategy = collector(pair, candleSize, 10)
    
    strategy.initialize()

    print("--------------------------------------------- STARTING DATA COLLECTION -----------------------------------------------------------")

    candle_data = candle_getter(convertNumericTimeToString(TimeHelpers.rewind(str(datetime.datetime.now())[0: -7], 60, timeStart.value )), pair, candleSize, market, output=True)
    data_rows = []
    starting_price = DataOperators.cleanCandle(candle_data[0])['close']
    for candle in candle_data:
        candle = DataOperators.cleanCandle(candle)

        if strategy.interValUpdate(candle):
            data = {}
            data['timestamp'] = convertNumericTimeToString(candle['timestamp'])
            for key in strategy.indicators.keys():
                for value in strategy.indicators[key].keys():
                    data[f"{key}_{value}"] = strategy.indicators[key][value]
            
            data['pNl'] =  100 * (candle['close'] - starting_price) / starting_price
            data_rows.append(data)
    
    

    for data in data_rows:
        print(data)

if __name__ == '__main__':
    IndicatorCollectedBacktest(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, Time.SIXMONTH, INDICATOR_COLLECTOR)