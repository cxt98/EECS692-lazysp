import numpy as np


class Selector:
    def weightsamp(self, G, p_candidate):
        # draw n samples based on G edges' estimate weights
        weight_sum = 0
        for i in range(len(p_candidate) - 1):
            node = G.edges[p_candidate[i], p_candidate[i + 1]]
            if node['eval'] is False:
                weight_sum += node['est']
        x = np.random.uniform(low=0, high=weight_sum)
        weight_sum = 0
        for i in range(len(p_candidate) - 1):
            node = G.edges[p_candidate[i], p_candidate[i + 1]]
            if x >= weight_sum and x < weight_sum + node['est'] and node['eval'] is False:
                return [(p_candidate[i], p_candidate[i + 1])]
            if node['eval'] is False:
                weight_sum += node['est']
    
    def partition(self, G, p_candidate, beta):
        return 0

    def expand(self, G, p_candidate):
        E_selected = []
        for i in range(len(p_candidate) - 1):
            if G.edges[p_candidate[i], p_candidate[i + 1]]['eval'] is False:
                v_frontier = p_candidate[i]
                for e in G.edges(v_frontier):
                    if G.edges[e]['eval'] is False:
                        E_selected.append(e)
                break
        return E_selected
    
    def forward(self, G, p_candidate):
        for i in range(len(p_candidate) - 1):
            if G.edges[p_candidate[i], p_candidate[i + 1]]['eval'] is False:
                return [(p_candidate[i], p_candidate[i + 1])]
    
    def reverse(self, G, p_candidate):
        for i in range(len(p_candidate) - 2, -1, -1):
            if G.edges[p_candidate[i], p_candidate[i + 1]]['eval'] is False:
                return [(p_candidate[i], p_candidate[i + 1])]

    def alternate(self, G, p_candidate, alternate_n):
        if alternate_n:
            return self.forward(G, p_candidate), 1 - alternate_n
        else:
            return self.reverse(G, p_candidate), 1 - alternate_n
    
    def bisection(self, G, p_candidate):
        dists = [len(p_candidate)] * (len(p_candidate) - 1)
        for i in range(len(p_candidate) - 1): # forward and backward, check eval
            if G.edges[p_candidate[i], p_candidate[i + 1]]['eval'] is True:
                dist = 0
            elif i == 0:
                dist = 1
            else:
                dist = dists[i - 1] + 1
            if dists[i] > dist:
                dists[i] = dist

            j = len(p_candidate) - 1 - i
            if G.edges[p_candidate[j - 1], p_candidate[j]]['eval'] is True:
                dist = 0
            elif i == 0:
                dist = 1
            else:
                dist = dists[j] + 1
            if dists[j - 1] > dist:
                dists[j - 1] = dist
        
        i_max = dists.index(max(dists))
        return [(p_candidate[i_max], p_candidate[i_max + 1])]