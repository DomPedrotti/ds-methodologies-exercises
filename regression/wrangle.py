#!/usr/bin/env python
# coding: utf-8

# In[84]:


#wrangle data
import warnings
warnings.filterwarnings('ignore')

from env import get_db_url
import pandas as pd
import numpy as np


# ### 1) Acquire customer_id, monthly_charges, tenure, and total_charges from telco_churn database for all customers with a 2 year contract.

# In[176]:


url = get_db_url('telco_churn')
df = pd.read_sql('''
SELECT customer_id, monthly_charges, total_charges
FROM customers
where contract_type_id = 3
''', url)


# In[177]:


df.head(5)


# In[178]:


df.shape


# In[179]:


df.describe()


# In[180]:


df.info()


# ### 2) Walk through the steps above using your new dataframe. You may handle the missing values however you feel is appropriate.

# In[181]:


# no null values
# total_charges may have some wrong data causing values to be object instead of floats


# In[182]:


df.sort_values('total_charges').head(15)


# In[183]:


df_clean = df[df.total_charges != ' ']


# In[184]:


df_clean.total_charges = df_clean.total_charges.apply(float)


# In[185]:


df.shape


# In[186]:


df.describe()


# ### 3) End with a python file wrangle.py that contains the function, *wrangle_telco()*, that will acquire the data and return a dataframe cleaned with no missing values.

# In[207]:


def wrangle_telco(df):
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    return df
def drop_nulls(df):
    return df.dropna()


# In[208]:


df.shape


# In[211]:


df_clean = wrangle_telco(df)
df_clean.total_charges = df_clean.total_charges.apply(float)

df_clean.sort_values('total_charges').tail(15)


# In[215]:


df.info()


# In[203]:


df_clean = drop_nulls(df_clean)
df_clean.shape


# In[ ]:




