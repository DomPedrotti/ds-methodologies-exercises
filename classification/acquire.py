from env import get_db_url
import pandas as pd

def get_titanic_data():
    query = 'select * from passengers'
    df = pd.read_sql(query, get_db_url('titanic_db'))
    return df


def get_iris_data():
    query = '''
    select * 
    from measurements
    join species 
    using(`species_id`)
    '''
    df = pd.read_sql(query, get_db_url('iris_db'))
    return df