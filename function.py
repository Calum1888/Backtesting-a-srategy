# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 19:38:14 2025

@author: c_reg
"""

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_data(stock, start, end):
    data = yf.download(stock, start, end)
    data.dropna(inplace=True)
    return data

def returns(data):
    sma_s=50 #periods for short rolling average
    sma_l=100 #periods for long moving average
    data['SMA_S'] = data['Close'].rolling(sma_s).mean() #short rolling average
    data['SMA_L'] = data['Close'].rolling(sma_l).mean() #short rolling average
    
    data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1,-1 ) #defines our position wrt the stock
    data['returns_b&h'] = np.log(data['Close'] / data['Close'].shift(1))
    data['strategy'] = data['returns_b&h'] * data['position'].shift(1) #strategy returns
    
    results = {}
    
    results['Cumulative Return (Buy and Hold)'] = np.exp(data['returns_b&h'].sum())
    results['Cumulative Return (Strategy)'] = np.exp(data['strategy'].sum())
    
    return data, results

def plot_returns(data, stock):
    buy_hold  = np.exp(data['returns_b&h'].cumsum())
    strat = np.exp(data['strategy'].cumsum())
    plt.figure(figsize=(12,8))
    plt.plot(data.index, buy_hold, label = 'Buy and Hold', color = 'blue')
    plt.plot(data.index, strat, label = 'Strategy', color = 'red')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.grid(True)
    plt.title(f'Buy and Hold versus Strategy: {stock}')
    plt.legend()
    plt.show()
                          
    

def backtest(stock, start, end):
    data = get_data(stock, start, end)
    returns(data)
    return plot_returns(data, stock)

    
    
    
    