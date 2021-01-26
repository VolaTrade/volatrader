import unittest
from BackTest.DarwinsDict import DarwinsDict 
from BackTest.Result import Result
from Helpers.Constants.Enums import Pair, Candle 

class TestDarwinsDict(unittest.TestCase):

    def testInsertSameKey(self):
        sof = DarwinsDict()

        r1 = Result(Pair.ETHUSDT, Candle.FIVE_MINUTE, None, None, 3, None, None, None, None)
        r1.setScore(3)
        r2 = Result(Pair.ETHUSDT, Candle.FIVE_MINUTE, None, None, 3, None, None, None, None)
        r2.setScore(10)
        sof.insert(r1)
        sof.insert(r2)

        expected = r2.score
        actual = sof.getResults()

        assert len(actual) == 1 

        assert type(actual) is list 

        actual = actual[0]
        
        self.assertEqual(actual.score, expected)


    def testInsertSameKeyBeta(self):
        sof = DarwinsDict()
        r1 = Result(Pair.ETHUSDT, Candle.FIVE_MINUTE, None, None, 3, None, None, None, None)
        r1.setScore(10)
        r1.setBeta(3)
        r2 = Result(Pair.ETHUSDT, Candle.FIVE_MINUTE, None, None, 3, None, None, None, None)
        r2.setScore(10)
        r2.setBeta(2)
        sof.insert(r1)
        sof.insert(r2)
        expected = r2.strat_score_beta
        actual = sof.getResults()

        assert len(actual) == 1 

        assert type(actual) is list 

        actual = actual[0]
        
        self.assertEqual(actual.strat_score_beta, expected)
        
    

    def testInsertDifferentKey(self):
        sof = DarwinsDict()

        r1 = Result(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, None, None, 3, None, None, None, None)
        r1.setScore(3)
        r2 = Result(Pair.ETHUSDT, Candle.FIVE_MINUTE, None, None, 3, None, None, None, None)
        r2.setScore(10)
        sof.insert(r1)
        sof.insert(r2)
        assert len(sof.getResults()) == 2

        