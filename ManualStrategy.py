from util import get_data
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals
import indicators as ind

class ManualStrategy:
    
    def calulate_SMA(self, sd, ed, symbol, normalize, window_size = 20):
        # calculate SMA and normalize
        SMA = ind.calculate_indicators(sd, ed, symbol, window_size = window_size)['SMA']
        if normalize: 
            SMA = SMA['SMA'] / SMA['SMA'][0]
        return SMA
    
    def calculate_BBP(self, sd, ed, symbol, window_size = 20):
        # calculate BBP and normalize
        BBP = ind.calculate_indicators(sd, ed, symbol, window_size = window_size)['BBP']
        return BBP
    
    def calculate_MACD(self, sd, ed, symbol, window_size = 20):
        # calculate BBP and normalize
        MACD = ind.calculate_indicators(sd, ed, symbol, window_size = window_size)['MACD']
        return MACD
        
    def testPolicy(self, symbol, sd, ed, sv):
        # get normalized prices for 'JPM'
        prices = get_data([symbol], pd.date_range(sd, ed))
        prices_symbol = prices[[symbol]]
        prices_symbol = prices_symbol.ffill().bfill()
        normalized_prices = prices_symbol[symbol] / prices_symbol[symbol][0]
        
        # get trading dates for 'SPY'
        df_trades = prices[['SPY']]
        df_trades = df_trades.rename(columns={'SPY': symbol})
        df_trades[symbol] = df_trades[symbol].astype('int32')
        df_trades[:] = 0
        dates = df_trades.index
        
        # calculate 3 indicators
        SMA = self.calulate_SMA(sd, ed, symbol, normalize = True, window_size = 20)
        BBP = self.calculate_BBP(sd, ed, symbol, window_size = 20)
        MACD = self.calculate_MACD(sd, ed, symbol, window_size = 20)
        
        current_position = 0
        num_action = 0
        
        def calculate_SMA_score(normalized_prices_current_date, SMA, current_date):
            # calculate SMA score
            SMA_current_date = SMA[current_date]
            if normalized_prices_current_date > SMA_current_date:
                SMA_score = 1
            elif normalized_prices_current_date < SMA_current_date:
                SMA_score = -1
            else:
                SMA_score = 0
            return SMA_score
        
        def calculate_MACD_score(MACD, current_date):
            # calculate MACD score
            MACD_current_date = MACD[current_date]
            if MACD_current_date > 0:
                MACD_score = -5
            elif MACD_current_date < 0:
                MACD_score = 2
            else:
                MACD_score = 1
            return MACD_score
                
        def calculate_BBP_score(BBP, current_date):
            # calculate BBP score
            BBP_current_date = BBP['BBP'][current_date]
            if BBP_current_date > 100:
                BBP_score = -1
            elif BBP_current_date < 0:
                BBP_score = 1
            else:
                BBP_score = 0
            return BBP_score
        
        for current_date in dates:
            num_action += 1
            
            normalized_prices_current_date = normalized_prices.loc[current_date]
            
            total_score = calculate_SMA_score(normalized_prices_current_date, SMA, current_date) + calculate_MACD_score(MACD, current_date) + calculate_BBP_score(BBP, current_date)
            if total_score >= 3:
                action = 1000 - current_position
            elif total_score <= -3:
                action = - 1000 - current_position
            else:
                action = -current_position
            
            # essentially taking 1 of 4 trading actions
            if num_action == 4:
                num_action = 0
                df_trades[symbol][current_date] = action
                current_position += action

            
        return df_trades

def create_benchmark_portval(sv, sd, ed, symbol):
    df = get_data([], pd.date_range(sd, ed))
    df = df.rename(columns={'SPY': symbol})
    df[symbol] = 0
    df.loc[df.index[0]] = 1000
    res = compute_portvals(df, symbol, start_val=sv, commission=9.95, impact=0.005)
    return res

def plot_graph(benchmark_portvals, manual_portvals, short, long, label):
    
    plt.figure(figsize=(16,8))
    plt.grid(axis='y')
    plt.title("Manual Strategy " + label)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.plot(benchmark_portvals, label="Benchmark", color = "purple")
    plt.plot(manual_portvals, label="Manual", color = "red")

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
    plt.savefig(f'images/manual_strategy_{label}.png')
    plt.close()
    
def create_table(benchmark_portvals, manual_portvals, label):
    # cumulative return
    cr_b = benchmark_portvals[-1] / benchmark_portvals[0] - 1
    cr_m = manual_portvals[-1] / manual_portvals[0] - 1

    # daily returns
    dr_b = (benchmark_portvals / benchmark_portvals.shift(1) - 1).iloc[1:]
    dr_m= (manual_portvals / manual_portvals.shift(1) - 1).iloc[1:]

    # standard deviation of daily returns
    sddr_b = dr_b.std()
    sddr_m = dr_m.std()

    # average daily returns
    adr_b = dr_b.mean()
    adr_m = dr_m.mean()
    
    data = [
    {'manual': {'cr': cr_m, 'adr': adr_m, 'sddr': sddr_m}},
    {'benchmark': {'cr': cr_b, 'adr': adr_b, 'sddr': sddr_b}}
    ]
    data_df = pd.DataFrame()

    # Iterate through the list and append data
    for item in data:
        key = list(item.keys())[0]  
        values = list(item.values())[0] 
        temp_df = pd.DataFrame(values, index=[key])
        data_df = data_df.append(temp_df)

    data_df.index.name = None
    data_df.to_csv(f'images/table_{label}.csv')
    return data_df


def plot_graph_with_label(label, sv, symbol):
    
    if label == 'in_sample':            
        sd = dt.datetime(2008, 1, 1)
        ed = dt.datetime(2009,12,31)
    elif label == 'out_of_sample':
        sd = dt.datetime(2010, 1, 1)
        ed = dt.datetime(2011, 12, 31)

    ms = ManualStrategy()   
    df_trades = ms.testPolicy(symbol, sd=sd, ed=ed, sv=sv)
    manual_portvals = compute_portvals(orders_df=df_trades, symbol=symbol, start_val=sv, commission=9.95, impact=0.005)
    benchmark_portvals = create_benchmark_portval(sv=sv, sd=sd, ed=ed, symbol=symbol)
    
    # normalize	benchmark and manual portfolio values
    benchmark_portvals = benchmark_portvals / benchmark_portvals[0]
    manual_portvals = manual_portvals / manual_portvals[0]
    
    
    long, short, actions = [], [], []
    current = 0
    action = 'OUT'
    for date in df_trades.index:
        current += df_trades.loc[date].loc[symbol]
        # print('-'*100)
        # print(f"current: {current}, last_action: {action}")
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
        # print(f"updated action: {action}")

    plot_graph(
        benchmark_portvals=benchmark_portvals, 
        manual_portvals=manual_portvals, 
        short=short, 
        long=long, 
        label=label
    )
    
    create_table(benchmark_portvals, manual_portvals, label)
    
def plot_all():
    plot_graph_with_label('in_sample', 10000, 'JPM')
    plot_graph_with_label('out_of_sample', 10000, 'JPM')
    
def author():
    return 'ylai67'

if __name__ == "__main__":
    print('Hello World')