import requests
import pandas as pd

def get_full_sales_data(refresh = False):
    '''
    get_full_sales_data(refresh = False):

    reads sales, items, and stores csv files and joins information into one data frame

    args:
    refresh: if True, will pull current data from the original source, else will read from local csv files

    returns:
    dataframe
    '''
    #get data, rewrites all csv files with fresh data if refresh == true
    items = get_items_data(refresh = refresh)
    stores = get_stores_data(refresh = refresh)
    sales = get_sales_data(refresh = refresh)

    #join data into one dataframe
    sales.rename(columns={'store' : 'store_id', 'item':'item_id'}, inplace= True)
    df = sales.merge(stores.set_index('store_id'), on ='store_id')
    df = df.merge(items.set_index('item_id'), on = 'item_id')
    df.drop(columns = 'Unnamed: 0', inplace = True)

    return df

def get_items_data(refresh = False):
    '''
    get_items_data(refresh = False):

    finds item data and returns dataframe

    args:
    refresh: if True, will pull current data from the original source, else will read from local csv files

    returns:
    dataframe
    '''
    # rewrites csv file with fresh data if refresh == True
    if refresh:
        refresh_items()

    #read data from csv
    item_data = pd.read_csv('items.csv')
    return item_data
    

def get_stores_data(refresh = False):
    '''
    get_stores_data(refresh = False):

    finds store data and returns dataframe

    args:
    refresh: if True, will pull current data from the original source, else will read from local csv files

    returns:
    dataframe
    '''
    # rewrites csv file with fresh data if refresh == True
    if refresh:
            refresh_stores()

    #read data from csv
    stores_data = pd.read_csv('stores.csv')
    return stores_data
    

def get_sales_data(refresh = False):
    '''
    get_sales_data(refresh = False):

    finds sales data and returns dataframe

    args:
    refresh: if True, will pull current data from the original source, else will read from local csv files

    returns:
    dataframe
    '''
    # rewrites csv file with fresh data if refresh == True
    if refresh:
            refresh_sales()

    #read data from csv
    sales_data = pd.read_csv('sales.csv')
    return sales_data
    
def get_opsd_data(refresh = False):
    '''
    get_opsd_data(refresh = False):

    finds opsd data and returns dataframe

    args:
    refresh: if True, will pull current data from the original source, else will read from local csv files

    returns:
    dataframe
    '''
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
    '''
    refresh_data(data = None):

    Reads values direct from items pages on https://python.zach.lol/api/v1 api and rewrites saved csv files with new data

    args:
    None

    Returns:
    None
    '''
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
    items_df.to_csv('items.csv', index= False)

def refresh_stores():
    '''
    refresh_data(data = None):

    Reads values direct from stores pages on https://python.zach.lol/api/v1 api and rewrites saved csv files with new data

    args:
    None

    Returns:
    None
    '''
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
    stores_df.to_csv('stores.csv', index= False)


def refresh_sales():
    '''
    refresh_data(data = None):

    Reads values direct from sales pages on https://python.zach.lol/api/v1 api and rewrites saved csv files with new data

    args:
    None

    Returns:
    None
    '''
    #establish api url
    base_url = 'https://python.zach.lol'

    #establish first page url
    sales_url = base_url + '/api/v1/sales'

    #get api page information and read from page payload
    response = requests.get(sales_url)
    page = response.json()['payload']
    
    #get url extension for next page
    page['next_page']

    #establish variable to hold sales information
    sales = []

    #iterates through pages till the last page and appends sales inforation, breaks when 'next_page' == None 
    while True:
        sales += page['sales']
        if page['next_page'] == None:
            break
        page_url = base_url + page['next_page']
        response = requests.get(page_url)
        page = response.json()['payload']
    sales_df = pd.DataFrame(sales)
    sales_df.to_csv('sales.csv', index=False)

def refresh_opsd():
    '''
    refresh_data(data = None):

    Reads values direct from https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv api and rewrites saved csv files with new data

    args:
    None

    Returns:
    None
    '''
    #read data
    opsd = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')

    #write data to csv
    opsd.to_csv('opsd.csv')
