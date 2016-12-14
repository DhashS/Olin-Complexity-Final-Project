import networkx as nx
import numpy as np
import pandas as pd

import random

def simple_greed(p, n, perf=False):
    """Takes p and produces a tour from a start node n by choosing
    the node with the lowest weight that it hasn't already visited.
    
    p :: [TSP-problem networkx graph]
    n :: [Integer] Start node
    
    returns: tour of p
    """
    n = int(n)
    seen = set()
    current_node = n
    seen.add(current_node)
    p_nodes = set(p.nodes())
    
    if not perf:
        cost_data = pd.DataFrame(columns=["$N$", "cost"])
        ts_data = pd.DataFrame(columns=["$N$", "progress", "current_cost", "nodes_touched", "nodes_remaining"])
    
    cost = 0

    while p_nodes.difference(seen):
        unseen_neighbors = [n for n in p.neighbors(current_node) if n not in seen]
        near_nodes = sorted(unseen_neighbors, key=lambda x: p.get_edge_data(current_node, x)['weight'])
        closest_node = near_nodes[0]
        cost += p.get_edge_data(current_node, closest_node)['weight']
        seen.add(closest_node)
        
        if not perf:
            ts_data = ts_data.append({"$N$" : n,
                                      "progress" : len(seen)/len(p_nodes),
                                      "current_cost": cost,
                                      "nodes_touched" : seen,
                                      "nodes_remaining" : p_nodes.difference(seen)},
                                     ignore_index = True)
               
        current_node = closest_node
        
    if not perf:    
        cost_data = cost_data.append({"$N$" : n,
                                      "cost" : cost},
                                     ignore_index = True)
        return (cost_data, ts_data)
    else:
        return cost
        
def random_choice(p, n, perf=False):
    """Takes p and produces a tour from a start node by choosing
    a random unvisited neighbor node
        
    p :: [TSP object]
    n :: [Integer] Start node
    
    returns: tour of p
    """
    n = int(n)
    seen = set()
    current_node = n
    seen.add(current_node)
    p_nodes = set(p.nodes())
    
    if not perf:
        cost_data = pd.DataFrame(columns=["$N$", "cost"])
        ts_data = pd.DataFrame(columns=["$N$", "progress", "current_cost", "nodes_touched", "nodes_remaining"])
    
    cost = 0
    
    
    while p_nodes.difference(seen):
        unseen_neighbors = [n for n in p.neighbors(current_node) if n not in seen]
        next_node = random.choice(unseen_neighbors)
        cost += p.get_edge_data(current_node, next_node)['weight']
        seen.add(next_node)
        
        if not perf:
            ts_data = ts_data.append({"$N$" : n,
                                      "progress" : len(seen)/len(p_nodes),
                                      "current_cost": cost, 
                                      "nodes_touched" : seen,
                                      "nodes_remaining" : p_nodes.difference(seen)},
                                     ignore_index = True)
        
        current_node = next_node
        
    if not perf:    
        cost_data = cost_data.append({"$N$" : n,
                                      "cost" : cost},
                                     ignore_index = True)
        return (cost_data, ts_data)
    else:
        return cost
    
def brute_force_N(p, n, perf=False):
    import itertools as it
    #Generate all possible tours (complete graph)
    tours = list(it.permutations(p.nodes())) #O(V!)
    costs = []
    
    if not perf:
        cost_data = pd.DataFrame(columns=["$N$", "cost"])
    
    #Evaluate all tours
    for tour in tours[:n]:
        cost = 0
        for n1, n2 in zip(tour, tour[1:]): #O(V)
            cost += p[n1][n2]['weight']
        costs.append(cost)
        
    if not perf:
        cost_data = cost_data.append({"$N$" : n,
                                      "cost" : min(costs)},
                                     ignore_index = True)
        return (cost_data, pd.DataFrame())
        
    #Choose tour with lowest cost
    return tours[np.argmin(costs)]

def brute_force(p, perf=False):
    import itertools as it
    #Generate all possible tours (complete graph)
    tours = list(it.permutations(p.nodes())) #O(V!)
    costs = []
    
    if not perf:
        cost_data = pd.DataFrame(columns=["$N$", "cost"])
    
    #Evaluate all tours
    for tour in tours:
        cost = 0
        for n1, n2 in zip(tour, tour[1:]): #O(V)
            cost += p[n1][n2]['weight']
        costs.append(cost)
        
    if not perf:
        cost_data = cost_data.append({"$N$" : len(p.nodes()),
                                      "cost" : min(costs),
                                      "opt_tour" : tours[np.argmin(costs)]},
                                     ignore_index = True)
        return (cost_data, pd.DataFrame())     
        
    #Choose tour with lowest cost
    return tours[np.argmin(costs)]
