from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
import numpy as np

def prep_iris(df):

    #drop id columns
    clean_df = df
    for i in df.columns.to_list():
        if '_id' in i:
            clean_df = clean_df.drop(i, axis = 1)

    #rename species_name to species
    clean_df.rename(columns = {'species_name':'species'}, inplace=True)

    #encode species
    encoder = LabelEncoder().fit(clean_df.species)
    clean_df.species = encoder.transform(clean_df.species)

    return clean_df


def prep_titanic(titan):

    # Handle the missing values in the embark_town and embarked columns.
    clean_titan=titan[ ~titan.embarked.isnull()]

    # Remove the deck column.
    clean_titan.drop('deck', axis = 1, inplace= True)

    # Use a label encoder to transform the embarked column.
    encoder = LabelEncoder().fit(clean_titan.embarked)
    clean_titan.embarked = encoder.transform(clean_titan.embarked)

    # Scale the age and fare columns using a min max scaler. Why might this be beneficial? When might you not want to do this?
    scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(clean_titan[['age', 'fare']])
    clean_titan[['age', 'fare']] = scaler.transform(clean_titan[['age', 'fare']])

    return clean_titan