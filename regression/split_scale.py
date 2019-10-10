import random
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler
from env import get_db_url
import wrangle
from pydataset import data

### As a customer analyst, I want to know who has spent the most money with us over their lifetime. I have monthly charges and tenure, so I think I will be able to use those two attributes as features to estimate total_charges. I need to do this within an average of \$5.00 per customer.

url = get_db_url('telco_churn')
df = pd.read_sql('''
SELECT customer_id, tenure, monthly_charges, total_charges
FROM customers
where contract_type_id = 3
''', url)
df = wrangle.drop_nulls(wrangle.wrangle_telco(df))

### Create split_scale.py that will contain the functions that follow. Each scaler function should create the object, fit and transform both train and test. They should return the scaler, train df scaled, test df scaled. Be sure your indices represent the original indices from train/test, as those represent the indices from the original dataframe. Be sure to set a random state where applicable for reproducibility!

def split_my_data(x, y, train_pct = .80):
    train_x, test_x, train_y, test_y = train_test_split(x, y, 
                                                        train_size = train_pct,
                                                        random_state = 123)
    return [train_x, train_y], [test_x, test_y]

def standard_scaler(train, test):
    scaler_object = StandardScaler(copy=True, 
                                   with_mean=True, 
                                   with_std=True).fit(train) 
    scaled_train = apply_object(train, scaler_object)
    scaled_test  = apply_object(test,  scaler_object)
    return scaler_object, scaled_train, scaled_test

def scale_inverse(array, scaler_object):
    return pd.DataFrame(scaler_object.inverse_transform(array), columns=array.columns.values).set_index([array.index.values])

def uniform_scaler(train, test, quantiles = 100):
    scaler_object = QuantileTransformer(n_quantiles=quantiles, 
                                 output_distribution='uniform', 
                                 random_state=123, 
                                 copy=True).fit(train)
    scaled_train = apply_object(train, scaler_object)
    scaled_test  = apply_object(test,  scaler_object)
    return scaler_object, scaled_train, scaled_test

def gaussian_scaler(train, test ,method = 'yeo-johnson'):
    scaler_object = PowerTransformer(method = method, 
                                     standardize = False, 
                                     copy = True).fit(train)
    scaled_train = apply_object(train, scaler_object)
    scaled_test  = apply_object(test,  scaler_object)
    return scaler_object, scaled_train, scaled_test
    
def min_max_scaler(train, test):
    scaler_object = MinMaxScaler(copy=True, 
                                 feature_range=(0,1)).fit(train)
    scaled_train = apply_object(train, scaler_object)
    scaled_test  = apply_object(test,  scaler_object)
    return scaler_object, scaled_train, scaled_test

def iqr_robust_scaler(train, test, quantiles = (25.0, 75.0)):
    scaler_object = RobustScaler(quantile_range = quantiles, 
                                 copy = True, with_centering=True, 
                                 with_scaling = True).fit(train)
    scaled_train = apply_object(train, scaler_object)
    scaled_test  = apply_object(test,  scaler_object)
    return scaler_object, scaled_train, scaled_test

def apply_object(x, scaler_object):
    return pd.DataFrame(scaler_object.transform(x), 
                        columns=x.columns.values).set_index([x.index.values])

