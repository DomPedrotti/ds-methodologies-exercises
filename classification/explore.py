import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


def plot_bars(features, target, df):
    for column in df[features].select_dtypes([object, int]).columns.tolist():
        if len(df[column].unique()) <= 5:
            sns.barplot(column, target, data=df)
            plt.title(column)
            plt.ylabel(target)
            plt.show()

def plot_violin(features, target, df):
    for descrete in df[features].select_dtypes([object,int]).columns.tolist():
        if df[descrete].nunique() <= 5:
            for continous in df[features].select_dtypes(float).columns.tolist():
                sns.violinplot(descrete, continous, hue=target,
                data=df, split=True, palette=['blue','orange'])
                plt.title(continous + 'x' + descrete)
                plt.ylabel(continous)
                plt.show()

