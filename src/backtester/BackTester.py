import re
import datetime
from Helpers.TimeHelpers import convertNumericTimeToString
from Trader.TradeSession import TradeSession
from Strategies import Strategies
import subprocess
from Helpers.Constants.Enums import Pair, Candle, Time, SessionType, Market
import pandas as pd
import os
from os import path
from Helpers.ArgParser import getParser
from Helpers.DataOperators import printLogo
from Helpers import TimeHelpers
from BackTest.BackTestBuilder import getBacktestResultsString, buildBackTest, buildHTML
from Helpers import DataOperators
from BackTest.GraphBuilder import generateGraphs  
from threading import Lock 
from BackTest.Result import Result
from BackTest.DarwinsDict import DarwinsDict
import json 
lock = Lock()

def backTest(pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: float, takeProfitPercent: float, principle: int, timeStart: Time, outputConsole=True, server=False):
    """
    main backtest function, prints backtest results, outputs graph results to html if desired 
    @:param pair -> pair you wish to run backtest on
    @:param candleSize -> size of candle you wish to use
    @:param strategy -> Buying strategy that you wish to implement
    @:param Stop-Loss percent
    @:param Take profit percent -> percent gain from buy-price at which you wish to sell
    @:param args optional TIME ENUM to specify timeline to test strategy upon
    """
    assert 0 < stopLossPercent < 100
    assert 0 < takeProfitPercent < 100
    assert isinstance(pair, Pair)
    assert isinstance(candleSize, Candle)


    takeProfitPercent = float(f"0{takeProfitPercent}" if takeProfitPercent < 10 else str(takeProfitPercent))
    stratString = strategy
    strategy = Strategies.getStrat(stratString)(pair, candleSize, principle)
    strategy.initialize()

    session = TradeSession(pair, candleSize, strategy, takeProfitPercent, stopLossPercent, stratString, SessionType.BACKTEST, console=True)
    json_file = f"{pair.value}{candleSize.value}.json"

    if outputConsole:
        print("--------------------------------------------- STARTING BACKTEST -----------------------------------------------------------")
        printLogo(type=SessionType.BACKTEST)


    candle_data = DataOperators.getCandlesFromTime(convertNumericTimeToString(TimeHelpers.rewind(str(datetime.datetime.now())[0: -7], 60, timeStart.value )), pair, candleSize, market, output=outputConsole)
    return_DF = buildBackTest(candle_data, session)
    pos, _ = session.getTradeData()

    if len(session.results) == 0:
        print("NO trades were made during backtest ---------> Returning")
        return 


    print("building result with ===>", timeStart)
    result = Result(session.pair, session.candleSize, session.sl, session.takeProfit, session.getTotalPL(), (pos/session.getTotalTrades()), session.dailyCloses, session.results, timeStart.name)
    result.buildAnalysis()

    if skeleton is not None:
        result.setParams(skeleton)
    if outputConsole:
        print(getBacktestResultsString(session))
        print("+===============================================")
        print(result.toString())
    

    #Automation case 
    if session.getTotalTrades() != 0 and darwin_dick is not None:
        lock.acquire()
        darwin_dick.insert(result)
        lock.release()

    return session 

def main(args):
    print("RUNNING BACKTEST WITH ARGS: ", args)
    backTest(args.pair, args.candleSize, args.strategy, args.stoploss, args.takeprofit, args.principle, Time[args.time], readFromDataBase=args.readFromDatabase,  outputGraph=args.outputGraph, market=Market[args.market])

if __name__ == '__main__':
    args = getParser()
    main(args)
