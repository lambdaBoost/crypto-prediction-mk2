# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 19:43:29 2021

@author: Alex
"""

import os
import pickle
import numpy as np

def get_xy_times(src, x_size=6, y_size=1, interval=1,  time_tolerance=60, recording_interval = 600):
    
    """
    builds a raw dataset of x trade arrays and one subsequeny y price array,
    one timestep after last x
    
    returns times of each datapoint
    
    """
    
    trade_files = os.listdir(os.path.join(src,'trades'))
    price_files = os.listdir(os.path.join(src,'prices'))
    
    trade_times = [int(w.replace('.p','')) for w in trade_files]
    price_times = [int(w.replace('.p','')) for w in price_files]
    
    
    trades_list = []
    prices_list = []
    
    for i in range(len(trade_times)-x_size-1):
        
        first_trade = trade_times[i]
        previous_trade = first_trade 
        
        block_trade_list = [first_trade]
        
        for s in range(x_size-1):
            
            next_trade = trade_times[i+s+1]
            
            if(abs(next_trade - previous_trade - recording_interval) < (time_tolerance)):
                
                block_trade_list.append(next_trade)
                
            
            previous_trade = next_trade
            
            
        #next time price is recorded after last trade
        price_time = min(price_times, key=lambda x:abs(x-(next_trade+recording_interval)))
        
        #if full trade block and price record present, add to x and y
        if(len(block_trade_list) == x_size and abs(price_time-next_trade-recording_interval < time_tolerance)):
            
            trades_list.append(block_trade_list)
            prices_list.append(price_time)
            
            
        return trades_list, prices_list
        
            
            
            
            
            