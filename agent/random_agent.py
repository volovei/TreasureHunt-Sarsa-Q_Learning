import numpy as np

class RandomAgent: # se quisermos so movimentos aleatórios
    def __init__(self, action_space):
        self.action_space = action_space

    def choose_action(self, state):
        return self.action_space.sample()
