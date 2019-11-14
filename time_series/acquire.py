import requests
import pandas as pd

def get_full_sales_data(refresh = False):

    #get data, rewrites all csv files with fresh data if refresh == true
    items = get_items_data(refresh = refresh)
    stores = get_stores_data(refresh = refresh)
    sales = get_sales_data(refresh = refresh)

    #join data into one dataframe
    stores.rename(columns={'store_id' : 'store'}, inplace= True)
    items.rename(columns={'item_id':'item'}, inplace= True)
    df = sales.join(stores.set_index('store'), on ='store')
    df = df.join(items.set_index('item'), on = 'item')

    return df

def get_items_data(refresh = False):
    # rewrites csv file with fresh data if refresh == True
    if refresh:
        refresh_items()

    #read data from csv
    item_data = pd.read_csv('items.csv')
    return item_data
    

def get_stores_data(refresh = False):
    # rewrites csv file with fresh data if refresh == True
    if refresh:
            refresh_stores()

    #read data from csv
    stores_data = pd.read_csv('stores.csv')
    return stores_data
    

def get_sales_data(refresh = False):
    # rewrites csv file with fresh data if refresh == True
    if refresh:
            refresh_sales()

    #read data from csv
    sales_data = pd.read_csv('sales.csv')
    return sales_data
    
def get_opsd_data(refresh = False):

    # rewrites csv file with fresh data if refresh == True
    if refresh:
            refresh_opsd()

    #read data from csv
    opsd_data = pd.read_csv('opsd.csv')
    return opsd_data
    
def refresh_data(data = None):
    '''
    refresh_data(data = None):

    Reads values direct from corresponding api and rewrites saved csv files with new data

    args:
    data: name of csv to refresh, data = 'all' will refresh all csv files

    Returns:
    None
    '''
    #refresh all csv files
    if (data == None) or (data == 'all'):
        refresh_items()
        refresh_stores()
        refresh_items()
        refresh_opsd()

    # refresh items csv
    elif data == 'items':
        refresh_items()

    #refresh stores csv
    elif data == 'stores':
        refresh_stores()

    #refresh sales csv
    elif data == 'sales':
        refresh_data()

    #refresh opsd data
    elif data == 'opsd':
        refresh_opsd()
    
    # catch incorrect input
    else:
        print("Incorrect entry for data. Try: 'items', 'stores', 'sales', 'opsd', or 'all")

def refresh_items():
    base_url = 'https://python.zach.lol'
    items_url = base_url + '/api/v1/items'
    response = requests.get(items_url)
    page = response.json()['payload']
    items = []
    while True:
        items += page['items']
        if page['next_page'] == None:
            break
        page_url = base_url + page['next_page']
        response = requests.get(page_url)
        page = response.json()['payload']
    items_df = pd.DataFrame(items)
    items_df.to_csv('items.csv')

def refresh_stores():
    base_url = 'https://python.zach.lol'
    stores_url = base_url + '/api/v1/stores'
    response = requests.get(stores_url)
    page = response.json()['payload']
    stores = []
    while True:
        stores += page['stores']
        if page['next_page'] == None:
            break
        page_url = base_url + page['next_page']
        response = requests.get(page_url)
        page = response.json()['payload']
    stores_df = pd.DataFrame(stores)
    stores_df.to_csv('stores.csv')


def refresh_sales():
    base_url = 'https://python.zach.lol'
    sales_url = base_url + '/api/v1/sales'
    response = requests.get(sales_url)
    page = response.json()['payload']
    page['next_page']
    sales = []
    while True:
        sales += page['sales']
        if page['next_page'] == None:
            break
        page_url = base_url + page['next_page']
        response = requests.get(page_url)
        page = response.json()['payload']
    sales_df = pd.DataFrame(sales)
    sales_df.to_csv('sales.csv')

def refresh_opsd():
    opsd = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    opsd.to_csv('opsd.csv')
