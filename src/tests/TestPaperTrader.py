import unittest 
from unittest.mock import Mock, MagicMock
from PaperTrader.PaperTrader import PaperTrader
from Strategies.Strategies import TEST_STRAT
from Helpers.Constants.Enums import Pair, Candle, Time
class TestPaperTrader(unittest.TestCase):



    def testIsProfitUpdateWithTwoVal(self):
        test_session =  PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None, Time.MONTH, None)
        test_session.currentPrice = 10
        expected = True 
        actual = test_session.isProfitUpdate(2)
        
        self.assertEqual(expected, actual)


    def testIsProfitUpdateWithoutTwoVal(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.currentPrice = 10
        expected = False
        actual = test_session.isProfitUpdate(1)
        self.assertEqual(expected, actual)


    def testIsTimeToUpdateNonZero(self):
        test_session =  PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.timeStep = 10 
        expected = True 
        actual = test_session.isTimeToUpdate(20)
        self.assertEqual(expected, actual)

        expected = False 
        actual = test_session.isTimeToUpdate(21)
        self.assertEqual(expected, actual)

    def testIsTimeToUpdateZero(self):
        test_session =PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.timeStep = 10 
        expected = True 
        actual = test_session.isTimeToUpdate(0)
        self.assertEqual(expected, actual)


    def testPreinstall(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        updateFunc = Mock()
        candles = [1] * 100
        expected_calls = 100
        test_session.preinstall(candles, updateFunc)
        actual = updateFunc.call_count
        self.assertEqual(expected_calls, actual)


    def testTerminationCheckTrue(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        reader = Mock()
        reader.return_value = False
        
        try:
            test_session.checkForTermination(reader)
            assert False 
        except Exception:
            assert True 

    # def testBuyUpdateHourlyUpdate(self):
    #     test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
    #     test_session.pair = Pair.ETHUSDT
    #     test_session.candleSize = Candle.FIVE_MINUTE
    #     test_session.takeProfitPercent = 2
    #     test_session.stopLossPercent = 3 
    #     tradeSess_func, candleFetch_func, slack_logger, file_logger, time = MagicMock(), Mock(), Mock(), Mock(), Mock()  
    #     getResults_func = Mock()
    #     tradeSess_func.update.return_value = True 
    #     tradeSess_func.update(None, None)
    #     expected = True 
    #     actual = test_session.buyUpdate(0, tradeSess_func, candleFetch_func, logToSlack=slack_logger, logDebugToFile=file_logger, time=time)

    #     self.assertEqual(expected, actual)
    #     print(slack_logger.call_count == 1) 
    #     assert slack_logger.call_count == 1 

    def testBuyUpdateCandleFetchException(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.pair = Pair.ETHUSDT
        test_session.candleSize = Candle.FIVE_MINUTE
        test_session.takeProfitPercent = 2
        test_session.stopLossPercent = 3 
        tradeSess_func, candleFetch_func, slack_logger, file_logger, time = MagicMock(), Mock(), Mock(), Mock(), Mock()  
        getResults_func = Mock()
        candleFetch_func.side_effect = Exception(Mock(), "fake")
        tradeSess_func.update.return_value = True 
        tradeSess_func.update(None, None)

        expected = None 
        actual = test_session.buyUpdate(0, tradeSess_func, candleFetch_func, logToSlack=slack_logger, logDebugToFile=file_logger, time=time)


        self.assertEqual(expected, actual)

    def testBuyUpdateTradeSessionReturnsFalse(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.pair = Pair.ETHUSDT
        test_session.candleSize = Candle.FIVE_MINUTE
        test_session.takeProfitPercent = 2
        test_session.stopLossPercent = 3 
        tradeSess_func, candleFetch_func, slack_logger, file_logger, time = MagicMock(), Mock(), Mock(), Mock(), Mock()  
        getResults_func = Mock()
        tradeSess_func.update.return_value = False 
        tradeSess_func.update(None, None)
        expected = False 
        actual = test_session.buyUpdate(34, tradeSess_func, candleFetch_func, logToSlack=slack_logger, logDebugToFile=file_logger, time=time)
        self.assertEqual(expected, actual)


    def testBuyUpdateTradeSessionReturnsTrue(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.pair = Pair.ETHUSDT
        test_session.candleSize = Candle.FIVE_MINUTE
        test_session.takeProfitPercent = 2
        test_session.stopLossPercent = 3 
        tradeSess_func, candleFetch_func, slack_logger, file_logger, time = MagicMock(), Mock(), Mock(), Mock(), Mock()  
        getResults_func = Mock()
        tradeSess_func.update.return_value = True 
        tradeSess_func.update(None, None)
        expected = True 
        actual = test_session.buyUpdate(34, tradeSess_func, candleFetch_func, logToSlack=slack_logger, logDebugToFile=file_logger, time=time, test=True)
        self.assertEqual(expected, actual)

    def testSellUpdateAPIreturnsBadData(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.pair = Pair.ETHUSDT
        binance_func, slack_logger, file_logger = Mock(), Mock(), Mock()
        session = Mock()
        time = Mock()
        binance_func.return_value = "FUCK"

        expected = None 
        actual = test_session.sellUpdate(session, binance_func, slack_logger, file_logger, time)

        self.assertEqual(expected, actual)
        slack_logger.assert_called_once()


    def testSellUpdateSessionReturnsTrue(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.pair = Pair.ETHUSDT
        binance_func, slack_logger, file_logger = Mock(), Mock(), Mock()
        session = Mock()
        session.update.return_value = True 
        session.update(None , None)
        time = Mock()
        binance_func.return_value = (12.4, None)     
        expected = True 
        actual = test_session.sellUpdate(session, binance_func, slack_logger, file_logger, time)

        
        self.assertEqual(expected, actual)


    def testSellUpdateSessionReturnsFalse(self):
        test_session = PaperTrader(None, Candle.FIFTEEEN_MINUTE, "TEST_STRAT", 1, 2, None,Time.MONTH, None)
        test_session.pair = Pair.ETHUSDT
        
        binance_func, slack_logger, file_logger = Mock(), Mock(), Mock()
        session = Mock()
        session.update.return_value = False 
        session.update(None , None)
        time = Mock()
        binance_func.return_value = (12.4, None)     
        expected = False 
        actual = test_session.sellUpdate(session, binance_func, slack_logger, file_logger, time)
        
        self.assertEqual(expected, actual)
