
from mdp import *
from learn import *
from walk import *
from cluster import *

def main(args=None):
    model = Maze(9, 9, [(4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8)])
    learner = QLearner(model)

    for i in range(10):
        g = makeLocalGraph(learner)
        (nodes, v) = cluster(g)
        learner.plan(nodes, v)

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
