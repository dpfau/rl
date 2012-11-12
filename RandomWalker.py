
import random

class RandomWalker(object):
    def __init__(self, model, options):
        self.model = model
        self.options = options

    def state(self):
        return model.state()

    def walk(self):
        option = random.choice(options)
        option.apply(model)
        return model.state()
