import networkx as nx
from scipy.spatial import distance

class LazySP:
    def __init__(self, G, u, v):
        self.G = G
        self.u = u
        self.v = v
    
    def estimate_distance(self, u, v):
        if 'pos' in self.G.nodes[u].keys():
            return distance.euclidean(self.G.nodes[u]['pos'], self.G.nodes[v]['pos'])
        return 0 # only for randomly connected graphs, with no actual positions

    def solve(self, sp_solver, selector, beta):
        eval_n = 0
        E_eval = set([])
        alternate_n = 0
        # for e in self.G.edges:
        #     w_lazy(e) = w_est(e)
        while True:
            try:
                if sp_solver == 'astar':
                    p_candidate = nx.astar_path(self.G, source=self.u, target=self.v, heuristic=self.estimate_distance, weight='est')
                else:
                    p_candidate = nx.shortest_path(self.G, source=self.u, target=self.v, weight='est', method=sp_solver) # use 'est' as current knowledge of map edge weights
            except nx.exception.NetworkXNoPath:
                print('no path')
                return [], 0
            p_evaled = True
            for i in range(len(p_candidate) - 1):
                if tuple(p_candidate[i:i+2]) not in E_eval:
                    p_evaled = False
                    break
            if p_evaled:
                return p_candidate, eval_n
            if selector.__name__ == 'alternate':
                E_selected, alternate_n = selector(G=self.G, p_candidate=p_candidate, alternate_n=alternate_n)
            elif selector.__name__ == 'partition':
                E_selected = selector(G=self.G, p_candidate=p_candidate, beta=beta)
            else:
                E_selected = selector(G=self.G, p_candidate=p_candidate)
            for e in set(E_selected).difference(E_eval):
                self.G.edges[e]['est'] = self.G.edges[e]['real'] # after evaluation, update 'est' to 'real' weights
                self.G.edges[e]['eval'] = True
                eval_n += 1
                E_eval.add(e)
                u, v = e # also add opposite direction, ensure (x, y) and (y, x) are together added to the set
                E_eval.add((v, u))
