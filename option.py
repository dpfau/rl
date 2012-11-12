
import random
import itertools

def wrandom(weights):
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
        stop = True
        while not stop:
            a = wrandom(self.act(model.state()))
            model.act(a)
            stop = random.random() < self.stop(model.state())

class Action(Option):
    def __init__(self, a):
        super(lambda s: a, lambda s: 1)
