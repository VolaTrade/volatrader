import unittest
from unittest.mock import Mock 
from Helpers.Constants.Enums import Indicator
from BackTest.AutomateBacktest import checkIfStratChanged, getAllPossibleIndicatorParamCombos, buildSkeleton


class TestAutomationFunctions(unittest.TestCase):

    
    def testStratChangedFunctionBasic(self):

        reader = Mock()
        func = Mock()
        func.return_value = ("0")
        reader.getStrategySource.return_value = (0, "1")
        expected = (True, 0, "0")
        actual = checkIfStratChanged("bullshit", reader, func)
        self.assertEqual(actual, expected)

        func.assert_called_once()
        reader.getStrategySource.assert_called_once()

    def testStratChangedFalseCase(self):

        reader = Mock()
        func = Mock()
        func.return_value = ("0")
        reader.getStrategySource.return_value = (0, "0")
        expected = (False, 0, None)
        actual = checkIfStratChanged("bullshit", reader, func)
        self.assertEqual(actual, expected)

        func.assert_called_once()
        reader.getStrategySource.assert_called_once()

    def testStratChangedErrorCase(self):

        reader = Mock()
        func = Mock()
        func.return_value = ("0")
        reader.getStrategySource.side_effect = Mock(side_effect=Exception('Test'))
        expected = (None, None, "0")
        actual = checkIfStratChanged("bullshit", reader, func)
        self.assertEqual(actual, expected)

    def testGetAllPossibleIndicatorParamCombos(self):
        
        mock_func = Mock()
        mock_func.return_value = [[1,2], [3, (6,7)]]

        expected = [(1,3), (1,6), (1,7), (2,3), (2,6), (2,7)]
        actual = getAllPossibleIndicatorParamCombos("TEST_STRAT", mock_func)

        self.assertEqual(expected, actual)


    def testGetAllPossibleIndicatorParamCombosWithNullVariationInd(self):
        mock_func = Mock()
        mock_func.return_value = [None, [1,2,3], [1]]

        expected = [(1,1), (2,1), (3,1)]
        actual = getAllPossibleIndicatorParamCombos("TEST_STRAT", mock_func)

        self.assertEqual(expected, actual)


    def testBuildSkeletonNoVariation(self):
        names_list = [Indicator.PATTERNTHREELINESTRIKE]
        indicators = [{
        "parameters": {"period": 4}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "pink"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True,
        "variation_period": None
        }]
        possibles = []

        expected = {'PATTERNTHREELINESTRIKE': {'parameters': {'period': 4}, 'graph_features': {'mode': 'markers', 'withCandles': True}, 'values': {'value': 'pink'}, 'user_adjusted': False, 'calculatedWithCandles': True, 'variation_period': None}, 'max': 4}

        actual = buildSkeleton(possibles, indicators, names_list)
        print(actual)
        self.assertEqual(expected, actual)


    def testBuildSkeletonVariation(self):
        names_list = [Indicator.SMA, Indicator.EMA]
        indicators = [{"parameters": {"period": 6},"graph_features": {"withCandles": True, "mode": 'lines'}, "values": {"value": "blue"},"calculatedWithCandles": False,"variation_period": {"values": [10, 15]}}, { "values":{"value": "yellow"}, "parameters": {"period": 8, "alpha": .3, "epsilon": 0}, "graph_features" : {"withCandles": True, "mode": "lines"},"calculatedWithCandles": False, "variation_period": None}]

        possibles = (1, 2, 3, 4)

        result = buildSkeleton(possibles, indicators, names_list)

        assert result["SMA"]['parameters']['period'] == 1 
        assert result['EMA']['parameters']['period'] == 2 
        assert result['EMA']['parameters']['alpha'] ==  3 
        assert result['EMA']['parameters']['epsilon']== 4