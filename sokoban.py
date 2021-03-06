#! /usr/bin/env python

import copy
from sys import exit
from itertools import chain
# Sokoban player

# Design inspired by stop writing class presentation

# level are defined in a file, in a "self evident" format where each char is a case
# on the map and are  represented by one of the following symbole
# using this format http://sokobano.de/wiki/index.php?title=Level_format
FREE = ' ' # free space
CRATE = '$'
OBJECTIVE = '.'
CRATE_ON_OBJECTIVE = '*'
WALL = '#'
PLAYER = '@'
PLAYER_ON_OBJECTIVE = '+'

# x is top to bottom, y is left to right
MOVES = {
    'n': (-1, 0),
    'e': (0, 1),
    's': (1, 0),
    'w': (0, -1),
}

def load_level(fname):
    """Load a level from a properly formated file, return a matrix

    Assume a proper level file, like not two player"""
    lines = open(fname).readlines()
    lines = [list(l.strip('\n')) for l in lines if not l.startswith(';')]
    return lines

def get_player_pos(level):
    """Let's be real it's not worth caching this"""
    for i, line in enumerate(level):
        for j, value in enumerate(line):
            if value in (PLAYER, PLAYER_ON_OBJECTIVE):
                return (i,j)

def print_level(level):
    for line in level:
        print ''.join(line)

def print_history(history):
    for cmd, level in history:
        print_level(level)
        raw_input('press enter to continue')


def is_free(level, x, y):
    return level[x][y] in (OBJECTIVE, FREE)


def has_won(level):
    """If there is no more crate or empty objective on the map we have won"""
    return all([case not in (CRATE, OBJECTIVE) for case in chain(*level)])


def copy_level(level):
    return copy.deepcopy(level)


def move(level, dx, dy):
    """Move player, return new board if move is permitted, false otherwhise"""
    old_x, old_y = get_player_pos(level)
    x, y = old_x + dx, old_y + dy
    level = copy_level(level)
    # check if we have a crate to move
    if level[x][y] in (CRATE, CRATE_ON_OBJECTIVE):
        if not is_free(level, x + dx, y + dy):
            return False
        if level[x][y] == CRATE_ON_OBJECTIVE:
            level[x][y] = OBJECTIVE
        else:
            level[x][y] = FREE
        if level[x + dx][y + dy] == OBJECTIVE:
            level[x + dx][y + dy] = CRATE_ON_OBJECTIVE
        else:
            level[x + dx][y + dy] = CRATE

    # once we have eventually moved the crate check if player can move
    if not is_free(level, x, y):
        return False

    if level[old_x][old_y] == PLAYER_ON_OBJECTIVE:
        level[old_x][old_y] = OBJECTIVE
    else:
        level[old_x][old_y] = FREE
    if level[x][y] == OBJECTIVE:
        level[x][y] = PLAYER_ON_OBJECTIVE
    else:
        level[x][y] = PLAYER
    return level


def backtrack(history):
    """Really slow non optimal sokoban resolver"""
    # print ''.join([c for (c,l) in history])
    cmd, level = history[-1]
    if has_won(level):
        return history

    if level in (l for (c,l) in history[:-1]):
        # Already explored
        return None

    for c, (dx, dy) in MOVES.items():
        r = move(level, dx, dy)
        if r:
            history.append((c,r))
            # h =  backtrack(history + [(c,r)])
            h =  backtrack(history)
            if h:
                return h
            history.pop()
    return None


def main(level_name):
    history = [('init', load_level(level_name))]
    undo = 0
    while not has_won(history[-1][1]):
        print_level(history[-1][1])
        print 'Move done', len(history) -1
        print 
        print 'Enter your move (N, E, S, W), u to undo or q to exit'
        cmd = raw_input('? ').lower()
        if cmd  == 'q':
            exit()
        elif cmd in MOVES.keys():
            dx, dy = MOVES[cmd]
            r =  move(history[-1][1], dx, dy)
            if r is False:
                print '!!!! Invalid move'
            else:
                history.append((cmd, r))
        elif cmd == 'h':
            print 'printing history'
            print_history(history)
            continue
        elif cmd == 'b':
            soluce = backtrack([('i', history[-1][1])])
            if soluce:
                print_history(soluce)
            continue
        elif cmd == 'u':
            print ' ====  Undoing last move.'
            if len(history) > 1:
                history.pop()
                undo += 1
            else:
                print 'Initial level'
            continue
        else:
            print ' ==== Unkown command'
            continue


    if has_won(history[-1][1]):
        print 'You won !'
        print 'You have used %s move' % (len(history) -1)
        print 'Moves :', ''.join([h[0] for h in history[1:]])
        if undo:
            print 'And %s' % undo

if __name__ == '__main__':
    import sys
    level = sys.argv[1] if len(sys.argv) > 1 else 'level00.sok'
    main(level)
