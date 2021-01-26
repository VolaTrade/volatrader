import unittest
from Trader.Indicators import IndicatorFunctions

class TestCandleStickIndicators(unittest.TestCase):


    def testBullCandle(self):
        candle = {"open":6 , "close": 16}
        expected = True 
        actual = IndicatorFunctions.BULL_CANDLE(candle)
        self.assertEqual(expected, actual)

    def testBearCandle(self):
        candle = {"open":10 , "close": 6}
        expected = True 
        actual = IndicatorFunctions.BEAR_CANDLE(candle)
        self.assertEqual(expected, actual)

    def testDifference(self):
        candle = {"open":10 , "close": 6}
        expected = 4 
        actual = IndicatorFunctions.DIFFERENCE(candle)
        self.assertEqual(expected, actual)

        candle = {"open":6 , "close": 10}
        expected = 4 
        actual = IndicatorFunctions.DIFFERENCE(candle)
        self.assertEqual(expected, actual)

    def testGreenMarubozu(self):
        expected = True 
        candle = {"open":8 ,"high": 10, "low": 8, "close": 10}
        actual = IndicatorFunctions.GREEN_MARUBOZU(candle)
        self.assertEqual(expected, actual)

    def testRedMarubozu(self):
        expected = True 
        candle = {"open":10 ,"high": 10, "low": 8, "close": 8}
        actual = IndicatorFunctions.RED_MARUBOZU(candle)
        self.assertEqual(expected, actual)


    def testThreeLineStrikeBullish(self):
        candles = [{"open":10 ,"high": 0, "low": 0, "close": 8}, {"open":8 ,"high": 0, "low": 0, "close": 6}, {"open":6 ,"high": 0, "low": 0, "close": 4}, {"open":3 ,"high": 0, "low": 0, "close": 11}]    
        expected = True  
        actual = IndicatorFunctions.PATTERNTHREELINESTRIKE(candles)
        self.assertEqual(expected, actual)

    def testThreeLineStrikeBearish(self):
        candles = [{"open":2 ,"high": 0, "low": 0, "close": 4}, {"open":4 ,"high": 0, "low": 0, "close": 6}, {"open":6 ,"high": 0, "low": 0, "close": 8}, {"open":9 ,"high": 0, "low": 0, "close": 1}]    
        expected = True 
        actual = IndicatorFunctions.PATTERNTHREELINESTRIKEBEARISHREVERSAL(candles)  
        self.assertEqual(expected, actual)

    def testAbandondedBaby(self):
        candles = [{"open":10 ,"high": 11, "low": 5, "close": 6}, {"open":3 ,"high": 4.5, "low": .5, "close": 2}, {"open":5,"high": 10, "low": 4.8, "close": 9}]
        expected = True
        actual = IndicatorFunctions.PATTERNABONDONEDBABY(candles)
        self.assertEqual(expected, actual)

    def testThreeInside(self):
        candles = [{"open":10 , "close": 5}, {"open":6 , "close": 7}, {"open":8, "close": 11}]
        expected = True 
        actual = IndicatorFunctions.PATTERNTHREEINSIDE(candles)
        self.assertEqual(expected, actual)
 

    def testHammer(self):
        candles = [{"open":10 , "close": 6}, {"open":6 ,"high":8.5 , "low": 2, "close": 8}, {"open":8 ,"high": 12, "low": 9, "close": 11}]    
        expected = True 
        actual = IndicatorFunctions.PATTERNHAMMER(candles)
        self.assertEqual(expected, actual)

        candles = [{"open":10 , "close": 6}, {"open":8 ,"high":8.5 , "low": 2, "close": 6}, {"open":8 ,"high": 12, "low": 9, "close": 11}]    
        expected = True 
        actual = IndicatorFunctions.PATTERNHAMMER(candles)
        self.assertEqual(expected, actual)


    
    def testTweezerTop(self):
        candles = [{"open":2 ,"high":3 , "low": 1.7, "close": 3}, {"open":3 ,"high": 3, "low": 1, "close": 1.4}] 

        expected = True 

        actual = IndicatorFunctions.PATTERNTWEEZERTOP(candles)

        self.assertEqual(expected, actual)


    def testTweezerBottom(self):
        candles = [{"open":2 ,"high":3 , "low": 1, "close": 1}, {"open":1 ,"high": 3, "low": 1, "close": 1.4}] 
        expected = True 
        actual = IndicatorFunctions.PATTERNTWEEZERBOTTOM(candles)

        self.assertEqual(expected, actual)
    