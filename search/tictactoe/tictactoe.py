"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0

    for row in board:
        for cell in row:
            if cell == X:
                num_x += 1
            if cell == O:
                num_o += 1
    return X if num_x <= num_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    row_num = 0

    for row in board:
        cell_num = 0
        for cell in row:
            if cell == EMPTY:
                actions.add((row_num, cell_num))
            cell_num += 1
        row_num += 1

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if len(action) != 2:
        raise Exception("Invalid action!")

    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception(f"Invalid action ({action[0]},{action[1]})!")

    if board[action[0]][action[1]] != EMPTY:
        Exception(f"Invalid action ({action[0]},{action[1]})!")

    tmp_board = copy.deepcopy(board)
    tmp_board[action[0]][action[1]] = player(board)
    return tmp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # row winning config
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return X if row[0] == X else O
    
    # column winning config
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return X if board[0][col] == X else O
    
    # diagonals winning config
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return X if board[0][0] == X else O
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return X if board[0][2] == X else O
    
    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # return True if there is a winner
    if winner(board) is not None:
        return True

    # return False if no winner but there are still empty cells
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # otherwise return True (no empty cells in the board and no winner)
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)

    if w == X:
        return 1

    if w == O:
        return -1

    return 0


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))

        # alpha-beta pruning
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))

        # alpha-beta pruning
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        print("minimax: Terminal board")
        return None

    current_player = player(board)

    if current_player == X:
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            value = min_value(result(board, action), -math.inf, math.inf)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    
    if current_player == O:
        best_value = math.inf
        best_action = None
        for action in actions(board):
            value = max_value(result(board, action), -math.inf, math.inf)
            if value < best_value:
                best_value = value
                best_action = action
        return best_action
