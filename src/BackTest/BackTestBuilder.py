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

def buildHTML(string=None, figs=None, server=True, filename="analysis.html"):
    config = dict({'scrollZoom': True})
    if os.path.exists(filename):
        os.remove(filename) #this deletes the file
    dashboard = open(filename, 'w')
    dashboard.write("<link rel=\"stylesheet\" href=\"https://unpkg.com/bulma@0.8.0/css/bulma.min.css\" />\"")
    dashboard.write("<div align=\"left\"><img src=\"square-logo.png\" alt=\"LOGO BABY\" style=\"width:400px;height:200px;\"></div>" if server is False else "<style> #logo {width: 25%; height: 25%; position: absolute; right: 5px; top: 5px;}</style><img id=\"logo\" src=\"{{url_for('static', filename='square-logo.png' )}}\"/>")
    if string is not None:
        dashboard.write(string)
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html(config=config).split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")
    return filename


def buildDataFrame(data: list, backtest: bool=True) -> pd.DataFrame:
    returns = pd.DataFrame(data)

    if backtest:
        returns.index = pd.to_datetime(returns['timestamp'])
        del returns['timestamp']   
    return returns

def buildVisualization(DataSet: list, indicators: list) -> pd.DataFrame: #TODO implement 
    maxx = 0
    data = {}
    for indicator in indicators:
        if indicator['period'] > maxx:
            maxx = indicator['period']

    for candle in DataSet:
        temp = indicators.copy()
        if maxx <= DataSet.index(candle):

            for indicator in indicators.keys():
                function = getFunction(indicator)

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


def getBacktestResultsString(session: TradeSession, html=False):
    stratString = session.stratString.replace("_", " ").lower().title()
    startVal, endVal= session.principleOverTime[0], session.principleOverTime[-1]
    pos, neg  = session.getTradeData()
    valColor = 'green' if endVal >startVal else 'red'
    totalPl = colored(str(session.getTotalPL())+ "%", valColor, attrs=['bold']) if not html else session.getTotalPL()
    
    returnString = ""
    returnString+=f"\t\tResults for {stratString}" if not html else ""
    returnString+=f"\n\t\tPair: {session.pair.value}" if not html else ""
    returnString+=f"\n\t\tCandle Size: {session.candleSize.value}" if not html else ""
    returnString+= ("<strong>" if html else "") + "\n\t\tStarting Principle: " + ("</strong>" if html else "") + f"${str(session.principleOverTime[0])}"
    if html:
        returnString = "<h>" +returnString + "</h>"
        returnString = f"<h1 style=\"color: black; class=\"dotted\";> <div align=\"center\"  style=\"border:2px solid {valColor}\"> Backtest Summary for {stratString} on {session.pair.value}/{session.candleSize.value} </div></h1>" + returnString
    returnString+= ("<h font-family: \"fantasy\"><br><strong>" if html else "") + ("\n\t\tFinal Portfolio Value: ") + ("</strong>" if html else "") + (f"${colored(str(endVal), valColor, attrs=['bold'])}" if not html else f"${endVal}") +  ("</h>" if html else "")
    returnString+=("<h font-family: \'fantasy\'><br><strong>" if html else "") + f"\n\t\tTotal PnL:  " + ("</strong>" if html else "") + str(totalPl) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tTotal Trades: " + ("</strong>" if html else "") + str(session.getTotalTrades()) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tStarting Backtest at: " + ("</strong>" if html else "") + convertNumericTimeToString(session.startTime) +  ("</h>" if html else "")
    returnString+=  ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tEnding Backtest at:" + ("</strong>" if html else "") + convertNumericTimeToString(session.finishTime) +  ("</h>" if html else "")
    returnString+=("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tProfitable Trades: " + ("</strong>" if html else "") + (colored(str(pos), 'green') if not html else str(pos)) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tUnprofitable Trades: " +("</strong>" if html else "") + (colored(str(neg), 'red') if not html else str(neg)) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tTake Profit: " + ("</strong>" if html else "") +  f"{str(session.takeProfit)}%" +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tStop Loss: " + ("</strong>" if html else "") + f"{session.getStopLossPercent()}%" + ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tTotal Fees: " + ("</strong>" if html else "") + f"${str(session.getTotalFees())}" + ("</h>" if html else "")
    return returnString

# TODO add slider
# TODO more functional ohlcv graph
# TODO Fix autoscaling for y-axis on ohlcv graph
# TODO Fix Volume graph
