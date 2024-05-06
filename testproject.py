import indicators as ind
import ManualStrategy
import datetime as dt
import StrategyLearner as sl 
import experiment1
import experiment2
import numpy as np
import random

def author():
    return 'ylai67'

if __name__ == "__main__": 
    # for i in range(3):
    #     # np.random.seed(42)
    #     # random.seed(42)
    #     indicators = ind.calculate_indicators(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), window_size=20)
    #     learner = sl.StrategyLearner(verbose = False, impact = 0.0, commission=0.0) 
    #     learner.add_evidence(symbol = "ML4T-220", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase 
    #     df_trades_strategy = learner.testPolicy(symbol = "ML4T-220", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # testing phase    
    #     # print(df_trades_strategy.tail(3))
    #     break
    ManualStrategy.plot_all()
    
    experiment1.experiment1(symbol='JPM')
    experiment2.experiment2(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000)
    
