from enum import Enum
import ccxt 
# from Helpers.API.Stock_API import STOCK_MARKET



class SessionType(Enum):
    BACKTEST = 0
    PAPERTRADE = 1
    LIVETRADE = 2


class Strategy(Enum):
    pass

class Pair(Enum):
    """
    Enum to represent all base/quote currency pairs
    """
    ETHUSDT = "ETHUSDT"
    BTCUSDT = "BTCUSDT"
    STXUSDT = "STXUSDT"
    XRPUSDT = 'XRPUSDT'
    ATOMBTC = "ATOMUSD"
    LTCUSDT = 'LTCUSDT'
    LINKUSDT = 'LINKUSDT'
    ORBS = 'ORBSUSDT'
    # ROBINETH = 'ETH'


class Time(Enum):
    """
    enum to represent all time instances
    """
    ONEDAY = 24
    THREEDAY = 72
    ONEWEEK = 168
    TWOWEEK = 336
    THREEWEEK = 504
    MONTH = 700
    TWOMONTH = 1400
    THREEMONTH = 2100
    SIXMONTH = 4200


pairs = [e.value for e in Pair]
candles = [e.value for e in Candle]
strats = [e.value for e in Strategy]
times = ['ONEWEEK', 'ONEDAY', 'THREEDAY', 'MONTH', 'THREEMONTH', 'SIXMONTH']
class Indicator(Enum):
    """
    Enum to represent indicator 
    """
    PED_BTC = "PED-BTC" 
   
indicators = [e.value for e in Indicator]

