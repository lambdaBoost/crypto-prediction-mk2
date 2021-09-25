

#TODO - use coinmarketcap api to filter on market cap
#look into aggregated trades - may be a better alternative

import os
import pandas as pd
import time
import pickle

from sklearn.preprocessing import MinMaxScaler
from crypto_predictor import datagrabber, data_process, cmc_data



api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
cmc_key = os.environ.get('COINMARKETCAP_API')

#currencies to get trade data against
BENCHMARK_CURRENCIES = ['ETH', 'BTC', 'BNB']


LIMIT = 100 #max number of trades per pair





if __name__ == "__main__":
    
    
    #get market cap data and viable currencies (just do once per day)
    
    top_pair = datagrabber.get_biggest_trading_pair(api_key, api_secret)
    
    top_pair_trades = datagrabber.get_recent_trades(top_pair, LIMIT, api_key, api_secret)
    
    #cutoff_time = datagrabber.get_max_time(top_pair_trades, LIMIT-1)
    
    full_pair_list = datagrabber.get_available_symbols(api_key, api_secret)
    
    currency_list = datagrabber.get_viable_currencies(BENCHMARK_CURRENCIES, full_pair_list)
    
    mc_data = cmc_data.get_mkp_caps(cmc_key)

    mc_data = cmc_data.filter_viable_coins(currency_list, mc_data, BENCHMARK_CURRENCIES, 100)
    
    qty_df = pd.DataFrame(columns = currency_list, index=BENCHMARK_CURRENCIES)
    price_df = pd.DataFrame(columns = currency_list, index=BENCHMARK_CURRENCIES)
    
    scaler = MinMaxScaler()
    mc_data[['mkt_cap']] = scaler.fit_transform(mc_data[['mkt_cap']])
    mc_data.reset_index(inplace=True)
    
   
    
    while True:
        
        #daily update mkt cap data (600 seconds after hour to avoid conflict with second conditional)
        if round(time.time()) % 43200 == 300:
            top_pair = datagrabber.get_biggest_trading_pair(api_key, api_secret)
    
            top_pair_trades = datagrabber.get_recent_trades(top_pair, LIMIT, api_key, api_secret)
    
            #cutoff_time = datagrabber.get_max_time(top_pair_trades, LIMIT-1)
    
            full_pair_list = datagrabber.get_available_symbols(api_key, api_secret)
    
            currency_list = datagrabber.get_viable_currencies(BENCHMARK_CURRENCIES, full_pair_list)
    
            mc_data = cmc_data.get_mkp_caps(cmc_key)
    
            mc_data = cmc_data.filter_viable_coins(currency_list, mc_data, BENCHMARK_CURRENCIES, 100)
    
            scaler = MinMaxScaler()
            mc_data[['mkt_cap']] = scaler.fit_transform(mc_data[['mkt_cap']])
        
    
            qty_df = pd.DataFrame(columns = currency_list, index=BENCHMARK_CURRENCIES)
            price_df = pd.DataFrame(columns = currency_list, index=BENCHMARK_CURRENCIES)
    
            mc_data.reset_index(inplace=True)
            
        
        if round(time.time()) % 600 == 0:
            
    
    
            #get trade data and build array
            for i in range(len(BENCHMARK_CURRENCIES)):
                for j in(range(len(mc_data))):
                    
                        
                    curr1 = BENCHMARK_CURRENCIES[i]
                    curr2 = mc_data['coin'][j]
                    mc = mc_data['mkt_cap'][j]
                        
                    pair = curr2 + curr1
                    print(pair)
                        
                    try:
                        trades = datagrabber.get_recent_trades(pair, LIMIT, api_key, api_secret)
                        #trades = datagrabber.filter_cutoff_time(trades, cutoff_time)
                        trade_total = sum(datagrabber.get_qty_from_trades(trades))
                        trade_price = datagrabber.get_price_from_trades(trades)
                            
                        qty_df[curr2][curr1] = trade_total
                        price_df[curr2][curr1] = trade_price
                            
                    except:
                        continue
                        
            
            #convert the qty and price data to a single df of total trade value in usd
            qty_df = data_process.remove_nas(qty_df)
            price_df = data_process.remove_nas(price_df)
            
            benchmark_prices = datagrabber.get_benchmark_currency_prices(BENCHMARK_CURRENCIES, api_key, api_secret)
            
            
            #total usd traded between all pairs
            trades_df = data_process.convert_trades_to_usd(qty_df, price_df, benchmark_prices)
        
            scaled_df = data_process.scale_df(trades_df)
            
            #input array for CNN
            data_array = data_process.vectors_to_array(scaled_df, 16, BENCHMARK_CURRENCIES, mc_data)
            pickle.dump( data_array, open( "./data/trades/" + str(round(time.time())) +".p", "wb" ) )
            #data_process.plot_3d_array(data_array)
            
            prices = datagrabber.get_all_prices(api_key, api_secret)
            pickle.dump( prices, open( "./data/prices/" + str(round(time.time())) +".p", "wb" ) )
    