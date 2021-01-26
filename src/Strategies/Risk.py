import numpy as np
import random
import math
import statistics

#CCi30 and rfr stuff
import requests
import re
from datetime import date
today = str(date.today())


'''Risk Measures'''

#Alpha is used in finance as a measure of performance, indicating when a strategy, trader, or portfolio manager has managed to beat the market return over some period. Alpha, often considered the active return on an investment, gauges the performance of an investment against a market index or benchmark that is considered to represent the market’s movement as a whole. The excess return of an investment relative to the return of a benchmark index is the investment’s alpha. Alpha may be positive or negative and is the result of active investing.
def Alpha(stock_return, market_return, risk_free_rate):
    return statistics.mean(stock_return) - CAPM(stock_return, market_return, risk_free_rate)
#It is important to understand the concept of alpha formula because it is used to measure the risk-adjusted performance of a portfolio.


# Beta is a measure of the volitility of a portfolio compared to the market
def Beta(stock_return_list, market_return_list):
    return Covariance(stock_return_list, market_return_list) / statistics.variance(market_return_list)


# Sharpe ratio is a proxy of total portfolio risk often used to compare the change in overall risk-return characteristics when a new asset or asset class is added to a portfolio
def Sharpe_Ratio(return_list, risk_free_rate): #percentage profit loss
    return (statistics.mean(return_list) - risk_free_rate) / statistics.stdev(return_list)

# Less than 1: Bad
# 1 – 1.99: Adequate/good
# 2 – 2.99: Very good
# Greater than 3: Excellent

# Limitations
# It assumes that returns are normally distributed (like rolling dices should eventually give a bell curve). However, financial markets are skewed away from the average due to surprising drops and spikes.
# Our Sharpe Ratio can be adjusted lengthening the measurement interval, which would lower the estimate of volatility.
# Also we could choose a period with the best potetential rather than a neutral look-back period


# Standard deviation used to help minimize your risk and still maximize returns. It measures how much the investment returns deviate from the mean of the probability distribution of investment
# Expected return measures the mean or expected value of probability distribution of investment returns. COULD BE GOOD TO IMPLEMENT LATER.
# Doesn't take risk into account and is based largely on historic data


#R-squared will give you an estimate of the relationship between movements of a dependent variable based on an independent variable's movements.
def R_sqr(output, regression_output):
    mean = statistics.mean(output)
    output = [(x - mean)**2 for x in output]
    regression_output = [(x - mean)**2 for x in regression_output]
    return sum(regression_output)/sum(output)
    #Closer to 1, the better
#SHOULD INCLUDE ADJUSTED R^2 LATER SO WE CAN COMPARE A REGRASSION W/ MULTIPLE INDEPENDENT VARIABLES


'''Variations of Risk Measures'''

"""# Rolling sharpe ratio provides a continually-updated, albeit rearward-looking, view of current reward-to-risk. Should help us identify strategy decay over time.
def Rolling_Sharpe_Ratio(return_list, risk_free_rate):
    # In order to calculate an annualised rolling Sharpe ratio it is necessary to make two modifications to this formula. The first is to reduce the set of returns to the last trailing number of annualised trading periods (e.g. for daily data this means take the last 252 close-to-close returns)
    # Multiply the value by the square root of the number of annual trading periods. For strategies trading on a daily timeframe the number of periods is equal to 252, the (approximate) number of trading days in the US
    return math.sqrt(len(return_list)) * Sharpe_Ratio(new_return_list, risk_free_rate)
    
THERE"S A BETTER (more accurate) WAY TO CALCULATE THIS

"""


# Sortino ratio is based off the Sharpe Ratio and differentiates harmful volatility from total overall volatility by using the asset's standard deviation of negative portfolio returns, called downside deviation, instead of the total standard deviation of portfolio returns.
def Sortino_Ratio(return_list, risk_free_rate):
    negative_return_list = [x for x in return_list if x < 0]
    n = len(negative_return_list)
    if(n > 1):
        return (statistics.mean(return_list) - risk_free_rate) / statistics.stdev(negative_return_list)  # focus on only the negative returns
    return "N/A"

# Higher number is better, similar to Sharpe ratio.
# The Sortino ratio improves upon the Sharpe ratio by isolating downside or negative volatility from total volatility by dividing excess return by the downside deviation instead of the total standard deviation of a portfolio or asset.


"""# Just as the Sortino ratio is modelled after the Sharpe Ratio, I wrote the equivalent using the Rolling Sharpe Ratio as my base and creating the Rolling Sortino Ratio. This probably has been done before, so I will research it, see if its viable, and update this portion.
def Rolling_Sortino_Ratio(return_list, period):
    new_return_list = return_list[(len(return_list) - period):len(return_list)]
    return math.sqrt(period) * Sortino_Ratio(new_return_list)"""


# Treynor ratio is based off the Sharpe Ratio and compares the risk of our portfolio to the risk of the market. Should allow us to determine reward-to-volatility ratio.
def Treynor_Ratio(stock_return_list, market_return_list, risk_free_rate):
    return (statistics.mean(stock_return_list) - risk_free_rate) / Beta(stock_return_list, market_return_list)

