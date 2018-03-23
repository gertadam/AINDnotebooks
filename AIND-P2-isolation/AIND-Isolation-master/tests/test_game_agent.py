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


TIME_LIMIT_MILLIS = 150

Verbose = False

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = game_agent.MinimaxPlayer()
        self.game = isolation.Board(self.player1, self.player2, 8, 8)

    def _test_minimax(self):
        print("---------- testing min max player ----------")
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = game_agent.MinimaxPlayer()
        
        for i in range(75):
            move = self.game.active_player.get_move(self.game, time_left = lambda : 100000   )
            print(move)
            self.game.apply_move(move)
            print(self.game.print_board())
        
        
    def test_alphabeta(self):

        lost = [0,0]

        for y in range(100):
            print("---------- testing alpha beta player (",y,")----------")
            self.player1 = game_agent.AlphaBetaPlayer(score_fn=custom_score_2)
            self.player2 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
            self.game = isolation.Board(self.player1, self.player2, 8, 8)

            time_millis = lambda: 1000 * timeit.default_timer()

            if Verbose:
                print(self.game.print_board())
            move = 0, 0

            for i in range(800):
                move_start = time_millis()
                time_left = lambda : TIME_LIMIT_MILLIS - (time_millis() - move_start)

                move = self.game.active_player.get_move(self.game, time_left )
                if self.game.is_loser(self.game.active_player):
                    if self.game.active_player == self.player1:
                        lost[0] += 1
                    else:
                        lost[1] += 1
                    print(lost)

                self.game.apply_move(move)
                if Verbose:
                    print("i:", i, "_", move)
                    print(self.game.print_board())
                if move == (-1, -1):
                    print("dead-end ")
                    move = 0, 0
                    break

        for x in range(2):
            print ("lost:",lost[x])

if __name__ == '__main__':
    unittest.main()
