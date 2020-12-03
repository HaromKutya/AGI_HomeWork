import numpy as np


def get_all_submatrices_of_shape(mat: np.array, shape: tuple):
    assert len(shape) == 2 and len(mat.shape) == 2
    result = []
    for i in range(mat.shape[0] - (shape[0] - 1)):
        for j in range(mat.shape[1] - (shape[1] - 1)):
            submat = mat[i:(i + shape[0]), j:(j + shape[1])]
            result.append(submat)
    return result


def has_game_ended(board: np.array, last_step: int, win_sequence_length: int = 4):
    if last_step == -1:
        return 0

    highest_occupied_index = np.where(board[:, last_step] == 0)[0][-1] + 1
    assert board[highest_occupied_index, last_step] != 0

    x, y = highest_occupied_index, last_step
    player = board[x, y]

    # down
    if (x + win_sequence_length) <= board.shape[0]:
        won = True
        for xi in range(x + 1, x + win_sequence_length):
            if board[xi, y] != player:
                won = False
                break
        if won:
            return player

    # (checking the upward direction is unnecessary)

    # right
    if (y + win_sequence_length) <= board.shape[1]:
        won = True
        for yi in range(y + 1, y + win_sequence_length):
            if board[x, yi] != player:
                won = False
                break
        if won:
            return player

    # left
    if (y - win_sequence_length) >= -1:
        won = True
        for yi in range(y - 1, y - win_sequence_length, -1):
            if board[x, yi] != player:
                won = False
                break
        if won:
            return player

    # down, right (diagonal)
    if (x + win_sequence_length) <= board.shape[0] and (y + win_sequence_length) <= board.shape[1]:
        won = True
        for xi, yi in zip(range(x + 1, x + win_sequence_length), range(y + 1, y + win_sequence_length)):
            if board[xi, yi] != player:
                won = False
                break
        if won:
            return player

    # down, left (diagonal)
    if (x + win_sequence_length) <= board.shape[0] and (y - win_sequence_length) >= -1:
        won = True
        for xi, yi in zip(range(x + 1, x + win_sequence_length), range(y - 1, y - win_sequence_length, -1)):
            if board[xi, yi] != player:
                won = False
                break
        if won:
            return player

    # up, right (diagonal)
    if (x - win_sequence_length) >= -1 and (y + win_sequence_length) <= board.shape[1]:
        won = True
        for xi, yi in zip(range(x - 1, x - win_sequence_length, -1), range(y + 1, y + win_sequence_length)):
            if board[xi, yi] != player:
                won = False
                break
        if won:
            return player

    # up, left (diagonal)
    if (x - win_sequence_length) >= -1 and (y - win_sequence_length) >= -1:
        won = True
        for xi, yi in zip(range(x - 1, x - win_sequence_length, -1), range(y - 1, y - win_sequence_length, -1)):
            if board[xi, yi] != player:
                won = False
                break
        if won:
            return player

    # return -1 if the board is full and neither of the players won (tie)
    if np.all(board != 0):
        return -1

    return 0


def get_possible_steps(board: np.array):
    return np.where(board[0, :] == 0)[0]


def execute_step(board: np.array, step: int):
    assert (board[0, step] == 0)
    board_local = board.copy()
    highest_index = np.where(board[:, step] == 0)[0][-1]
    player = 1 if np.sum(board == 1) == np.sum(board == 2) else 2
    board_local[highest_index, step] = player
    return board_local


def execute_multiple_steps(initial_board: np.array, steps: list):
    board = initial_board.copy()
    for step in steps:
        board = execute_step(board, step)
    return board


def flip_players(board: np.array):
    board_local = board.copy()
    player1_loc = board_local == 1
    player2_loc = board_local == 2
    board_local[player1_loc] = 2
    board_local[player2_loc] = 1
    return board_local


if __name__ == "__main__":
    board_local = np.zeros(shape=(6, 7))
    board_local[:, 3] = 1
    get_possible_steps(board_local)
