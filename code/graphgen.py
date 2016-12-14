import numpy as np
import networkx as nx
import itertools as it

def EUC_2D(n, D=2):
    num_cities = n
    
    rand_cities = np.random.randn(num_cities*D).reshape(num_cities, D)

    def distance(v1, v2):
        return np.linalg.norm(v1-v2)

    graph_edges = list(it.combinations(range(rand_cities.shape[0]), D))
    edge_weights = [distance(c1, c2) for c1, c2 in it.combinations(rand_cities, D)]

    G = nx.Graph()
    u_v_w = [(u, v, w) for (u, v), w in zip(graph_edges, edge_weights)]
    G.add_weighted_edges_from(u_v_w)
    
    return G