from pydataset import data
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols
from sklearn.metrics import explained_variance_score
import seaborn as sns
import math
import warnings
warnings.filterwarnings('ignore')


def plot_residuals(x,y,dataframe):
    sns.residplot(x,y,data = dataframe)

def regression_errors(y,yhat):
    sse = ((yhat - y)**2).sum()
    ess = ((yhat - y.mean())**2).sum()
    tss = sse + ess
    mse = sse/len(y)
    rmse = math.sqrt(mse)
    return {'sse': sse, 'ess': ess, 'tss': tss, 'mse' : mse, 'rmse' : rmse }

def baseline_mean_errors(y):
    yhat = y.mean()
    sse = ((yhat - y)**2).sum()
    mse = sse/len(y)
    rmse = math.sqrt(mse)
    return {'sse': sse, 'mse' : mse, 'rmse' : rmse }