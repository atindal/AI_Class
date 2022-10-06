from select import select
from sys import maxunicode
from telnetlib import theNULL
from environments.connect_four import ConnectFourState, ConnectFour
import numpy as np

#def get_most_in_row(arr):
#    highest = -1
#
#    counter = 0
#    currentSlot = 0
#
#    for slot in arr:
#        if slot == currentSlot:
#            counter = counter + 1
#        elif slot != currentSlot:
#            counter = 1
#        
#        if counter > highest:
#            highest = counter
#
#    return highest

def get_min_offset(arr):
    string = ""
    for v in arr:
        if v == -1: 
            string = string + 'a'
        elif v == 0: 
            string = string + 'b'
        elif v == 1: 
            string = string + 'c'
    
    #case1 = "baa"
    #case2 = "aab"
    case3 = "baaa"
    case4 = "aaab"

    print(string)
    if case3 in string or case4 in string:
        print("found 3 in a row + 0")
        return -10000000000 # NEVER pick this state! this state

    #if case1 in string or case2 in string:
    #    print("found 2 in a row + 0")
    #    return -1000000
    
    return 0


def hasEmptySlot(arr):
    for value in arr:
        if value == 0:
            return True

    return False

def heuristic(state: ConnectFourState, env) -> float:
    if env.is_terminal(state):
        return 100000000
    
    lines = state.get_lines()

    heuristic = 0

    for line in lines:
        #if len(line) > 3 and hasEmptySlot(line):
            heuristic = heuristic + get_min_offset(line)
           

    return heuristic

def max_value(state: ConnectFourState, env: ConnectFour, maxDepth: int, currDepth: int):
    print("max_value", currDepth)
    if env.is_terminal(state):
        return env.utility(state), None

    v = -10000000000000000000
    move = None

    if currDepth < maxDepth:
        for action in env.get_actions(state):
            v2, a2 = min_value(env.next_state(state, action), env, maxDepth, currDepth)
            if v2 > v:
                v=v2
                move = action
        return v, move
    else:
        bestValue = -10000000000000000000
        selectedMove = None

        heuristics = []

        for action in env.get_actions(state):
            value = heuristic(env.next_state(state, action), env)
            heuristics.append([value, action])
            move = action

            print("heuristic:", action, value)

            if value > bestValue:
                bestValue = value
                selectedMove = move

        print("final heuristics:")
        print(heuristics)
        print("selected heuristic:", bestValue, selectedMove)
        return bestValue, selectedMove

def min_value(state: ConnectFourState, env: ConnectFour, maxDepth: int, currDepth: int):
    if env.is_terminal(state):
        return env.utility(state), None

    v = 10000000000000000000
    move = None

    for action in env.get_actions(state):
        v2, a2 = max_value(env.next_state(state, action), env, maxDepth, currDepth+1)

        if currDepth < maxDepth:
            if v2 < v:
                v=v2
                move = action
    
            return v, move
        else:
            return v2, a2


def heuristic_minimax_search(state: ConnectFourState, env: ConnectFour, maxDepth: int) -> int:
    value, move = max_value(state, env, maxDepth, 0)
    return move

