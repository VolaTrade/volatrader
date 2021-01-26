import indicators
import pandas as pd
import numpy as np
import ta
import statistics as stats


def getFunction(name: str):
	return globals()[name]



def BB(closes, param_dict) -> dict:
	return indicators.BOLINGER_BANDS(np.array(closes), param_dict['period'])


def EMA(closes, param_map):
	return indicators.EMA(np.array(closes), param_map['period'], param_map['alpha'], param_map['epsilon'])[-1]


def TRUERANGE(candle1: dict, candle2: dict) -> float:
    return max(candle2['high'] - candle2['low'], candle1['high'] - candle2['close'], candle1['close'] - candle2['close'])


def ATR(candles: list, period: int) -> float:
    size = len(candles)
    sum_vals = 0.0  
    for i in range(size-period+1, size):
        sum_vals += TRUERANGE(candles[i-1], candles[i])

    return sum_vals/period


def SMOOTHED_ATR(candles: list, period: int) -> float:
    return ATR(candles, period-1) + (TRUERANGE(candles[2], candles[-1]) / period)   

def FIBBOLINGER(closes: list, param_dict) -> set:
	lower, _, lowerTwo, lowerOne, ma, upperOne, upperTwo, _, upper = indicators.FIB_BANDS(np.array(closes), param_dict['period'])
	return lower, lowerTwo, lowerOne, ma, upperOne, upperTwo, upper
            
def WMA(closes: list, param_dict: dict) -> float:
	return indicators.WMA(np.array(closes), param_dict['period'], param_dict['weighted_factor'])

def MOM(closes: list, param_dict)->float:
    return indicators.MOMENTUM(np.array(closes), param_dict['period']) 


def RSIDIVERGENCE(candles: list) -> float:
    fourteen = RSI(candles, 14)
    five = RSI(candles, 5)
    return fourteen - five 

def PATTERNHAMMER(candles: list) -> bool:
	c1, c2, c3 = candles[-3], candles[-2], candles[-1]

	if BEAR_CANDLE(c1)  and BULL_CANDLE(c3):
		if BULL_CANDLE(c2):
			if (c2['open'] - c2['low']) >= 2 * (c2['close'] -c2['open']):
				return True 

		else:
			if (c2['close'] - c2['low']) >= 2 * (c2['open'] -c2['close']):
				return True


	return False 


def FIB(closes: list, param_dict: dict) -> float:
    return indicators.FIB(np.array(closes), param_dict['period'])
    
def RSI(prices, param_dict):
	n = int(param_dict['period'])
	deltas = np.diff(prices)
	seed = deltas[:n + 1]
	up = seed[seed >= 0].sum() / n
	down = -seed[seed < 0].sum() / n
	rs = up / down
	rsi = np.zeros_like(prices)
	rsi[:n] = 100. - 100. / (1. + rs)

	for i in range(n, len(prices)):
		delta = deltas[i - 1]  # cause the diff is 1 shorter

		if delta > 0:
			upval = delta
			downval = 0.
		else:
			upval = 0.
			downval = -delta

		up = (up * (n - 1) + upval) / n
		down = (down * (n - 1) + downval) / n

		rs = up/down
		rsi[i] = 100. - 100./(1.+rs)

	return rsi[-1]

def SMA(closes: list, param_dict: dict) -> float:
		return indicators.SMA(np.array(closes), int(param_dict['period']))



BEAR_CANDLE = lambda candle: candle['close'] < candle['open']

BULL_CANDLE = lambda candle: candle['close'] > candle['open']

DIFFERENCE = lambda candle: (candle['open'] - candle['close']) if BEAR_CANDLE(candle) else (candle['close'] - candle['open'])

GREEN_MARUBOZU = lambda candle: candle['close'] == candle['high'] and candle['low'] == candle['open']

RED_MARUBOZU = lambda candle: candle['close'] == candle['low'] and candle['high'] == candle['open'] 



def PATTERNABONDONEDBABY(candles):
	c1, c2, c3 = candles[-3], candles[-2], candles[-1]

	if BEAR_CANDLE(c1) and BEAR_CANDLE(c2) and BULL_CANDLE(c3):
		if c2['high'] < c1['low'] and c2['high'] < c3['low']:
			if ((c2['high'] - c2['open']) + (c2['close'] - c2['low'])) > (c2['open'] - c2['close']):
				return True 


	return False 
# Note
def PATTERNONNECKLINE(candles, n=3):

	sdv = stats.stdev([DIFFERENCE(e) for e in candles])
	mean = sum([DIFFERENCE(e) for e in candles]) / len(candles)
	thirdCandle = candles[-3]
	secondCandle = candles[-2]
	firstCandle = candles[-1]
	if (mean + sdv * 2) > DIFFERENCE(thirdCandle):
		if (int(firstCandle['close']) == int(thirdCandle['close']) and int(secondCandle['close']) == int(
				firstCandle['close'])):
			if BULL_CANDLE(thirdCandle) and BEAR_CANDLE(secondCandle) and BEAR_CANDLE(firstCandle):
				if firstCandle['close'] >= thirdCandle['close'] and firstCandle['open'] <= thirdCandle['open']:
					return True

	return False 



