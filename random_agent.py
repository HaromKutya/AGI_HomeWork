import numpy as np
from agent import Agent


class RandomAgent(Agent):
    def step(self, game_state: np.array):
        return list(np.random.permutation(game_state.shape[1]))

    def game_ended(self, has_won: bool):
        pass
