import matplotlib.pyplot as plt 
import numpy as np

def adjust_percentiles(adjust_param, percentiles):
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