def PATTERNTHREELINESTRIKE(candles) -> bool:
    
    candle1, candle2, candle3, candle4 = candles[-4], candles[-3], candles[-2], candles[-1]

    if BEAR_CANDLE(candle1) and BEAR_CANDLE(candle2) and BEAR_CANDLE(candle3) and BULL_CANDLE(candle4):
        for candle in [candle1, candle2, candle3]:
            if candle['open'] > candle4['close'] or candle['close'] < candle4['open']:
                return False 
        
        if candle3['open'] <= candle2['close'] and candle2['open'] <= candle1['close']:
            return True 

    return False 



def PATTERNTHREELINESTRIKEBEARISHREVERSAL(candles) -> bool:
    
	candle1, candle2, candle3, candle4 = candles[-4], candles[-3], candles[-2], candles[-1]

	if BULL_CANDLE(candle1) and BULL_CANDLE(candle2) and BULL_CANDLE(candle3) and BEAR_CANDLE(candle4):
		for candle in [candle1, candle2, candle3]:
			if candle['open'] > candle4['open'] or candle['close'] < candle4['close']:
				return False 
					
		if candle3['open'] >= candle2['close'] and candle2['open'] >= candle1['close']:
			return True 

	return False 




def PATTERNTHREEWHITESOLDIERS(candles: list) -> bool:
	thirdCandle = candles[-3]
	secondCandle = candles[-2]
	firstCandle = candles[-1]
	
	for candle in [firstCandle, secondCandle, thirdCandle]:
		if (candle['close'] - candle['open']) > ((candle['high'] - (candle['close']) + (candle['open'] - candle['low']))):
			pass
		else:
			return False 

	if BULL_CANDLE(thirdCandle):
		if BULL_CANDLE(secondCandle):
			if BULL_CANDLE(firstCandle):
					return True

	return False

def PATTERNTHREEBLACKCROWES(candles: list) -> bool:
	thirdCandle = candles[-3]
	secondCandle = candles[-2]
	firstCandle = candles[-1]
	
	for candle in [firstCandle, secondCandle, thirdCandle]:
		if (candle['open'] - candle['close']) > ((candle['high'] - (candle['open']) + (candle['close'] - candle['low']))):
			pass
		else:
			return False 

	if BEAR_CANDLE(thirdCandle):
		if BEAR_CANDLE(secondCandle):
			if BEAR_CANDLE(firstCandle):
					return True

	return False


def PATTERNSPINNINGTOP(candle: dict) -> bool:  #TODO implement variations.. currently only supports perfect symmetry 
	if BULL_CANDLE(candle):
		if (candle['high'] - candle['close']) == (candle['open'] - candle['low']):
			return True 

	else:
		if (candle['close'] - candle['low']) == (candle['high'] - candle['close']):
			return True 



	return False 




def PATTERNTWEEZERTOP(candles: list):
	c1, c2 = candles[-2], candles[-1]

	if BULL_CANDLE(c1) and BEAR_CANDLE(c2):
		if c1['close'] ==  c1['high'] and c2['open'] == c2['high']:
			if c1['high'] == c2['high']:
				return True 


	return False 


def PATTERNTWEEZERBOTTOM(candles: list):
	c1, c2 = candles[-2], candles[-1]

	if BEAR_CANDLE(c1) and BULL_CANDLE(c2):
		if c1['close'] ==  c1['low'] and c2['open'] == c2['low']:
			if c1['low'] == c2['low']:
				return True 


	return False 


def PATTERNTHREEINSIDE(candles: list) -> bool:
	c1, c2, c3 = candles[-3], candles[-2], candles[-1]
	if BEAR_CANDLE(c1) and BULL_CANDLE(c2) and BULL_CANDLE(c3):
		if DIFFERENCE(c1) > DIFFERENCE(c3) > DIFFERENCE(c2):
			if c2['close'] < c1['open'] and c2['open'] > c1['close']:
				if c3['close'] > c1['open']:
					return True 


	return False  


def PATTERNTHREEBEARISHSOLDIERS(candles: list) -> bool:
	thirdCandle = candles[-3]
	secondCandle = candles[-2]
	firstCandle = candles[-1]

	if BEAR_CANDLE(thirdCandle):
		if BEAR_CANDLE(secondCandle):
			if BEAR_CANDLE(firstCandle):
				if secondCandle['open'] == thirdCandle['close'] and firstCandle['open'] == secondCandle['close']:
					return True

	return False
