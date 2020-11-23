"""
    Definitions of `Explorer Agents` which can be used to make a possibly not-so-random walk in the game-tree.
    
    Author: Levente Alekszejenkó
"""

import numpy as np

def get_guess_homogenous():
    """
        returns homogenous 1/7 probability
    """
    return (1/7)*np.ones(7)

class get_guess_centroid():
    def __init__(self):
        samples = np.random.normal(3.5, 1, int(1e7))
        self.mass = np.array([0,0,0,0, 0,0,0])
        self.mass[0] = len(samples[samples<1])
        for i in range(1,7):
            self.mass[i] = len(samples[samples<(i+1)])-np.sum(self.mass[:i])
        print(self.mass)
    
    def __call__(self):
        return self.mass/1e7