from parsers import TSP
from algs import *

import matplotlib.pyplot as plt
import seaborn as sns
from ggplot import ggplot, aes, geom_point, geom_hline, ggtitle, geom_line

import pandas as pd
import numpy as np
import tempfile

from decorator import decorator
import os
import time

import ipyparallel as ipp
import tempfile

def get_stats(name="", path="../img/", data=None, plots=[], module_dir=None):
    if name not in os.listdir(path):
        os.mkdir(path+name)
 
    path = path+name+'/'
    
    if not module_dir:
        module_dir = os.getcwd()
    
    if not type(data) == TSP:
        raise NotImplementedError("Only type TSP allowed")
       


    def _get_stats(f, *args, **kwargs):

        c = ipp.Client()
        dview = c[:]
        
        with dview.sync_imports():
            import os
            dview.apply_sync(os.chdir, module_dir)
        
        @dview.parallel(block=True)
        def parwork(N):
            cost, tss = f(data.graph, N)
            cost.to_csv(cost_tf_name, mode='a', header=False, sep='\t', index=False)
            tss.to_csv(tss_tf_name, mode='a', header=False, sep='\t', index=False)
            return (cost.columns, tss.columns)

        costs = []
        tss = []
        
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode='a+') as cost_tf:
            with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode='a+') as tss_tf:
                cost_tf_name = cost_tf.name
                tss_tf_name = tss_tf.name
                
                dview.block=True
                df_cols = parwork.map(args[0])
                
                cost_tf.flush()
                tss_tf.flush()
                
                cost_tf.seek(0)
                tss_tf.seek(0)
                
                costs = [tuple(l.split('\t')) for l in cost_tf.readlines()]
                costs = pd.DataFrame.from_records(costs, columns=df_cols[0][0])
                costs = costs.apply(pd.to_numeric, errors='ignore').reset_index()
                
                
                tss = [tuple(l.split('\t')) for l in tss_tf.readlines()]
                tss = pd.DataFrame.from_records(tss, columns=df_cols[0][1])
                tss = tss.apply(pd.to_numeric, errors='ignore').reset_index()
                

        #Display
        for plot in plots:
            p = plot(costs, tss, path, f)
        
        return(costs, tss)
    return decorator(_get_stats)

def scatter_vis(costs, tss, path, f):
    plt.figure()
    p = ggplot(costs,
       aes(x="$N$",
           y="cost")) +\
    geom_point() +\
    geom_hline(y=costs.cost.mean(), color="grey") +\
    geom_hline(y=costs.cost.max(), color="red") +\
    geom_hline(y=costs.cost.min(), color="green") +\
    ggtitle(f.__name__)

    p.save(path+scatter_vis.__name__+".pdf")

def dist_across_cost(costs, tss, path, f):
    plt.figure()
    p = sns.violinplot(data=costs,
                       y="cost",
                       saturation=0)
    sns.plt.title(f.__name__)
    fig = p.get_figure()
    fig.savefig(path+dist_across_cost.__name__+".pdf")

    
def cost_progress_trace(costs, tss, path, f):
    plt.figure()
    p = sns.tsplot(tss, 
                   unit="$N$",
                   time="progress",
                   value="current_cost", 
                   err_style="unit_traces")
    sns.plt.title(f.__name__)
    fig = p.get_figure()
    fig.savefig(path+cost_progress_trace.__name__+".pdf")
  
