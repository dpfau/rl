
import numpy as NP
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as NX

from mdp import *
from option import *

def cluster(g):
    nodes = sorted(g.nodes())
    W = NP.array(NX.linalg.adjacency_matrix(g, nodes))
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
    return (nodes, v)
