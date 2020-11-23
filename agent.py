import numpy as np

from game import Game


class Agent(object):
    """
    The parent class for agents.
    """
    def __init__(self, game: Game):
        super(Agent, self).__init__()
        self.game = game

    def step(self, game_state: np.array):
        """
        The step function of the agent.
        :param game_state: The current state of the game, where:
                           0: empty field
                           1: field occupied by the current player
                           2: field occupied by the opponent
        :return: The list of all possible moves in descending order by desirability.
        (so the first move is the most desirable)
        """
        raise NotImplementedError

    def game_ended(self, has_won: bool):
        raise NotImplementedError


class HumanAgent(Agent):
    def __init__(self, game: Game):
        super(HumanAgent, self).__init__(game)

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
