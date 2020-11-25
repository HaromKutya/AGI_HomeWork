import numpy as np


def get_all_submatrices_of_shape(mat: np.array, shape: tuple):
    assert len(shape) == 2 and len(mat.shape) == 2
    result = []
    for i in range(mat.shape[0] - (shape[0] - 1)):
        for j in range(mat.shape[1] - (shape[1] - 1)):
            submat = mat[i:(i + shape[0]), j:(j + shape[1])]
            result.append(submat)
    return result


def has_game_ended(board: np.array, player_count: int = 2, win_sequence_length: int = 4):
    horizontal = get_all_submatrices_of_shape(board, shape=(1, win_sequence_length))
    for submat in horizontal:
        for i in range(1, player_count + 1):
            if np.all(submat == i):
                return i

    vertical = get_all_submatrices_of_shape(board, shape=(win_sequence_length, 1))
    for submat in vertical:
        for i in range(1, player_count + 1):
            if np.all(submat == i):
                return i

    square = get_all_submatrices_of_shape(board, shape=(win_sequence_length, win_sequence_length))
    for submat in square:
        for i in range(1, player_count + 1):
            if np.all(submat.diagonal() == i) or np.all(submat[:, ::-1].diagonal() == i):
                return i

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
