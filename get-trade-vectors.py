

#TODO - use coinmarketcap api to filter on market cap
#look into aggregated trades - may be a better alternative

import os
import pandas as pd

from crypto_predictor import datagrabber



api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

#currencies to get trade data against
BENCHMARK_CURRENCIES = ['ETH', 'BTC', 'BNB']


LIMIT = 100 #max number of trades per pair





if __name__ == "__main__":
    
    top_pair = datagrabber.get_biggest_trading_pair(api_key, api_secret)
    
    top_pair_trades = datagrabber.get_recent_trades(top_pair, LIMIT, api_key, api_secret)
    
    #cutoff_time = datagrabber.get_max_time(top_pair_trades, LIMIT-1)
    
    full_pair_list = datagrabber.get_available_symbols(api_key, api_secret)
    
    currency_list = datagrabber.get_viable_currencies(BENCHMARK_CURRENCIES, full_pair_list)
    
    
    results_df = pd.DataFrame(columns = currency_list, index=BENCHMARK_CURRENCIES)
    
    
    for i in range(len(BENCHMARK_CURRENCIES)):
        for j in(range(len(currency_list))):
            if i != j:
                
                curr1 = BENCHMARK_CURRENCIES[i]
                curr2 = currency_list[j]
                pair = curr2 + curr1
                print(pair)
                
                try:
                    trades = datagrabber.get_recent_trades(pair, LIMIT, api_key, api_secret)
                    #trades = datagrabber.filter_cutoff_time(trades, cutoff_time)
                    trade_total = sum(datagrabber.get_qty_from_trades(trades))
                    
                    results_df[curr2][curr1] = trade_total
                    
                except:
                    continue

