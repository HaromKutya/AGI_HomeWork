import numpy as np

from agent import Agent
from game import Game


class RandomAgent(Agent):
    def __init__(self, game: Game):
        super(RandomAgent, self).__init__(game)

    def game_started(self, initial_state: np.array):
        pass

    def step(self, game_state: np.array):
        return list(np.random.permutation(game_state.shape[1]))

    def game_ended(self, has_won: bool):
        pass
