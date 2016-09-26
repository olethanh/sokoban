from sokoban import has_won, move, is_free
import sokoban

WON_LEVEL = """
##########
####@   ##
##       #
##    ####
##** #####
##########
"""
INIT_LEVEL = """
##########
####@   ##
##  $$   #
##    ####
##.. #####
##########
"""


MOVE = """
##########
####  @ ##
##  $$   #
##    ####
##.. #####
##########
"""

def load_from_string(s):
    lines = s.split('\n')
    lines = [list(l) for l in lines if l]
    return lines

def test_has_won_ok():
    l = load_from_string(WON_LEVEL)
    assert has_won(l) == True


def test_has_won_fail():
    l = load_from_string(INIT_LEVEL)
    assert has_won(l) == False

def test_is_free():
    l = load_from_string(INIT_LEVEL)
    assert is_free(l, 0, 0) == False
    assert is_free(l, 2, 2) == True

def test_move_ok():
    l = load_from_string(MOVE)
    assert move(l, 0, 1) != False

def test_move_CRATE():
    l = load_from_string( """
##########
####@   ##
##  $$   #
##    ####
##.. #####
##########
""")
    after = load_from_string("""
##########
####    ##
##  @$   #
##  $ ####
##.. #####
##########
""")
    #sokoban.print_level(move(l, 1, 0))
    #sokoban.print_level(after)
    assert move(l, 1, 0) == after

def test_move_TWO_CRATE():
    before = load_from_string( """
##########
####    ##
##  $$@  #
##    ####
##.. #####
##########
""")
    assert move(before, 0, -1) == False

def test_move_CRATE_obj():
    before = load_from_string( """
##########
####    ##
## @ $   #
## $  ####
##.. #####
##########
""")
    after = load_from_string("""
##########
####    ##
##   $   #
## @  ####
##.* #####
##########
""")
    sokoban.print_level(move(before, 1, 0))
    sokoban.print_level(after)
    assert move(before, 1, 0) == after

def test_move_PLAYER_OBJ():
    before = load_from_string( """
@.
""")
    after = load_from_string("""
 +
""")
    sokoban.print_level(move(before, 0, 1))
    sokoban.print_level(after)
    assert move(before, 0, 1) == after

def test_move_PLAYER_OUT_OBJ():
    before = load_from_string( """
 +
""")
    after = load_from_string("""
@.
""")
    sokoban.print_level(move(before, 0, -1))
    sokoban.print_level(after)
    assert move(before, 0, -1) == after

def test_backtrack():
   init = load_from_string("""
        ########
        ###@   #
        ##. $  #
        ########
    """)
   res = sokoban.backtrack([('i', init)])
   assert isinstance(res, list)
   assert len(res) <= 12 # initial result not very optimised

def test_backtrack_uninishable():
   init = load_from_string("""
        #####
        #$@.#
        #   #
        #####
    """)
   res = sokoban.backtrack([('i', init)])
   assert res is None

def test_crash():
    before = load_from_string("""
        ##########
        ####    ##
        ##    $@ #
        ##    ####
        ##*. #####
        ##########
    """)
    after = load_from_string("""
        ##########
        ####    ##
        ##   $@  #
        ##    ####
        ##*. #####
        ##########
    """)
    sokoban.print_level(move(before, 0, -1))
    assert move(before, 0, -1) == after

