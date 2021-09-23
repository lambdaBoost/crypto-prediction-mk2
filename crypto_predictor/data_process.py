# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 20:24:03 2021

@author: Alex
"""

from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    
    


def scale_df(df):
    
    """
    exponentially scale the dataframe
    for now scales entire df between -1 and 1
    I think thats better than row wise as it maintains relative importance
    of benchmarks
    maintains -ive values as -ive and +ive as +ive
    """
    
    
    
    
    min_val = np.min(df.values)
    max_val = np.max(df.values)
    
    #get rid of zeros for logarithmic scaling
    df=df.replace(0,1)
    
    #record whether +ive or -ive
    sign_mask = df>0
    sign_mask = sign_mask.replace(True,1)
    sign_mask = sign_mask.replace(False,-1)
    
    df = abs(df)
    
    df = np.log(df)
    
    df = df * sign_mask.values
    
    #-1 to 1 scaling
    max_abs = max(abs(np.min(df.values)), np.max(df.values))
    df_scaled = df/max_abs
    
    return df_scaled

def vectors_to_array(df, size, benchmark_currencies, mc_data):
    """
    convert trade vectors to an n-space array where coords of each point 
    represents the trade vector of a given currency. Each point carries the 
    value of the relative market cap of that currency
    
    centre of array is zero in real world terms

    Parameters
    ----------
    df : pandas dataframe
        scaled dataframe of trade vectors
    size: int
        side length of array
    benchmark_currencies: str
        list of benchmark currencies
        mc_data: DataFrame
            list of top ccs by market cap. from the filter_viable_coins method

    Returns
    -------
    None.

    """
    
    ary = np.zeros((size,size,size))
    
    #rescale the dataframe and round so points fall at discrete points in the array
    #note we round all values so values are discrete
    
    size = size-1 #to deal with zero indexing for arrays
    
    df = df.multiply(size/2)
    df = df+(size/2)
    
    df = df.round()
    
    
    
    for c in df.columns:
        
        pos = []
        
        for i in range(len(benchmark_currencies)):
            coord = int(df[c][i])
            pos.append(coord)
        
        pos = tuple(pos)
        
        try:
            ary[pos] = ary[pos] + mc_data[mc_data['coin']==c]['mkt_cap'].values[0]
            
        except:
            print(c + 'not included in array due to name mismatch')
        
    return ary

def plot_3d_array(ary):
    """
    

    Parameters
    ----------
    ary : numpy array
        array of data

    Returns
    -------
    plot of spatial positions 

    """
    
    x,y,z = ary.nonzero()
    
    nonzeros_list = []
    for i in range(len(x)):
        nonzeros_list.append(ary[x[i], y[i], z[i]])
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, -z, zdir='z', c= nonzeros_list, marker='s', s=96)
    
    


    