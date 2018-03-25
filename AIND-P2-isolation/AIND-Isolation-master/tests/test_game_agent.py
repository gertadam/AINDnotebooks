"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""
from importlib import reload
from sample_players import (GreedyPlayer, RandomPlayer, open_move_score,
                            improved_score, center_score)

from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)

import game_agent
import isolation
import unittest
import timeit

# gert adam test_gam_agent.py

#
# iteratools
# combinations score_fn_list * score_fn_list
#
# list comprehensions
# resultlist=[[[play_match(first, second) for num_matches in range(100)]
#               (if not (first == second)) for second in scorelist] for first in score_fn_list]


TIME_LIMIT_MILLIS = 150

Verbose = False
Boxes   = False
height  = 8
width   = 8

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = game_agent.MinimaxPlayer()
        self.game = isolation.Board(self.player1, self.player2, height, width)

    def _test_minimax(self):
        print("---------- testing min max player ----------")
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = game_agent.MinimaxPlayer()
        
        for i in range(75):
            move = self.game.active_player.get_move(self.game, time_left = lambda : 100000)
            print(move)
            self.game.apply_move(move)
            print(self.game.print_board())
        
        
    def test_alphabeta(self):
        #
        global lost
        global player_lost
        MATCHES = 25
        #
        def play_match(first, second):
            print("*************************** *************************** *************************** ", "\n")
            print(" --------------- ", first, " versus ", second, " ---------------- ", "\n")
            print("\n")
            print("---------------- testing alpha beta player(", num_matches, ") -------------------------", "\n")
            print("*************************** *************************** *************************** ", "\n")
            self.player1 = game_agent.AlphaBetaPlayer(first)
            self.player2 = game_agent.AlphaBetaPlayer(second)
            self.game = isolation.Board(self.player1, self.player2, height, width)

            time_millis = lambda: 1000 * timeit.default_timer()

            if Verbose or Boxes:
                print(self.game.print_board())

            for i in range(800):
                move_start = time_millis()
                time_left = lambda: TIME_LIMIT_MILLIS - (time_millis() - move_start)

                move = self.game.active_player.get_move(self.game, time_left)
                if self.game.is_loser(self.game.active_player):
                    if self.game.active_player == self.player1:
                        lost[0] += 1
                    else:
                        lost[1] += 1
                    print("test_game.. lost:", lost)
                    # if move == (-1, -1): must be the same as "is_loser"
                    print("*************************** *************************** ", "\n")
                    print("                   dead-end reached ", "\n")
                    print("*************************** *************************** ", "\n")
                    break
                else:
                    self.game.apply_move(move)
                    if Verbose or Boxes:
                        print("i:", i, "_", move, "\n")
                        print(self.game.print_board(), "\n")
            for x in range(2):
                print ("lost:", lost[x], "\n")
            print("*************************** *************************** *************************** ")
            print("player_lost:", player_lost)
            print("*************************** *************************** *************************** ", "\n")

        def play_Greedy(first):
            print("*************************** *************************** *************************** ", "\n")
            print(" --------------- ", first, " versus improved-Greedy ---------------- ", "\n")
            print("\n")
            print("---------------- testing alpha beta player(", num_matches, ") -------------------------", "\n")
            print("*************************** *************************** *************************** ", "\n")
            self.player1 = game_agent.AlphaBetaPlayer(first)
            self.player2 = GreedyPlayer()
            self.game = isolation.Board(self.player1, self.player2, height, width)

            time_millis = lambda: 1000 * timeit.default_timer()

            if Verbose or Boxes:
                print(self.game.print_board())

            for i in range(800):
                move_start = time_millis()
                time_left = lambda: TIME_LIMIT_MILLIS - (time_millis() - move_start)

                move = self.game.active_player.get_move(self.game, time_left)
                if self.game.is_loser(self.game.active_player):
                    if self.game.active_player == self.player1:
                        lost[0] += 1
                    else:
                        lost[1] += 1
                    print("test_game.. lost:", lost)
                    # if move == (-1, -1): must be the same as "is_loser"
                    print("*************************** *************************** ", "\n")
                    print("                   dead-end reached ", "\n")
                    print("*************************** *************************** ", "\n")
                    break
                else:
                    self.game.apply_move(move)
                    if Verbose or Boxes:
                        print("i:", i, "_", move, "\n")
                        print(self.game.print_board(), "\n")
            for x in range(2):
                print ("lost:", lost[x], "\n")
            print("*************************** *************************** *************************** ")
            print("player_lost:", player_lost)
            print("*************************** *************************** *************************** ", "\n")

        # Main
        score_fn_list = ["score_fn=custom_score", "score_fn=custom_score_2", "score_fn=custom_score_3", "score_fn=improved_score"]
        lost = [0, 0]
        player_lost = [0, 0, 0, 0]
        for idx, first in enumerate(score_fn_list):
            for second in score_fn_list:

                # if not (first == second):     # matches all (incl. against yourself)
                                                # x matches as first - x as second
                                                # first plays all from above + greedy with improved eval func

                for num_matches in range(MATCHES):
                    play_match(first, second)
                player_lost[idx] += lost[0]
                lost = [0, 0]
            for num_matches in range(MATCHES):
                play_Greedy(first)
            player_lost[idx] += lost[0]
            lost = [0, 0]

if __name__ == '__main__':
    unittest.main()
