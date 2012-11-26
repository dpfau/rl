
import numpy as NP
import networkx as NX

from mdp import *
from option import *
from RandomWalker import *

SHORT_WALK = 1000

def makeLocalGraph(model, options, walker=None):
    if walker is None:
        walker = RandomWalker(model, options)
    g = NX.DiGraph()
    s = walker.state()
    print(s)
    g.add_node(s)
    for i in range(SHORT_WALK):
        (t, r) = walker.walk()
        if t not in g:
            print(t)
            g.add_node(t)
        if g.has_edge(s, t):
            g[s][t]['weight'] -= r
        else:
            g.add_edge(s, t, weight=1)
        s = t
    return g

def cluster(g):
    S = NX.linalg.adjacency_matrix(g)
##    print(S)
    # since we're using a DiGraph, make S symmetric
    # but is this the right way to do this?
    S += S.T
    d = 1/NP.sqrt(S.sum(axis=1))
    L = NP.eye(d.shape[0]) - (S*d).T * d
    (vals, vecs) = NP.linalg.eig(L)
    vs = sorted(zip(vals, itertools.count(), vecs), reverse=True)
    v = vs[1][2]
    return v

def main(args=None):
    model = Maze(9, 9, [(4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8)])
    actions = [Action(a) for a in model.actions()]
    g = makeLocalGraph(model, actions)
    v = cluster(g)
    print(v)
