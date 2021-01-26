import numpy as np
import random
import math
from scipy import special

# 252 trading periods over a year for stocks

# risk free rate is 3 month US Treasury bill's interest rate used by most US traders (SUGGESTION TO USE IEF INSTEAD)


# Standard deviation used to help minimize your risk and still maximize returns. It measures how much the investment returns deviate from the mean of the probability distribution of investments
def Standard_Deviation(return_list):
    return math.sqrt(Variance(return_list))
# Expected return measures the mean or expected value of probability distribution of investment returns. COULD BE GOOD TO IMPLEMENT LATER.
# Doesn't take risk into account and is based largely on historic data


# Variance measures variability from the average. The variance statistic can help determine the risk when purchasing a specific security.
def Variance(return_list):
    average_return = Mean(return_list)
    variance_list = [(x-average_return)**2 for x in return_list]
    return sum(variance_list) / len(variance_list)

# Market risk premium can be calculated by subtracting the risk-free rate from the expected equity market return, providing a quantitative measure of the extra return demanded by market participants for increased risk. NEED MORE INFO.
def Market_Risk_Premium(market_return):
    return Market_return(market_return) - risk_free_rate

# Covariance.
def Covariance(return_list, return_list2):
    xm = Mean(return_list)
    ym = Mean(return_list2)
    covariance = 0
    n = len(return_list)
    for i in range(n):
        covariance += (return_list[i] - xm) * (return_list2[i] - ym)
    return  covariance/(n - 1)
    # https://www.investopedia.com/terms/c/covariance.asp

# For investors, high kurtosis of the return distribution implies that the investor will experience occasional extreme returns (either positive or negative), more extreme than the usual + or - three standard deviations from the mean that is predicted by the normal distribution of returns. This phenomenon is known as kurtosis risk.
def Kurtosis(return_list):
    average = Mean(return_list)
    x1_list = [(x-average)**2 for x in return_list]
    x2_list = [(x-average)**4 for x in return_list]
    x1 = sum(x1_list) / len(x1_list)
    x2 = sum(x2_list) / len(x2_list)
    return (x2 / (x1 ** 2)) - 3

# NEED MORE INFO ON WHICH FORMULA IS MORE ACCURATE
def Kurtosis2(return_list):
    length = len(return_list)
    average = Mean(return_list)
    x1_list = [(x-average)**2 for x in return_list]
    x2_list = [(x-average)**4 for x in return_list]
    x1 = sum(x1_list) / (length - 1)
    x2 = sum(x2_list) / length
    return ((length * (length + 1)) / ((length - 1)*(length - 2)*(length - 3)))*(x2 / (x1 ** 2)) - (3*((length - 1) ** 2 / (length - 2)*(length - 3)))
# kurtosis = (0 +- 3 * standard deviation). Normal risk
# kurtosis > (0 + 3 * standard deviation). High risk
# kurtosis < (0 - 3 * standard deviation). Less risk


#A Recession is 2 quarters of negative GDP growth. BUY companies offering lower prices, vices such as alcohol (but not gambling!), and entertainment such as video games and netflix. Wait till Recession ends and put shit ton of money into the market and enjoy the upswing of recovery.
def isRecession():
    return bool(gdp_list[0] < 0 & gdp_list[1] < 0)

#Looks at GDP, unemployment, and inflation to determine strength of the economy. Higher the number more money people have to dump into stocks.
def Economic_Strength():
    total = 0
    score = 100/3
    if(gross_domestic_product > 0):
        total += gross_domestic_product * score/2.5 #2-3% growth for a healthy economy
    if(short_term_unemployment >= 4 & short_term_unemployment <= 6):
        total += score #between 4% - 6% for a healthy economy
    #elif(short_term_unemployment < 4):
        #total += score - (score/2 * (4-short_term_unemployment)) #too little unemployment leads to inflation but that is covered now in CPI
    elif(short_term_unemployment > 6):
        total += score - (score/2 * (short_term_unemployment-6))
    CPI_growth = Percentage_Growth(CPI_list[0],CPI_list[1])
    if (CPI_growth < 3.5):
        total += score - (score/2 * (CPI_growth - 3.5)) # < 3.5% for a healthy economy
    elif(CPI_growth > 0):
        total += score
    return total

#Price-to-Earnings (P/E) Ratio. Fundamental tool to evaluate stocks
def Price_Earnings_Ratio(market_value, earnings, total_shares):
    return (market_value/total_shares)/(earnings/total_shares)
    #P/E ratio by dividing a company's market value per share by its earnings per share.
    #if > 1 overvalued (sell)
    #if < 1 undervalued (buy)

#Limitations to the P/E Ratio
#The first part of the P/E equation or price is straightforward as the current market price of the stock is easily obtained. 
# On the other hand, determining an appropriate earnings number can be more difficult. 
# Investors must determine how to define earnings and the factors that impact earnings. As a result, there are some limitations to the P/E ratio as certain factors can impact the P/E of a company. Those limitations include:

#Volatile market prices, The earnings makeup of a company are often difficult to determine, Earnings growth is not included in the P/E ratio


