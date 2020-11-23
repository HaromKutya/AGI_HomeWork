import numpy as np

from agent import Agent
from utils import has_game_ended, execute_step, flip_players


def simulate_game(initial_board: np.array, sequence: list):
    current_player = True
    board = initial_board
    for preferences in sequence:
        game_state = has_game_ended(board=board)
        if game_state != 0:
            return game_state
        board = execute_step(board=board, preferences=preferences, player_symbol=1 if current_player else 2)
        current_player = not current_player
    return 0


class Game(object):
    def __init__(self, player_1: Agent, player_2: Agent, board_shape: tuple = (6, 7)):
        self._player_1 = player_1
        self._player_2 = player_2
        self._board_shape = board_shape
        self.board = np.zeros(shape=self._board_shape, dtype=np.int8)
        self.history = []

    def check_game_ended(self):
        result = has_game_ended(self.board)
        if result == 0:
            return False

        if result == 1:
            self._player_1.game_ended(has_won=True)
            self._player_2.game_ended(has_won=False)
        elif result == 2:
            self._player_1.game_ended(has_won=False)
            self._player_2.game_ended(has_won=True)
        elif result == -1:
            self._player_1.game_ended(has_won=False)
            self._player_2.game_ended(has_won=False)

        return True

    def reset_board(self):
        self.board = np.zeros(shape=self._board_shape, dtype=np.int8)

    def play_a_game(self):
        self.reset_board()
        self.history = []

        current_player = True

        while not self.check_game_ended():
            if current_player:
                preferences = self._player_1.step(game_state=self.board)
            else:
                preferences = self._player_2.step(game_state=flip_players(self.board))
            self.board = execute_step(board=self.board, preferences=preferences, player_symbol=1 if current_player else 2)
            self.history.append(self.board.copy())
            current_player = not current_player
