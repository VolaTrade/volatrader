from Trader.SellLogic import Instance
import unittest

class TestTrailingStop(unittest.TestCase):
        

        def testSellLogicFloatGreaterThanTen(self):

            test_instance = Instance()
            test_instance.setStopLossPercent(25.5)
            test_instance.run(100.0)
            expected = True 
            actual = test_instance.run(74.5)

            self.assertEqual(expected, actual)


        def testSellLogicIntGreaterThanTen(self):


            test_instance = Instance()
            test_instance.setStopLossPercent(25)
            test_instance.run(100.0)
            expected = True 
            actual = test_instance.run(75.0)

            self.assertEqual(expected, actual)

        def testSellLogicFloatLessThanTen(self):

            test_instance = Instance()
            test_instance.setStopLossPercent(1.1)
            test_instance.run(100.0)
            expected = 98.9 
            actual = test_instance.slVal
            
            self.assertEqual(expected, actual)


        def testSellLogicIntLessThanTen(self):

            test_instance = Instance()
            test_instance.setStopLossPercent(1)
            test_instance.run(100.0)
            expected = 99.0
            actual = test_instance.slVal

            self.assertEqual(expected, actual)

        
        def testSellLogicIntEqualTen(self):

            test_instance = Instance()
            test_instance.setStopLossPercent(10)
            test_instance.run(100.0)
            expected = 90.0
            actual = test_instance.slVal

            self.assertEqual(expected, actual)

        
