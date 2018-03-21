"""game_agent.py Gert
Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
Verbose = False
Bugging = False


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

    # simple -> fast -> deep
    if game.is_loser(player):
        return float("-inf")
    elif game.is_winner(player):
        return float("inf")

    move_num = game.move_count

    oppo_mov = len(game.get_legal_moves(game.get_opponent(player)))
    if oppo_mov == 1:
        return float(50000 + move_num)
    elif oppo_mov == 2:
        return float(10000 + move_num)

    my_moves = len(game.get_legal_moves(player))
    if my_moves == 1:
        return float(-50000 - move_num)
    elif my_moves == 2:
        return float(-10000 - move_num)

    mov_diff_value = my_moves - (1.7 * oppo_mov)

    # we prefer to be in the center.. until we cannot
    cur_loc = game.get_player_location(player)
    if 1 <= cur_loc[0] <= game.height - 2 and 1 <= cur_loc[1] <= game.width - 2:
        cl_value = 1000
    else:
        cl_value = -1000

    return float(mov_diff_value * 2000) + cl_value + move_num * 5


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


    # mov#+centrloc
    if game.is_loser(player):
        return float("-inf")
    elif game.is_winner(player):
        return float("inf")

    blanks_count = [0, 0, 0, 0]
    height       = game.height
    width        = game.width
    center_h     = height//2
    center_w     = width//2

    # On the 8by8-Board Max is 16 blanks
    blankslist = game.get_blank_spaces()
    for loc in blankslist:
        if loc[0] <= center_h-1:
            if loc[1] <= center_w-1:
                blanks_count[0] += 1
            elif loc[1] >= width-center_w:
                blanks_count[1] += 1
        elif loc[0] >= height-center_h:
            if loc[1] <= center_w-1:
                blanks_count[2] += 1
            elif loc[1] >= width-center_w:
                blanks_count[3] += 1

    if Verbose or Bugging:
        print("blanks_count", blanks_count)

    # We want to move to the area with most blanks

    if cur_loc[0] <= center_h-1:
        if cur_loc[1] <= center_w-1:
            return float(blanks_count[0])
        elif cur_loc[1] >= width-center_w:
            return float(blanks_count[1])
    elif cur_loc[0] >= height-center_h:
        if cur_loc[1] <= center_w-1:
            return float(blanks_count[2])
        elif cur_loc[1] >= width-center_w:
            return float(blanks_count[3])

    # on odd boardsizes the rest are mid-board
    return float(5)


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

    # count +_diff
    if game.is_loser(player):
        return float("-inf")
    elif game.is_winner(player):
        return float("inf")

    # what it takes to be a winner - have the "highest move number"
    move_num = game.move_count

    # staying away from the edges - becomes ever more important. Hence multiplied by move_num
    cur_loc = game.get_player_location(player)
    # current location inside inner box
    if 1 <= cur_loc[0] <= game.height - 2 and 1 <= cur_loc[1] <= game.width - 2:
        cl_value = 100 + move_num
    else:
        # current location along the board edges
        cl_value = -100 - move_num

    # Is our next move going to take us to the Board.edge
    # thereby reducing the number of legal moves available
    # to us.
    # In the opening-moves, it is not a problem
    # that we move along the edge, but it
    # increasingly becomes a challenge.
    turn_effect = move_num                  # the "speed" of the effect based on move_num

    in_area      = []
    outside_area = []
    # how many next moves are in the center
    legal_list = game.get_legal_moves()
    for in_out in legal_list:
        if 1 <= in_out[0] <= game.height-2 and 1 <= in_out[1] <= game.width-2:
            in_area.append(in_out)         # could be 1-8
        else:
            outside_area.append(in_out)    # can only be 1-4

    in_val = len(in_area)*turn_effect                 # *  *1, *2, *3, *4 ...

    # the longer we play the game - the more -
    # we want to avoid having to risk getting "trapped" outside
    # out has -by far- the best score to start with -
    # after 15 turns - they switch - af 30 out goes negative
    out_val = len(outside_area)*(30-turn_effect)     #  *29, *28, *27, *26 ...

    state_value = cl_value + in_val * 20 + out_val + move_num

    return float(state_value)

def custom_score_4(game, player):
    # Here we retire the implemented ideas, that did not work
    # lets divide the board into 4 squares

    """
    :param game:
    :param player:
    :return: float(bl_multi)

    # blanks_count = [0, 0, 0, 0]
    # height       = game.height
    # width        = game.width
    # center_h     = height//2
    # center_w     = width//2
    #
    # # On the 8by8-Board Max is 16 blanks
    # blankslist = game.get_blank_spaces()
    # for loc in blankslist:
    #     if loc[0] <= center_h-1:
    #         if loc[1] <= center_w-1:
    #             blanks_count[0] += 1
    #         elif loc[1] >= width-center_w:
    #             blanks_count[1] += 1
    #     elif loc[0] >= height-center_h:
    #         if loc[1] <= center_w-1:
    #             blanks_count[2] += 1
    #         elif loc[1] >= width-center_w:
    #             blanks_count[3] += 1
    #
    # if Verbose or Bugging:
    #     print("blanks_count", blanks_count)
    #
    # # We want to move to the area with most blanks
    # bl_multi = 0
    # if cur_loc[0] <= center_h-1:
    #     if cur_loc[1] <= center_w-1:
    #         bl_multi = blanks_count[0]
    #     elif cur_loc[1] >= width-center_w:
    #         bl_multi = blanks_count[1]
    # elif cur_loc[0] >= height-center_h:
    #     if cur_loc[1] <= center_w-1:
    #         bl_multi = blanks_count[2]
    #     elif cur_loc[1] >= width-center_w:
    #         bl_multi = blanks_count[3]
    #
    # return float(bl_multi)
    """

    pass


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

        legal_list = game.get_legal_moves()
        if Verbose or Bugging:
            print("legal:", legal_list)

        if len(legal_list) == 0:
            return (-1, -1)
        elif len(legal_list) == 1:
            return legal_list[0]

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = legal_list[0]

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
        # minimax decision main
        self.time_test()

        legal_list = game.get_legal_moves()

        if len(legal_list) == 0:
            return (-1, -1)
        # init
        best_move = legal_list[0]

        best_score = float("-inf")

        # max(legal, min_value(state,depth)
        for m in legal_list:
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
        num_legal = len(legal_list)

        if Verbose or Bugging:
            print("legal_list:", legal_list)

        if num_legal == 0:
            return (-1, -1)
        elif num_legal == 1:
            return legal_list[0]

        # init
        best_move = legal_list[0]

        blanks_list = game.get_blank_spaces()

        # iterative deepening
        for depth in range(1, len(blanks_list)):
            try:
                best_move = self.alphabeta(game, depth)

            except SearchTimeout:
                return best_move
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
        Implement depth-limited minimax search with alpha-beta
        pruning as described in the lectures.

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

        max_branch, move = self.next_node(game, depth, alpha, beta, IsMax_value)

        return move

    def next_node(self, gameState, depth, alpha, beta, IsMax_value):
        self.time_test()
        legal_list = gameState.get_legal_moves()
        legal_moves = len(legal_list)

        if legal_moves == 0:
            if IsMax_value:
                return float("-inf"), (-1, -1)
            else:
                return float("inf"), (-1, -1)
        # init
        move_for_v = legal_list[0]

        if IsMax_value:
            v = float("-inf")
        else:
            v = float("inf")

        if self.terminal_test(gameState):
            if IsMax_value:
                return float("-inf"), move_for_v  # by assumption 2
            else:
                return float("inf"), move_for_v  # by assumption 2

        if depth == 0 or legal_moves == 1:
            if Verbose:
                print("move#:", gameState.move_count)
            return self.score(gameState, self), move_for_v

        for m in legal_list:
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
