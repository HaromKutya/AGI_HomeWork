import numpy as np
from agent import Agent
from random_agent import RandomAgent


class AIAgent(Agent):
    def __init__(self):
        super(AIAgent, self).__init__()
        self.helper_agent = RandomAgent()

    def step(self, game_state: np.array):
        return self.helper_agent.step(game_state)

    def game_ended(self, has_won: bool):
        pass

