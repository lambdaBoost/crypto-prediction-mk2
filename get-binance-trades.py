# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 19:05:03 2021

@author: Alex
"""

#TODO - check pairs exist on binance before looping through every combination

import os
import pandas as pd
from binance.client import Client


api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

#list of top 20 for now. Use seperate api to automatically populate this later
CURRENCIES = ['ETH', 'BTC', 'USDT', 'ADA', 'BNB', 'XRP', 'SOL', 'DOT', 'DOGE',
              'USDC', 'BUSD', 'LUNA', 'LINK','UNI', 'LTC', 'BCH', 'AVAX',
              'ALGO', 'ICP', 'ATOM']



LIMIT = 100 #max number of trades per pair

def make_trading_pairs(currency_list):
    """
    
    Returns
    -------
    list of all possible trading pairs from the currencies list

    """
    
    pair_list = list()
    
    for i in range(len(currency_list)):
        for j in(range(len(currency_list))):
            if i != j:
                pair = currency_list[i] + currency_list[j]
                pair_list.append(pair)
                
    return pair_list

def get_biggest_trading_pair():
    
    client = Client(api_key, api_secret)
    
    exchange_info = client.get_exchange_info()
    
    pair = exchange_info['symbols'][0]['symbol']
    
    return pair
    
    

def get_recent_trades(sym, lim):
    
    client = Client(api_key, api_secret)

    res = client.get_recent_trades(symbol=sym, limit=lim)
    

    return res


def get_max_time(trades, limit):
    """
    gets time of least recent trades from a retrieved json of recent trades

    Parameters
    ----------
    trades : list
        json from get_recent_trades.

    Returns
    -------
    None.

    """
    
    time = trades[limit]['time']
    
    return time

def filter_cutoff_time(trades, cut_time):
    
    """"
    filter out trades before the cutoff time
    
    """
    
    filtered = [d for d in trades if d['time'] < cut_time]
    
    return filtered


    
def get_qty_from_trades(trades):
    """
    return trade sizes from list of trades. uses isbuyermaker flag to define
    sells and buys using
    
    isBuyerMaker = true -> SELL
    isBuyerMaker = false -> BUY

    """
    
    qtys = [d['qty'] for d in trades]
    isBuyerMaker = [d['isBuyerMaker'] for d in trades]
    isBuyerMaker = [int(i) for i in isBuyerMaker]
    qtys = [float(i) for i in qtys]

    #multiply sells by -1 and buys by 1
    isBuyerMaker = [((-2*i)+1) for i in isBuyerMaker]  #convert to + and -1
    qtys = [a*b for a,b in zip(qtys,isBuyerMaker)]
    
    #probably dont need this if data is to be stored in a matrix
   # if(len(qtys) < limit):
        
    #    qtys += [0] * (limit - len(qtys))
    
    return qtys




if __name__ == "__main__":
    
    top_pair = get_biggest_trading_pair()
    
    top_pair_trades = get_recent_trades(top_pair, LIMIT)
    
    cutoff_time = get_max_time(top_pair_trades, LIMIT-1)
    
    
    results_df = pd.DataFrame(columns = CURRENCIES, index=CURRENCIES)
    
    
    for i in range(len(CURRENCIES)):
        for j in(range(len(CURRENCIES))):
            if i != j:
                
                curr1 = CURRENCIES[i]
                curr2 = CURRENCIES[j]
                pair = curr1 + curr2
                print(pair)
                
                try:
                    trades = get_recent_trades(pair, LIMIT)
                    trades = filter_cutoff_time(trades, cutoff_time)
                    trade_total = sum(get_qty_from_trades(trades))
                
                    results_df[curr1][curr2] = trade_total
                    
                except:
                    continue

