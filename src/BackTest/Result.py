from Strategies import Risk
import re
import math
import statistics
class Result:

    def __init__(self, pair, candle, sl, tp, pnl, accuracy, stock_dict, results, timeframe):
        self.key = f"{pair.value}-{candle.value}"
        self.pair = pair
        self.candle = candle
        self.sl = sl
        self.tp = tp 
        self.accuracy = accuracy
        self.stock_dict = stock_dict
        self.results = results 
        self.score = pnl 
        self.strat_score_beta = 0
        self.time_frame = timeframe
        self.params = None 

        self.error = -1
        self.size = 0
        self.std_err = -1
        self.ci = []
        self.ev = 0
        self.mean = 0
        self.strat_pnl = 0


    def setBeta(self, beta: float) -> None:
        self.strat_score_beta = beta


    def setParams(self, params: dict) -> None:
        self.params = params


    def buildAnalysis(self):
        rfr, market_dict = self.getData()
        return_list, stock_return, market_return, risk_free_rate = modifyData(rfr, market_dict)
        self.analyzeScores(return_list, stock_return, market_return, risk_free_rate)
        self.analyzeData(return_list, stock_return)
        self.analyzeSample(return_list, 1.96)
        
    def getData(self):
        return Risk.RFRall(), Risk.CCi30()
    
    def modifyData(self, rfr, market_dict):
        print(self.results)
        dates = [sdate for mdate in market_dict.keys() for sdate in self.stock_dict.keys() if mdate == sdate]
        stock_return = [float(self.stock_dict[date]) for date in dates]
        market_return = [float(market_dict[date]) for date in dates]
        rfr_list = [float(rfr[date]) for date in dates for rdate in rfr.keys() if date == rdate]
        
        n = len(rfr_list)
        if(n == 0):
            risk_free_rate = Risk.RFR()
        else:
            risk_free_rate = statistics.mean(rfr_list)
        stock_return = Risk.Percent_list(stock_return)
        market_return = Risk.Percent_list(market_return)

        return_dict = {}
        for result in self.results:
            bt = re.split(' ', result["buytime"])
            buytime = bt[0]
            return_dict[buytime] = float(result["profitloss"])

        print(dates)
        for i in range(len(dates) - 1):
            if dates[i] in return_dict.keys():
                return_list.append(return_dict[dates[i]])
            else:
                return_list.append(0)
        print(return_list)
        return return_list, stock_return, market_return, risk_free_rate

    def analyzeScores(self, return_list, stock_return, market_return, risk_free_rate):
        self.stock_score_alpha = Risk.Alpha(stock_return, market_return, risk_free_rate)
        self.stock_score_beta = Risk.Beta(stock_return, market_return)
        self.score_alpha = Risk.Alpha(return_list, market_return, risk_free_rate)
        self.score_beta = Risk.Beta(return_list, market_return)
        self.strat_score_alpha = score_alpha - stock_score_alpha
        self.strat_score_beta = score_beta - stock_score_beta

        self.score = self.strat_score_alpha

    def analyzeData(self, return_list, stock_return):
        self.strat_pnl = sum(return_list)
        self.mean = statistics.mean(stock_return)

        ev_profit = [float(result["profitloss"]) for result in self.results if (float(result["profitloss"]) > 0)]
        ev_loss = [float(result["profitloss"]) for result in self.results if (float(result["profitloss"]) < 0)]
        self.ev = Risk.Expected_Value(statistics.mean(ev_profit), self.accuracy, statistics.mean(ev_loss))

    def analyzeSample(self, return_list, z_score):
        self.size = len(return_list)
        self.ci = Risk.Confidence_Interval(return_list, z_score)
        self.std_err = abs(Risk.Standard_Error(return_list))
        self.error = abs(Risk.Margin_Error(return_list, z_score))
        self.sample_size = Risk.Sample_Size(return_list, z_score, 0.1)

    def setScore(self, score):
        self.score = score 

    def toString(self):
        return f"{self.pair}/{self.candle} {self.sl}|{self.tp}:\nAccuracy: {self.accuracy*100}%\tExpected Value: {self.ev}\tStock Mean: {self.mean}\nTotal Stock PnL: {self.stock_pnl}\tTotal Strategy PnL: {self.strat_pnl}\nAlpha Strategy Score: {self.strat_score_alpha}\tBeta Strategy Score: {self.strat_score_beta}\nAlpha Stock Score: {self.stock_score_alpha}\tBeta Stock Score: {self.stock_score_beta}\nTotal Alpha Score: {self.score_alpha}\tTotal Beta Score: {self.score_beta}\n+===============================================\nStock Sharpe Ratio: {Risk.Sharpe_Ratio(self.stock_return, self.risk_free_rate)}\tStock Sortino: {Risk.Sortino_Ratio(self.stock_return, self.risk_free_rate)}\tStock Treynor: {Risk.Treynor_Ratio(self.stock_return, self.market_return, self.risk_free_rate)}\nStrategy Sharpe Ratio: {Risk.Sharpe_Ratio(self.return_list, self.risk_free_rate)}\tStrategy Sortino: {Risk.Sortino_Ratio(self.return_list, self.risk_free_rate)}\tStrategy Treynor: {Risk.Treynor_Ratio(self.return_list, self.market_return, self.risk_free_rate)}\n+===============================================\nZ-Score: {self.z_score}\tConfidence Interval: {self.ci}\nMargin of Error: ±{self.error}\tStandard Error: ±{self.std_err}\nIdeal sample size: {self.sample_size}\tReal sample size: {self.size}"

