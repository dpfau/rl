
import numpy as NP

def cluster(g):
    S = g.getAdj()
    d = S.sum(axis=0) ** -.5
    L = NP.eye(d.shape[0]) - (S*d).T * d
    (vals, vecs) = NP.linalg.eig(L)
    v = sort(zip(vals, vecs), reverse=True)[1][1]
    return v
