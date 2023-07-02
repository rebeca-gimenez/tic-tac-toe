'''
Tic Tac Toe GUI using classes and Tkinter
Author: Rebeca Gimenez

Board options:
Defines nboard
1. Traditional (3x3 board): nboard = 3
2. NxN Board: nboard = n
3. Ultimate (3x3 board within each cell): nboard = 3

Player options
Defines oneplayer and trials
1. Single player easy: oneplayer = True, trials =
2. Single player hard: oneplayer = True, trials =
3. 2 players (against a friend): oneplayer = False, trials = 0

Game options
Defines xfirst
1. X plays first: xfirst = True

For this game we assume that the user always plays first
'''

import tkinter as tk
import TicTacToeGame as game
import TicTacToeComp as comp
#import TicTacToeComp as computer
#Add options to play against the computer
    
class TicTacToeGUI():
    """
    A GUI class for the Tic-Tac-Toe (TTT) Game
    """
    def __init__(self, master):
        """
        Initializes the TTT GUI class
        
        master: root window
        nboard: int, board of size n x n
        oneplayer: bool, True for a single player
        trials: int, number of trials for the computer as a player code
        xfirst: bool, True if x plays first
        
        Delete
        self._nboard = nboard
        self._oneplayer = oneplayer
        self._trials = trials
        """
        #The first color for "X" and "O" is background, the second is foreground
        #Label color is foreground.
        #Labels have the same background as Frame
        self._colors = {"X": ("#F7C59F","#FF6B35"), "O": ("#B9DAF4", "#1A659E"), 
                        "Label": "#003A66", "Frame": "#FAFAF0", "Button": "#EFEFD0"}
        
        self._xfirst = True
        #Board options
        self._nboard = 3
        
        #Player options
        self._oneplayer = False
        self._trials = 0
        
        #Window
        self._master = master
        self._master.title("Tic-Tac-Toe")
        self._master.configure(bg= self._colors["Frame"])
        #Replace with your own icon
        #self._master.iconbitmap("C:/Users/gimen/Documents/Branding/rg-oswald-bold.ico")
        
        #Buttons (Cells of the TicTacToe)
        self._buttons = {}
        
        #Labels
        self.new_game_state_labels()
        
        self.menu_bar()
        #Start newgame
        #Initializes board class, with an empty board
        self.newgame()
        
    def newgame(self):
        """
        Restarts the game
        """
        #Reset first player
        if self._xfirst:
            self._cur_player = "X"
        else:
            self._cur_player = "O"
            
        #Remove old buttons
        for button in self._buttons:
            button.grid_remove()
        #Add new board buttons
        self._board = game.TicTacToe(self._nboard,self._xfirst)
        self.draw_board()
        
        #Remove old labels
        for label in self._labels:
            self._labels[label].grid_remove() 
        #Add new labels
        self.new_game_state_labels()
        self.game_state_labels()

    def draw_board(self):
        """
        Updates board labels using the board imported from TicTacToeGame
        The board is drawn using buttons because they link the click position 
        with the grid.
        """
        #Create buttons
        for num in range(self._nboard*self._nboard):
            b_row = num // self._nboard
            b_col = num % self._nboard
            button = tk.Button(self._master, text=" ", bg=self._colors["Button"] ,font=('Gill Sans Ultra Bold', "22"), height=1, width=3)
            button.grid(row=b_row+3, column=b_col)
            button.config(command=lambda button=button: self.clicked(button))
            #Save button in a dictionary
            self._buttons[button] = (b_row,b_col)
    
    def clicked(self, button):
        """
        When clicking in an empty cell, it changes the text and disables the
        button

        button : tk.Button widget
        """
        if button["text"] == " ":
            button["text"] =  self._cur_player
            button.config(state="disabled", disabledforeground=self._colors[self._cur_player][1], bg=self._colors[self._cur_player][0])
            
            self._board.set_symbol(self._buttons[button][0], self._buttons[button][1], 
                                   self._cur_player)
            self._cur_player = game.switch_player(self._cur_player)   
            self.game_state_labels()
            #print(self._board)
        if self._cur_player=="O" and self._oneplayer == True and self._board.check_win() == None:
            move = comp.mc_move(self._board, self._cur_player, self._trials)
            for key, value in self._buttons.items():
                if value == move:
                    button = key
                else:
                    pass
            button["text"] =  self._cur_player
            button.config(state="disabled", disabledforeground=self._colors[self._cur_player][1], bg=self._colors[self._cur_player][0])
            self._board.set_symbol(move[0], move[1], self._cur_player)
            self._cur_player = game.switch_player(self._cur_player)   
            self.game_state_labels()
            #print(self._board)
                    
    def new_game_state_labels(self):
        """
        Creates game state labels
        """
        self._labels = {}
        #State of the game and turn labels
        state = tk.Label(self._master, text="In progress...", width=17,
                             font=('Gill Sans Ultra Bold', "12"), 
                             fg=self._colors["Label"],
                             bg= self._colors["Frame"])
        state.grid(row=0, column=0, columnspan=self._nboard)
        turn = tk.Label(self._master, text="", font=("Arial", "10"), 
                        fg=self._colors["Label"], bg= self._colors["Frame"])
        turn.grid(row=1, column=0, columnspan=self._nboard)
        
        self._labels["state"] = state
        self._labels["turn"] = turn
        
    def game_state_labels(self):
        """
        Updates game state labels
        self._labels["state"] = state
        self._labels["turn"] = turn
        
        state indicates the state the game is in: in progress or finished
        turn indicates the player's turn

        """
        result = self._board.check_win()
        computer_res = {"D": "It's a draw", "X": "You won!", "O": "Computer won"}
        #1 player (against the computer)
        #Game in progress
        if self._oneplayer == True:
            if result == None and self._cur_player == "X":
                self._labels["turn"]["text"] = "It's your turn"  
            elif result == None and self._cur_player == "O":
                self._labels["turn"]["text"] = "..."  
            else:
                self._labels["turn"]["text"] = "Click 'New game'"
                self._labels["state"]["text"] = computer_res[result]
                for button in self._buttons:
                    button.config(state="disabled")
        #2 players
        else:
            if result == None:
                self._labels["turn"]["text"] = "It's " + self._cur_player + "'s turn"    
            elif result == "D":
                self._labels["turn"]["text"] = "Click 'New game'"
                self._labels["state"]["text"] = "It's a draw"
            else:
                self._labels["turn"]["text"] = "Click 'New game'"
                self._labels["state"].config(fg=self._colors[result][1])
                self._labels["state"]["text"] = result + " won!"
                for button in self._buttons:
                    button.config(state="disabled")
              
    def against_friend(self, boolean):
        """
        Defines variables for 2 players (against a friend)
        oneplayer = False, trials = 0
        oneplayer: bool, True for a single player
        """
        if boolean:
            self._oneplayer = False
            self._trials = 0
        else:
            self._oneplayer = True
            self._trials = self._nboard*self._nboard
        #New game
        self.newgame()
       
    def n_board(self, number):
        """
        Resets the game to a nxn board
        """
        #New game
        self._nboard = number
        self.newgame()
        
    def colors(self, number):
        if number == 1:
            self._colors = {"X": ("#F7C59F","#FF6B35"), "O": ("#B9DAF4", "#1A659E"), 
                            "Label": "#003A66", "Frame": "#FAFAF0", "Button": "#EFEFD0"}
        elif number == 2:
            self._colors = {"X": ("#D7F9FF","#0E1C36"), "O": ("#F9FBF2", "#0E1C36"), 
                            "Label": "#0E1C36", "Frame": "#EFF3FB", "Button": "#FFEDE1"}
        else:
            self._colors = {"X": ("#44A1A0","#FFFFFA"), "O": ("#78CDD7", "#FFFFFA"), 
                            "Label": "#FFFFFA", "Frame": "#138690", "Button": "#247B7B"}
        self.newgame()
        self._master.configure(bg= self._colors["Frame"])
        
    def menu_bar(self):
        """
        Menu bar options for Tic-Tac-Toe game
        """
        #Create menu
        ttt_menu = tk.Menu(self._master)
        self._master.config(menu=ttt_menu)
        
        #Create options for the menu bar
        game_menu = tk.Menu(ttt_menu)
        player_menu = tk.Menu(ttt_menu)
        colors_menu = tk.Menu(ttt_menu)
        
        #Create sub-menu for game_menu
        nxn_menu = tk.Menu(ttt_menu)
        
        #Add options to the menu bar
        ttt_menu.add_cascade(label="Boards", menu=game_menu)
        ttt_menu.add_cascade(label="Players", menu=player_menu)
        ttt_menu.add_cascade(label="Colors", menu=colors_menu)
        ttt_menu.add_command(label="New game", command=self.newgame)
        
        #Add sub-menu to the game_menu
        game_menu.add_command(label="Traditional 3x3", command=lambda: self.n_board(3))
        game_menu.add_cascade(label="Bigger board", menu=nxn_menu)
        
        #Add dropdown options for game menu
        #Traditional: 3x3 board
        #Bigger board: nxn Board
        #Ultimate: a TTT inside each TTT cell
        nxn_menu.add_command(label="4x4", command=lambda: self.n_board(4))
        nxn_menu.add_command(label="5x5", command=lambda: self.n_board(5))
        nxn_menu.add_command(label="6x6", command=lambda: self.n_board(6))
        nxn_menu.add_command(label="7x7", command=lambda: self.n_board(7))
        nxn_menu.add_command(label="8x8", command=lambda: self.n_board(8))
        nxn_menu.add_command(label="9x9", command=lambda: self.n_board(9))
        
        #Add dropdown options for player menu
        #2 players: against a friend
        #1 player: against the computer
        player_menu.add_command(label="2 players", command=lambda: self.against_friend(True))
        player_menu.add_command(label="1 player", command=lambda: self.against_friend(False))
        
        #Player menu: against a friend, against the computer
        #Symbol options: "X" plays first, "O" plays first
        colors_menu.add_command(label="Blue and orange", command=lambda: self.colors(1))
        colors_menu.add_command(label="Clear", command=lambda: self.colors(2))
        colors_menu.add_command(label="Green", command=lambda: self.colors(3))

root = tk.Tk()
test = TicTacToeGUI(root)
root.mainloop()