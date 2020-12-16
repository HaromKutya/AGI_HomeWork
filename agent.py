import numpy as np

from game import Game


class Agent(object):
    """
    The parent class for agents.
    """
    def __init__(self, game: Game):
        super(Agent, self).__init__()
        self.game = game

    def game_started(self, initial_state: np.array):
        """
        Notify the agent if the game has started.
        :param initial_state: The initial board of the game.
        :return: None
        """
        raise NotImplementedError

    def step(self, game_state: np.array, last_step: int):
        """
        The step function of the agent.
        :param game_state: The current state of the game, where:
                           0: empty field
                           1: field occupied by the current player
                           2: field occupied by the opponent
        :param last_step: The last step made by the opponent.
        :return: The list of all possible moves in descending order by desirability.
        (so the first move is the most desirable)
        """
        raise NotImplementedError

    def game_ended(self, has_won: bool, last_game_state: np.array, last_step: int):
        """
        Notify the agent if the game has ended.
        :param has_won: True if the agent has won the game. False otherwise.
        :return: None
        """
        raise NotImplementedError


class HumanAgent(Agent):
    def __init__(self, game: Game):
        super(HumanAgent, self).__init__(game)

    def game_started(self, initial_state: np.array):
        pass

    def step(self, game_state: np.array, last_step: int):
        for row in game_state:
            print(" ".join([str(element) for element in row]))

        col_highest_indices = (game_state != 0).argmax(axis=0)
        for col in range(game_state.shape[1]):
            if np.all(game_state[:, col] == 0):
                col_highest_indices[col] = game_state.shape[1] - 1
        while True:
            selected = int(input("step: "))
            if col_highest_indices[selected] > 0:
                break
            print("The selected column is full. Select another!")
        return selected

    def game_ended(self, has_won: bool, last_game_state: np.array, last_step: int):
        if has_won:
            print("Congrats! You Won!")
        else:
            print("Too bad! You Lost!")
