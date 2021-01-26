from enum import Enum
import ccxt 
# from Helpers.API.Stock_API import STOCK_MARKET


class MarketType(Enum):
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    STOCK = "STOCK"



class Candle(Enum):
    """
    Enum to represent all possible candle sizes
    """
    ONE_MINUTE = "1m"
    FIVE_MINUTE = "5m"
    FIFTEEEN_MINUTE = "15m"
    THIRTY_MINUTE = '30m'
    HOUR = '1h'
    # THREE_HOUR = "3h"
    # TWELVE_HOUR = "12h"
    # ONE_DAY = '1d'
    # THREE_DAY = '3d'
    # ONE_WEEK = '1w'
    # THRE_WEEK = "3w"

class Market(Enum):
    BINANCE = ccxt.binance()
    KRAKEN = ccxt.kraken()

class SessionType(Enum):
    BACKTEST = 0
    PAPERTRADE = 1
    LIVETRADE = 2


class Strategy(Enum):
    FIBONNACI_BOLINGER_STRATEGY = "FIBONNACI_BOLINGER_STRATEGY"
    TEST = "TEST_STRAT"
    THREE_LINE_STRIKE_STRATEGY = "THREE_LINE_STRIKE_STRATEGY"
    BB = 'BOLINGER_BANDS_STRATEGY'
    MOM = "MOMENTUM_STRATEGY"
    WMA = "WEIGHTED_MOVING_AVERAGE_STRATEGY"
    EMA = "EXPONENTIAL_MOVING_AVERAGE_STRATEGY"
    CANDLESTRAT = "QUICK_CANDLE_STRATEGY"
    SP = "SUPPORT_RESISTANCE_STRATEGY"

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
    FIBBOLINGER = "FIBBOLINGER" 
    PATTERNTHREEBLACKCROWES = "PATTERNTHREEBLACKCROWES"
    PATTERNTHREEINSIDE = "PATTERNTHREEINSIDE"
    PATTERNTHREELINESTRIKE = "PATTERNTHREELINESTRIKE"
    PATTERNTHREEWHITESOLDIERS= "PATTERNTHREEWHITESOLDIERS"
    PATTERNTWEEZERTOP = "PATTERNTWEEZERTOP"
    PATTERNTWEEZERBOTTOM = "PATTERNTWEEZERTOP"
    BEARISHBABY = "PATTERNABONDONEDBABY"
    HAMMER = "PATTERNHAMMER"
    BB = "BB"   
    EMA = "EMA"
    MOM = "MOM"
    SMA = "SMA"
    WMA = "WMA"
    RSI = "RSI"

indicators = [e.value for e in Indicator]

