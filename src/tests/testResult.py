import unittest
from Backtest import Result

class TestResult(unittest.TestCase):
    def testBuildResult(self):
        result = Result.Result(0, 0, 0, 0, 100, 100, {}, {})
        self.assertEqual(result.score, 100)
    
    def testGetData(self):
        result = Result.Result(0, 0, 0, 0, 100, 100, {}, {})
        return_list, stock_return, market_return, risk_free_rate = result.modifyData([], [10, 12, 16.8, 21.84])
        self.assertFalse(risk_free_rate, 0)

    
    def testAnalyzeScore(self):
        result = Result.Result(0, 0, 0, 0, 100, 100, {}, {})
        result.analyzeScores([10, 0, 0], [10, 20, 30],[20, 40, 30], 0,)
        self.assertFalse(risk_free_rate, 0)

    def testAnalyzeData(self):
        result = Result.Result(0, 0, 0, 0, 100, 100, {}, {})
        result.analyzeData([10, 0, 0], [10, 20, 30])
        self.assertEqual(result.stock_pnl, 60) 

    def testAnalyzeSample(self):
        result = Result.Result(0, 0, 0, 0, 100, 100, {}, {})
        result.analyzeSample([10, 0, 0], 1.96)
        self.assertEqual(result.size, 3)
        
    def testCompetitor(self):
        result = Result.Result(0, 0, 0, 0, 100, 100, {}, {})
        competitor_list = [-1, 17, 1, 18, 5, 3, 7, 3, 7, 13, 13, 8, 15, 13, 6, 1, 7, 9, 16, 3, 6, 3, -1, -2, 5, 8, 4, 7, 3, 1]
        rfr, market = getData()
        result.analyzeData()