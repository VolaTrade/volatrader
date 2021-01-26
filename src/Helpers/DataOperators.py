import copy
import decimal
import datetime
import time
from unicodedata import numeric
import ccxt
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from Helpers.Constants.Enums import Indicator, Pair, Candle, SessionType, Market
from Helpers.Logger import logToSlack, MessageType
import re   
import requests 
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format
from termcolor import colored
from typing import Dict, List, Union, Tuple 
import traceback
import indicators 
import numpy as np
from Helpers.TimeHelpers import convertNumericTimeToString, rewind
'''
    Helper Script w/ utility functions that are referenced throughout master program
'''
# common constants

# -----------------------------------------------------------------------------
cleaner = lambda word: word if not isinstance(word, decimal.Decimal) else str(word)  # cleans bounds to be parsed easier


# -----------------------------------------------------------------------------

     #'2017-09-01 00:00:00'

def getCandlesFromTime(from_datetime: str, pair: Pair, candleSize: Candle, market, output=True) -> List[Dict[str,str]]:
    from_datetime = from_datetime[0 : 10] + " 00:00:00"
    # print("------------------>", from_datetime)
    msec = 1000
    minute = 60 * msec
    fifteen_minute = minute * 15
    five_minute = minute * 5
    thirty_minute = minute * 30
    hour = minute * 60 
    hold = 60
    exchange = market.value
    if candleSize.value == "1h":
        step = hour

    if candleSize.value == "15m":
        step = fifteen_minute

    elif candleSize.value == "5m":
        step = five_minute

    else:
        step = thirty_minute
    # -----------------------------------------------------------------------------
    from_timestamp = exchange.parse8601(from_datetime)

    # -----------------------------------------------------------------------------

    now = exchange.milliseconds()

    # -----------------------------------------------------------------------------

    data = []

    while from_timestamp < now:

        try:
            if output:
                print(exchange.milliseconds(), colored('Fetching candles starting from', color="grey"), exchange.iso8601(from_timestamp))
            ohlcvs = exchange.fetch_ohlcv(pair.value.replace("USDT", '/USDT'), candleSize.value, from_timestamp)
            if output:
                print(exchange.milliseconds(), 'Fetched', len(ohlcvs), 'candles')
            first = ohlcvs[0][0]
            last = ohlcvs[-1][0]
            if first == last:
                return data
            
            if output:
                print(colored('First candle epoch', color='grey'), first, exchange.iso8601(first))
                print(colored('Last candle epoch', color='grey'), last, exchange.iso8601(last))
            from_timestamp += len(ohlcvs) * step
            data += ohlcvs

        except Exception as error:
            
            print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
            time.sleep(hold)
    return data


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])



def convertCandlesToDict(candles: List[List[str]]) -> List[Dict[str, Union[str, float, int]]]:
    """
    converts list candle data to list of dictionary
    ..... ie: list ==> list[dict{}]
    @:param candles = list of candles
    @:returns dictionary of candles
    """
    assert isinstance(candles, list)
    final = []
    for candle in candles:
        try:
            final.append(cleanCandle(candle))

        except Exception as e:
            print("Error", e)

    return final


def cleanCandle(candle: List[str]) -> Dict[str, Union[str, int, float]]:
    """
    Cleans candle OHLCV values to only extrapolate numeric values
    @:param candle = candle dictionary ex = {'timestamp': 3982435, 'open': '.235', high: '.325', low: '.20', close: '2.7', volume: '69'}
    @:returns cleaned candle
    """

    it = iter(candle)
    time = int(next(it))
    o = cleaner(next(it))
    h = cleaner(next(it))
    l = cleaner(next(it))
    c = cleaner(next(it))
    volume = cleaner(next(it))

    return {
        'timestamp': time,
        'open': o,
        'high': h,
        'low': l,
        'close': c,
        'volume': volume,
    }
    


import random

def printLogo(type: SessionType=None)-> None:
    colors = [ 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'grey']

    fonts = ['speed', 'starwars', "stampatello"]

    font = random.choice(fonts)
    text_color = random.choice(colors).lower()
    highlight = f'on_{random.choice(colors)}'.lower()

    init(strip=not sys.stdout.isatty()) 
    cprint(figlet_format('VolaTrade', font=font),
       text_color, None, attrs=['blink'])

    if type is SessionType.BACKTEST:
        cprint(figlet_format('[BACKTEST]', font=font),
    text_color, None, attrs=['blink'])

    if type is SessionType.PAPERTRADE:
        cprint(figlet_format('[PAPER]', font=font),
        text_color, None, attrs=['blink'])

    if type is SessionType.LIVETRADE:
        cprint(figlet_format('[VOLATRADER]', font=font),
        text_color, None, attrs=['blink']) 

    if type is None:
        cprint(figlet_format('[NOTIFICATIONS]', font=font),
        text_color, None, attrs=['blink']) 

def fetchCandleData(api: ccxt.Exchange, pair: Pair, candleSize: Candle, limit: int=500, retries: int=3, time=time, log=logToSlack) -> List[Dict[str, numeric]]:
    
    if retries == 0:
        raise TimeoutError("Maximum retries for fetchCandleData exceeded")
    try:
        print(pair.value.replace("USDT", "/USDT"))
        print(candleSize.value)
        print(limit)
        return api.fetchOHLCV(pair.value.replace("USDT", "/USDT"), candleSize.value, limit=limit)

    except Exception as e:
        
        if isinstance(e, (ccxt.RequestTimeout, ccxt.DDoSProtection, ccxt.ExchangeNotAvailable)): #worth retrying 
            error = "trying again in 15 seconds" 
            log(f"[{e}]{traceback.format_exc()}{error}", messageType=MessageType.ERROR)
            time.sleep(15)
            fetchCandleData(api, pair, candleSize, limit, retries=retries-1, time=time, log=log)

        else:
            error = "Unrecoverable error from ccxt .. gonna have kill shit"
            log(f"[{e}]{traceback.format_exc()}{error}", messageType=MessageType.ERROR)
            raise e


def fetchVolumeData(pair: Pair, candleSize: Candle, market: Market= Market.BINANCE) -> tuple:
    candle_data = getCandlesFromTime(convertNumericTimeToString(rewind(str(datetime.datetime.now())[0: -7], 60, 4200)), pair, candleSize, market, output=True)
    volumes = [e[5] for e in candle_data]
    print(v)
    return (sum(volumes) /  len(volumes)) , indicators.SDV(np.array(volumes), len(volumes))


def fetchOrderBookForPair(pair: Pair, market: Market=Market.BINANCE) -> Dict[str, Union[List[List[float]], float]]: 

    try:
        return self.api.fetchOrderBook(self.pair.value)

    except Exception as e:
        logToSlack(f"[{e}]{traceback.format_exc()}", messageType=MessageType.ERROR)
