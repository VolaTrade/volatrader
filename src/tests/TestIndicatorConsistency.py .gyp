import unittest 
from Helpers.Constants.Enums import Indicator
from Indicators.IndicatorFunctions import getFunction
from Indicator.IndicatorConstants import getIndicator 
class TestIndicatorConsistency(unittest.TestCase):


    def testEqualityConsistency(self):
        enums = [e.value for e in Indicator]

        for value in enums:

            try:
                _ = getFunction(value)
            except Exception as e:
                print(e)
                self.assertFalse()

            try:
                _ = getIndicator(value)

            except Exception as e:
                print(e)
                self.assertFalse()

        self.assertTrue()