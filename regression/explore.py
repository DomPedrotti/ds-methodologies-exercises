# exploration method functions
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import seaborn as sns

import wrangle as wgl
import split_scale as ss 

def plot_variable_pairs(dataframe):
    g = sns.PairGrid(dataframe)
    g.map_diag(plt.hist)
    g.map_offdiag(plt.scatter);


def months_to_years(tenure_months, df):
    df['tenure_months'] = tenure_months/12
    return df



def plot_categorical_and_continous_vars(categorical_var, continuous_var, df):
    pass