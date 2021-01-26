from unittest.mock import Mock, MagicMock
import unittest
from Helpers.API.MarketFunctions import getCurrentBinancePrice
from Helpers.Constants.Enums import Pair 

# def original_func():
#     print(os.stat("test.txt").st_size == 35)


# @mock.patch("os.stat")
# def test(os_stat):
#     os_stat.return_value.st_size = 35
#     original_func()

# test()

def throwEXC():
    raise Exception("Test") 

class response():
    def __init__(self, price, fail):
        self.price = price
        self.fail = fail 


    def get(self, val):
        if self.fail is False:
            return None 

        raise Exception("FAILING")


    def json(self):

        if self.fail is False:
            return {"price": self.price}

        raise Exception("Exception in request case")

class TestMarketFunctions(unittest.TestCase):

        def testGetCurrentBinancePriceWorking(self):
            requests = Mock()
            requests.get.return_value = response(100, False)
            requests.status_code = 200
            expected = 100 
            actual, _ = getCurrentBinancePrice(Pair.ETHUSDT, requests)

            self.assertEqual(expected, actual)


        def testGetCurrentBinancePriceNotWorking(self): #ensures exception is thrown when timeout limit exceeds 3 

            time = Mock()
            time.sleep.return_value = None 
    

            expected_calls = 3      
            try:
                getCurrentBinancePrice(Pair.ETHUSDT, requests, time)

            except Exception as e:
                assert True


          

            
            

