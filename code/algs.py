import networkx as nx
import numpy as np

import random

def simple_greed(p, n):
    """Takes p and produces a tour from a start node n by choosing
    the node with the lowest weight that it hasn't already visited.
    
    p :: [TSP object]
    n :: [Integer] Start node
    
    returns: tour of p
    """
    seen = set()
    current_node = n
    seen.add(current_node)
    p_nodes = set(p.graph.nodes())
    
    cost = 0
    ts = pd.DataFrame(columns=["$N$", "current_cost", "nodes_touched", "nodes_remaining"])

    while p_nodes.difference(seen):
        unseen_neighbors = [n for n in p.graph.neighbors(current_node) if n not in seen]
        near_nodes = sorted(unseen_neighbors, key=lambda x: p.graph.get_edge_data(current_node, x)['weight'])
        closest_node = near_nodes[0]
        cost += p.graph.get_edge_data(current_node, closest_node)['weight']
        seen.add(closest_node)
        
        ts = ts.append({"$N$" : n,
                   "progress" : len(seen)/len(p_nodes),
                   "current_cost": cost, 
                   "nodes_touched" : seen,
                   "nodes_remaining" : p_nodes.difference(seen)},
                  ignore_index = True)
               
        current_node = closest_node
    return (cost, ts)
        
def random_choice(p, n):
    """Takes p and produces a tour from a start node by choosing
    a random unvisited neighbor node
        
    p :: [TSP object]
    n :: [Integer] Start node
    
    returns: tour of p
    """
    seen = set()
    current_node = n
    seen.add(current_node)
    p_nodes = set(p.graph.nodes())
    
    cost = 0
    
    while p_nodes.difference(seen):
        unseen_neighbors = [n for n in p.graph.neighbors(current_node) if n not in seen]
        next_node = random.choice(unseen_neighbors)
        cost += p.graph.get_edge_data(current_node, next_node)['weight']
        seen.add(next_node)
        current_node = next_node
    return cost
