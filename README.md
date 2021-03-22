# Strategies

### Strategy Development 

 All strategies must be of form: 
```
class README_STRATEGY(strategy):
    def __init__(self, pair: Pair, candle: Candle, principle: int):
        super().__init__(pair, candle, principle)
        self.indicatorConstants = [] #Insert indicators to use 

    def checkBuy(self, candle):
        if self.interValUpdate(candle) is False:  #This super method updates the indicator values dynamically and automatically 
            return WAIT 
        
        #insert buy execution logic here 
    
        return HODL 
    
        # All indicators are stored in self.indicators object
```
Strategy must be/have:
* Subclass of strategy class
* checkBuy method that returns some boolean value 
