# alphabeta

import copy, sys, random, gui
from board import *

visited = 0

# generic minimax functions

def alpha_beta_search(player, state, depth_limit, turn):
    completed = True
    global visited
    visited = 0
    
    alpha = -1 * sys.maxint
    beta = sys.maxint

    values = []
    actions = []
    depth = 0
    #print "turn" + str(turn)
    for a in state.legal_moves():
        state.move(a)
        visited += 1
        actions.append(a)
        values.append(min_value(player, state, depth, depth_limit, turn, alpha, beta))
        state.undo_move(a)
    
        #print "turn " + str(state.turn)
    
    if None in values: 
        completed = False
    
    max_value = max(values)
    i = values.index(max_value)
    
    if player.stopped:
        player.finished = True
    
    #print visited
    print "RETURN", actions[i]
    return actions[i], depth, visited, max_value, completed

def max_value(player, state, depth, depth_limit, turn, alpha, beta):

    if player.stopped:
        print "stopped"
        return None
    
    if cutoff_test(player, state, depth, depth_limit):
        return eval(state, turn)
    
    depth += 1
    
    value = -1 * sys.maxint
    for a in state.legal_moves():
        state.move(a) 
             
        global visited
        visited += 1 
        
        value = max((value, min_value(player, state, depth, depth_limit, turn, alpha, beta)))
        state.undo_move(a) 
        
        if value >= beta:
            return value
        alpha = max(alpha, value)
        
    return value

def min_value(player, state, depth, depth_limit, turn, alpha, beta):

    if player.stopped:
        print "stopped"
        return None
    
    if cutoff_test(player, state, depth, depth_limit):
        return eval(state, turn)
    
    depth +=1
    
    value = sys.maxint
    for a in state.legal_moves():
        
        global visited
        visited += 1
        
        state.move(a)
        value = min((value, max_value(player, state, depth, depth_limit, turn, alpha, beta))) 
        state.undo_move(a) 
        
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value
        
# minimax functions specific for this scenario:

def cutoff_test(player, state, depth, depth_limit):
    win, winner, x, y = state.is_win()
    return win or state.check_tie() or depth > depth_limit or player.stopped

def utility(state, turn):
    min = -1 * (sys.maxint)
    max = sys.maxint
    
    win, winner, start, end = state.is_win()
    if win:
        if winner == turn:
            return max
        else:
            return min 
    if state.check_tie():
        return 0
    return random.randint(min, max)

# evaluation of specific segment
def e(s, turn):
    #if it contains no disks or disks from both players return 0
    if (s[0] == s[1] == s[2] == s[3] == 0 or ((s[0] == 1 or s[1] == 1 or 
                                               s[2] == 1 or s[3] == 1) and 
        (s[0] == 2 or s[1] == 2 or s[2] == 2 or s[3] ==2))):
        return 0
    counter = 0
    # 100 if there are 3 of your disks, 10 if there are two, 1 if there is 1
    # sign depends on turn
    for piece in s: 
        if piece != 0:
            counter += 1
            if piece == turn:
                sign = 1
            else:
                sign = -1
            
    if counter == 3:
        return sign * 100
    if counter == 2: 
        return sign * 10
    return sign * counter

# if not a win state, returns the sum of e(segment) for all segments on board
# if win state, returns the normal utility function
def eval(state, turn):
    min = -1 * (sys.maxint)
    max = sys.maxint
    
    win, winner, start, end = state.is_win()
    if win:
        if winner == turn:
            return max
        else:
            return min 
    
    sum = 0
    
    # horizontal segments    
    for col in range(state.width - 3):
            for row in range(state.height):
                segment = [state.state[col][row], state.state[col+1][row], 
                           state.state[col+2][row], state.state[col+3][row]]
                sum += e(segment, turn)

    # vertical segments        
    for row in range(state.height - 3):
        for col in range(state.width):
            segment = [state.state[col][row], state.state[col][row+1], 
                       state.state[col][row+2], state.state[col][row+3]]
            sum += e(segment, turn)        
    
    # diagonal up segments    
    for col in range(state.width - 3):
            for row in range(state.height - 3):
                segment = [state.state[col][row], state.state[col+1][row+1], 
                           state.state[col+2][row+2], state.state[col+3][row+3]]
                sum += e(segment, turn)  
                
    # diagonal down segments    
    for col in range(state.width - 3):
            for row in range(3, state.height):
                segment = [state.state[col][row], state.state[col+1][row-1], 
                           state.state[col+2][row-2], state.state[col+3][row-3]]
                sum += e(segment, turn)  
    
    return sum  

# takes a state and returns the evaluation function for the red player
def eval_c4(state): 
    return eval(state, 1)

if __name__ == "__main__":
    state = Board()
    print eval_c4(state)
    
    state.move(1) #red
    state.move(1) #black
    state.move(2) #red
    state.move(3)
    print state
    print "value:", eval_c4(state)
    
    print ""
    
    
    
    
    
                
                 
        
