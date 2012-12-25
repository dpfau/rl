
import numpy as NP
import networkx as NX
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from mdp import *
from option import *
from RandomWalker import *

SHORT_WALK = 10000

def makeLocalGraph(model, options, walker=None):
    if walker is None:
        walker = RandomWalker(model, options)
    g = NX.DiGraph()
    s = walker.state()
    g.add_node(s)
    for i in range(SHORT_WALK):
        (t, r) = walker.walk()
        if t not in g:
            g.add_node(t)
        if g.has_edge(s, t):
            g[s][t]['weight'] -= 1/r
        else:
            g.add_edge(s, t, weight=-1/r)
        s = t
    return g

def cluster(g):
    W = NP.array(NX.linalg.adjacency_matrix(g, sorted(g.nodes())))
    # since we're using a DiGraph, make W symmetric
    # but is this the right way to do this?
    W += W.T
    D = NP.diag(W.sum(axis=1))
    # Unnormalized:
##    L = D - W
    # Normalized asymmetric:
    L = NP.eye(len(g)) - NP.linalg.inv(D).dot(W)
    (vals, vecs) = NP.linalg.eig(L)
    vs = sorted(zip(vals, itertools.count(), vecs.T))
    v = vs[1][2]
    return v

def main(args=None):
    model = Maze(9, 9, [(4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8)])
    actions = [Action(a) for a in model.actions()]
    g = makeLocalGraph(model, actions)
    v = cluster(g)

    # visualization
    tab = [[(x, y) in model.walls for y in range(model.w)] for x in range(model.h)]
    for (node, val) in zip(sorted(g.nodes()), v):
        tab[node[0]][node[1]] = val#(val * val.conjugate()).real**.5
    tab += NP.min(tab)
    tab /= NP.max(tab)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(tab, cmap=cm.coolwarm, interpolation='nearest')
    plt.show()
