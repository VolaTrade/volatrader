
"""
Indicator skeletons ... defines each individual indicator's logic 
"""
from typing import Dict
import copy 

def getPeriod(name: str):
    return globals()[name]['parameters']['period']

def getIndicator(name:  str):
    return copy.deepcopy(globals()[name])

def getModifiableIndicator(name:  str):
    return globals()[name]


BB = {"parameters": {"period": 14}, 
        "graph_features": {"withCandles": True, "mode": "lines"}, 
        "values": {
            'MOVING AVERAGE BB': "black", 
            'UPPER BAND BB': "grey", 
            'LOWER BAND BB': "grey"
            },
        "calculatedWithCandles": False, 
        "variation_period": {"period": None}
    }

EMA = { 
        "values":{"value": "yellow"}, 
        "parameters": {"period": 8, "alpha": .3, "epsilon": 0}, 
        "graph_features" : {"withCandles": True, "mode": "lines"},
        "calculatedWithCandles": False, 
        "variation_period": {"period": None}

    }

FIBBOLINGER = {
        "values": {
                    "Lower Band": "grey" ,
                    "FIB -2": "yellow", 
                    "Fib -1": "red",
                    "moving average": "black",
                    "FIB 1": "green",
                    "FIB 2": "blue",
                    "Upper Band": "grey"
                },

        "parameters": {"period": 100}, 
        "graph_features": {"mode": "lines", "withCandles": True},
        "calculatedWithCandles": False,
        "variation_period": {"period": [50, 100]}


        }
        
PATTERNABONDONEDBABY = {
        "parameters": {"period": 3}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "yellow"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True, 
        "variation_period": {"period": None}

    }


PATTERNHAMMER = {
        "parameters": {"period": 3}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "yellow"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True,
        "variation_period": {"period": None}
 
    }

PATTERNTHREEBLACKCROWES = {
        "parameters": {"period": 3}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "pink"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True, 
        "variation_period": {"period": None}
    }

PATTERNTHREEINSIDE = {
        "parameters": {"period": 3}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "pink"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True, 
        "variation_period": {"period": None}
    }

PATTERNTHREELINESTRIKE = {
        "parameters": {"period": 4}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "pink"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True,
        "variation_period": {"period": None}
    }

PATTERNTHREEWHITESOLDIERS = {
        "parameters": {"period": 3, "scalar": 1.5}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "yellow"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True, 
        "variation_period": {"period": None}
    }

PATTERNTWEEZERTOP = {
        "parameters": {"period": 2}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "yellow"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True, 
        "variation_period": {"period": None}
    }

PATTERNTWEEZERBOTTOM = {
       "parameters": {"period": 2}, 
        "graph_features": {"mode": "markers", "withCandles": True}, 
        "values": {"value": "yellow"}, 
        "user_adjusted": False,
        "calculatedWithCandles": True, 
        "variation_period": {"period": None}
}

MOM = {
    "parameters": {"period": 20}, 
    "graph_features" : {"withCandles": False, "mode": 'lines'},
    "values": {"value": "blue"},
    "calculatedWithCandles": False,
    "variation_period": {"period" : [5, 100]}

    }

RSI = {
    "parameters": {"period": 12}, 
    "graph_features" : {"withCandles": False, "mode": 'lines'},
    "values": {"value": "red"},
    "calculatedWithCandles": False, 
    "variation_period": {"period": [10, 100]}
}

SMA = {
    "parameters": {"period": 6},
    "graph_features": {"withCandles": True, "mode": 'lines'},
    "values": {"value": "blue"},
    "calculatedWithCandles": False,
    "variation_period": {"period": [10, 15]
    }
}

WMA =  { #TODO find the variation zones that can be applied for each param 
    "parameters" : {"period": 4, "weighted_factor": 10}, 
    "graph_features": {"mode": "lines", "withCandles": True}, 
    "values": {"value" : "white"},
    "calculatedWithCandles": False, 
    "variation_period": {"period": [3, (4,5)] , "weighted_factor": [(10, 11)]}
    }
