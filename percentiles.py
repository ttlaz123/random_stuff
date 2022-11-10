import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from scipy.stats import norm

def adjust_percentiles(percentiles, adjust_param = 0.25):
    adjusted_list = []
    for i in range(len(percentiles)):
        if(i == 0):
            old = percentiles[i]*(1-adjust_param) 
            new = percentiles[i+1]*adjust_param 
        elif(i == len(percentiles) - 1):
            old = percentiles[i]*(1-adjust_param)
            new = percentiles[i-1]*adjust_param
        else:
            old = percentiles[i]*(1-2*adjust_param)
            new = percentiles[i-1]*adjust_param + percentiles[i+1]*adjust_param 
        adjusted_list.append(old+new)

    return adjusted_list 

def graph_adjustments(ranks, percentages):
    fig, axs = plt.subplots(1, len(percentages))
    for i in range(len(percentages)):
        axs[i].bar(ranks, percentages[i])
        axs[i].set_xticklabels(ranks, rotation=90)
        mean,std=norm.fit(percentages[i])
        x = np.linspace(0, len(ranks), 100)
        y = norm.pdf(x, mean, std)
        axs[i].plot(x, y)  
        
    plt.show()

def load_percentiles(file_name):
    # reads in spreadsheet, returns dataframe
    # dataframe has following headers:
    # Rank, Percentages, Percentile
    header_row = 5
    df = pd.read_csv(file_name, skiprows=header_row)
    df.dropna(how='all', axis=1, inplace=True)
    return df


def iter_adjustments(ranks, percentages):
    num_iter = 5
    adjusted = []
    temp = percentages
    adjusted.append(temp)
    num_iter = 5
    for i in range(num_iter):
        
        temp = adjust_percentiles(temp)
        adjusted.append(temp)
    
    graph_adjustments(ranks, adjusted)


def main():
    filename = '/Users/Varian 348/Downloads/tftpercentiles.csv'
    df = load_percentiles(filename)
    iter_adjustments(df['Rank'],df['Percentage'])

if __name__ == '__main__':
    main()
