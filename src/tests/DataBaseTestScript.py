import os
import sys
import uuid
sys.path.append(os.path.dirname(os.getcwd()))
from DataBasePY.DBReader import DBReader
from DataBasePY.DBwriter import DBwriter
from DataBasePY.DBwriter import DBoperations
from Helpers.Constants.Enums import Pair, Candle, Time 
from termcolor import colored
from datetime import datetime
from Helpers.TimeHelpers import convertNumericTimeToString
from psycopg2.extras import register_uuid
from BackTest.Result import Result 
import traceback
import inspect

register_uuid()

# Any new arguments should be added here
r = Result(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, 2, 4, 4.3, 12.8, None, None, "SIXMONTH")
r.setScore(12)
r.setBeta(4)
r.setParams(       {
    "SMA": {
        "values": {
            "value": "blue"
        },
        "parameters": {
            "period": 15
        },
        "graph_features": {
            "mode": "lines",
            "withCandles": True
        },
        "variation_period": {
            "values": [
                10,
                15
            ]
        },
        "calculatedWithCandles": False
    },
    "WMA": {
        "values": {
            "value": "white"
        },
        "parameters": {
            "period": 4,
            "weighted_factor": 10
        },
        "graph_features": {
            "mode": "lines",
            "withCandles": True
        },
        "variation_period": {
            "period": [
                3,
                [
                    4,
                    5
                ]
            ],
            "weighted_factor": [
                [
                    10,
                    11
                ]
            ]
        },
        "calculatedWithCandles": False
    },
    "max": 15
})
failed, total = 0, 0 

test_params = {
    'sessionId': str(uuid.uuid4()),
    'pair':  Pair.ETHUSDT,
    'mean':  100.23,
    'candle': Candle.FIFTEEEN_MINUTE,
    'sdv': 32.33,
    'start_time': convertNumericTimeToString(datetime.now()),
    'end_time': convertNumericTimeToString(datetime.now()),
    'strategy': 'TEST_STRAT',
    'sl': 2.3,
    'tp': 4.4,
    'principle': 10000,
    'results': {'buyTime': 'buyTime', 'buyPrice': 150.23, 'sellTime': 'selltime', 'sellPrice': 155.32, 'profitLoss': 2.3},
    'pnl': 1.2,
    'support': 2.3,
    'resistance': 2.3,
    "strat_name": "TEST_STRAT",
    "version_num": 1,
    "source": "class TEST_STRAT()A;LDSFJ;AKLGJ;ASGKAJG;LAKJ;",
    "result" : r,
    "version_num": 2, 
    "time_stamp": "2020-06-26 00:00:00",

    
}

# Finds all valid function names with
operatorMethods = [method_name for method_name in dir(DBoperations)]

isValidMethod = lambda method_name, db_class: method_name.find('__') == -1 and callable(getattr(db_class, method_name)) and method_name not in operatorMethods

writerMethods = [method_name for method_name in dir(DBwriter) if isValidMethod(method_name, DBwriter)]
readerMethods = [method_name for method_name in dir(DBReader) if isValidMethod(method_name, DBReader)]


def testDbFunc(method, args):
    try:
        print(*args)
        method(*args)

    except Exception as e:
        print('Failed test: ')
        traceback.print_exc()

        return False
    return True


def test(db):
    global failed 
    global total 
    for method_name in (writerMethods if isinstance(db, DBwriter) else readerMethods):

        method = getattr(db, method_name)

        try:
            method_params = [test_params[arg] for arg in inspect.getfullargspec(method)[0] if arg != 'self']

        except:
            raise Exception("Method parameters not found for " + method_name + "() ... please enter them into the test_params dict"   )

        method_tup = tuple(method_params)
        passed = testDbFunc(method, method_tup)
        if not passed:
            failed +=1 
            print(colored(f'x - {method_name} test did not pass', 'red'))
        else:
            print(colored(u'\u2713' + f' - {method_name} test passed', 'green'))
        total += 1

def main():
    reader = DBReader()
    writer = DBwriter()
    test(writer)
    test(reader)

    print(f"\n{total-failed}/{total} " + colored("tests passed", "red" if failed != 0 else "green"))

main()
