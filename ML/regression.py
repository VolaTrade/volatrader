import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def Linear(x, y):# x is indicators, y is price

    # sckit-learn implementation

    # Model initialization
    regression_model = LinearRegression()
    # Fit the data(train the model)
    regression_model.fit(x, y)
    # Predict
    y_predicted = regression_model.predict(x)

    # model evaluation
    rmse = mean_squared_error(y, y_predicted)
    r2 = r2_score(y, y_predicted)

    # printing values
    print('Slope:' ,regression_model.coef_)
    print('Intercept:', regression_model.intercept_)
    print('Root mean squared error: ', rmse)
    print('R2 score: ', r2)

    # plotting values

    # data points
    plt.scatter(x, y, s=10)
    plt.xlabel('x')
    plt.ylabel('y')

    # predicted values
    plt.plot(x, y_predicted, color='r')
    plt.show()
    return regression_model.coef_, regression_model.intercept_, rsme, r2

