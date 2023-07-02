"""
Tic-Tac-Toe code to play against the computer

Uses the Monte Carlo method to select the next move the computer will make

Code developed for the Principles of Computing Part 1, week 3, project.

Note: The Monte Carlo method uses repeated random sampling to obtain 
numerical results.
"""

import random
import TicTacToeGame as game
#import poc_ttt_provided as provided

#Score constants for the players
cur_score = 1.0         #Current player
other_score = 1.0       #Other player
    
def mc_trial(board, cur_player):
    """
    The function plays a game making random moves.
    1 trial: 1 game played with random moves, alternating
    between players, from current state to finished state.
    
    board: current board grid (a list of lists).
    cur_player: trial starts with current player ("X" or "O").
    
    Modifies the board input. It does not return anything.
    The modified board will contain the state of the game.
    """
    player = cur_player
    winner = None
    empty_list = board.empty_squares()
    #Run game (trial)
    while winner == None:
        #Pick an empty square randomly
        row, col = random.choice(empty_list)
        #Move (set "X" or "O" in the empty square)
        board.set_symbol(row, col, player)
        #Check state of the game
        winner = board.check_win()
        player = game.switch_player(player)
        #print("Winner:", winner)
        #print(board)
    
def mc_update_scores(scores, board, player):
    '''
    Scores the completed Tic-Tac-Toe board.
    
    scores: grid (a list of lists), with board dimensions.
    board: from a completed game.
    player: which player the machine player (computer) is.
    
    It does not return anything. Fills scores in place.
    '''
    winner = board.check_win()
    #Draw: all squares should receive a score of 0
    if winner == "D":
        pass
    else:
        #Computer wins: all squares should receive a score of 1
        if winner == player:
            num = 1
        #User wins: all squares should receive a score of -1
        else:
            num = -1
        #Square that matches current player gets n*cur_score.
        #Square that matches other player gets n*(-other_score).
        #All empty squares should get a score of 0.
        for row in range(board.board_size()):
            for col in range(board.board_size()):
                if board.get_item(row, col) == player:
                    scores[row][col] += num*cur_score
                elif board.get_item(row, col) == game.switch_player(player):
                    scores[row][col] += -num*other_score
                else:
                    scores[row][col] += 0    
    
def get_best_move(board, scores): 
    '''
    Finds all the empty squares in the current board with the maximum score.
    This function shouldn't be called with a board without empty squares.
     
    board: current board.
    scores: grid (a list of lists), same dimensions as the board.
    
    Randomly returns one square as a (row, column) tuple. 
    '''
    squares = board.empty_squares() #List of tuples (row, col)
    if squares != []:
        scoreslist = [] #List of scores with the same size as squares
        for square in squares:
            scoreslist.append(scores[square[0]][square[1]])
        maxscore = max(scoreslist)
        #Randomly choose one square with max score
        maxsquares = [] #List squares (row, col) with the maximum score
        for square in squares:
            if scores[square[0]][square[1]] == maxscore:
                maxsquares.append(square)
        result = random.choice(maxsquares)
        return result
    else:
        pass
    
def mc_move(board, player, trials):
    """
    Monte Carlo simulation.
    
    board: current board grid (a list of lists).
    player: trial starts with current player ("X" or "O").
    trials: number of trials to run.
    1 trial: 1 game played with random moves, alternating
    between players, from current state to finished state.
    
    Returns a move for the machine player as a (row, column) tuple.
    """
    #Scores grid
    scoreg = [[0 for dummycol in range(board.board_size())]
              for dummyrow in range(board.board_size())]
    if board.check_win() == None:
        #For each trial
        for dummy in range(trials):
            #Copy the current board
            cloned = board.copy()
            #Play a game with random moves
            mc_trial(cloned, player)
            #Update the scores grid
            mc_update_scores(scoreg, cloned, player)
    #After the trials, return an empty square with the maximum score
    return get_best_move(board, scoreg)
