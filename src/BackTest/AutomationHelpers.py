import os 
import sys
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from Trader.Indicators.IndicatorConstants import getIndicator, getModifiableIndicator
from Strategies.Strategies import getStratIndicatorNames
import itertools
from DataBasePY.DBReader import DBReader
from typing import List, Tuple
from Strategies.Strategies import getStratSourceCode    
import copy 

def checkIfStratChanged(strat_name: str, reader: DBReader=DBReader(), getStratSourceCode=getStratSourceCode) -> tuple:
    current_source: str = getStratSourceCode(strat_name)

    try:
        version, database_source = reader.getStrategySource(strat_name)

    except Exception as e: #strategy isn't in table yet 
        print("strategy DNE")
        return None, None, current_source 

    print("version ----> ", version)
    if database_source != current_source: #strategy is in table, but different 
        return True, version, current_source

    return False, version, None #strategy is in table, but the same 



def getIndicatorVariationsList(names: list):
    
    return [getIndicator(e.value)['variation_period'] for e in names]


#TODO unit test
def getAllPossibleIndicatorParamCombos(strategy: str, getIndicatorVariationsList=getIndicatorVariationsList) -> Tuple[list, int]:

    names: list = getStratIndicatorNames(strategy)
    possibles: list = []

        
    for variation_period in getIndicatorVariationsList(names):
        l: list = []

        if variation_period is None:
            continue

        for period in variation_period:

            if isinstance(period, tuple):

                for other_val in range(period[0], period[1]+1):
                    print("TUPLE CASE")
                    l.append(other_val)
            else:
                print("NONTUPLE CASE")
                l.append(period)

        possibles.append(l)

    

    return [e for e in itertools.product(*possibles)]


#TODO unit test 
def buildSkeleton(possibilities: tuple, indicators: List[dict], names_list: List[str]) -> dict: 
    index: int = 0 
    skeleton = {}
    for ind, indicator in enumerate(indicators):

        param_dict = {}
        skeleton[names_list[ind].value] = indicator.copy()

        for key in indicator['parameters'].keys():
            
            if len(possibilities) == 0:
                param_dict[key], skeleton['max'] = indicator['parameters']['period'], indicator['parameters']['period']
            else:
                param_dict[key] = possibilities[index] 
                index += 1 

        skeleton[names_list[ind].value]["parameters"] =  param_dict.copy()

    if len(possibilities) != 0:
        skeleton["max"] = max(possibilities)

    return skeleton

def getIndicatorsList(names_list: List[str]) -> List[dict]:
    return [getModifiableIndicator(e.value) for e in names_list]



