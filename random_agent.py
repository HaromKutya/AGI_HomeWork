import numpy as np

from agent import Agent
from game import Game

from utils import get_possible_steps


class RandomAgent(Agent):
    def __init__(self, game: Game):
        super(RandomAgent, self).__init__(game)
        self.game = game

    def game_started(self, initial_state: np.array):
        pass

    def step(self, game_state: np.array, last_step: int):
        opts = get_possible_steps(game_state)
        [result] = np.random.choice(opts, 1, replace=False)
        return result

    def game_ended(self, has_won: bool):
        pass
