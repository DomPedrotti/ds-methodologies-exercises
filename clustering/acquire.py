import pandas as pd
from env import get_db_url

def df_summary(df):
    print('--- Shape: {}'.format(df.shape))
    print('--- Info')
    df.info()
    print('--- Descriptions')
    print(df.describe(include='all'))
    print('--- Nulls By Column')
    print(nulls_by_col(df))
    print('--- Nulls By Row')
    print(nulls_by_row(df))
    print('--- Value Counts')
    print(df_value_counts(df))

def nulls_by_col(df):
    count_missing = df.isnull().sum()
    average_missing = count_missing/df.shape[0]
    cols_missing = pd.DataFrame({'num_rows_missing': count_missing, 'pct_rows_missing': average_missing})
    return cols_missing

def nulls_by_row(df):
    num_cols_missing = df.isnull().sum(axis = 1)
    pct_cols_missing = num_cols_missing/df.shape[1]
    num_rows = pd.DataFrame({'num_rows':num_cols_missing}).groupby(num_cols_missing).count()
    num_pct = pd.DataFrame({'num_cols_missing': num_cols_missing, 'pct_cols_missing': pct_cols_missing})
    missing_stats = pd.merge(num_pct, num_rows, left_on='num_cols_missing', right_on=num_rows.index).drop_duplicates()
    missing_stats = missing_stats.sort_values('num_cols_missing').reset_index(drop = True)
    return missing_stats

def df_value_counts(df):
    counts = pd.Series([])
    for i, col in enumerate(df.columns.values):
        if df[col].dtype == 'object':
            col_count = df[col].value_counts()
        else:
            col_count = df[col].value_counts(bins=10, sort=False)
        counts = counts.append(col_count)
    return counts

def get_zillow_data():
    query = '''
    select * 
    from `predictions_2017`
    left join properties_2017
    using(`parcelid`)
    left join `airconditioningtype`
    using (`airconditioningtypeid`)
    left join `architecturalstyletype` as arch
    using(`architecturalstyletypeid`)
    left join `buildingclasstype`
    using(`buildingclasstypeid`)
    left join `heatingorsystemtype`
    using(`heatingorsystemtypeid`)
    left join `propertylandusetype`
    using(`propertylandusetypeid`)
    left join `storytype`
    using(`storytypeid`)
    left join `typeconstructiontype`
    using(`typeconstructiontypeid`)
    where (`latitude` is not null) and (`longitude` is not NULL)
    '''
    df = pd.read_sql(query, get_db_url('zillow'))
    
    df = df.sort_values(by = ['transactiondate'], axis = 0).drop_duplicates(keep = 'last', subset = 'parcelid')

    df.drop('id', axis = 1, inplace=True)

    return df

get_zillow_data()