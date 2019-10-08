#data wrangling
# The first step will be to acquire and prep the data. Do your work for this exercise in a file named wrangle.py.
from scipy import stats
import pandas as pd
import numpy as np
from pydataset import data 
from env import get_db_url

# Acquire customer_id, monthly_charges, tenure, and total_charges from telco_churn database for all customers with a 2 year contract.
url = get_db_url('telco_churn')
df = pd.read_sql('''
SELECT customer_id, monthly_charges, tenure, total_charges
FROM customers
WHERE contract_type_id = 3''', url)
# Walk through the steps above using your new dataframe. You may handle the missing values however you feel is appropriate.

# End with a python file wrangle.py that contains the function, wrangle_telco(), that will acquire the data and return a dataframe cleaned with no missing values.