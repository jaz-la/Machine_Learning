from util import memoize, run_search_function
import time

def basic_evaluate(board, player_id, col):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified.
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass


def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


def minimax(board, depth, eval_fn=basic_evaluate,
            get_next_moves_fn=get_all_next_moves,
            is_terminal_fn=is_terminal,
            verbose=True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    expanded = 1
    # if is_terminal_fn(depth, board):
    #     print "terminated"
    #     return eval_fn(board, board.get_current_player_id())
    # else:
    tic = time.clock()
    ret = max_node_value(board,depth,eval_fn,get_next_moves_fn,is_terminal_fn, -1)
    toc = time.clock()
    timeItr = toc - tic
    expanded = expanded + ret[2]
    print "Nodes Expanded: " + str(expanded)
    print "Execution Time: " + str(timeItr)
    return ret[0],expanded,timeItr

def max_node_value(board,depth,eval_fn,get_next_moves_fn,is_terminal_fn, last_col):
    if is_terminal_fn(depth, board):
        return (None,eval_fn(board, board.get_current_player_id(), last_col), 0)
    max = None
    col_slct = None
    expanded = 0
    for col, new_board in get_next_moves_fn(board):
        (tmp, node_val, ret_exp) = min_node_value( new_board, depth-1,eval_fn,get_next_moves_fn,is_terminal_fn, col)
        expanded = expanded + 1 + ret_exp
        if max == None or node_val > max:
            max = node_val
            col_slct = col
    return (col_slct, max, expanded)

def min_node_value(board,depth,eval_fn,get_next_moves_fn,is_terminal_fn, last_col):
    if is_terminal_fn(depth, board):
        return (None,eval_fn(board, board.get_other_player_id(), last_col), 0)
    min = None
    col_slct = None
    expanded = 0
    for col, new_board in get_next_moves_fn(board):
        (tmp, node_val, ret_exp) = max_node_value( new_board, depth-1,eval_fn,get_next_moves_fn,is_terminal_fn, col)
        expanded = expanded + 1 + ret_exp
        if min == None or node_val < min:
            min = node_val
            col_slct = col
    return (col_slct, min, expanded)


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


def new_evaluate(board,player_id, col):
    winner_id = board.is_win()
    if winner_id != 0:
        if winner_id == player_id:
            return 1000
        else:
            score = -1000
    else:
        if col >= 0 and board.get_height_of_column(col) >=1:
            if board.do_move(col).do_move(col).is_game_over():
                return -1000
        score = board.longest_chain(board.get_current_player_id()) * 10
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)

    return score

def new_longest_evaluate(board,player_id, col):
    score = board.longest_chain(board.get_current_player_id()) * 10
    return score

def basic_longest_evaluate(board, player_id,col):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified.
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)

    return score

random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)

basic_longest_player = lambda board: minimax(board, depth=4, eval_fn=basic_longest_evaluate)
new_longest_player = lambda board: minimax(board, depth=4, eval_fn=new_longest_evaluate)


progressive_deepening_player = lambda board: run_search_function(
    board, search_fn=minimax, eval_fn=basic_evaluate)
