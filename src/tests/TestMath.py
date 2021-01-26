import unittest
import math
import statistics
from Strategies import Risk

class TestMath(unittest.TestCase):
    def testPercentList(self):
        output = [30, 40, 45, 40, 20]
        expected = [-25.0, -11.11111111111111, 12.5, 100.0]
        output = Risk.Percent_list(output)
        self.assertEqual(expected, output)

    def testCovariance(self):
        expected = 841.6666666666666
        output1 = [-30, 10, 5, 19]
        output2 = [-25.0, -11.11111111111111, 12.5, 100.0]
        output = Risk.Covariance(output1, output2)
        self.assertEqual(expected, output)

    def testBeta(self):
        output1 = [-30, 10, 5, 19]
        output2 = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = 841.6666666666666/statistics.variance(output2)
        output = Risk.Beta(output1, output2)
        self.assertEqual(expected, output)

    def testCAPM(self): 
        output1 = [-30, 10, 5, 19]
        output2 = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = (841.6666666666666/statistics.variance(output2)) * statistics.mean(output2)
        output = Risk.CAPM(output1, output2, 0)
        self.assertEqual(expected, output)

    def testAlpha(self): 
        output1 = [-30, 10, 5, 19]
        output2 = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = statistics.mean(output1) - ((841.6666666666666/statistics.variance(output2)) * statistics.mean(output2))
        output = Risk.Alpha(output1, output2, 0)
        self.assertEqual(expected, output)

    def testSharpe(self):
        output = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = statistics.mean(output)/statistics.stdev(output)
        output = Risk.Sharpe_Ratio(output, 0)
        self.assertEqual(expected, output)
    
    """def testRollingSharpe(self):
        output = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = math.sqrt(4)*(statistics.mean(output)/math.sqrt(3148.6304012345677))
        output = Risk.Rolling_Sharpe_Ratio(output, 0)
        self.assertEqual(expected, output)"""
    
    def testSortino(self):
        output = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = statistics.mean(output)/statistics.stdev([-25.0, -11.11111111111111])
        output = Risk.Sortino_Ratio(output, 0)
        self.assertEqual(expected, output)
    
    def testTreynor(self):
        output1 = [-30, 10, 5, 19]
        output2 = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = statistics.mean(output1)/(841.6666666666666/statistics.variance(output2))
        output = Risk.Treynor_Ratio(output1, output2, 0)
        self.assertEqual(expected, output)

    """def testEV(self):
        output = [30, 40, 45, 40, 20]
        expected = [-25.0, -11.11111111111111, 12.5, 100.0]
        
        output = Expected_Value(average_returns, probability, loss)
        self.assertEqual(expected, output) MIGHT NEED A BETTER VERSION TO CALCULATE IT"""

    def testCorrelation(self):
        output1 = [-30, 10, 5, 19]
        output2 = [-30, 10, 5, 19]
        expected = 0.9999999999999999
        output = Risk.Correlation(output1, output2)
        self.assertEqual(expected, output)
    def testCorrelation2(self):
        output1 = [-30, 10, 5, 19]
        output2 = [30, -10, -5, -19]
        expected = -0.9999999999999999
        output = Risk.Correlation(output1, output2)
        self.assertEqual(expected, output)
    def testCorrelation3(self):
        output1 = [-30, 10, 5, 19]
        output2 = [-25.0, -11.11111111111111, 12.5, 100.0]
        expected = 0.698853092597985
        output = Risk.Correlation(output1, output2)
        self.assertEqual(expected, output)
        
    