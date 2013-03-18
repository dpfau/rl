
import random
import itertools
import collections

def wrandom(weights):
    if not isinstance(weights, collections.Iterable):
        # deterministic choice
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
        steps = 0
        reward = 0
        while not stop:
            a = wrandom(self.act(model.state()))
            # TODO: consider the discount
            (_, r) = model.act(a)
            reward += r * model.discount()**steps
            steps += 1
            stop = random.random() < self.stop(model.state())
        return (steps, reward)
