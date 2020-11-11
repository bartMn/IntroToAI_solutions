"""
Tic Tac Toe Player
"""
import copy
from random import randint as rand

X = "X"
O = "O"
EMPTY = None
Moves= None


def initial_state():
    """
    Returns starting state of the board.
    """
    global Moves
    Moves=0
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_o=0
    count_x=0
    for i in range(3):
        for j in range(3):
            if board[i][j]== X:
                count_x+= 1
            elif board[i][j]== O:
                count_o+= 1
            
    if  count_x <= count_o:
        return  X
    else:
        return O
    
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]== EMPTY:
                possible_moves.add((i, j))
            else:
                continue
    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board= copy.deepcopy(board)
  #  print(player(board)+ "'s turn :"+str(action[0])+str(action[1]))
    if new_board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid move!!!")
    else:
        new_board[action[0]][action[1]]= player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        count_o=0
        count_x=0
        for j in range(3):
            if board[i][j]== X:
                count_x+=1
                if count_x== 3:
                    return X
            elif board[i][j]== O:
                count_o+=1
                if count_o== 3:
                    return O

            
    for j in range(3):
        count_o=0
        count_x=0
        for i in range(3):
            
            if board[i][j]== X:
                count_x+=1
                if count_x== 3:
                    return X
            elif board[i][j]== O:
                count_o+=1
                if count_o== 3:
                    return O
           
            
    count_o=0
    count_x=0
    for x in range(3):
        if board[x][x]== X:
             count_x+=1
             if count_x== 3:
                 return X
        elif board[x][x]== O:
            count_o+=1
            if count_o== 3:
                return O
            
    count_o=0
    count_x=0
    for x in range(3):
        if board[x][2-x]== X:
             count_x+=1
             if count_x== 3:
                 return X
        elif board[x][2-x]== O:
            count_o+=1
            if count_o== 3:
                return O
        
    return None
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    N=0
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                N+=1
            
    if winner(board) is not None:
        return True
    elif N==0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)== X:
        return 1
    elif winner(board)== O:
        return -1
    else:
        return 0
    
def MAX(board):
    if terminal(board):
   #     print("terminal is reached"+ str(utility(board)))
        return ((utility(board), None))
    v_max=-2    
    for action in actions(board):
        v= MIN(result(board, action))[0]
        if v== 1:
            return (v, action)
        if v>v_max:
            v_max= v
            act= action
    return ((v_max, act))

def MIN(board):
    if terminal(board):
   #     print("terminal is reached"+ str(utility(board)))
        return ((utility(board), None))
    v_min=2
    for action in actions(board):
        v= MAX(result(board, action))[0]
        if v== -1:
           return (v, action)
        if v_min>v:
            v_min= v
            act= action
    return ((v_min, act))

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    global Moves
    if player(board)== X:
        if Moves == 0:
            i=rand(0,2)
            j=rand(0,2)
            Moves+=1
            return (i, j) 
        return MAX(board)[1]
    elif player(board)== O:
        return MIN(board)[1]
        
         