""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		  		 		  		  		    	 		 		   		 		  
import random  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		  		 		  		  		    	 		 		   		 		  
import util as ut 
import indicators as ind
import QLearner as ql		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  		 		  		  		    	 		 		   		 		  
    """
    def author():
        return 'ylai67'
    
    def calulate_SMA(self, sd, ed, symbol, normalize, window_size = 20):
        # calculate SMA and normalize
        SMA = ind.calculate_indicators(sd, ed, symbol, window_size = window_size)['SMA']
        if normalize: 
            SMA = SMA['SMA'] / SMA['SMA'][0]
        return SMA
    
    def calculate_BBP(self, sd, ed, symbol, window_size):
        # calculate BBP and normalize
        BBP = ind.calculate_indicators(sd, ed, symbol, window_size)['BBP']
        return BBP
    
    def calculate_MACD(self, sd, ed, symbol, window_size):
        # calculate BBP and normalize
        MACD = ind.calculate_indicators(sd, ed, symbol, window_size)['MACD']
        return MACD
     		  	   		  		 		  		  		    	 		 		   		 		  
    # constructor  		  	   		  		 		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.005, commission=9.95):  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		  		 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		  		 		  		  		    	 		 		   		 		  
        self.commission = commission
        
        self.learner = ql.QLearner(num_states=384,\
            num_actions = 3, \
            alpha = 0.2, \
            gamma = 0.9, \
            rar = 0.9, \
            radr = 0.99, \
            dyna = 100, \
            verbose=False)   		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		   		  	   		  		 		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		  		 		  		  		    	 		 		   		 		  
        self,  		  	   		  		 		  		  		    	 		 		   		 		  
        symbol="JPM",  		  	   		  		 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		  		 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		  		 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		  		 		  		  		    	 		 		   		 		  
    ):  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		  		 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		  		 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		  		 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		  		 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		  		 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        SMA_10 = self.calulate_SMA(sd, ed, symbol, normalize = False, window_size = 10)   
        SMA_30 = self.calulate_SMA(sd, ed, symbol, normalize = False, window_size = 30)  
        SMA_100 = self.calulate_SMA(sd, ed, symbol, normalize = False, window_size = 100) 
        MACD = self.calculate_MACD(sd, ed, symbol, window_size = 20)
        BBP_20 = self.calculate_BBP(sd, ed, symbol, window_size = 20) 
        BBP_50 = self.calculate_BBP(sd, ed, symbol, window_size = 50) 
        BBP_100 = self.calculate_BBP(sd, ed, symbol, window_size = 100) 
           	 		 		   		 		          
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices_symbol = prices[[symbol]]
        prices_symbol = prices_symbol.ffill().bfill()
        prices_symbol_normalized = prices_symbol[symbol] / prices_symbol[symbol][0]
        
        df_trades = prices[['SPY']]
        df_trades = df_trades.rename(columns={'SPY': symbol})
        df_trades[symbol] = df_trades[symbol].astype('int32')
        df_trades[:] = 0
        dates = df_trades.index 
        
        SMA_10_copy = SMA_10.copy()
        SMA_100_copy = SMA_100.copy()
        SMA_30_copy = SMA_30.copy()
        SMA_10[prices_symbol[symbol] > SMA_10_copy['SMA']] = 1
        SMA_10[prices_symbol[symbol] <= SMA_10_copy['SMA']] = 0
        SMA_100[prices_symbol[symbol] > SMA_100_copy['SMA']] = 1
        SMA_100[prices_symbol[symbol] <= SMA_100_copy['SMA']] = 0
        SMA_30[prices_symbol[symbol] > SMA_30_copy['SMA']] = 1
        SMA_30[prices_symbol[symbol] <= SMA_30_copy['SMA']] = 0
        MACD = (MACD > 0) * 1
        BBP_20 = (BBP_20 > 1) * 1
        BBP_100 = (BBP_100 > 1) * 1
        BBP_50 = (BBP_50 > 1) * 1
        # print('discretized')
        # print(BBP_50.head())
        
        # current_position, previous_position = 0, 0
        # current_cash, previous_cash = sv, sv
        
        for train_iteration in range(20):
            # query learner to train
            current_position, previous_position = 0, 0
            current_cash, previous_cash = sv, sv
            for i in range(1, len(dates)):
                current_date = dates[i]

                s_prime = self.calculate_state(
                    current_position=current_position, 
                    SMA_30=SMA_30.loc[current_date], 
                    SMA_10=SMA_10.loc[current_date], 
                    SMA_100=SMA_100.loc[current_date], 
                    MACD=MACD.loc[current_date], 
                    BBP_20=BBP_20.loc[current_date], 
                    BBP_100=BBP_100.loc[current_date], 
                    BBP_50=BBP_50.loc[current_date], 
                )

                # r = (current_position * prices_symbol_normalized.loc[current_date] + current_cash) - \
                #     (previous_position * prices_symbol_normalized.loc[current_date] + previous_cash)

                r = (current_position * prices_symbol.loc[current_date].loc[symbol] + current_cash) - \
                    (previous_position * prices_symbol.loc[current_date].loc[symbol] + previous_cash)
                
                next_action = self.learner.query(s_prime, r)
                if next_action == 0: # short/sell
                    trade = -1000 - current_position
                elif next_action == 1: # out/hold
                    trade = - current_position
                elif next_action == 2: # long/buy
                    trade = 1000 - current_position
                    
                previous_position = current_position
                current_position += trade
                df_trades.loc[current_date].loc[symbol] = trade

                previous_cash = current_cash
                # current_cash += (-prices_symbol.loc[current_date].loc[symbol]) * (1 + impact) * trade - self.commission
                
                if trade > 0: # long/buy
                    # impact = self.impact
                    current_cash += (-prices_symbol.loc[current_date].loc[symbol]) * (1 + self.impact) * trade - self.commission
                elif trade < 0: # short/sell
                    # impact = -self.impact
                    current_cash += (-prices_symbol.loc[current_date].loc[symbol]) * (1 - self.impact) * trade - self.commission
                
        
            # get cumulative return of current agent and print to screen
            if train_iteration % 5 == 0:
                print('*'*100)
                print('Iteration: ', train_iteration)
                cumulative_return = current_cash - sv
                print('cumulative return', cumulative_return)
                                                                                
    def calculate_state(self, current_position, SMA_30, SMA_10, SMA_100, MACD, BBP_20, BBP_100, BBP_50):
        idx = 0
        if current_position == -1000:
            idx += 0
        elif current_position == 0:
            idx += 128
        elif current_position == 1000:
            idx += 256
        idx += BBP_50['BBP'] * 64 + SMA_30['SMA'] * 32 + SMA_10['SMA'] * 16 + SMA_100['SMA'] * 8 + MACD * 4 + BBP_20['BBP'] * 2 + BBP_100['BBP'] 
        return int(idx)	  	   		  		 		  		  		    	 		 		   		 		  
         		  	   		  		 		  		  		    	 		 		   		 		    		  	   		  		 		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		  		 		  		  		    	 		 		   		 		  
        self,  		  	   		  		 		  		  		    	 		 		   		 		  
        symbol="JPM",  		  	   		  		 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		  		 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		  		 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		  		 		  		  		    	 		 		   		 		  
    ):  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		  		 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		  		 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		  		 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		  		 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		  		 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		  		 		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		  		 		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		  		 		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		  		 		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		  		 		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		   		   	  			  	 		  		  		    	 		 		   		 		  

        SMA_10 = self.calulate_SMA(sd, ed, symbol, normalize = False, window_size = 10)  
        SMA_100 = self.calulate_SMA(sd, ed, symbol, normalize = False, window_size = 100) 
        SMA_30 = self.calulate_SMA(sd, ed, symbol, normalize = False, window_size = 30)   
        MACD = self.calculate_MACD(sd, ed, symbol, window_size = 20)
        BBP_20 = self.calculate_BBP(sd, ed, symbol, window_size = 20) 
        BBP_100 = self.calculate_BBP(sd, ed, symbol, window_size = 100)
        BBP_50 = self.calculate_BBP(sd, ed, symbol, window_size = 50)
        
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices_symbol = prices[[symbol]]
        prices_symbol = prices_symbol.ffill().bfill()
        
        df_trades = prices[['SPY']]
        df_trades = df_trades.rename(columns={'SPY': symbol})
        df_trades[symbol] = df_trades[symbol].astype('int32')
        df_trades[:] = 0
        dates = df_trades.index  
        
        SMA_10_copy = SMA_10.copy()
        SMA_100_copy = SMA_100.copy()
        SMA_30_copy = SMA_30.copy()
        
        SMA_10[prices_symbol[symbol] > SMA_10_copy['SMA']] = 1
        SMA_10[prices_symbol[symbol] <= SMA_10_copy['SMA']] = 0
        SMA_100[prices_symbol[symbol] > SMA_100_copy['SMA']] = 1
        SMA_100[prices_symbol[symbol] <= SMA_100_copy['SMA']] = 0
        SMA_30[prices_symbol[symbol] > SMA_30_copy['SMA']] = 1
        SMA_30[prices_symbol[symbol] <= SMA_30_copy['SMA']] = 0
        MACD = (MACD > 0) * 1
        BBP_20 = (BBP_20 > 1) * 1
        BBP_100 = (BBP_100 > 1) * 1
        BBP_50 = (BBP_50 > 1) * 1

        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices_symbol = prices[[symbol]]
        prices_symbol = prices_symbol.ffill().bfill()
        
        df_trades = prices[['SPY']]
        df_trades = df_trades.rename(columns={'SPY': symbol})
        df_trades[symbol] = df_trades[symbol].astype('int32')
        df_trades[:] = 0
        dates = df_trades.index 
	  	 		  		  		    	 		 		   		 		  			  	 		  		  		    	 		 		   		 		  
        current_position = 0

        for i in range(1, len(dates)):
            current_date = dates[i]
            s_prime = self.calculate_state(
                current_position=current_position, 
                SMA_30=SMA_30.loc[current_date], 
                SMA_10=SMA_10.loc[current_date], 
                SMA_100=SMA_100.loc[current_date], 
                MACD=MACD.loc[current_date], 
                BBP_20=BBP_20.loc[current_date], 
                BBP_100=BBP_100.loc[current_date], 
                BBP_50=BBP_50.loc[current_date]
            )

            next_action = self.learner.querysetstate(s_prime)
            if next_action == 0:
                trade = -1000 - current_position
            elif next_action == 1:
                trade = -current_position
            else:
                trade = 1000 - current_position

            current_position += trade
            df_trades.loc[current_date].loc[symbol] = trade
        return df_trades
 		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		  		 		  		  		    	 		 		   		 		  
