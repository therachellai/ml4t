def author():
    return "ylai67"

from StrategyLearner import StrategyLearner
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals


def experiment2(symbol, sd, ed, sv):

    df_trades1, trades1_portval = calculate_trades_and_portval(symbol, sd, ed, sv, impact=0.000, commission=0.00)
    df_trades2, trades2_portval = calculate_trades_and_portval(symbol, sd, ed, sv, impact=0.005, commission=0.00)
    df_trades3, trades3_portval = calculate_trades_and_portval(symbol, sd, ed, sv, impact=0.010, commission=0.00)
    
    plot_graphs(((trades1_portval, 0.000, 'red'), (trades2_portval, 0.005, 'green'), (trades3_portval, 0.010, 'blue')))

    res_list = []
    res1 = plot_trades_case(df_trades1, trades1_portval, 0.000, symbol)
    res2 = plot_trades_case(df_trades2, trades2_portval, 0.005, symbol)
    res3 = plot_trades_case(df_trades3, trades3_portval, 0.010, symbol)
    res_list.append(res1)
    res_list.append(res2)
    res_list.append(res3)
    # print(res_list)
    x_values = [str(item[0]) for item in res_list]
    y_values = [item[1] for item in res_list]
    plot_bar_graph(x_values, y_values)
    
def plot_bar_graph(x_values, y_values):
    plt.bar(x_values, y_values)
    plt.xlabel('Impact Value')
    plt.ylabel('Number Of Trades')
    plt.title('Number Of Trades For Each Impact Value')
    plt.savefig('images/experiment2_bar_graph.png')
    plt.close()
   
def plot_trades_case(df_trades, trades_portval, impact, symbol):
    long, short = get_trades(df_trades, symbol)
    trades_portval = trades_portval / trades_portval[0]
    return plot_trades(trades_portval, long, short, impact)
    
def calculate_trades_and_portval(symbol, sd, ed, sv, impact, commission=0.00):
    learner = StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner.add_evidence(symbol = symbol, sd=sd, ed=ed, sv = sv)
    df_trades = learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv)
    trades_portval = compute_portvals(df_trades, symbol, start_val = sv, commission=0, impact=impact)
    return df_trades, trades_portval
    
def plot_graphs(trades_portvals):
    plt.figure(figsize=(16,8))
    plt.grid(axis='y')
    plt.title("Effective of Impact Value on Cummulative Return (From In-Sample Data)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    for i in range(len(trades_portvals)):
        trades_portval_info = trades_portvals[i]
        trades_portval, impact, color = trades_portval_info[0], trades_portval_info[1], trades_portval_info[2]
        trades_portval = trades_portval / trades_portval[0]
        plt.plot(trades_portval, label=f"impact = {impact}", color = color)
    plt.legend()
    plt.savefig("images/experiment2.png", bbox_inches='tight')
    plt.close()

def get_trades(df_trades, symbol):
    long, short, actions = [], [], []
    current = 0
    action = 'OUT'
    for date in df_trades.index:
        current += df_trades.loc[date].loc[symbol]
        if current < 0:
            if action != 'SHORT':
                action = 'SHORT'
                actions.append(action)
                short.append(date)
        elif current > 0:
            if action != 'LONG':
                action = 'LONG'
                actions.append(action)
                long.append(date)
        else:
            action = 'OUT'
    print(actions)
    return long, short

def plot_trades(df_trades, long, short, impact):

    plt.figure(figsize=(16,8))
    plt.grid(axis='y')
    plt.title("Number of trades: " + str(len(long) + len(short)) + ", Impact Value: " + str(impact))
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.plot(df_trades, color = "red", label = "Strategy Learner")

    label_set = False
    for date in short:
        if not label_set:
            plt.axvline(date, linestyle="--", color="black", label="Short entry points")
            label_set = True
        else:
            plt.axvline(date, linestyle="--", color="black")
    label_set = False
    for date in long:
        if not label_set:
            plt.axvline(date, linestyle="--", color="blue", label="Long entry points")
            label_set = True
        else:
            plt.axvline(date, linestyle="--", color="blue")

    plt.legend()
    plt.savefig(f"images/experiment2_{impact}.png", bbox_inches='tight')
    plt.close()
    return (impact, len(long) + len(short))

if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("Hello World")
