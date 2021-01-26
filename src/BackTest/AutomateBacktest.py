import os 
import sys
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from BackTest.BackTester import automatedBacktest
from BackTest.AutomationHelpers import checkIfStratChanged, buildSkeleton, getAllPossibleIndicatorParamCombos, getIndicatorsList
from Helpers.Constants.Enums import Pair, Candle, Time, Market
from Helpers.SystemHelpers import removeJsonFromDir
import argparse
import subprocess
from BackTest.DarwinsDict import DarwinsDict
from BackTest.Result import Result 
from threading import Thread
from threading import BoundedSemaphore
import time 
from typing import List
from DataBasePY.DBReader import DBReader
from DataBasePY.DBwriter import DBwriter
from Strategies.Strategies import getStratSourceCode, getStratIndicatorNames
from datetime import datetime
from timeit import default_timer as timer 
from threading import Lock 
writer = DBwriter()
reader = DBReader()

maximumNumberOfThreads = 20
threadLimiter = BoundedSemaphore(maximumNumberOfThreads)
threadLock = Lock()
class BacktestWorker(Thread):

    def __init__(self, pair: Pair, candleSize: Candle, strategy: str, sl: int, tp: int, principle: float, sof: DarwinsDict, skeleton: dict, status_list):
        
        super(BacktestWorker, self).__init__()
        self.pair = pair
        self.candleSize = candleSize
        self.strategy = strategy
        self.sl = sl
        self.tp = tp 
        self.principle = principle
        self.SOF = sof
        self.skeleton = skeleton

    def run(self):
        
        threadLimiter.acquire()
        try:
            automatedBacktest(self.pair, self.candleSize, self.strategy, self.sl, self.tp, self.principle, Time["MONTH"], self.SOF, self.skeleton)
        finally:
            threadLimiter.release()




def automateAndVariate(pairs: List[Pair], candleSizes: List[Candle], stopLossRange: int, strategy: str, timeFrame=None, principle=1000) -> None:
    
    key_set: list =  []
    index: int = 0
    running_threads: list = []
    sof: DarwinsDict = DarwinsDict()
    start = time.time()
    total: int = 0 
    start = timer()
    tupleSets = getAllPossibleIndicatorParamCombos(strategy)


    for pair in pairs:    
        for sl in range(stopLossRange):
            sl+= .1
            tp = sl * 2
            for candleSize in candleSizes:
                names = getStratIndicatorNames(strategy)

                for tupleSet in tupleSets: 
                    skeleton = buildSkeleton(tupleSet, getIndicatorsList(names), names)

                    thread = BacktestWorker(Pair(pair), Candle(candleSize), strategy, sl, tp, principle, sof, skeleton, total)
                    key = f"{pair}-{candleSize}"
                    if key not in key_set:
                        key_set.append(key)
                        thread.start()
                        thread.join()

                    else:
                        thread.start()

                    if threadLock.locked():
                        threadLock.release()
                    total += 1 
                    running_threads.append(thread)


                   
    
    _ = [e.join() for e in running_threads]

    end = timer()
    time_passed = start - end 
    print("===================================================================================================")
    print(f"=================================  RAN {total} BACKTESTS IN {time_passed} =========================================")
    print("===================================================================================================")
    print("============================= WRITING BEST RESULTS TO DATABASE ====================================")
    print("===================================================================================================")

    removeJsonFromDir()
    changed, version, source = checkIfStratChanged(strategy)

    if changed:
        version += 1 
        writer.writeStrategy(strategy, version, source)

    elif changed is None:
        version = 0 
        writer.writeStrategy(strategy, version, source)



    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for result in sof.getResults():
        writer.writeBackTestData(result, version, timestamp, strategy)

def main(args):
    print("running w/ args ", args)
    automateAndVariate(args.pairs, args.candles, args.stoploss, args.strategy, args.time, args.principle)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Use this to backtest your strategies")
    parser.add_argument('-p', '--pairs', type=str, required=True, nargs='*',
                    help='Pairs to backtest for. Reference Enums.py for more details')
    parser.add_argument('--candles', '-candleSizes', type=str, required=True, nargs='*',
                    help="Candle size to get data for (5m, 15m, 30m, etc)")
    parser.add_argument('--strategy', '-strat', type=str, required=True,
                    help="Strategy to backtest")
    parser.add_argument('-sl', '--stoploss', type=int, default=1,
                    help="Trailing stop loss percentage")
    parser.add_argument('--principle', '-investment', type=int, default=10000,
                    help="Starting capital")
    parser.add_argument('-t','--time', type=str, default="MONTH",
                    help="Total time to backtest on")
    parser.add_argument("--market", type=str, default="BINANCE",
                    help="Market to be used")

    args = parser.parse_args()

    main(args)

