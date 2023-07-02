"""
Class for the Tic-Tac-Toe game
It creates a board and checks the state of the game
"""
def switch_player(cur_player):
    """
    Function to alternate between player "X" and "O"
    """
    if cur_player == "X":
        return "O"
    if cur_player == "O":
        return "X"
        
class TicTacToe():
    """
    Class for the Tic-Tac-Toe game
    """
    def __init__(self, nboard, xfirst = True, board = None ):
        """
        Initializes the Tic-Tac-Toe board
        
        Parameters
            nboard: int, board of size n x n
            xfirst: bool, True if x plays first
            board: list representation of the game
        """
        self._nboard = nboard
        self._xfirst = xfirst
        
        if board == None:
            #Create empty board
            self._board = [[' ' for dummy_col in range(nboard)] 
                           for dummy_row in range(nboard)]
        else:
            #Copy board
            self._board = [[board[row][col] for col in range(nboard)] 
                           for row in range(nboard)]
    
    def __str__(self):
        """
        Returns string representation of the game
        """
        game_string = ''
        for row in self._board:
            game_string += str(row) + "\n"
        return game_string
    
    def get_item(self, row, col):
        """
        Returns item at position (row, col)
            row: int, board row
            col: int, board column
        Returns: string corresponding to ' ', 'X' or 'O'
        Used in TicTacToeGUI.py
        """
        return self._board[row][col]
    
    def set_symbol(self, row, col, player):
        """
        Set player "X" or "O" at position (row, col)
            row: int, board row
            col: int, board column
        Modifies board in place
        
        Used in TicTacToeGUI.py
        Used in TicTacToeComp
        """
        if self._board[row][col] == " ":
            self._board[row][col] = player
    
    def check_win(self):
        """
        Checks if the game is:
            In progress: returns None
            Finished: returns the winner, "X" or "O". For draws returns "D"
        
        Used in TicTacToeGUI.py
        """
        board = self._board
        #In a nxn board, there are n rows, n columns, 2 diagonals
        directions = []
        #Add list of rows
        directions = list(board)
        #Add list of columns
        directions += [[board[rowidx][colidx] for rowidx in range(self._nboard)] 
                  for colidx in range(self._nboard)]
        #Add list of diagonals
        diag1, diag2 = [], []
        for index in range(len(board)):
            diag1 += board[index][index]
            diag2 += board[index][len(board) - 1 - index]
        directions.append(diag1)
        directions.append(diag2)
        empty = 0
        #For each line count "X", "O" and " "
        for line in directions:
            if line.count("X") == self._nboard:
                return "X"
            elif line.count("O") == self._nboard:
                return "O"
            else:
                empty += line.count(" ")
        if empty > 0:
            return None
        else:
            return "D"
    
    def empty_squares(self):
        """
        Returns a list of the empty squares as (row, column) tuples
        
        Used in TicTacToeComp
        """
        empty = []
        for row in range(self._nboard):
            for column in range(self._nboard):
                if self._board[row][column] == " ":
                    empty.append((row,column))
        return empty
    
    def board_size(self):
        """
        From a nxn board, returns n
        Used in TicTacToeComp
        """
        return self._nboard
    
    def copy(self):
        """
        Return a copy of the board
        Used in TicTacToeComp
        """
        return TicTacToe(self._nboard, self._xfirst, self._board)

        