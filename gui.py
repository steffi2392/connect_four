# Simple connect-four gui for cs76
# author:  Devin Balkcom

from cs1lib import *
from board import Board
from alphabeta import  *
from minimax import  *

from threading import Thread

from random import randint

OX, OY = 60, 60
CELLW, CELLH = 40, 40

ALLOWED_TIME = 10

class ConnectFourGui:
    
    # my_move_fn and opponent_move_fn are called to get 
    def __init__(self, player1, player2):
        
        self.players = [player1, player2]
      
        
    def start(self):
        self.board = Board()
        start_graphics(self.__mainloop, "Connect Four", flipped_y = True)
    
    def __mainloop(self):
        enable_smoothing()      
                
        turn = 0
        win, winner, start, end = self.board.is_win()        
        while not window_closed() and not win and not self.board.check_tie():
            
            # redraw everything
            clear()
            print self.board
            self.board.draw(OX, OY, CELLW, CELLH)
            request_redraw()
            sleep(.02)
            
            # request that the player start finding a move
            def start_move_fn():
                self.players[turn].start_finding_move(self.board)
                
            self.players[turn].stopped = False
            
            player_thread = Thread(target = start_move_fn)
            print "Player " + str(turn + 1) + ", go!"
            player_thread.start()
        
            # busy-wait until either the player reports that she/he is ready, or
            #   until maximum allowed time has elapsed
            
            total_time = 0.0
            while not self.players[turn].stopped and not window_closed():
                sleep(.05)
                total_time += .05
                
                if total_time > ALLOWED_TIME:
                    self.players[turn].stop()
                    print "  Time's up, player ", turn+1
           
           # let the recursion catch up 
            while not self.players[turn].finished:
                i=0
            
            # time is up, take the best move found so far
            move = self.players[turn].best_move
            print "move is " + str(move)
            print self.board
            
            # make the move, if it is legal
            if move is not None and self.board.is_legal(move):
                self.board.move(move)
                print "MOVED"
            else:
                print "Illegal move, player " + str(turn+1) + " forfeits turn."
                self.board.switch_turns()
                
            print self.board
            
            turn = (turn + 1) % 2
            win, winner, start, end = self.board.is_win()  
            
        # redraw everything
        clear()
        self.board.draw(OX, OY, CELLW, CELLH)
        request_redraw()
        print "Player " + str(winner) + " wins!"
        

class Player:
    def __init__(self):
        self.best_move = -1
        self.stopped = True
        self.finished = True
        self.depth_hit = -1
        self.visited = -1
        self.value = -1
                    
    def stop(self):
        self.stopped = True


class MousePlayer(Player):

    def start_finding_move(self, board):
        
        self.stopped = False
        self.best_move = -1
        
        # callback for mouse press
        def mouse_press():
            
            # compute the column of the click
            click_column = (mouse_x() - OX) / CELLW
    
            if board.is_legal(click_column):
                self.best_move = click_column
                self.stopped = True
                
        set_mouse_button_function(mouse_press)
        
        # busy-wait until stopped either by a selection or
        #  because allowed time has expired
        while not window_closed() and not self.stopped:
            sleep(.02)
            
        
class StupidAIPlayer(Player):
        
    def start_finding_move(self, board):
        self.stopped = False
        while not self.stopped:
            self.best_move = randint(0, 6)
            sleep(.05)
            
class SmartAIPlayer(Player):
    
    def start_finding_move(self, board):
        completed = False
        self.stopped = False
        self.finished = False
        depth = 1
        while not self.finished:
            #print depth
            #self.best_move = minimax_decisions(self, board, depth, board.turn)
            #best_move, depth_hit, visited, value, completed = minimax_decision(self, board, depth, board.turn)
            best_move, depth_hit, visited, value, completed = alpha_beta_search(self, board, depth, board.turn)
            
            # only records move from this if it completed the search at that depth
            if completed:
                self.best_move = best_move
                self.depth_hit = depth_hit
                self.visisted = visited
                self.value = value
            
            #print "best move: " + str(self.best_move)
            depth +=1
        
    
if __name__ == "__main__":
    player1 = SmartAIPlayer()
    #player1 = MousePlayer()
    player2 = MousePlayer()

    gui = ConnectFourGui(player1, player2)
    gui.start()
