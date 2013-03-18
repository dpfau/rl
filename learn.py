
import numpy as NP
import itertools

from option import *

class QLearner(object):
    def __init__(self, model, learning_rate=0.1, options=None):
        self.model = model
        self.learning_rate = learning_rate
        if options is None:
            options = self.model.actions()
        self.options = list(options)
        self.options_lu = dict(zip(self.options, itertools.count()))
        self.states_lu = {}
        self.q = NP.ones((0, len(self.options))) * self.model.max_reward

    def state(self):
        return self.model.state()

    def actions(self):
        return range(len(self.options))

    def discount(self):
        return self.model.discount()

    def act(self, o):
        from_state = self.model.state()
        if from_state not in self.states_lu:
            self.states_lu[from_state] = len(self.states_lu)
            self.q = NP.vstack([self.q, NP.ones(len(self.options)) * self.model.max_reward])
        s = self.states_lu[from_state]
        option = self.options[o]
        if isinstance(option, Option):
            (k, r) = option.apply(self)
        else:
            (k, r) = self.model.act(option)
        to_state = self.model.state()
        if to_state not in self.states_lu:
            self.states_lu[to_state] = len(self.states_lu)
            self.q = NP.vstack([self.q, NP.ones(len(self.options)) * self.model.max_reward])
        s_ = self.states_lu[to_state]
        # On-policy
##        self.q[s, o] += self.learning_rate * (r + self.model.discount()**k * self.q[s_].max() - self.q[s, o])
        # Off-policy for uniform policy
        self.q[s, o] += self.learning_rate * (r + self.model.discount()**k * NP.mean(self.q[s_]) - self.q[s, o])
        return (k, r)

    def plan(self, nodes, subgoal):
        real_subgoal = NP.ones(len(self.states_lu)) * self.model.max_reward
        real_subgoal[[self.states_lu[node] for node in nodes]] = subgoal
        act = NP.argmax(self.q, axis=1)
        stop = NP.diag(self.q.take(act, axis=1)) <= real_subgoal
        lu = self.states_lu.copy()
        o = Option(lambda s: act[lu[s]] if s in lu else NP.ones(len(self.options)) / len(self.options),
                   lambda s: stop[lu[s]] if s in lu else 0)
        self.options_lu[o] = len(self.options)
        self.options.append(o)
        self.q = NP.hstack([self.q, NP.ones((len(self.states_lu), 1)) * self.model.max_reward])
