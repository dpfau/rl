
import random
import networkx as NX

SHORT_WALK = 100

class RandomWalker(object):
    def __init__(self, model, options=None):
        self.model = model
        if options is None:
            self.options = self.model.actions()
        else:
            self.options = options

    def state(self):
        return self.model.state()

    def walk(self):
        option = random.choice(list(self.options))
        (steps, reward) = self.model.act(option)
        return (self.model.state(), reward)

def makeLocalGraph(model, options=None, walker=None):
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
