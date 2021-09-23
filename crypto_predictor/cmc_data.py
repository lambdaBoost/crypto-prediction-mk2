# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 19:45:26 2021

@author: Alex
"""

import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd


def get_mkp_caps(key, lim = 5000):
    """
    

    Parameters
    ----------
    key : str
        api key for coinmarketcap
    lim: int
        top n currencies by mkt cap

    Returns
    -------
    dict of cc data by market cap

    """
    
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':str(lim),
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': key,
    }
    
    session = Session()
    session.headers.update(headers)
    
    try:
      response = session.get(url, params=parameters)
      dat = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      
    mc_dict = dat['data']


    df = pd.DataFrame(columns = ['coin','mkt_cap'], index=range(len(mc_dict)))
    
    for i in range(len(mc_dict)):
        
        df['coin'][i] = mc_dict[i]['symbol']
        df['mkt_cap'][i] = mc_dict[i]['quote']['USD']['market_cap']
        
        
    return df



def filter_viable_coins(currency_list, mc_data, benchmark_currencies, lim):
    """
    filters a list of viable currencies to get the top 'n' by market cap
    excludes benchmark currencies

    Parameters
    ----------
    currency_list : list
        list of viable currencies
    mc_data : DataFrame
        dataframe of top coins by mc
    benchmark_currencies: list
        list of the benchmark currencies
    lim: int
        number of currencies desired to be used as independant variables]

    Returns
    -------
    dataframe of top currencies by market cap

    """
    
    mc_data = mc_data[~mc_data['coin'].isin(benchmark_currencies)]
    
    mc_data = mc_data.head(lim)
    
    return mc_data




