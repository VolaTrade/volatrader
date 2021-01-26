import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
from Helpers.Constants.Enums import Pair, Candle
from Helpers.TimeHelpers import convertNumericTimeToString
from termcolor import colored
import numpy as np
from Trader.Indicators.IndicatorConstants import getIndicator
from Trader.Indicators.IndicatorFunctions import getFunction
from Helpers import TimeHelpers 
from Trader.TradeSession import TradeSession
from DataBasePY.DBReader import DBReader 
from Helpers import DataOperators 


def buildDataFrame(data: list, backtest: bool=True) -> pd.DataFrame:
    returns = pd.DataFrame(data)

    if backtest:
        returns.index = pd.to_datetime(returns['timestamp'])
        del returns['timestamp']   
    return returns


def updateVal(data: dict, updateValue: bool) -> None:
    if updateValue is True:
        data['buy'], data['sell'] = data['close'], 'NaN'

    elif updateValue is False:
        data['buy'], data['sell'] = 'NaN', data['close']
    else:

        data['buy'], data['sell'] = 'NaN', 'NaN'


bought = False 
sold = False 
def updatePaperValue(data: dict, paper_results: str):
    global bought 
    global sold 

    if bought and sold:
        paper_results.pop(0)
        bought = False 
        sold = False 
    
    if paper_results[0]['buytime'] <= data['timestamp'] and not bought:
        data['buytime'] = paper_results['buyprice']
        bought = True 

    else:
        data['buytime'] = 'NaN'

    if paper_results[0]['selltime'] <= data['timestamp']:
        data['selltime'] = paper_results['sellprice']
        sold = True 

    else:
        data['selltime'] = 'NaN'

       


def buildPaperTradeResults(sessionID: str) -> list:
    return DBReader().getPaperTradeSession(sessionID)


def updatePatternValues(data, candle):

    for key in data:
        if isinstance(data[key], bool):
            if data[key] is False:
                data[key] = 'NaN'

            else:
                data[key] = candle['close']



def buildBackTest(DataSet: list, session: TradeSession) -> pd.DataFrame:
    dataRows = []
    strategy = session.STRATEGY
    count = strategy.candleLimit 


    for unfiltered_candle in DataSet:
        candle = DataOperators.cleanCandle(unfiltered_candle)
        data = {}
        updateValue = session.update(candle)
        if strategy.candleLimit <= DataSet.index(unfiltered_candle):
            candle['timestamp'] = TimeHelpers.convertNumericTimeToString(candle['timestamp']) 
            indicator_value_dict = session.STRATEGY.returnIndicators()
            data.update(candle)
            updatePatternValues(indicator_value_dict, candle)
            data.update(indicator_value_dict) 
            dataRows.append(data)
    
    return buildDataFrame(dataRows)
    
    # TODO functionalize... possibly pass session as a param to backtest builder 