#For negative values of Beta, the Ratio does not give meaningful values.
#When comparing two portfolios, the Ratio does not indicate the significance of the difference of the values, as they are ordinal. For example, a Treynor Ratio of 0.5 is better than one of 0.25, but not necessarily twice as good.
#The numerator is the excess return to the risk-free rate. The denominator is the Beta of the portfolio, or, in other words, a measure of its systematic risk.

# A main weakness of the Treynor ratio is its backward-looking nature. Investments are likely to perform and behave differently in the future than they did in the past. The accuracy of the Treynor ratio is highly dependent on the use of appropriate benchmarks to measure beta.
# When comparing similar investments, the higher Treynor ratio is better, all else equal, but there is no definition of how much better it is than the other investments.


'''Statistics Sample Functions'''
def Standard_Error(return_list):
    return statistics.stdev(return_list)/math.sqrt(len(return_list))

def Margin_Error(return_list, z_score):
    return z_score * (statistics.stdev(return_list)/math.sqrt(len(return_list)))
    #2.58: 99% confidence

def Sample_Size(return_list, z_score, error):
    return 4*(z_score)**2*statistics.variance(return_list)/(2*error)**2

def Confidence_Interval(return_list, z_score):
    mean = statistics.mean(return_list)
    std = statistics.stdev(return_list)
    n = len(return_list)
    confidence_interval = [(mean-z_score*std/math.sqrt(n)), (mean+z_score*std/math.sqrt(n))]
    return confidence_interval


'''Predictive Functions'''
# Capital Asset Pricing Model (CAPM). The formula for calculating the expected return of an asset given its risk.
def CAPM(stock_return, market_return, risk_free_rate):
    return risk_free_rate + Beta(stock_return, market_return) * (statistics.mean(market_return) - risk_free_rate)

#Expected Value gives the average of all gains and losses over an infinite amount of time given the probability of occurence and average returns. Remember strategies "decay" over time meaning they become less viable as others use new/different strategies.
def Expected_Value(average_returns, probability, loss): #reduced, easy to understand version
    if(probability > 1):
        probability = probability/100
    return average_returns*probability + (loss*(1-probability))

#The correlation coefficient is a statistical measure of the strength of the relationship between the relative movements of two variables. The values range between -1.0 and 1.0. A calculated number greater than 1.0 or less than -1.0 means that there was an error in the correlation measurement. A correlation of -1.0 shows a perfect negative correlation, while a correlation of 1.0 shows a perfect positive correlation. A correlation of 0.0 shows no linear relationship between the movement of the two variables.
def Correlation(return_list, correlary):
    return (Covariance(return_list, correlary)/(statistics.stdev(return_list)*statistics.stdev(correlary)))
#Analysts in some fields of study do not consider correlations important until the value surpasses at least 0.8. However, a correlation coefficient with an absolute value of 0.9 or greater would represent a very strong relationship.

'''Other Functions'''

def Percent_list(return_list):
    return_list = [(return_list[i] - return_list[i+1])/return_list[i+1]*100 for i in range(len(return_list) - 1)]

    return return_list

# Variance measures variability from the average. The variance statistic can help determine the risk when purchasing a specific security.


# Covariance.
def Covariance(return_list, return_list2):
    xm = statistics.mean(return_list)
    ym = statistics.mean(return_list2)
    covariance = 0
    n = len(return_list)
    for i in range(n):
        covariance += (return_list[i] - xm) * (return_list2[i] - ym)
    return  covariance/(n - 1)
    # https://www.investopedia.com/terms/c/covariance.asp


'''Important Values'''

def CCi30():
    try:
        url = "https://cci30.com/ajax/getIndexHistory.php"
        r = requests.get(url)

        stringlist = re.split(',|\n', r.text)
        dictionary = {}
        length = len(stringlist) - 1
        i = 6
        while i < length:
            dictionary[stringlist[i]] = float(stringlist[i+3])
            i += 6
        
        r.close() 
    
        return dictionary
    
    except Exception as e:
        print("Error fetching CCI30 data: ", e)
        raise e

def CCi30list():
    try:
        dictionary = CCi30()
        date = dictionary.keys()
        data = dictionary.values()
        data = [float(x) for x in data]
        return date, data
    except Exception as e:
        print("Error fetching CCI30 data: ", e)
        raise e

def RFR():
    try:    
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DGS3MO&scale=left&cosd=2015-06-10&coed=2020-06-10&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=" + today + "&revision_date=" + today + "&nd=1982-01-04"
        r = requests.get(url)

        stringlist = re.split(',|\n', r.text)
        i = len(stringlist) - 2
        while stringlist[i] == ".":
            i -= 2
        r.close() 

        return float(stringlist[i])
    except Exception as e:
        print("Error fetching CCI30 data: ", e)
        raise e

def RFRall():
    try:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DGS3MO&scale=left&cosd=2015-06-10&coed=2020-06-10&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=" + today + "&revision_date=" + today + "&nd=1982-01-04"
        r = requests.get(url)

        stringlist = re.split(',|\n', r.text)
        dictionary = {}
        i = 2
        length = len(stringlist) - 2
        while i < length:
            if stringlist[i+1] != ".":
                dictionary[stringlist[i]] = float(stringlist[i+1])
            else:
                dictionary[stringlist[i]] = float(stringlist[i-1])
            i+=2
        
        r.close() 
        
        return dictionary
    except Exception as e:
        print("Error fetching CCI30 data: ", e)
        raise e
