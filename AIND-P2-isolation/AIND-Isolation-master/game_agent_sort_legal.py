"""game_agent.py Gert
Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
#from numba import jit
Verbose = True


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

    mov_diff = ((my_moves - 1.6 * oppo_mov) * 1000)
    value = cl_value + mov_diff

    # comparing values * multiplicators
    # cl_value               values   (-2000) - (2000)
    #
    # we subtract oppo_mov
    # - (in most cases there will be only a difference of 1-3)
    # mov_diff               values   (-6000) - (6000)

    return float(value)


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
        legal_list = game.get_legal_moves()
        if Verbose:
            print("legal_list:", legal_list)

        if len(legal_list) == 0:
            return (-1, -1)

        #init
        best_move = legal_list[0]

        blanks_list = game.get_blank_spaces()

        # Not able to submit -the udacity tester Fails when I use this
        # max_player_moves = len(blanks_list)/2

        #iterative deepening
        for depth in range(1, len(blanks_list)):
            try:
                best_move = self.alphabeta(game, depth)

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

        def sort_legal_list(legal_list, blanks_list):
            # we want to be in an area with many blanks, so look at them first
            self.time_test()
            tmp_legal_list = []
            loc_blanks = []
            values_written_list = []
            for loc in legal_list:
                blanks_in_box = []
                boxsize = 2
                min_r = loc[0] - boxsize
                min_c = loc[1] - boxsize
                max_r = loc[0] + boxsize
                max_c = loc[1] + boxsize
                for blank in blanks_list:
                    if min_r <= blank[0] <= max_r and min_c <= blank[1] <= max_c:
                        blanks_in_box.append(blank)
                # loc_blanks 0 - 24
                loc_blanks.append(len(blanks_in_box))
            if Verbose :
                    print("loc_blanks", loc_blanks)
            for counter in range(len(loc_blanks)):
                if Verbose:
                    print("for counter in range counter-1:", counter)
                    print("for counter in range len(tmp_legal_list):", len(tmp_legal_list))
                    print("for counter in range legal_list[counter]:", legal_list[counter])
                    print("for counter in range loc_blanks[counter]:", loc_blanks[counter])
                if len(tmp_legal_list) == 0:
                    tmp_legal_list.append(legal_list[counter])
                    values_written_list.append(loc_blanks[counter])
                else:
                    #first element in enumerate is 0
                    max_z = len(tmp_legal_list)
                    if Verbose:
                        print("else: tmp_legal_list:", tmp_legal_list)
                        print("else: values_written_list:", values_written_list)
                        print("else: max_z:", max_z)

                    for z in range(max_z):
                        if Verbose:
                            print("efter for, tmp_legal_list:", tmp_legal_list)
                            print("efter for, values_written_list:", values_written_list)
                            print("efter for, max_z:", max_z)
                            print("efter for, z:", z)
                        if z == max_z:
                            tmp_legal_list.append(legal_list[counter])
                            values_written_list.append(loc_blanks[counter])
                            if Verbose:
                                print("if z+1 == max_z: tmp_legal_list:", tmp_legal_list)
                                print("if z+1 == max_z: values_written_list:", values_written_list)
                                print("if z+1 == max_z: max_z:", max_z)
                                print("if z+1 == max_z: z:", z)
                        elif values_written_list[z] <= loc_blanks[counter]:
                            tmp_legal_list.insert(z, legal_list[counter])
                            values_written_list.insert(z, loc_blanks[counter])
                        if Verbose:
                            print("elif values_written_list[z] tmp_legal_list:", tmp_legal_list)
                            print("elif values_written_list[z] values_written_list:", values_written_list)
                            print("elif values_written_list[z] max_z:", max_z)
                            print("elif values_written_list[z] z:", z)
                    if Verbose:
                        print("tmp_legal_list:", tmp_legal_list)
                        print("values_written_list:", values_written_list)
                        print("max_z:", max_z)

                if Verbose:
                    print("values_written_list", values_written_list)
                    print("tmp_legal_list:", tmp_legal_list)
                if Verbose:
                    print("tmp_legal_list:", tmp_legal_list)
                    print("values_written_list:", values_written_list)


            return tmp_legal_list

        blanks_list = gameState.get_blank_spaces()
        legal_list = gameState.get_legal_moves()
        legal_moves = len(legal_list)
        if Verbose:
            print("legal_moves:", legal_moves)

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

        if (1 < legal_moves < 9):
            if Verbose:
                print("1-8legal_list:", legal_list )
            legal_list = sort_legal_list(legal_list, blanks_list)

        #init
        move_for_v = legal_list[0]

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

        for m in legal_list:
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

