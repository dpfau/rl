
import random
import itertools
import collections

def wrandom(weights):
    if isinstance(weights, str):
        return weights
    r = random.random()
    for (w, i) in zip(weights, itertools.count()):
        if r < w:
            return i
        r = r - w

class Option(object):
    def __init__(self, act, stop):
        self.act = act
        self.stop = stop

    def apply(self, model):
        stop = False
        reward = 0
        while not stop:
            a = wrandom(self.act(model.state()))
            # TODO: consider the discount
            reward += model.act(a)
            stop = random.random() < self.stop(model.state())
        return reward

class Action(Option):
    def __init__(self, a):
        self.a = a
        Option.__init__(self, lambda s: a, lambda s: 1)

    def __repr__(self):
        return self.a
