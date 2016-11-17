import argparse
import networkx as nx
from numpy.linalg import norm

class TSP():
    def __init__(self, file=None):
        assert(file.endswith(".tsp"))
        self.supported_edge_weights = ["EUC_2D"]
        
        self.spec = {}
        self.graph = nx.Graph()
        
        with open(file) as f:
            lines = f.readlines()
            
        lines = list(map(lambda x: x[:-1], lines)) #strip the newlines
            
        self.pack(lines)
        
        
    def pack(self, lineset):
        """Impliments the grammar in http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/DOC.PS
           or at least the relavant bits...
           
           -----Parameters-----
           lineset: All lines of a .tsp file
           
           -----Output-----
           Modifies the class variables to encapsulate the data in the TSP file"""
        
        
        spec_keys = ["NAME", "TYPE", "COMMENT", "DIMENSION", "EDGE_WEIGHT_TYPE"]
        data_keys = ["NODE_COORD_SECTION", "TOUR_SECTION"]
        
        for line in lineset:
            #Specification parsing
            for k in spec_keys:
                if k in line:
                    arg = line.split(':')[-1][1:] #get last after : char and strip the first char, a space
                    self.spec[k.lower()] = arg
                    
        self.spec = argparse.Namespace(**self.spec)
                    
        if self.spec.edge_weight_type not in self.supported_edge_weights:
            raise NotImplementedError("{} not in {}".format(self.spec.edge_weight_type,
                                                            self.supported_edge_weights))
        

        def build_slices(lst, slicers):
            last_i = None
            sections = {}
            for i, l in enumerate(lst):
                if l in slicers:
                    if last_i == None:
                        last_i = i+1
                    else:
                        sections[lst[i]] = (last_i, i)
                        
            if last_i:
                if lst[-1] == "EOF":
                    sections[lst[last_i-1]] = (last_i, -1)
                else:
                    sections[lst[last_i-1]] = (last_i, None)
            return sections

        slices = build_slices(lineset, data_keys)


        for k, (start, stop) in slices.items():
            if k == "NODE_COORD_SECTION":
                nodes = lineset[start:stop]
                if self.spec.edge_weight_type == "EUC_2D":
                    for n in nodes:
                        num, x, y = n.split()
                        x, y = float(x), float(y)
                        self.graph.add_node(num, attr_dict={"x":x, "y":y})
                        for other_node in self.graph.nodes():
                            attrs = self.graph.node[other_node]
                            other_x, other_y = attrs["x"], attrs["y"]
                            l2_dist = norm([x-other_x, y-other_y])    
                            self.graph.add_edge(num, other_node, weight=l2_dist)
            if k == "TOUR_SECTION":
                nodes = lineset[start:stop]
                self.optimal_tour = nodes




