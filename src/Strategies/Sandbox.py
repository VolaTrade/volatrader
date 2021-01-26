from Strategies import Risk
import math
import statistics

def skeleton(indicator_list, stock_returns, start, end, future):
    coeff = correlationSignificance(indicator_list, stock_returns, start, end, future)
    if(coeff == 0):
        return False #Don't write anything
    buildRegression(name, time, stock_returns, indicator_dict)
    if(regressionSignificance(name, time, weight, bias, y_list, x_list)):
        return True #Write both into DB
    return False #Dont write regression. Write the indicator w/ correlation, it is correlated but not linearly.

def correlationSignificance(indicator_list, stock_returns, start, end, future):
    t_value = 1.701 
    n = len(indicator_list) # Sample size must be 30

    stock_returns = [stock_returns[i] for i in enumerate(stock_returns) if i in range(start+future, end+future+1)]
    indicator_list = [indicator_list[i] for i in enumerate(indicator_list) if i in range(start, end+1)]
    
    coeff = Risk.Correlation(stock_returns, indicator_list)
    test_statistic = (abs(coeff) - .8)/math.sqrt((1-coeff**2)/n-2)

    if(abs(test_statistic) > abs(t_value)):
        return coeff
    return 0

def buildRegression(name, time, stock_returns, indicator_dict):
    #Convert tuple indicator_dict into indicator_matrix, indicator_names
    indicator_matrix = [[],[]]
    indicator_names = []

    #fit data
    weights, bias, rsme, r2 = ML.Linear(indicator_matrix, stock_returns)

    #create dictionary of indicator name and weights
    weights_dict[name] = weight

    return name, time, weights_dict, bias, rsme, r2 #write all info into DB

def regressionSignificance(name, time, weight, bias, indicator_list, stock_returns):
    t_value = 1.701
    n = len(indicator_list) # Sample size must be 30

    y_mean = statistics.mean(indicator_list)
    indicator_list = [(y - y_mean)**2 for y in indicator_list]
    x_mean = statistics.mean(stock_returns)
    stock_returns = [(x - x_mean)**2 for x in stock_returns]
    
    SE = math.sqrt(sum(indicator_list)/(n - 2))/math.sqrt(sum(stock_returns)) #where yi is the value of the dependent variable for observation i, ŷi is estimated value of the dependent variable for observation i, xi is the observed value of the independent variable for observation i, x is the mean of the independent variable, and n is the number of observations.
    test_statistic = weight/SE #where b1 is the slope of the sample regression line, and SE is the standard error of the slope.
    
    if (abs(test_statistic) > abs(t_value)):
            return True
    return False
    