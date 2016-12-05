from parsers import TSP
from algs import simple_greed

import matplotlib.pyplot as plt
import seaborn as sns
from ggplot import ggplot, aes, geom_point, geom_hline, ggtitle, geom_line

import pandas as pd
import numpy as np

from decorator import decorator
import os
import time

def get_stats(name="", path="../img/", data=None, plots=[]):
    if name not in os.listdir(path):
        os.mkdir(path+name)
 
    path = path+name+'/'
    
    if not type(data) == TSP:
        raise NotImplementedError("Only type TSP allowed")

    def _get_stats(f, *args, **kwargs):
        #Data aggregation
        costs = []
        tss = []
        
        for input_args in args[0]:
            cost, ts = f(data, input_args)
            costs.append(cost)
            tss.append(ts)
    
        tss = pd.concat(tss)
        costs = pd.concat(costs)
        
        #Display
        for plot in plots:
            p = plot(costs, tss, path)
        
        return(costs, tss)
    return decorator(_get_stats)

def scatter_vis(costs, tss, path):
    plt.figure()
    p = ggplot(costs,
       aes(x="$N$",
           y="cost")) +\
    geom_point() +\
    geom_hline(y=costs.cost.mean(), color="grey") +\
    geom_hline(y=costs.cost.max(), color="red") +\
    geom_hline(y=costs.cost.min(), color="green") +\
    ggtitle("Simple greedy algorithm tour performance, $N$ is starting node")
    
    p.save(path+scatter_vis.__name__+".pdf")

def dist_across_cost(costs, tss, path):
    plt.figure()
    p = sns.violinplot(data=costs,
                       y="cost",
                       saturation=0)
    fig = p.get_figure()
    fig.savefig(path+dist_across_cost.__name__+".pdf")

    
def cost_progress_trace(costs, tss, path):
    plt.figure()
    p = sns.tsplot(tss, 
                   unit="$N$",
                   time="progress",
                   value="current_cost", 
                   err_style="unit_traces")
    fig = p.get_figure()
    fig.savefig(path+cost_progress_trace.__name__+".pdf")
  
