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

def brute_force_N_no_reduce(p, n, perf=False):
    import itertools as it
    #Generate all possible tours (complete graph)
    tours = list(it.permutations(p.nodes())) #O(V!)
    costs = []
    
    if not perf:
        cost_data = pd.DataFrame(columns=["$N$", "cost", "opt_cost"])
    
    #Evaluate all tours
    for tour in tours[:n]:
        cost = 0
        for n1, n2 in zip(tour, tour[1:]): #O(V)
            cost += p[n1][n2]['weight']
        costs.append(cost)
        
    if not perf:
        cost_data = cost_data.append({"$N$" : n,
                                      "cost" : costs[-1],
                                      "opt_cost" : min(costs)},
                                     ignore_index = True)
        return (cost_data, pd.DataFrame())
        
    #Choose tour with lowest cost
    return tours[np.argmin(costs)]

def ant_colony(G, greed_start=0, n_ants=100, start_pheromone=None, step_pheromone=None, ant_pheromone=None, perf=False):
    
    if start_pheromone == None:
        start_pheromone = n_ants**2
    if step_pheromone == None:
        step_pheromone = start_pheromone/n_ants
    if ant_pheromone == None:
        ant_pheromone = n_ants
        
    for n1, n2 in G.edges_iter():
        G[n1][n2]['pheromone'] = start_pheromone
    
    for ant in range(n_ants):
        start_node = np.random.choice(G.nodes())
        current_node = start_node
        seen_nodes = [start_node]
        
        while len(seen_nodes) < len(G.nodes()):
            
            p_nodes = [G[current_node][n]['pheromone']/(G[current_node][n]['weight'])**2  for n in G.neighbors(current_node) if n not in seen_nodes] 
            next_node = np.random.choice([n for n in G.neighbors(current_node) if n not in seen_nodes], p=[p/sum(p_nodes) for p in p_nodes])
            seen_nodes.append(next_node)
            current_node = next_node
            
        for n1, n2 in zip(seen_nodes, seen_nodes[1:]):
            G[n1][n2]['pheromone'] += ant_pheromone/len(seen_nodes)
            
    #run a greedy agent now, cost function being inverse phermone level
    print("done with ants")
    if not perf:
        cost_data = pd.DataFrame(columns=["$N$", "cost"])
        ts_data = pd.DataFrame(columns=["$N$", "progress", "current_cost", "nodes_touched", "nodes_remaining"])
        
    start_node = greed_start
    seen_nodes = {start_node}
    current_node = start_node
    
    pher_cost = 0
    route_cost = 0
    while set(G.nodes()).difference(seen_nodes):
        neighbors = [n for n in G.neighbors(current_node) if n not in seen_nodes]
        pheromone_view = [1/G[current_node][next_node]['pheromone'] for next_node in neighbors]
        max_pher_idx = np.argmin(pheromone_view)
        next_node = neighbors[max_pher_idx]
        pher_cost += pheromone_view[max_pher_idx]
        route_cost += G[current_node][next_node]['weight']
        seen_nodes.update({next_node})
        current_node = next_node
         
        if not perf:
            ts_data = ts_data.append({"$N$":start_node,
                                      "progress": len(seen_nodes) / len(G.nodes()),
                                      "current_cost": route_cost,
                                      "nodes_touched" : seen_nodes,
                                      "nodes_remaining" : seen_nodes - set(G.nodes())},
                                    ignore_index=True)
                
        
            
    if not perf:    
        cost_data = cost_data.append({"$N$" : start_node,
                                      "cost" : route_cost},
                                     ignore_index = True)
        return (cost_data, ts_data)
    else:
        return cost
            

def minimum_perfect_matching(G):
    G_c = G.copy()
    from functools import reduce
    import itertools as it
    perfect_matchings = []
    for match_cand in it.combinations(G.edges(), len(G)//2):
        seen_nodes = set()
        inset = []
        for n_pair in match_cand:
            a, b = n_pair
            if a in seen_nodes or b in seen_nodes:
                inset.append(True)
            else:
                seen_nodes.update(set(n_pair))
                inset.append(False)
      
        if not reduce(lambda x, y: x or y, inset):
            perfect_matchings.append(match_cand)
            
    costs = []
    for match in perfect_matchings:
        cost = 0
        for a, b in match:
            cost +=  G[a][b]['weight']
        costs.append(cost)
            
    G_c.remove_edges_from([e for e in G.edges() if e not in list(perfect_matchings[np.argmin(costs)])])
    return G_c
