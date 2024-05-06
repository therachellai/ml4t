import pandas as pd 
from util import get_data 

def convert_to_orders_file(df_trades, symbol):
    
    """An improved version of the marketsim code accepts a “trades” DataFrame (instead of a file). 
    More info on the trades data frame is below. It is OK not to submit this file if you have subsumed 
    its functionality into one of your other required code files. This file has a different name and a 
    slightly different setup than your previous project. However, that solution can be used with several 
    edits for the new requirements. """

    dates = df_trades.index
    order_col = pd.DataFrame(0, index = dates, columns = ['Shares'])
    action_col = pd.DataFrame('', index = dates, columns = ['Order'])
    symbol_col = pd.DataFrame(symbol, index = dates, columns = ['Symbol'])
    
    for i in range(len(dates)):
        # amount = df_trades.loc[dates[i]].loc[symbol]
        amount = df_trades['JPM'].loc[dates[i]] 
        if amount <= 0:
            action_col.loc[dates[i]].loc['Order'] = "SELL"
        else: 
            action_col.loc[dates[i]].loc['Order'] = "BUY"
        order_col.loc[dates[i]].loc['Shares'] = abs(amount)
    df_trades = pd.concat([symbol_col, action_col, order_col], axis=1)
    return df_trades

def compute_portvals(  		  	   		  		 		  		  		    	 		 		   		 		  
    orders_df,
    symbol,  		  	   		  		 		  		  		    	 		 		   		 		  
    start_val=1000000,  		  	   		  		 		  		  		    	 		 		   		 		  
    commission=9.95,  		  	   		  		 		  		  		    	 		 		   		 		  
    impact=0.005  		  	   		  		 		  		  		    	 		 		   		 		  
):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param orders_file: trades dataFrame  		  	   		  		 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		  		 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		  		 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    
    # read in orders dataFrame
    orders = orders_df
    orders = convert_to_orders_file(orders, symbol)
    
    # determine start and end date and unique symbols in the order book		  	   		  		 		  		  		    	 		 		   		 		  
    start_date = orders.index[0]		  	   		  		 		  		  		    	 		 		   		 		  
    end_date = orders.index[-1]
    symbols = list(orders['Symbol'].unique())
    
    # read in prices dataFrame and create Cash colume of value 1.00
    # fill foward and backward so that there isn't missing value
    prices = get_data(symbols, pd.date_range(start_date, end_date))
    prices.rename_axis('Date')
    prices['Cash'] = 1.00
    prices.ffill().bfill()
    
    # create trades dataFrame as a copy of prices dataFrame; then fill in with 0
    trades = prices.copy()
    trades[:] = 0
    
    # iterate through rows in the orders dataFrame to tranfer all the information from there to the trades dataFrame
    for date, row in orders.iterrows():
        symbol = row['Symbol']
        num_shares = row['Shares']
        order = row['Order']
        cash_col = 'Cash'
        price = prices.loc[date][symbol]
        
        # update the columns of the trades dataFrame where the number of shares traded in each day is put in respective cells
        # negative num_shares suggest selling and positive suggest buying
        # update cash value, taking into consideration buy/sell, commisions, and market impact
        if order == 'BUY':
            trades.loc[date,symbol] += num_shares # num_shares
            trades.loc[date,cash_col] -= num_shares * price * (1 + impact) # market impact
        elif order == 'SELL':
            trades.loc[date,symbol] -= num_shares # num_shares
            trades.loc[date,cash_col] += num_shares * price * (1 - impact) # market impact
        else:
            print('There is an issue with the order action.')    
            
        trades.loc[date,cash_col] -= commission # commissions
    
    # create trades dataFrame as a copy of trades dataFrame
    # initialize with start_val, then calculate cumulative sum of trades to get current holdings for each day
    holdings = trades.copy()
    holdings['Cash'][0] += start_val
    holdings = holdings.cumsum()
    
    # create values dataFrame and initialize to 0
    # then, fill in with product of prices and holdings 
    # (we can do this because) pandas allow cell-by-cell operation
    values = trades.copy()
    values[:] = 0
    values = prices * holdings # this is why it is important to set cash value to 1
    
    # create portvals dataFrame by summing each row of values to get the total portfolio value
    portvals = values.sum(axis=1)	   		  		 		  		  		    	 		 		   		 		  
      		  	   		  		 		  		  		    	 		 		   		 		  
    return portvals 

def author():
    return "ylai67"

if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    pass