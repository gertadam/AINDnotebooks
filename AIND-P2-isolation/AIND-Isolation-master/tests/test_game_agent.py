"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import timeit
TIME_LIMIT_MILLIS = 150

import isolation
import game_agent

from importlib import reload


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
        
        for i in range(50):
            move = self.game.active_player.get_move(self.game, time_left = lambda : 100000   )
            print(move)
            self.game.apply_move(move)
            print(self.game.print_board())
        
        
    def test_alphabeta(self):
        print("---------- testing alpha beta player ----------")
        self.player1 = game_agent.AlphaBetaPlayer()
        self.player2 = game_agent.AlphaBetaPlayer()
        self.game = isolation.Board(self.player1, self.player2, 8, 8)

            
        time_millis = lambda: 1000 * timeit.default_timer()

        print(self.game.print_board())
            
            
        for i in range(800):
            move_start = time_millis()
            time_left = lambda : TIME_LIMIT_MILLIS - (time_millis() - move_start)

            move = self.game.active_player.get_move(self.game, time_left )    
            print("i:", i, "_", move)
            self.game.apply_move(move)
            print(self.game.print_board())
            if move == (-1, -1):
                break


if __name__ == '__main__':
    unittest.main()
