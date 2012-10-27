# Connect four board class
# First version by Devin Balkcom, January 2012

from cs1lib import *

BOARD_WIDTH = 7     # hardcode the board size to be 7x7
BOARD_HEIGHT = 6


def draw_piece(ox, oy, cellw, cellh, column, row, turn):
    
    x = ox + (column +.5) * cellw    
    y = oy + (row + .5) * cellh
    
    radius = min(cellw, cellh) / 2 *.8
    
    if turn == 0:
        set_fill_color(1, 1, 1)
    elif turn == 1:
        set_fill_color(1, 0, 0)
    elif turn == 2:
        set_fill_color(0, 0, 0)
    
    draw_circle(x, y, radius)

class Board:
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        
        # state is a list of columns, zero-indexed.
        #   for example, state[3] would be the fourth column,
        #   and state[3][4] would be the 5th piece from the bottom.
        self.state = [[0 for y in range(self.height)] for x in range(self.width)]
        
        # A list to keep track of how many pieces are in each column
        self.column_count = BOARD_WIDTH *[0]
        
        # a variable to keep track of whose turn it is.  Value 1 or 2.
        self.turn = 1
    
    def is_legal(self, move_column):
        return move_column >= 0 and move_column < self.width \
            and self.column_count[move_column] < self.height
        
        
    # move a piece.     
    def move(self, column):
        
        self.state[column][ self.column_count[column] ] = self.turn
        self.column_count[column] += 1
        
        self.switch_turns()

    # returns a sorted list of legal moves, given a Board object with a 
    # particular state
    def legal_moves(self):
        moves = []
        for i in range(self.width):
            if self.column_count[i] < self.height:
                moves.append(i)
        return moves
    
    # undoes the move m returning the state to its predecessor state       
    def undo_move(self, m):
        row = self.column_count[m] - 1
        self.state[m][row] = 0
        
        self.column_count[m] -= 1
        self.switch_turns()
    
    # next player's turn.  3 - 2 is 1, and 3 - 1 is 2,
    # so subtracting current turn from 3 will swap turns
    def switch_turns(self):
        self.turn = 3 - self.turn
    
    # returns true if the game ends in a tie (no more possibile moves)    
    def check_tie(self):
        for col in self.column_count:
            if col < self.height: 
                return False
        return True
    
    # checks to see if someone has won
    # returns a tuple (true/false, player, location of first piece in segment, 
    # location of last piece in segment)
    def is_win(self):
        # check for horizontal wins 
        for col in range(self.width - 3):
            for row in range(self.height):
                if (self.state[col][row] == self.state[col+1][row] == 
                    self.state[col+2][row] == self.state[col+3][row] != 0):
                    return (True, self.state[col][row], (col,row), (col+3, row))
        
        # check for vertical wins        
        for row in range(self.height - 3):
            for col in range(self.width):
                if (self.state[col][row] == self.state[col][row+1] == 
                    self.state[col][row+2] == self.state[col][row+3] != 0):
                    return (True, self.state[col][row], (col, row), (col, row+3))
        
        # check for diagonal-up wins        
        for col in range(self.width - 3):
            for row in range(self.height - 3):
                if (self.state[col][row] == self.state[col+1][row+1] == 
                    self.state[col+2][row+2] == self.state[col+3][row+3] != 0):
                    return (True, self.state[col][row], (col,row), (col+3, row+3))
                
        # check for diagonal-down wins
        for col in range(self.width - 3):
            for row in range(3, self.height):
                if (self.state[col][row] == self.state[col+1][row-1] == 
                    self.state[col+2][row-2] == self.state[col+3][row-3] != 0):
                    return (True, self.state[col][row], (col, row), (col+3, row-3))
                
        return (False, 0, 0, 0)
                
            
        
    def __str__(self):
        str_list = [];
        
        for y in range(self.height):
            for x in range(self.width):
                str_list.append(str(self.state[x][self.height - y - 1]))
            str_list.append("\n")
            
        return "".join(str_list)
            
    
    def draw(self, ox, oy, cellw, cellh):
        
        enable_fill()
     
        # draw the pieces
        
        for r in range(self.height):
            for c in range(self.width):
                draw_piece(ox, oy, cellw, cellh, c, r, self.state[c][r])    
    
 
# unit tests for Board
if __name__ == "__main__":
    from random import randint
    
    b = Board()
    print b.state
    print len(b.state[0])
    
    b.move(3)
    b.move(3)
    b.move(3)
    b.move(3)
    b.move(2)
    b.move(2)
    b.move(2)
    b.move(2)
    b.move(2)
    b.move(4)
    b.move(4)
    b.move(4)
    b.move(4)
    b.move(4)
    b.move(1)
    b.move(1)
    b.move(5)
    b.move(5)
    b.move(5)
    print b
    print b.is_win()
    print ""
    b.move(6)
    print b
    print b.is_win()
    
    raw_input()
    
    for i in range(50):
        move = randint(0, b.width - 1)
        print "moving ", move
        if not b.move(move):
            print "  failed, column full"
        
        print ""
        print b
        
        print "\nPress return to continue."
        raw_input()            
        