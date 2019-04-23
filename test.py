import networkx as nx 
from lazysp import LazySP
from selector import Selector
from copy import deepcopy
import numpy as np
import ghalton
from scipy.spatial import distance
from utils import *
import random

node_n = 100
edge_prob = 0.05

path_n = 3
algos = ['dijkstra', 'astar']#, 'bellman-ford'
selectors = ['weightsamp']#'expand', 'forward', 'reverse', 'alternate', 'bisection', 'partition'
betas = [2, 21, 3]

# 1. random connected graphs
G1 = nx.gnp_random_graph(node_n, edge_prob)
S = Selector()
for (u, v) in G1.edges():
    G1.edges[u, v]['est'] = 1.0
    G1.edges[u, v]['eval'] = False
    G1.edges[u, v]['real'] = random_edgelen()

# 2. roadmap graphs on the unit square from Halton sequence
sequencer = ghalton.GeneralizedHalton(2, 68)
points = [tuple(p) for p in sequencer.get(100)]
connect_r = 0.25

G2 = nx.Graph()
obs = generate_obstacles()
for i, p in enumerate(points):
    G2.add_node(i, pos=p)
for i, j in [(x, y) for x in range(len(G2.nodes)) for y in range(len(G2.nodes)) if x < y]:
    u = G2.nodes[i]['pos']
    v = G2.nodes[j]['pos']
    if distance.euclidean(u, v) <= connect_r:
        G2.add_edge(i, j, eval=False, est=distance.euclidean(u, v), real=obstacle_edgelen(u, v, obs))



graphs = [(G1, 'random connected graphs'),
          (G2, 'roadmap graphs on the unit square')
          ]

stats = np.zeros(shape=(len(graphs), len(algos), len(selectors)))
for i, g in enumerate(graphs):
    print(g[1])
    for j, algo in enumerate(algos):
        for k, selector in enumerate(selectors):
            eval_n_sum = 0
            valid_n = 0
            for m in range(path_n):
                start, goal = random.sample(range(node_n), 2)
                sp = LazySP(deepcopy(g[0]), start, goal)
                path, eval_n = sp.solve(algo, eval('S.' + selector), betas[i])
                if eval_n != 0:
                    print('algorithm: ' + algo + '  selector: ' + selector + '  eval_n: ' + str(eval_n))
                    eval_n_sum += eval_n
                    valid_n += 1
            stats[i][j][k] = eval_n_sum / valid_n

print(stats)