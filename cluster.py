
import numpy as NP
import networkx as NX

import RandomWalker

def makeLocalGraph(model, options, walker=None):
    if walker is None:
        walker = RandomWalker(model, options)
    g = NX.DiGraph()
    s = walker.state()
    g.add_node(s)
    for i in range(aShortWalk):
        t = walker.walk()
        g.add_node(t)
        if g.has_edge(s, t):
            g[s][t]['weight'] += 1
        else:
            g.add_edge(s, t, weight=1)
        s = t
    return g

def cluster(g):
    S = NX.linalg.adjacency_matrix(g)
    # since we're using a DiGraph, make S symmetric
    S += S.T
    d = S.sum(axis=0) ** -.5
    L = NP.eye(d.shape[0]) - (S*d).T * d
    (vals, vecs) = NP.linalg.eig(L)
    v = sort(zip(vals, vecs), reverse=True)[1][1]
    return v
