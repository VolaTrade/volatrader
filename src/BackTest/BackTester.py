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


def automatedBacktest(pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: float, takeProfitPercent: float, principle: int, timeStart: Time, darwin_dick: DarwinsDict, skeleton: dict, market=Market.BINANCE,  test=False, paper=None):

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


    if skeleton is not None:
        strategy.skeleton = skeleton
        strategy.candleLimit = strategy.skeleton['max']

    session = TradeSession(pair, candleSize, strategy, takeProfitPercent, stopLossPercent, stratString, SessionType.BACKTEST, console=True if darwin_dick is None else False)
    json_file = f"{pair.value}{candleSize.value}.json"
    print(f"json file -------------> {json_file}")
    if outputConsole:
        print("--------------------------------------------- STARTING BACKTEST -----------------------------------------------------------")
        printLogo(type=SessionType.BACKTEST)

    if (os.path.isfile(json_file) and darwin_dick is not None) or test is True: #only perform caching when automated backtesting is done  ss
        print(f"loading from file ---> {json_file}")
        with open(json_file, "r") as fp:
            candle_data = json.loads(fp.read())

    else:
        candle_data = DataOperators.getCandlesFromTime(convertNumericTimeToString(TimeHelpers.rewind(str(datetime.datetime.now())[0: -7], 60, timeStart.value )), pair, candleSize, market, output=outputConsole)
        print(f"writing to file ------------> {json_file}")

        if darwin_dick is not None: 
            with open(json_file, 'w') as fp:
                json.dump(candle_data, fp)

    return_DF = buildBackTest(candle_data, session, paper)
    pos, _ = session.getTradeData()

    if len(session.results) == 0:
        print("NO trades were made during backtest ---------> Returning")
        return

    if debug:
        print("building result with timeframe ===>", timeStart)
    result = Result(session.pair, session.candleSize, session.sl, session.takeProfit, session.getTotalPL(), (pos/session.getTotalTrades()), session.dailyCloses, session.results, timeStart.name)
    result.buildAnalysis()

    result.setParams(skeleton)

    if debug:
        print(getBacktestResultsString(session))
        print("+===============================================")
        print(result.toString())
    
    #Automation case 
    if session.getTotalTrades() != 0:
        lock.acquire()
        darwin_dick.insert(result)
        os.system('cls' if os.name == 'nt' else 'clear')
        lock.release()
        print(darwin_dick.toString())


def backTest(pair: Pair, candleSize: Candle, strategy: str, stopLossPercent: float, takeProfitPercent: float, principle: int, timeStart: Time, outputConsole=True, outputGraph=True, market=Market.BINANCE, server=False):
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
    
    if outputGraph:
        analysis_directory = "/home/adrian/volatrade-production/src/Server/templates/analysis.html" if os.environ['DATABASE_NAME'] == 'PRODUCTION' else "templates/analysis.html"
        buildHTML(getBacktestResultsString(session, html=True), generateGraphs(return_DF, session), server, analysis_directory)

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
