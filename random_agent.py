import numpy as np

from agent import Agent
from game import Game

from utils import get_possible_steps, has_game_ended


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

    def game_ended(self, has_won: bool, last_game_state: np.array, last_step: int):
        pass

class CentroidRandomAgent(RandomAgent):
    def __init__(self, game: Game):
        super(CentroidRandomAgent, self).__init__(game)
        samples = np.random.normal(3.5, 1, int(1e7))
        self.mass = np.array([0,0,0,0, 0,0,0])
        self.mass[0] = len(samples[samples<1])
        for i in range(1,7):
            self.mass[i] = len(samples[samples<(i+1)])-np.sum(self.mass[:i])
        self.mass = self.mass/1e7

    def step(self, game_state: np.array, last_step: int):
        pos_steps = get_possible_steps(game_state)
        opts = [1 if i in pos_steps else 0 for i in range(7)]
        opts = opts*self.mass
        return np.argmax(opts)

class GreedyRandomAgent(RandomAgent):
    '''
        This greedy RandomAgent simulates an adaptive guessing appoach:
        If we add a single step and the game finishes, then it is a good step
        because we either win the game or prevent our opponent.

        Otherwise it returns a simply random answer. 
    '''
    def __init__(self, game: Game):
        super(GreedyRandomAgent, self).__init__(game)

    def step(self, game_state: np.array, last_step: int):
        opts = get_possible_steps(game_state)
        for i in opts:
            board_local = game_state.copy()
            highest_index = np.where(board_local[:, i] == 0)[0][-1]
            board_local[highest_index, i] = 1
            if has_game_ended(board_local, i):
                return i
            else:
                board_local[highest_index, i] = 2
                if has_game_ended(board_local, i):
                    return i
        [result] = np.random.choice(opts, 1, replace=False)
        return result

class MinimalistRandomAgent(RandomAgent):
    '''
        This Agent tries to choose the cell which
        produces the flattest possible table after its step.
    '''

    def __init__(self, game:Game):
        super(MinimalistRandomAgent, self).__init__(game)
    
    def step(self, game_state: np.array, last_step: int):
        opts = get_possible_steps(game_state)
        min_val, min_step = 6, opts[0]
        for i in opts:
            board_local = game_state.copy()
            highest_index = np.where(board_local[:, i] == 0)[0][-1]
            if highest_index < min_val:
              min_val = highest_index
              min_step = i
        return min_step
