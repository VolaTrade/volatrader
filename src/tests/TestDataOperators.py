from Helpers.DataOperators import convertCandlesToDict, cleanCandle, fetchCandleData
from unittest.mock import Mock 
from Helpers.Constants.Enums import Pair, Candle 
import ccxt 
import unittest
import traceback

class TestDataOperators(unittest.TestCase):

    def testCleanCandle(self):
        candle_in = [123452457256, 1, 2, 3, 4, 24365]
        expected = {"timestamp": 123452457256, "open": 1, "high": 2, "low": 3, "close": 4, "volume": 24365}
        actual = cleanCandle(candle_in)
        assert expected == actual

    def testConvertCandlesToDict(self):

        candles = [[113234, 1,1,1,1, 3], [14341234, 2,2,2,2, 4]]
        expected = [{"timestamp": 113234, 'open': 1, 'high': 1, 'low': 1,'close': 1, 'volume': 3}, {"timestamp": 14341234,    'open': 2, 'high': 2, 'low': 2,'close': 2, 'volume': 4}]
        output = convertCandlesToDict(candles)
        print(candles)
        assert expected == output

    def testWrongValueConvertCandlesToDict(self):
        candles = [{"open"}]

        try:
            convertCandlesToDict(candles)

        except AssertionError:
            assert True


    def testFetchCandleDataFailureRetries(self):
        api = Mock()
        api.fetchOHLCV.side_effect = ccxt.RequestTimeout(Mock, 'not found')
        t = Mock()
        slack_logger = Mock()
        slack_logger.return_val = None
        try:
            fetchCandleData(api, Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, time=t, log=slack_logger)

        except TimeoutError as e:          
            assert True  


    def testFetchCandleDataGenericFailure(self):
        api = Mock()
        api.fetchOHLCV.side_effect = Exception(Mock, 'generic')
        t = Mock()
        slack_logger = Mock()
        slack_logger.return_val = None
        try:
            fetchCandleData(api, Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, time=t, log=slack_logger)

        except Exception as e:
            print(e)
            assert str(e).find('generic') != -1


    def testFetchCandleDataNonFailure(self):
        api = Mock()
        t = Mock()
        slack_logger = Mock()
        slack_logger.return_val = None
        try:
            fetchCandleData(api, Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, time=t, log=slack_logger)
        
        except Exception as e:
            assert False 


        assert True
