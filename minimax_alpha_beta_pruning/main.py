from util import INFINITY


# 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 0

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 0

# 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

# This section will contain occasional lines that you can uncomment to play
# the game interactively. Be sure to re-comment them when you're done with
# them.  Please don't turn in a problem set that sits there asking the
# grader-bot to play a game!
##
# Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

# Uncomment this line to play a game as black:
#run_game(basic_player, human_player)
#run_game(basic_player, human_player)

# Or watch the computer play against itself:
#run_game(basic_player, basic_player)

# Change this evaluation function so that it tries to win as soon as possible,
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

#run_game(random_player, human_player)



def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    raise NotImplementedError


# Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

# You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

# Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.
##
# You can use minimax() in basicplayer.py as an example.


def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    if is_terminal_fn(depth, board):
        return eval_fn(board, board.get_current_player_id())
    else:
        import time
        expanded = 1
        tic = time.clock()
        ret = alpha_beta_max(board,depth,eval_fn,get_next_moves_fn,is_terminal_fn)
        toc = time.clock()
        timeItr = toc - tic
        expanded = expanded + ret[2]
        print "Nodes Expanded: " + str(expanded)
        print "Execution Time: " + str(timeItr)
        return ret[0],expanded,timeItr

def alpha_beta_max(board,depth,eval_fn,get_next_moves_fn,is_terminal_fn,alpha=None,beta=None,last_col=-1):
    if is_terminal_fn(depth, board):
        return (None,eval_fn(board, board.get_current_player_id(), last_col), 0)

    max = None
    col_slct = None
    expanded = 0
    for col, new_board in get_next_moves_fn(board):
        (tmp, node_val, ret_exp) = alpha_beta_min( new_board, depth-1,eval_fn,get_next_moves_fn,is_terminal_fn, alpha, beta, col)
        expanded = expanded + 1 + ret_exp
        if max == None or node_val > max:
            max = node_val
            col_slct = col
        if beta != None and beta <= max:
            return (col_slct,max, expanded)
        if alpha == None or max > alpha:
            alpha = max
    return (col_slct, max, expanded)

def alpha_beta_min(board,depth,eval_fn,get_next_moves_fn,is_terminal_fn,alpha=None,beta=None, last_col=-1):
    if is_terminal_fn(depth, board):
        return (None,eval_fn(board, board.get_other_player_id(), last_col), 0)
    min = None
    col_slct = None
    expanded = 0
    for col, new_board in get_next_moves_fn(board):
        (tmp, node_val, ret_exp) = alpha_beta_max( new_board, depth-1,eval_fn,get_next_moves_fn,is_terminal_fn, alpha, beta,col)
        expanded = expanded + 1 + ret_exp
        if min == None or node_val < min:
            min = node_val
            col_slct = col
        if alpha != None and alpha >= min:
            return (col_slct,min, expanded)
        if beta == None or min < beta:
            beta = min
    return (col_slct, min, expanded)


# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined
# alpha-beta-search.)
# alphabeta_player = lambda board: alpha_beta_search(board,
#                                                   depth=8,
#                                                   eval_fn=focused_evaluate)
alphabeta_player = lambda board: alpha_beta_search(
    board, depth=4, eval_fn=new_evaluate)

alphabeta_longest_player = lambda board: alpha_beta_search(
    board, depth=4, eval_fn=new_longest_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

# Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the
# same depth.

# def better_evaluate(board):
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = ((0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 2, 2, 1, 1, 2, 0),
                    (0, 2, 1, 2, 1, 2, 0),
                    (2, 1, 2, 1, 1, 1, 0),
                    )
    test_board_1 = ConnectFourBoard(board_array=board_tuples,
                                    current_player=1)
    test_board_2 = ConnectFourBoard(board_array=board_tuples,
                                    current_player=2)
    # better evaluate from player 1
    print "%s => %s" % (test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" % (test_board_2, better_evaluate(test_board_2))

# A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

# your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

# Uncomment to watch your player play a game:
#run_game(your_player, your_player)

# Uncomment this (or run it in the command window) to see how you do
# on the tournament that will be graded.
#run_game(your_player, basic_player)

# These three functions are used by the tester; please don't modify them!


def run_test_game(player1, player2, board):
    assert isinstance(globals()[
                      board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])


def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[
                      board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

# This function runs your alpha-beta implementation using a tree as the search
# rather than a live connect four game.   This will be easier to debug.


def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)

# Do you want us to use your code in a tournament against other students? See
# the description in the problem set. The tournament is completely optional
# and has no effect on your grade.
COMPETE = (None)

# The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""


print "uncomment lines in lab3.py, below line 253 to select a test case"
#Question1:
#run_game(basic_player, human_player)
#run_game(basic_player, basic_player)

#Question2:
#run_game(new_player, basic_player)

#Question3:
#run_game(alphabeta_player,basic_player)

#Question4.1:
#run_game(alphabeta_player, human_player, ConnectFourBoard(5))

#Question4.2:
run_longest_streak(basic_longest_player, alphabeta_longest_player,ConnectLongestBoard(20))
