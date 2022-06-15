"""
Tic Tac Toe Player
"""

import math
import copy
from queue import Empty

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
    numX = 0
    numO = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "X":
                numX += 1
            elif board[i][j] == "O":
                numO += 1
    
    if numX == numO:
        return "X"
    elif numX > numO:
        return "O"
    elif numX < numO:
        return "X"



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add(tuple((i, j)))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Checking for valid action
    if (board[action[0]][action[1]] != EMPTY) or (action[0] not in [0, 1, 2]) or (action[1] not in [0, 1, 2]):
        raise Exception("Invalid action...")

    boardCopy = copy.deepcopy(board)
    boardCopy[action[0]][action[1]] = player(board)

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        # Checking vertical X
        if board[i][0] == X and board[i][1] == X and board[i][2] == X:
            return X
        # Checking vertical O
        if board[i][0] == O and board[i][1] == O and board[i][2] == O:
            return O
        # Checking horizontal X
        if board[0][i] == X and board[1][i] == X and board[2][i] == X:
            return X
        # Checking horizontal O
        if board[0][i] == O and board[1][i] == O and board[2][i] == O:
            return O
    # Checking diagonal X
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    # Checking diagonal O
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][2] == O and board[1][1] == O and board[0][2] == O:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True

    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == EMPTY):
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        _, action =  maxValue(board)
        return action
    else:
        _, action = minValue(board)
        return action


def maxValue(board):
    if terminal(board):
        return utility(board), None
        
    bestValue = -math.inf
    bestAction = None

    for action in actions(board):
        currValue, _ = minValue(result(board, action))
        #Best case check
        if currValue == 1:
            return currValue, action

        if currValue > bestValue:
            bestValue = currValue
            bestAction = action
       
    return bestValue, bestAction


def minValue(board):
    if terminal(board):
        return utility(board), None

    bestValue = math.inf
    bestAction = None

    for action in actions(board):
        currValue, _ = maxValue(result(board, action))
        # Best case check
        if currValue == -1:
            return currValue, action

        if currValue < bestValue:
            bestValue = currValue
            bestAction = action

    return bestValue, bestAction