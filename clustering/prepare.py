from summarize import nulls_by_col

def handle_missing_values(df, prop_required_column= .95, prop_required_row = .8):
    missing_columns = nulls_by_col(df)
    features = missing_columns[missing_columns.pct_rows_missing < (1-prop_required_column)].index.tolist()
    
    df = df[features]

    thresh = int(df.shape[1]*prop_required_row) + 1
    df = df.dropna( thresh = thresh )
    
    return df

def get_single_unit_properties(df):

    df = (df[(df.propertylandusedesc == 'Single Family Residential') |
             (df.propertylandusedesc == 'Manufactured, Modular, Prefabricated Homes')])

    return df
    