from util import get_data 
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

def calculate_indicators(sd, ed, symbol, window_size):
    delta = dt.timedelta(200)
    
    # delta = dt.timedelta(60)
    history_sd = sd - delta
    prices = get_data([symbol], pd.date_range(history_sd, ed))
    prices_SPY = prices['SPY']
    prices_symbol = prices[symbol]
    prices_symbol = prices_symbol.ffill().bfill()
    
    d = {}
    sma = calculate_SMA(sd, prices_symbol, window_size)
    d['SMA'] = sma
    d['BBP'] = compute_bbp(sd, prices_symbol, sma, window_size)
    d['MACD'] = compute_MACD(sd, prices_symbol, short_period=12, long_period=26, signal_period=9)
    return d
    
####################################################################################################
# SMA (simple moving average)
def calculate_SMA(sd, prices_symbol, window_size):  
    sma = pd.DataFrame(index=prices_symbol.index)
    column_name = "Value"
    prices_symbol = prices_symbol.to_frame(column_name)
    sma['SMA'] = prices_symbol['Value'].rolling(window=window_size, min_periods=window_size).mean()
    sma = sma.loc[sd:]
    return sma

####################################################################################################
# MACD
def compute_MACD(sd, prices_symbol, short_period=12, long_period=26, signal_period=9):
    column_name = "Value"
    prices_symbol = prices_symbol.to_frame(column_name)
    ema_short = prices_symbol['Value'].ewm(span=short_period, adjust=False).mean()
    ema_long = prices_symbol['Value'].ewm(span=long_period, adjust=False).mean()
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    macd_histogram = macd_histogram.loc[sd:]
    return macd_histogram

####################################################################################################
# BBP (bollinger band percentage)
def compute_bb(sd, prices_symbol, sma, window_size):
    bb = pd.DataFrame(index=prices_symbol.index)
    band_width = pd.DataFrame(index=prices_symbol.index)
    column_name = "Value"
    prices_symbol = prices_symbol.to_frame(column_name)
    band_width['band_width'] = prices_symbol["Value"].rolling(window = window_size, min_periods = window_size).std()
    band_width.dropna(inplace=True)
    bb['upper'] = sma['SMA'] + (band_width['band_width'] * 2)
    bb['lower'] = sma['SMA'] - (band_width['band_width'] * 2)
    bb = bb.loc[sd:]
    return bb

def compute_bbp(sd, prices_symbol, sma, window_size = 20):
    bb = compute_bb(sd, prices_symbol, sma, window_size = window_size)
    column_name = "Value"
    prices_symbol = prices_symbol.to_frame(column_name)
    bbp = prices_symbol.copy()
    bbp['BBP'] = (bbp['Value'] - bb['lower']) / (bb['upper'] - bb['lower']) * 100
    bbp = bbp.drop(columns='Value')
    bbp = bbp.loc[sd:]
    return bbp

####################################################################################################

def author():
    return "ylai67"   		  	   		  		 		  		  		    	 		 		   		 		  			  	   		  		 		  		  		    	 		 		   		 		     		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    indicators = calculate_indicators(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), window_size = 20)
    print(indicators)