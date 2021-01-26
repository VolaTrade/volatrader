import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
from Helpers.Constants.Enums import Pair, Candle
from termcolor import colored
import numpy as np
from Trader.Indicators.IndicatorConstants import getIndicator
from Helpers import TimeHelpers 
from Trader.TradeSession import TradeSession


def buildIndicators(fig, df: pd.DataFrame, indicators: dict, skeleton: dict) -> None:
    rowNum = 3
    for indicator in indicators.keys():
        withCandles = skeleton[indicator]['graph_features']['withCandles']
        for key in skeleton[indicator]["values"]:
                if key != "parameters" and key != "user_adjusted":
                    print("------------------------------------------------------------------><><> ", key)
                    print(getIndicator(indicator))
                    fig.add_trace(go.Scatter(x=df.index, yaxis=("y2" if withCandles is True else f"y{rowNum}"), y=df[f"{indicator}_{key}"],
                            name=f"{indicator.upper()}{skeleton[indicator]['parameters']['period']}_{key}",  mode=skeleton[indicator]['graph_features']['mode'], line=dict(color=getIndicator(indicator)['values'][key], width=1)), row = (1 if withCandles is True else rowNum), col=1)
 
        if not withCandles:
            rowNum+=1


def updateColors(df: pd.DataFrame) -> list:
    color = []
    for index, row in df.iterrows():
        if row['close'] > row['open']:
            color.append('green')
        else:
            color.append('red')

    return color


# Returns a candlestick graph with buy and sell points
def generateCandleGraph(candle_data: pd.DataFrame, session: TradeSession):
    fig = make_subplots(rows=5, cols=1)
    color = updateColors(candle_data)
    fig.add_trace(go.Candlestick(x=candle_data.index, yaxis="y2",
                    open=candle_data['open'],
                    high=candle_data['high'],
                    low=candle_data['low'],
                    close=candle_data['close'],
                    name="CANDLES"), row=1, col=1)
    fig.add_trace(go.Bar(x=candle_data.index, y=candle_data['volume'], name="Volume", marker=dict(color=color), yaxis='y'), row=2, col=1)

    buildIndicators(fig, candle_data, session.STRATEGY.indicators, session.STRATEGY.skeleton)

    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['buy'], yaxis="y2", mode='markers', line=dict(color='blue', width=14), name = "BUY"), row=1, col=1)
    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['sell'], yaxis="y2", mode='markers', line=dict(color='black', width=14), name="SELL"), row=1, col=1)
    fig.update_layout(
        autosize=False,
        height=3000,
        width=1500,
        title={
        'text': f"CANDLE STICK GRAPH WITH USED INDICATORS",
        'y':1,
        'x':0.5,
        "font" : dict(family="Roboto ", size=14),
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig

# buytime buyprice, selltime sellprice profitloss
def generateTransactionHistoryTable(results):
    df = pd.DataFrame(results)
    cols = ['<b>Transaction Number</b>']
    cols = cols + [f"<b>{e.capitalize()}</b>" for e in df.columns]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(cols),
            fill_color='paleturquoise',
            align='left',
            font=dict(color='black', size=14)),
        cells=dict(values=[df.index, df.buytime, df.buyprice, df.selltime, df.sellprice, df.profitloss],
        fill_color='lavender',
        align='left',))
    ])

    fig.update_layout(title={
        'text': "Transaction History"
    })

    return fig


def generateLinePlot(data, y_value, graph_title):
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x = data.index,
                        y = data[y_value],
                        name = y_value.upper()))

    fig.update_layout(
        autosize=False,
        height=400,
        width=1500,
            title={
                'text': graph_title,
                'y':0.9,
                'x':0.5,
            },

    )


    return fig
    

def generateGraphs(candle_data: pd.DataFrame, session: TradeSession):
    candleGraph = generateCandleGraph(candle_data, session)
    # linePlot = generateLinePlot(candle_data, 'principle', "Principle Over Time")
    return [candleGraph]
    