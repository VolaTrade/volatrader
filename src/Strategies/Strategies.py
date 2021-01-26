import inspect
from Helpers.Constants.Enums import Indicator, Candle, Pair
from Helpers.TimeHelpers import convertNumericTimeToString
from Trader.Indicators import IndicatorFunctions
from Helpers.TimeHelpers import convertNumericTimeToString
from Trader.Indicators.IndicatorConstants import getIndicator, getModifiableIndicator

BUY, SELL, GO = True, True, True 
HODL, WAIT, DONT_SCALE = False, False, False

def getStratSourceCode(stratName: str) -> str:

    try:
        st: str  = inspect.getsource(getStrat(stratName))
        return st.strip().replace("\n", "").replace(" ", "")

    except Exception:
        raise Exception("Strategy name does not exist...")





def getStrat(name: str):
    """
    returns strategy function with a list of indicators to use with it
    :param name: Name of strategy
    :returns: strategy function and list of indicators used w/ strategy
    """
    c = globals()[name]
    return c


def getIndicatorPeriodValues(indicators: list) -> tuple:
    maxx = 0
    indicator_dic = {}
    skeleton = {}
    for indicator in indicators:
        copy = getIndicator(indicator.value)
        if copy['parameters']['period'] > maxx: 
            maxx = copy['parameters']['period'] #determines maximum candle limit 
        indicator_dic[indicator.value] = copy['values']
        skeleton[indicator.value] = copy

    return indicator_dic, skeleton, maxx


def getStratIndicators(name: str):
    c = globals()[name](None, None, None)
    temp = []
    for indicator in c.indicatorConstants:
        push = getModifiableIndicator(indicator.value)
        if "user_adjusted" not in push: 
            temp.append(push['parameters'])
    return temp


def getStratIndicatorNames(name: str):
    c = globals()[name]
    c = c(None, None, None)
    return c.indicatorConstants


class strategy():

    def __init__(self, pair=None, candleSize=None, principle=None):
        self.pair = pair
        self.candleSize = candleSize
        self.candleLimit = 0
        self.indicatorConstants = []
        self.indicators = {}
        self.principle = principle
        self.candles = []
        self.closes = []

    def initialize(self):
        self.indicators, self.skeleton, self.candleLimit = getIndicatorPeriodValues(self.indicatorConstants)

    def checkSell(self, candle):
        return HODL

    def returnIndicators(self):
        temp = {}
        for indicator in self.indicators.keys():
            temp_2 = self.skeleton[indicator]['values'].copy()
            for key in temp_2:  
                temp[f"{indicator}_{key}"] = temp_2[key]
        return temp

    def interValUpdate(self, candle: dict) -> bool:
        self.closes.append(candle['close'])
        self.candles.append(candle)
        if len(self.closes) < self.candleLimit or len(self.candles) < self.candleLimit:
            return HODL

        self.updateIndicatorValues(self.candles, self.closes)
        self.closes.pop(0)
        self.candles.pop(0)
        return GO 


    def buyUpdate(self, candle):
        self.interValUpdate(candle)
        

    def updateIndicatorValues(self, candles: list, closes: list):

        for key in self.indicators.keys():
            func = IndicatorFunctions.getFunction(key)
            if self.skeleton[key]['calculatedWithCandles']:
                if "user_adjusted" not in self.skeleton[key].keys():
                    results = func(candles, self.skeleton[key]['parameters'])

                else:
                    results = func(candles)


            else:
                results = func(closes, self.skeleton[key]['parameters'])
            
            if isinstance(results, tuple):
                it = iter(results) 
                for value_key in self.indicators[key]:
                    self.indicators[key][value_key] = next(it)

            else:
                self.indicators[key]['value'] = results

    def checkTakeProfitScale(self):
        return DONT_SCALE   

    def checkStopLossScale(self):
        return DONT_SCALE


class TEST_STRAT(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)

    def checkBuy(self, candle=None):
        return BUY

class THREE_LINE_STRIKE_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.candles = []
        self.indicatorConstants = [Indicator.PATTERNTHREELINESTRIKE]

    def checkBuy(self, candle):  
    
        return self.indicators['PATTERNTHREELINESTRIKE']['value']

class FIBONNACI_BOLINGER_STRATEGY(strategy):

    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.FIBBOLINGER, Indicator.PATTERNTHREEBLACKCROWES, Indicator.HAMMER]

    def checkBuy(self, candle):

        if candle['close'] > self.indicators['FIBBOLINGER']['moving average']:
            return BUY

        return HODL



class BOLINGER_BANDS_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.BB, Indicator.EMA, Indicator.PATTERNTHREEINSIDE]

    def checkBuy(self, candle):
        bolingerBands = indicators['BB']
        if(candle['close'] > bolingerBands['UPPER BAND BB']) or candle['close'] > self.indicators['EMA']['value']:
            return BUY
        
        return HODL 


class MOMENTUM_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.MOM]
        self.closes = []

    def checkBuy(self, candle):
        self.closes.append(candle['close'])
        if len(self.closes) < self.candleLimit:
            return HODL
        momentum = self.indicators['MOM']
        momentum['values'] = IndicatorFunctions.MOM(self.closes, int(momentum['period']))
        value = momentum['values']
        self.closes.pop(0)
        if value > 0:
            return BUY

        return SELL 


class WEIGHTED_MOVING_AVERAGE_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.WMA, Indicator.SMA]

    def checkBuy(self, candle):
        if self.indicators['WMA']['value'] > candle['close'] or self.indicators['SMA']['value'] > candle['close']:
            return BUY

        return SELL 


class EXPONENTIAL_MOVING_AVERAGE_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.EMA]
        self.closes = []

    def checkBuy(self, candle):
        self.closes.append(candle['close'])
        if len(self.closes) < self.candleLimit + 1:
            return HODL

        print(self.closes)
        self.indicators['EMA']['value'] = IndicatorFunctions.EMA(self.closes, self.indicators['EMA']['parameters'])   
        wma = self.indicators['EMA']['value']  
        value = wma
        self.closes.pop(0)
        if value > candle['close']:
            return BUY

        return SELL 



class SUPPORT_RESISTANCE_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.PATTERNTHREELINESTRIKE, Indicator.PATTERNTHREEINSIDE]
        self.support = 0
        self.resistance = 0 
        self.timestep = 0

    def checkBuy(self, candle):

        self.timestep += 1

        if (self.support == 0 and self.resistance == 0) or self.timestep % 10 == 0:
            print(convertNumericTimeToString(candle['timestamp']))
            self.support = input("Please enter support : ")
            self.resistance = input("Please enter resistance: ")

        
        if int(self.support) == int(candle['close']):
            if self.indicators["PATTERNTHREELINESTRIKE"]['value'] or self.indicators['PATTERNTHREEINSIDE']['value']:
                return BUY 


        return SELL 



"""

class REGRESSION_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [Indicator.EMA]
        self.closes = []
        self.weights_dict = weights_dict #get from DB
        self.bias = bias #get from DB
        self.mse = rmse #get from DB

    def checkBuy(self, candle):
        #if lower_bound > acutal_price → buy
        #elif upper_bound < acutal_price → sell
        #else → hold (maybe buy/hold?)
        self.closes.append(candle['close'])
        if len(self.closes) < self.candleLimit + 1:
            return HODL

        print(self.closes)
        self.indicators['EMA']['value'] = IndicatorFunctions.EMA(self.closes, self.indicators['EMA']['parameters'])   
        wma = self.indicators['EMA']['value']  
        value = wma
        self.closes.pop(0)
        if value > candle['close']:
            return BUY

        return SELL"""
    
