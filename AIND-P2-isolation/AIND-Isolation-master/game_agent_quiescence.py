"""game_agent.py Gert
Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
#from numba import jit
Verbose = False


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # move_diff score
    oppo_mov = len(game.get_legal_moves(game.get_opponent(player)))
    my_moves = len(game.get_legal_moves(player))

    if oppo_mov == 0:
        return float("inf")
    if my_moves == 0:
        return float("-inf")

    if oppo_mov == 1:
        return float(5000)
    if my_moves == 1:
        return float(-5000)

    if oppo_mov == 2:
        return float(500)
    if my_moves == 2:
        return float(-500)

    move_diff = (my_moves - 1.6 * oppo_mov) * 20

    return float(move_diff)



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # Combined_score
    # @jit(parallel=True)
    # @jit(nopython=True, parallel=True)  # broke the function
    def find_blanks(loc_list1, blanks_list):
        spaces_in_area = []

        # we want to be in the area with many blanks
        for x in loc_list1:
            boxsize = 2
            min_r = x[0] - boxsize
            min_c = x[1] - boxsize
            max_r = x[0] + boxsize
            max_c = x[1] + boxsize

            #  blanks in box can be up to 25 - 8 pos moves 8*25 up to 200spaces
            for blank in blanks_list:
                if min_r <= blank[0] <= max_r and min_c <= blank[1] <= max_c:
                    spaces_in_area.append(blank)

        return len(spaces_in_area)

    p_loc = game.get_player_location(player)
    legal_list1 = game.get_legal_moves()
    blanks_list = game.get_blank_spaces()

    legal_list1.append(p_loc)
    num_blanks = find_blanks(legal_list1, blanks_list)

    if 1 <= p_loc[0] <= game.height - 2 and 1 <= p_loc[1] <= game.width - 2:
        cl_value = 2000
    else:
        cl_value = -2000

    # moves can tally up to 8
    oppo_mov = float(len(game.get_legal_moves(game.get_opponent(player))))
    my_moves = len(game.get_legal_moves(player))
    if oppo_mov == 0:
        return float("inf")
    if my_moves == 0:
        return float("-inf")

    if oppo_mov == 1:
        return float(10000)
    if my_moves == 1:
        return float(-10000)

    if oppo_mov == 2:
        return float(5000)
    if my_moves == 2:
        return float(-5000)

    in_box = num_blanks * 20
    mov_diff = ((my_moves - 1.6 * oppo_mov) * 500)
    value = in_box + cl_value + mov_diff

    return float(value)

    # comparing values * multiplicators
    # in_box                 values        2  -   400
    # cl_value               values   (-2000) - (2000)
    #
    # we subtract oppo_mov so in most cases there will be only a difference of 1-3
    # mov_diff               values   (-1500) - (1500)

    """ I have fiddled about with the values and their multiplicators
        I come up with different evaluation-ideas tried them out induvidually
        and tested them against this combined score
        even though this combined score is very much slower (offcourse) 
        (- 8% off the overall runtime compared to 4% for score -)
        it still ocationally performs better than "move_diff score"
        I therefore changed the tournament.py:
        - to play 50 games (a 100 games in total pr opponent) (takes 2 hours on my machine) 
        when playing 100 games "move_diff score" is better
        
        I tried to order the value given an observed gamestate feature
        in such a way the the player would be guided clearly
        My conclusions were:
            my venture into the box idea was a so-so 
            - a real high num_blanks will count overall, hence positions with many blanks should be preferred
            my attempt at "keeping my player from straying toward the Edge" - was not effective, I guess
            
            this combined score does not constitute a better evaluation function !

    """



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # in_or_out score
    blanks_list = game.get_blank_spaces()
    # counting up towards the final conclusion
    turn = (game.height*game.width)-len(blanks_list)
    turn_effect = turn * 0.1       # how much effect

    # keep inside the middle
    cur_loc = game.get_player_location(player)
    if 1 <= cur_loc[0] <= game.height-2 and 1 <= cur_loc[1] <= game.width-2:
        cl_value=100
    else:
        cl_value=-100


    in_area      = []
    outside_area = []
    # how many next moves are in the center
    legal_list = game.get_legal_moves()
    for in_out in legal_list:
        if 1 <= in_out[0] <= game.height-2 and 1 <= in_out[1] <= game.width-2:
            in_area.append(in_out)         # could be 1-8
        else:
            outside_area.append(in_out)    # can only be 1-4

    in_val  = len(in_area)*turn_effect            # *  0.1 0.2 0.3 0.4 0.5 0.6

    # the longer we play the move we want to avoid getting "trapped" outside
    out_val = len(outside_area)*(1-turn_effect)   # *  0.9 0.8 0.7 0.6 0.5 0.4

    return float(cl_value+in_val+out_val)



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal = game.get_legal_moves()
        if Verbose:
            print("legal:", legal)

        if len(legal) == 0:
            return (-1, -1)
        #init
        best_move = legal[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        #minimax decision main
        self.time_test()

        legal = game.get_legal_moves()

        if len(legal) == 0:
            return (-1, -1)
        #init
        best_move = legal[0]

        best_score = float("-inf")

        # max(legal, min_value(state,depth)
        for m in legal:
            v = self.min_value(game.forecast_move(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
        return best_move

    def min_value(self, gameState, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        self.time_test()

        if self.terminal_test(gameState):
            return float("inf")  # by assumption 2

        v = float("inf")
        if depth == 0:
            return self.score(gameState, self)

        for m in gameState.get_legal_moves():
            v = min(v, self.max_value(gameState.forecast_move(m), depth - 1))
        return v

    def max_value(self, gameState, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        self.time_test()

        if self.terminal_test(gameState):
            return float("-inf")  # by assumption 2

        v = float("-inf")
        if depth == 0:
            return self.score(gameState, self)
        else:
            for m in gameState.get_legal_moves():
                v = max(v, self.min_value(gameState.forecast_move(m), depth - 1))
            return v

    def terminal_test(self, gamestate):
        moves_available = bool(gamestate.get_legal_moves())  # by Assumption 1
        return not moves_available

    def time_test(self):
        if (self.time_left() < self.TIMER_THRESHOLD):
            if Verbose:
                print("Timeout")
            raise SearchTimeout()


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        legal = game.get_legal_moves()
        if Verbose:
            print("legal:", legal)

        if len(legal) == 0:
            return (-1, -1)

        best_move = legal[0]

        blanks_list = game.get_blank_spaces()

        # Not able to submit -the udacity tester Fails when I use this
        # max_player_moves = len(blanks_list)/2

        # Not able to submit -the udacity tester Fails when I use this
        # let's assume that: the same returning best_move at 24 consecutive depth is enough for quiescence
        bm = [(99, 99)]
        initvalue = 99 - 1
        initloc = (initvalue, initvalue)
        # the first element is already in
        for i in range(23):
            bm.append(initloc)
            initvalue -= 1
            initloc = (initvalue, initvalue)

        quiescent_range = 24

        #iterative deepening
        for depth in range(1, len(blanks_list)):
            try:
                best_move = self.alphabeta(game, depth)

                # Not able to submit -the udacity tester Fails when I use this
                # recording the last 24 best_moves
                if quiescent_range == 24:
                    quiescent_range = 0
                bm[quiescent_range] = best_move
                quiescent_range += 1

                # are they alike ?
                Alike=True
                for i in range(24):
                    if best_move != bm[i]:
                        Alike=False

                # quiescence, 24 consecutive
                if Alike:
                    if Verbose:
                        print("quiescence", bm)
                    return best_move

            except SearchTimeout:
                return best_move
        return best_move

#    @jit(nopython=True, parallel=True)
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.time_test()

        # The top level nodes are a Max
        # initializations
        IsMax_value = True

        # Not able to submit -the udacity tester Fails when I use this
        # Extended_depth = False
        # max_branch, move = self.next_node(game, depth, alpha, beta, IsMax_value, Extended_depth)

        max_branch, move = self.next_node(game, depth, alpha, beta, IsMax_value)

        return move



    # @jit(nopython=True, parallel=True)
    # Not able to submit -the udacity tester Fails when I use this
    # def next_node(self, gameState, depth, alpha, beta, IsMax_value, Extended_depth):

    def next_node(self, gameState, depth, alpha, beta, IsMax_value):
        legal = gameState.get_legal_moves()
        legal_moves = len(legal)
        self.time_test()

        # Not able to submit -the udacity tester Fails when I use this
        #if Verbose:
        #    if depth == 3:
        #        print("depth3 - legal:", legal_moves)
        #    if Extended_depth:
        #        print("Extended")

        #if (legal_moves == 3) and (depth == 3) and (not Extended_depth):
        #    depth = 6
        #    Extended_depth = True
        #    if Verbose:
        #        print("Extended")

        if legal_moves == 0:
            if IsMax_value:
                return float("-inf"), (-1, -1)
            else:
                return float("inf"), (-1, -1)
        #init
        move_for_v = legal[0]

        if IsMax_value:
            v = float("-inf")
        else:
            v = float("inf")

        if self.terminal_test(gameState):
            if IsMax_value:
                return float("-inf"), move_for_v  # by assumption 2
            else:
                return float("inf"), move_for_v   # by assumption 2

        if depth == 0:
            return self.score(gameState, self), move_for_v

        for m in legal:
            # Not able to submit -the udacity tester Fails when I use this
            #node_value, node_move = self.next_node(gameState.forecast_move(m), depth - 1, alpha, beta, not IsMax_value, Extended_depth)

            node_value, node_move = self.next_node(gameState.forecast_move(m), depth - 1, alpha, beta, not IsMax_value)

            if IsMax_value:
                if node_value > v:
                    v = node_value
                    move_for_v = m

                if (v >= beta):
                    return v, move_for_v
                alpha = max(alpha, v)

            else:
                if node_value < v:
                    v = node_value
                    move_for_v = m

                if (v <= alpha):
                    return v, move_for_v
                beta = min(beta, v)

        return v, move_for_v



    def terminal_test(self, gamestate):
        moves_available = bool(gamestate.get_legal_moves())  # by Assumption 1
        return not moves_available

    def time_test(self):
        if (self.time_left() < self.TIMER_THRESHOLD):
            if Verbose:
                print("Timeout")
            raise SearchTimeout()

