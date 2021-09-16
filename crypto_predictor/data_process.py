# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 20:24:03 2021

@author: Alex
"""

from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def remove_nas(df):
    
    """
    remove all the na columns from the trade vectors
    replaces remaining nas with 0 (technically correct since no trades 
                                   occurred between these pairs)
    
    """
    
    df.dropna(axis=1, how='all', inplace=True)
    df.fillna(0, inplace=True)
    
    return df


def convert_trades_to_usd(trades_df, price_df, benchmark_prices):
    """
    
    takes identically sized trades and prices df and prices of benchmarks
    outputs total traded value of each pair in usd
    
    hardly an elegant way of doing it but it works and is fast
    
    """
    
    assert trades_df.shape == price_df.shape, 'trade and price dataframes are of different size'
    
    df = trades_df * price_df
    
    benchmark_df = pd.DataFrame(columns = df.columns, index=benchmark_prices.index)
    
    for c in benchmark_df.columns:
        benchmark_df[c] = benchmark_prices['usd'].tolist()
    
    df = df*benchmark_df
    
    return df
    
    


def scale_vectors(df):
    
    """
    scale the dataframe
    for now scales between -1 and 1 row-wise
    """

    