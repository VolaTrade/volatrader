from .strategy_interface import StrategyInterface

class TestStrategy(StrategyInterface):

    def __init__(self):
        super().__init__()

    def check_buy(self):
        return True 

    def check_sell(self):
        return True