import StrategyLearner as sl 
import ManualStrategy
from marketsimcode import compute_portvals
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt

def experiment1(symbol):
    trained_learner = experiment1_case(symbol=symbol, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000, commission=9.95, impact=0.005, label='in_sample')
    experiment1_case(symbol=symbol, sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv=100000, commission=9.95, impact=0.005, label='out_of_sample', learner=trained_learner)

def experiment1_case(symbol, sd, ed, sv, commission, impact, label, learner=None):
    manual = ManualStrategy.ManualStrategy()
    manual_trades = manual.testPolicy(symbol, sd=sd, ed=ed, sv=sv)
    manual_portvals = compute_portvals(manual_trades, symbol, start_val = sv, commission=commission, impact=impact)
    benchmark_portvals = ManualStrategy.create_benchmark_portval(sv=sv, sd=sd, ed=ed, symbol=symbol)
   
    if label == "in_sample":
        learner = sl.StrategyLearner(verbose=False, impact=impact , commission=commission) 
        learner.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    elif label == "out_of_sample":
        assert learner is not None
    else:
        raise ValueError("UNKNOWN EXPERIMENT LABEL")
    
    learner_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    strategy_portvals = compute_portvals(learner_trades, symbol, start_val=sv, commission=commission, impact=impact)
    
    benchmark_portvals = benchmark_portvals / benchmark_portvals[0]
    manual_portvals = manual_portvals / manual_portvals[0]
    strategy_portvals = strategy_portvals / strategy_portvals[0]
    
    plot_graphs(benchmark_portvals, manual_portvals, strategy_portvals, label)
    return learner

def plot_graphs(benchmark_portvals, manual_portvals, strategy_portvals, label):
    
    plt.figure(figsize=(16,8))
    plt.grid(axis='y')
    plt.title("Comparison Between Benchmark, Manual Strategy, and Strategy Learner (QLearner)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.plot(benchmark_portvals, label="Benchmark", color = "blue")
    plt.plot(manual_portvals, label="Manual", color = "green")
    plt.plot(strategy_portvals, label="Strategy (QLearner)", color = "red")

    plt.legend()
    plt.savefig(f"images/experiment1_{label}.png", bbox_inches='tight')
    plt.close()

def author():
    return 'ylai67'

if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    experiment1(symbol='JPM')
