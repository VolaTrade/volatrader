import unittest 
from Helpers.Constants.Enums import Indicator
from Trader.Indicators.IndicatorFunctions import getFunction
from Trader.Indicators.IndicatorConstants import getIndicator 
class TestIndicatorConsistency(unittest.TestCase):


    def testEqualityConsistency(self):
        enums = [e.value for e in Indicator]

        for value in enums:
            print(value)
            try:
                _ = getFunction(value)
            except Exception as e:
                raise e
                

            try:
                _ = getIndicator(value)

            except Exception as e:
                raise e 

        assert True, "All tests passed"


    def testAllConstantsHaveProperKeys(self):

        enums = [e.value for e in Indicator]
        keys = ["parameters", "graph_features", "values", "calculatedWithCandles", "variation_period"]
        for value in enums:

            ind = getIndicator(value)

            for key in keys:

                if key not in ind.keys():
                    assert False, f"Key --> {key} not found for --> {value}"


    def testAllConstantsHaveProperValues(self):
        enums = [e.value for e in Indicator]

        for value in enums:
            ind = getIndicator(value)

            for key in ind['variation_period'].keys():
                assert ind['variation_period'][key] is None or isinstance(ind['variation_period'][key], list)

