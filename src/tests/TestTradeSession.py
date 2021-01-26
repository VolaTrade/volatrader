from Trader.TradeSession import TradeSession
from Strategies.Strategies import getStrat
from Strategies.Strategies import strategy
from Helpers.Constants.Enums import Pair, Candle
from unittest.mock import Mock 
import unittest
import pytest
import math 

float_format = lambda number: float("{:.2f}".format(number))
threshold = 1

class TestStratUp(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)

    def checkTakeProfitScale(self):
        return 2 


    def checkStopLossScale(self):
        return 2

    def checkBuy(self, candle_mock: dict):
        return True 



class TestStratDown(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)

    def checkTakeProfitScale(self):
        return 2


    def checkStopLossScale(self):
        return .5

    def checkBuy(self, candle_mock: dict):
        return False 
class TestTradeSession(unittest.TestCase):

    def testFees(self):
        temp_session = TradeSession(None, None, None, 0, None, None)

        temp_session.buyUpdate({'close': 10.0, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 12.0, 'timestamp': 1585958500000})
        self.assertEqual(temp_session.getTotalFees(), 2)

    def testTradeData(self):
        temp_session = TradeSession(None, None, None, 0, None, None)
        temp_session.buyUpdate({'close': 10.0, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 12.0, 'timestamp': 1585958500000})
        temp_session.buyUpdate({'close': 34.0, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 11.0, 'timestamp': 1585958500000})

        actual_pos, actual_neg = temp_session.getTradeData()

        self.assertEqual(actual_pos, 1)
        self.assertEqual(actual_neg, 1)


    def testResults(self):
        temp_session = TradeSession(None, None, None, 0, None, None)
        temp_session.buyUpdate({'close': 10.01, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 8.008, 'timestamp': 1585958500000})

        self.assertEqual(float_format(temp_session.results[0]['profitloss']), -20.00)
        temp_session.buyUpdate({'close': 8.008, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 10.01, 'timestamp': 1585958500000})
        self.assertEqual(float_format(temp_session.results[1]['profitloss']), 20.00)

    def testGetTotalPL(self):
        temp_session = TradeSession(None, None, None, 0, None, None)
        temp_session.buyUpdate({'close': 10.01, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 8.008, 'timestamp': 1585958500000})
        temp_session.buyUpdate({'close': 8.008, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 10.01, 'timestamp': 1585958500000})
        self.assertEqual(temp_session.getTotalPL(), 0)


    def testTakeProfit(self):
        temp_session = TradeSession(None, None, None, 25, 3, None)
        temp_session.buyPrice = 100
        expected = True
        temp_session.calculateTakeProfit()

        actual = temp_session.CHECK_TAKEPROFIT({'close': 125})
        self.assertEqual(expected, actual)
        expected = False
        actual = temp_session.CHECK_TAKEPROFIT({'close': 124})
        self.assertEqual(expected, actual)
    


    def testStopLoss(self):
        temp_session = TradeSession(None, None, None, 25, 25, None)
        temp_session.buyPrice = 50
        temp_session.CHECK_STOPLOSS({'close': 100})
        expected = True 
        actual = temp_session.CHECK_STOPLOSS({'close': 75})
        self.assertEqual(actual, expected)

        expected = False 
        temp_session = TradeSession(None, None, None, 25, 25, None)
        temp_session.buyPrice = 100
        actual = temp_session.CHECK_STOPLOSS({'close': 76})
        self.assertEqual(actual, expected)

    def testGetTotalTrades(self):
        temp_session = TradeSession(None, None, None, 0, None, None)
        temp_session.buyUpdate({'close': 10.01, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 8.008, 'timestamp': 1585958500000})
        temp_session.buyUpdate({'close': 8.008, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 10.01, 'timestamp': 1585958500000})
        expected = 2
        actual = temp_session.getTotalTrades()
        self.assertEqual(expected, actual)


    def testPortfolioChange(self):
        strat = getStrat("TEST_STRAT")(None, None, None)
        strat.initialize()
        temp_session = TradeSession(None, None, strat, 1, 1, None)
        temp_session.update({'close': 10.01, 'timestamp': 1585958400000})
        temp_session.update({'close': 8.008, 'timestamp': 1585958500000})

        expected = 800
        actual = temp_session.getPrincipleList()[-1]
        print(actual)
        print(expected)
        diff = abs(actual - expected)
        self.assertTrue(diff < threshold)   #almost equal

        temp_session.checkBuy({'close': 8.008, 'timestamp': 1585958400000})
        temp_session.checkSell({'close': 10.01, 'timestamp': 1585958500000})

        expected = 1000 
        actual = temp_session.getPrincipleList()[-1]
        diff = abs(actual - expected)
        self.assertTrue(diff < threshold)



    def testGetCurrentPnl(self):
    
        strat = getStrat("TEST_STRAT")(None, None, None)
        strat.initialize()
        temp_session = TradeSession(None, None, strat, 4, 4, None)
        temp_session.update({'close': 10.01, 'timestamp': 1585958400000})
        expected = -20 
        actual = temp_session.getCurrentPnl(8.008)

        diff = abs(actual - expected)
        self.assertTrue(diff < threshold)

    def testStrategySellUpdate(self):

        strat = getStrat("TEST_STRAT")(None, None, None)
        strat.initialize()
        temp_session = TradeSession(None, None, strat, 4, 4, None)
        self.assertEqual(False, temp_session.STRATEGY.checkSell({"I am a test": None}))
        

    def testAccuracy(self):
        temp_session = TradeSession(None, None, None, 0, None, None)
        temp_session.buyUpdate({'close': 10.01, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 8.008, 'timestamp': 1585958500000})
        temp_session.buyUpdate({'close': 8.008, 'timestamp': 1585958400000})
        temp_session.sellUpdate({'close': 10.01, 'timestamp': 1585958500000})

        expected = .5 
        actual = temp_session.getAccuracy()
        self.assertEqual(expected, actual)

    #this won't pass locally but will pass remotely on build/deploy due to timestamp
    def testDailyUpdates(self):
        expected = {'2020-06-13': 235.05, '2020-06-14': 10.01}
        temp_session = TradeSession(None, None, None, 0, None, None)
        temp_session.checkDailyPriceCloseChange({'close': 10.01, 'timestamp': 1592028900000})
        temp_session.checkDailyPriceCloseChange({'close': 236.37,'timestamp':  1592116200000})
        temp_session.checkDailyPriceCloseChange({'close': 10.01, 'timestamp': 1592035200000})
        temp_session.checkDailyPriceCloseChange({'close': 235.05,'timestamp':  1592120700000})

        actual = temp_session.getDailyCloses()
        self.assertEqual(actual, expected)


    def testTakeProfitCalculationLessThanOne(self):
        expected = 1.003
        temp_session = TradeSession(None, None, None, 0, None, None)
        actual = temp_session.getTakeProfitScalar(.3)
        self.assertEqual(expected, actual)    

    def testTakeProfitCalculationFloatValue(self):
        expected = 1.015 
        temp_session = TradeSession(None, None, None, 0, None, None)
        actual = temp_session.getTakeProfitScalar(1.5)
        self.assertEqual(expected, actual)


    def testTakeProfitCalculationIntegerValue(self):
        expected = 1.01
        temp_session = TradeSession(None, None, None, 0, None, None)
        actual = temp_session.getTakeProfitScalar(1)
        self.assertEqual(expected, actual)

    def testTakeProfitCalculationBigIntegers(self):
        expected = 1.25 
        temp_session = TradeSession(None, None, None, 0, None, None)
        actual = temp_session.getTakeProfitScalar(25)
        self.assertEqual(actual, expected)


    def testTakeProfitCalculationBigFloat(self):
        expected = 1.256
        temp_session = TradeSession(None, None, None, 0, None, None)
        actual = temp_session.getTakeProfitScalar(25.6)
        self.assertEqual(actual, expected)

    def testStopLossScalarUp(self):
        expected = 8.0 
        temp_session = TradeSession(None, None, TestStratUp(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, 200), 10.0, 4.0, None)
        temp_session.buyPrice = 10.01
        temp_session.quantity = 10
        temp_session.bought = True 
        temp_session.update({'close': 10.01, 'timestamp': 1592028900000})
        actual = temp_session.sl
        
        self.assertEqual(expected, actual)


        expected = True 
        actual = temp_session.CHECK_STOPLOSS({'close': 9.1, 'timestamp': 1592028900000})
        self.assertEqual(expected, actual)

    def testStopLossScalarDown(self):
        expected = 2.0
        temp_session = TradeSession(None, None, TestStratDown(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, 200), 10.0, 4.0, None)
        temp_session.buyPrice = 10.01
        temp_session.quantity = 10
        temp_session.bought = True 
        temp_session.update({'close': 10.01, 'timestamp': 1589892300000})
        actual = temp_session.sl
        self.assertEqual(expected, actual)

        expected = True 
        print(f"new stop loss --------------> {temp_session.sellStrat.toString()}")
        actual = temp_session.CHECK_STOPLOSS({'close': 9.40, 'timestamp': 1589892300000})
        self.assertEqual(expected, actual)
        
    def testTakeProfitScalarUp(self):
        expected = 8.0 
        temp_session = TradeSession(None, None, TestStratUp(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, 200), 10.0, 4.0, None)
        temp_session.buyPrice = 10.01
        temp_session.quantity = 10
        temp_session.bought = True 
        temp_session.update({'close': 10.01, 'timestamp': 1592028900000})
        actual = temp_session.sl
        
        self.assertEqual(expected, actual)


        expected = False 
        actual = temp_session.CHECK_TAKEPROFIT({'close': 11.4, 'timestamp': 1592028900000})
        self.assertEqual(expected, actual)


    def testPriceUpdate(self): #this should fail locally 
        strat = getStrat("TEST_STRAT")(None, None, None)
        strat.initialize()
        temp_session = TradeSession(None, None, strat, 4, 4, None)
        temp_session.update({"close": 2, "timestamp": 1593457200000 - 25200000})
        temp_session.update({"close": 22, "timestamp": 1593500400000 - 25200000})
        expected = {"2020-06-29": {"open": 2, "close": 22}}
        actual = temp_session.openClose
        self.assertEqual(expected, actual)
