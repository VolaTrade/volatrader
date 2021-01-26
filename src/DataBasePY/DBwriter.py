import datetime
import time
import os
from Helpers.Constants.Enums import Candle, Pair, Indicator
from Helpers.API.CMC_api import getMarketData, getMacroEconomicData
from Helpers.DataOperators import truncate
from DataBasePY.DBoperations import DBoperations
import psycopg2
from psycopg2.extras import Json, register_uuid
import json
import ccxt
from Helpers.Logger import logToSlack, MessageType, logDebugToFile, logErrorToFile
from Strategies.Strategies import getStratIndicators
from Helpers.TimeHelpers import convertNumericTimeToString
from BackTest.Result import Result 
from typing import Dict


class DBwriter(DBoperations):
    """
    DataBase writer class to handle data base write operations
    @inherited from DBopertions
    """

    def __init__(self):
        super().__init__()


    def writeVolumeData(self, pair: Pair, candle: Candle, mean: float, sdv: float) -> None:
        query: str = "INSERT INTO STATISTIC_TABLE(pair, candle, mean_volume, volume_sd) VALUES (%s, %s, %s, %s);"
        params: tuple = (pair.value, candle.value, mean, sdv)

        try:
            logDebugToFile(query)
            self.writeExecute(query, params)

        except Exception as e:
            logErrorToFile(e)
            raise e



    def deletePaperTradeSession(self, sessionId: str) -> None:
        query: str = "DELETE FROM papertrader_results WHERE session_id = %s;"
        params: tuple = (sessionId,)
        self.writeExecute(query, params)

    def killPaperTraderSession(self, sessionId=None) -> None:

        if sessionId is not None:
            query: str = "UPDATE papertrader_results set ACTIVE = False WHERE session_id = %s;"
            params: tuple = (sessionId,)

        else:
            query: str = 'UPDATE papertrade_results set ACTIVE = False WHERE running_on = %s;'
            print("KILL PAPER TRADER QUERY")
            params: tuple = (os.environ.get("DATABASE_NAME"))

        self.writeExecute(query, params)

    def writePaperTradeStart(self, sessionId: str, start_time: str, strategy: str, pair: Pair, candle: Candle, principle: float, sl: float, tp: float) -> None:
        """
        Writes initial strategy information when a PaperTrade Session is started
        """
        where = os.environ.get("DATABASE_NAME")
        query = "INSERT INTO papertrader_results (session_id, session_start_time, active, strategy, pair, candle,  principle, running_on, indicators, stoploss, takeprofit) " \
            "VALUES (%s, %s, True, %s, %s, %s, %s, %s, %s, %s, %s);"
        params: tuple = (sessionId, start_time, strategy, pair.value, candle.value, principle, str(where), json.dumps(getStratIndicators(strategy), default=str), sl, tp)


        try:
            self.writeExecute(query, params)

        except Exception as e:
            logErrorToFile(e)
            raise e


    def writePaperTradeEnd(self, sessionId) -> None:
        """
        Writes the time of the paper trade session when the session is completed
        """
        query: str = "UPDATE papertrader_results set session_end_time = %s, active = False WHERE session_id = %s;"
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        params: tuple = (now, sessionId)
        logDebugToFile("Finished paper trader, writing results")

        try:
            self.writeExecute(query, params)
        except Exception as e:
            logDebugToFile("Error writing paper trader end data")
            raise e


    def writeTransactionData(self, results, sessionId) -> None:
        """
        Writes transaction data to jsonb using sessionId as a key
        """

        logDebugToFile("Inserting paper trader results...")
        query: str = "UPDATE papertrader_results SET transactions = %s WHERE session_id = %s;"
        params: tuple = (json.dumps(results, default=str), sessionId)
        logDebugToFile(query)
        try:
            self.writeExecute(query, params)

        except Exception as e:
            logDebugToFile("Error updating transaction data: ")
            raise e


    def writeTotalPnl(self, pnl: float, principle: int, sessionId: str) -> None:
        """
        Writes the total pnl to the database every 5 minutes
        """

        query: str = "UPDATE papertrader_results SET total_pnl = %s WHERE session_id = %s; UPDATE papertrader_results SET principle = %s WHERE session_id = %s;"

        params: tuple = (pnl, sessionId, principle, sessionId)

        logDebugToFile("Writing total pnl to database")
        logDebugToFile(query)
        try:
            self.writeExecute(query, params)

        except Exception as e:
            logErrorToFile("Error updating pnl value")
            raise e
        print("SUCCESSFULLY WROTE PNL")

    def writeSupportResistance(self, pair: Pair, candle: Candle, support: float, resistance: float) -> None:
        """
        writes support resistance to data base
        """
        
        query: str = "INSERT INTO support_resistance (ts, pair, candle, support, resistance) VALUES (%s, %s, %s, %s, %s)\
                ON CONFLICT (pair, candle) DO UPDATE SET support = EXCLUDED.support, resistance = EXCLUDED.resistance, ts = EXCLUDED.ts;"

        params: tuple = (str(datetime.datetime.now()), pair.value, candle.value, support, resistance)
        logDebugToFile(query)
        try:
            self.writeExecute(query, params)

        except Exception as e:
            logErrorToFile("Error writing support resistance")
            raise e


    def writeStrategy(self, strat_name: str, version_num: int, source: str) -> None:
        """
        writes strategy source code into DB 
        """
        query: str = "INSERT INTO STRATEGIES(strategy, version_number, source) VALUES(%s, %s, %s);"

        params: tuple = (strat_name, version_num, source)

        try:
            self.writeExecute(query, params)

        except Exception as e:
            logErrorToFile("Error writing strategy data to database")
            raise e 

    def writeBackTestData(self, result: Result, version_num, time_stamp: str, strat_name: str) -> None:
        """
        Writes backtest result to database table
        """
        query: str = "INSERT INTO BACKTEST_RESULTS(time_stamp, strategy, version, pair, candle, takeprofit, stoploss, indicator_values, timeframe, score, beta_score)\
                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        
        params: dict = {}
        
        for key in result.params:
            if key != "max":
                params[key] = result.params[key]['parameters']
       
        
        params: tuple = (time_stamp, strat_name, version_num, result.pair.value, result.candle.value, result.tp, result.sl, json.dumps(params, default=str), result.time_frame, result.score, result.strat_score_beta)

        print("Current Tuple --------------> ", params)

        try:
            self.writeExecute(query, params)

        except Exception as e:
            logErrorToFile("Error writing backtest data to DB")
            raise e 
