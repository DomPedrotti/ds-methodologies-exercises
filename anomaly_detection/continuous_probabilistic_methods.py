import matplotlib.pyplot as plt
import pandas as pd


def get_lower_and_upper_bounds(series, method = 'iqr', multiplier = 1.5):
    '''
    get_lower_and_upper_bounds(series, method = 'iqr', multiplier = 1.5)

    function to identify outliers in data
    calculates upper and lower bound for outliers in data using specified method, at specified sensitivity

    args:
    series -  pandas series containing numerical values
    method - (str) specified method, 
        'iqr' - uses product of multiplier and the interquartile range (difference between 75th and 25th percentiles) to determine bounds
        'std' - uses product of multiplier and the standard deviation of data to determine bounds (assumes normality)
    multiplier - (float) sensitivity of function to outliers, choose a larger multiplier to relax sensitivity to outliers

    returns:
    (tuple of floats) lower bound and upper bound
    '''
    #determine method to use
    if method == 'iqr':
        #find interquartile range, add to 75th pctl for upper bound and sutract from 25th for lower
        iqr_range = series.quantile(.75)-series.quantile(.25)
        lower_bound = series.quantile(.25) - (iqr_range * multiplier)
        upper_bound = series.quantile(.75) + (iqr_range * multiplier)
    elif method == 'std':
        #find standard deviation, add to mean for upper bound and subtract for lower
        sigma = series.std()
        mu = series.mean()
        lower_bound = mu - (sigma * multiplier)
        upper_bound = mu + (sigma * multiplier)
    #return calculated bounds
    return lower_bound,upper_bound


def plot_columns(series, outlier_method = 'iqr', multiplier = [1.5]):
    plt.scatter(x = series.index, y = series)
    
    #plot upper and lower outlier bounds
    if type(multiplier) is not list:
        multiplier = [multiplier]
    for i in multiplier:
        low,high = get_lower_and_upper_bounds(series, method = outlier_method, multiplier = i)
        plt.hlines(low, xmin= series.index.min(), xmax=series.index.max(), linestyles=':')
        plt.hlines(high, xmin= series.index.min(), xmax=series.index.max(), linestyles=':')
        
    #make plot
    plt.title(series.name)
    plt.xticks(rotation = 45)
    plt.show()