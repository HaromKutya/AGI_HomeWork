import numpy as np


class Agent(object):
    def step(self, game_state: np.array):
        raise NotImplementedError

    def game_ended(self, has_won: bool):
        raise NotImplementedError


class RandomAgent(Agent):
    def step(self, game_state: np.array):
        return list(np.random.permutation(game_state.shape[1]))

    def game_ended(self, has_won: bool):
        pass


class HumanAgent(Agent):
    def step(self, game_state: np.array):
        for row in game_state:
            print("".join([str(element) for element in row]))

        col_highest_indices = (game_state != 0).argmax(axis=0)
        for col in range(game_state.shape[1]):
            if np.all(game_state[:, col] == 0):
                col_highest_indices[col] = game_state.shape[1] - 1
        while True:
            selected = int(input("step: "))
            if col_highest_indices[selected] > 0:
                break
            print("The selected column is full. Select another!")
        return [selected]

    def game_ended(self, has_won: bool):
        if has_won:
            print("Congrats! You Won!")
        else:
            print("Too bad! You Lost!")
