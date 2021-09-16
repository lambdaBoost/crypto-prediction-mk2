# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 19:05:03 2021

@author: Alex
"""

#TODO - check pairs exist on binance before looping through every combination
#look into aggregated trades - may be a better alternative

import os
import pandas as pd

from crypto_predictor import datagrabber



api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

#list of top 20 for now. Use seperate api to automatically populate this later
CURRENCIES = ['ETH', 'BTC', 'USDT', 'ADA', 'BNB', 'XRP', 'SOL', 'DOT', 'DOGE',
              'USDC', 'BUSD', 'LUNA', 'LINK','UNI', 'LTC', 'BCH', 'AVAX',
              'ALGO', 'ICP', 'ATOM']



LIMIT = 100 #max number of trades per pair






if __name__ == "__main__":
    
    top_pair = datagrabber.get_biggest_trading_pair(api_key, api_secret)
    
    top_pair_trades = datagrabber.get_recent_trades(top_pair, LIMIT, api_key, api_secret)
    
    cutoff_time = datagrabber.get_max_time(top_pair_trades, LIMIT-1)
    
    
    results_df = pd.DataFrame(columns = CURRENCIES, index=CURRENCIES)
    
    
    for i in range(len(CURRENCIES)):
        for j in(range(len(CURRENCIES))):
            if i != j:
                
                curr1 = CURRENCIES[i]
                curr2 = CURRENCIES[j]
                pair = curr1 + curr2
                print(pair)
                
                try:
                    trades = datagrabber.get_recent_trades(pair, LIMIT, api_key, api_secret)
                    trades = datagrabber.filter_cutoff_time(trades, cutoff_time)
                    trade_total = sum(datagrabber.get_qty_from_trades(trades))
                
                    results_df[curr1][curr2] = trade_total
                    
                except:
                    continue

