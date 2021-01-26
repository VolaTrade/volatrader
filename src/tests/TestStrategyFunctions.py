import unittest
from Strategies.Strategies import getIndicatorPeriodValues, getStratSourceCode
from Helpers.Constants.Enums import Indicator

class TestStrategyFunctions(unittest.TestCase):

    # def testGetIndicatorPeriodValues(self):
    #     indicators = [Indicator.PATTERNTHREELINESTRIKE]
    #     expected_max = 4
    #     expected_skeleton = {"PATTERNTHREELINESTRIKE": {
    #     "parameters": {"period": 4}, 
    #     "graph_features": {"mode": "markers", "withCandles": True}, 
    #     "values": {"value": "pink"}, 
    #     "user_adjusted": False,
    #     "calculatedWithCandles": True, 
    #     "variation_period": None,
    #     }}
        
    #     expected_indicators = {'PATTERNTHREELINESTRIKE': {'value': 'pink'}}
    #     actual_dict, actual_skeleton, actual_max = getIndicatorPeriodValues(indicators)
    #     self.assertEqual(expected_max, actual_max)
    #     self.assertEqual(expected_indicators, actual_dict)
    #     self.assertEqual(expected_skeleton, actual_skeleton)

        #TODO insert more 

    def testStratSourceCode(self):
        expected = "classTEST_STRAT(strategy):def__init__(self,pair:Pair,candle:Candle,principle:int):super().__init__(pair,candle,principle)defcheckBuy(self,candle=None):returnBUY"
        actual = getStratSourceCode("TEST_STRAT")
        print(f"actual ----> {actual}")
        self.assertEqual(expected, actual)


    def testStratSourceFailure(self):

        try:
            getStratSourceCode("FAKE_NAME")
            assert False

        except Exception:
             assert True 
