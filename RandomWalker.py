
import random

class RandomWalker(object):
    def __init__(self, model, options):
        self.model = model
        self.options = options

    def state(self):
        return self.model.state()

    def walk(self):
        option = random.choice(self.options)
        reward = option.apply(self.model)
        return (self.model.state(), reward)
