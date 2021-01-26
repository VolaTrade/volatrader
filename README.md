# The Volatrader


## Installation

## Components
1. [Backtester](#Backtester)
2. [PaperTrader](#PaperTrader)
3. [LiveTrader](#LiveTrader)
4. [DataBase](#DataBase)


## To fix make changes on server live, run this command:
`systemctl restart volatrade-production`

## Backtester
To run a backtest, make sure you're in `src/BackTest` and run the following:
```bash
python Backtester.py -p <Pair> --candleSize <candlesize> --strategy <strategy> -sl <stoploss percentage> -tp <take profit percentage> --principle <principle> --readFromDatabase <optional; false> --outputGraph True -t <timet to backtest on>
```

## PaperTrader
To start a paper trading instance, run the following replacing <> with your own params
```bash
python PaperTraderDriver.py --pair <pair> --candlesize <candlesize> --strategy <strat> -sl <stoploss> -tp <takeprofit> -pr <principle>   
```

## LiveTrader
Yet to be implemented; Let's figure out a working strat before we blow all of our cash ;)


## DataBase
### To Access
Ensure [postgresql](https://www.postgresql.org/download/) is installed


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
