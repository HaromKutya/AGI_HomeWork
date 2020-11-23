import numpy as np

from utils import has_game_ended, execute_step, flip_players


def simulate_game(initial_board: np.array, sequence: list):
    """
    Simulates a game from the given initial board and step sequence.
    :param initial_board: The game state from which the simulation starts from.
    The notation must be: 0=empty, 1=current_player, 2: opponent
    :param sequence: The sequence of moves starting with player 1 (the current player)
    and alternating between the two players.
    :return: -1: draw,
              0: the game is still running
              1: the current player (player 1) won
              2: the opponent (player 2) won
    """
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
    """
    The object representing a game sequence.
    """
    def __init__(self, board_shape: tuple = (6, 7)):
        """
        :param board_shape: The shape of the playing field. It defaults to (6, 7) as for the original Connect4 game.
        """
        self._board_shape = board_shape
        self.board = np.zeros(shape=self._board_shape, dtype=np.int8)
        self.history = []

    def check_game_ended(self, player_1, player_2):
        """
        Check if the game has ended and notifies the players accordingly.
        :return: True if the game is over, False otherwise.
        """
        result = has_game_ended(self.board)
        if result == 0:
            return False

        if result == 1:
            player_1.game_ended(has_won=True)
            player_2.game_ended(has_won=False)
        elif result == 2:
            player_1.game_ended(has_won=False)
            player_2.game_ended(has_won=True)
        elif result == -1:
            player_1.game_ended(has_won=False)
            player_2.game_ended(has_won=False)

        return True

    def reset_board(self):
        """
        Resets the board to its initial state.
        :return: None
        """
        self.board = np.zeros(shape=self._board_shape, dtype=np.int8)

    def get_history(self):
        """
        Returns the list of game states after every taken move, starting with the first move.
        :return: The list of game states after every taken move, starting with the first move.
        """
        return self.history

    def play_a_game(self, player_1, player_2):
        """
        Runs a game with two players, player_1 makes the first move.
        :param player_1: The starting player.
        :param player_2: The other player.
        :return: None
        """
        self.reset_board()
        self.history = []

        current_player = True

        while not self.check_game_ended(player_1, player_2):
            if current_player:
                preferences = player_1.step(game_state=self.board)
            else:
                preferences = player_2.step(game_state=flip_players(self.board))
            self.board = execute_step(board=self.board, preferences=preferences, player_symbol=1 if current_player else 2)
            self.history.append(self.board.copy())
            current_player = not current_player