#The PEG ratio measures the relationship between the price/earnings ratio and earnings growth to provide investors with a more complete story than the P/E alone. 
def PEG(market_value, earnings, total_shares, earnings_per_share_growth):
    PE = Price_Earnings_Ratio(market_value, earnings, total_shares) #*The number used for annual growth rate can vary. It can be forward (predicted growth) or trailing and can be anywhere from a one-to-five-year time span. Please check with the source providing the PEG ratio to determine what type of growth number and time frame is being used in the calculation.
    return PE/earnings_per_share_growth
    #PEG ratio by dividing PE by annual earnings per share growth
    #if > 1 overvalued (sell)
    #if < 1 undervalued (buy)

#Expected Value gives the average of all gains and losses over an infinite amount of time given the probability of occurence and average returns. Remember strategies "decay" over time meaning they become less viable as others use new/different strategies.
def Expected_Value(average_returns, probability, loss): #reduced, easy to understand version
    return average_returns*probability - (loss*(1-probability))
    
#def Expected_Value(average_returns, probability): #advanced
    #return #integral(0, infinity)(x*f(x)*d(x))

def Stock_Correlation(stock_return, stock_return2):
    #need to make it take from the last n indices of the return lists
    n = len(stock_return)
    sum1 = sum(stock_return)
    sum2 = sum(stock_return2)
    xy_return = [x for x in stock_return * y for y in stock_return2]
    xy_sum = sum(xy_return)
    sqr_return = [x**2 for x in stock_return]
    sqr_sum = sum(sqr_return)
    sqr_return2 = [x**2 for x in stock_return2]
    sqr_sum2 = sum(sqr_return2)
    return ((n*xy_sum - sum1*sum2)/math.sqrt((n*sqr_return-sum1**2)*(n*sqr_return2-sum2**2)))
#A correlation -1 shows that as one stock goes up the other will tend to go down and vice versa


#percentage_growth takes 2 values and returns the % gained or lost
def Percentage_Growth(original, next_int):
    return ((next_int - original)/original)*100

# Average Returns. It can help measure the past performance of a security or the performance of a portfolio.
def Mean(return_list):
    # Average Return = Sum of Returns/Number of Returns
    return sum(return_list)/len(return_list)

#The simple average of returns is an easy calculation, but it is not very accurate. For more accurate returns calculations, analysts and investors also use frequently the geometric mean or money-weighted return.


#WIP
'''   
    #Fear and greed indicator: https://www.investopedia.com/terms/f/fear-and-greed-index.asp
    def Fear_Greed(): 
        return

    #Usually higher in bear markets
    def Volatility():
        return
'''


def generateCorrelationMatrix():
    matrix = [[]]
    stocklist = getStocks() #need to make method getStocks
    for i in range(stocklist):
        cor_list = []
        for j in range(stocklist):
            if i == j:
                cor_list.append(0)
            else:
                value = Stock_Correlation(getData(stocklist[i]), getData(stocklist[j])) #need to make method getData
                if value >= 1 | value <= -1:
                    cor_list.append(value)
                else:
                    cor_list.append(0)
        matrix.append(cor_list)
    return matrix



# Monte Carlo Simulation are used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of random variables. It is a technique used to understand the impact of risk and uncertainty in prediction and forecasting models.
def Monte_Carlo(return_list):
    # Periodic Daily Return=ln( Previous Day’s Price/Day’s Price)
    # Drift=Average Daily Return − Variance/2
    # Random Value=σ×NORMSINV(RAND())
    # Next Day’s Price=Today’s Price×e**(Drift+Random Value)
    current_price = return_list[len(return_list) - 1]
    previous_price = return_list[len(return_list) - 2]
    periodic_return = math.log(current_price/previous_price)
    drift = Mean(return_list) - Variance(return_list) / 2
    random_value = Standard_Deviation(return_list) * ICND(random.randrange(0, 1))
    return current_price*math.exp(drift+random_value)
#Examines of the properties of estimators.

# Repeat this calculation the desired number of times (each repetition represents one day) to obtain a simulation of future price movement. By generating an arbitrary number of simulations, you can assess the probability that a security's price will follow given trajectory.
# The most likely return is at the middle of the curve, meaning there is an equal chance that the actual return will be higher or lower than that value. The probability that the actual return will be within one standard deviation of the most probable ("expected") rate is 68%; that it will be within two standard deviations is 95%; and that it will be within three standard deviations is 99.7%. Still, there is no guarantee that the most expected outcome will occur, or that actual movements will not exceed the wildest projections.
# Crucially, Monte Carlo simulations ignore everything that is not built into the price movement (macro trends, company leadership, hype, cyclical factors); in other words, they assume perfectly efficient markets. For example, the fact that Time Warner lowered its guidance for the year on November 4 is not reflected here, except in the price movement for that day, the last value in the data; if that fact were accounted for, the bulk of simulations would probably not predict a modest rise in price.

# I think this should be used in conjunction with fibonnaci arcs to get a better picture of the more "correct" predictions.

#Inverse Cumulative Normal Distribution(ICND)
def ICND(random_num):
    return random_num


def Quantile(return_list, p_score):
    return Mean(return_list) + Standard_Deviation(return_list) * math.sqrt(2)*special.erfinv(2*p_score-1)

#Expected Return given alpha and beta
def Expected_Return(stock_return, market_return):
    return Alpha(stock_return, market_return) + Beta(stock_return, market_return) * Total_percent_return(market_return)

#IDEAS

"""def p(return_list):
    return special.erf(len(return_list)/math.sqrt(2))"""
