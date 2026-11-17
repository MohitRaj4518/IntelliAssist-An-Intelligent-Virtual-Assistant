"""
Unit Test Suite for IntelliAssist AI Algorithms
Validates all 13 AI algorithms across edge cases and typical inputs.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.search_algorithms import depth_first_search, breadth_first_search, iterative_deepening_search
from algorithms.optimization_algorithms import simulated_annealing_tsp, hill_climbing
from algorithms.wumpus_world import WumpusWorld
from algorithms.eight_puzzle import solve_eight_puzzle, is_solvable
from algorithms.towers_of_hanoi import solve_towers_of_hanoi
from algorithms.informed_search import a_star_grid, d_star_dynamic_replan
from algorithms.bayesian_network import run_bayesian_network, BayesianNetwork
from algorithms.em_algorithm import run_em_gmm
from algorithms.hidden_markov_model import run_hidden_markov_model, HiddenMarkovModel


class TestSearchAlgorithms(unittest.TestCase):
    def test_dfs(self):
        res = depth_first_search(start='A', goal='J')
        self.assertTrue(res['success'])
        self.assertEqual(res['path'][0], 'A')
        self.assertEqual(res['path'][-1], 'J')

    def test_bfs(self):
        res = breadth_first_search(start='A', goal='J')
        self.assertTrue(res['success'])
        self.assertEqual(res['path'][0], 'A')
        self.assertEqual(res['path'][-1], 'J')

    def test_ids(self):
        res = iterative_deepening_search(start='A', goal='J', max_depth=6)
        self.assertTrue(res['success'])
        self.assertEqual(res['path'][0], 'A')
        self.assertEqual(res['path'][-1], 'J')


class TestOptimizationAlgorithms(unittest.TestCase):
    def test_simulated_annealing(self):
        res = simulated_annealing_tsp(initial_temp=500.0, cooling_rate=0.90, stopping_temp=1.0, max_iter=100)
        self.assertTrue(res['success'])
        self.assertLessEqual(res['best_cost'], res['initial_cost'])

    def test_hill_climbing(self):
        res = hill_climbing(start_x=1.5, variant="steepest")
        self.assertTrue(res['success'])
        self.assertIn("steps", res)


class TestClassicalAIPuzzles(unittest.TestCase):
    def test_wumpus_world(self):
        ww = WumpusWorld()
        res = ww.solve_autonomously(max_steps=15)
        self.assertIn("steps", res)
        self.assertGreater(len(res['steps']), 0)

    def test_eight_puzzle_solvability(self):
        solvable_board = ((1, 2, 3), (4, 0, 6), (7, 5, 8))
        solvable, _ = is_solvable(solvable_board)
        self.assertTrue(solvable)

        res = solve_eight_puzzle(solvable_board)
        self.assertTrue(res['success'])
        self.assertGreaterEqual(res['total_moves'], 0)

    def test_eight_puzzle_unsolvable(self):
        unsolvable_board = ((1, 2, 3), (4, 5, 6), (8, 7, 0))
        solvable, _ = is_solvable(unsolvable_board)
        self.assertFalse(solvable)

        res = solve_eight_puzzle(unsolvable_board)
        self.assertFalse(res['success'])
        self.assertIn("UNSOLVABLE", res['error'])

    def test_towers_of_hanoi(self):
        for n in [3, 4, 5]:
            res = solve_towers_of_hanoi(num_disks=n)
            self.assertEqual(res['total_moves'], (2 ** n) - 1)


class TestInformedSearch(unittest.TestCase):
    def test_a_star_grid(self):
        res = a_star_grid(start=(0, 0), goal=(9, 9))
        self.assertTrue(res['success'])
        self.assertEqual(res['path'][0], [0, 0])
        self.assertEqual(res['path'][-1], [9, 9])

    def test_d_star_replanning(self):
        res = d_star_dynamic_replan(start=(0, 0), goal=(9, 9))
        self.assertTrue(res['success'])
        self.assertIn("dynamic_obstacle", res)


class TestProbabilisticAI(unittest.TestCase):
    def test_bayesian_network(self):
        bn = BayesianNetwork()
        res = bn.query_posterior("Rain", {"WetGrass": True})
        self.assertTrue(res['success'])
        # In Rain/Sprinkler/WetGrass standard model, P(Rain=True | WetGrass=True) ~ 0.7079
        self.assertAlmostEqual(res['posterior_probabilities']['True'], 0.7079, places=2)

    def test_em_algorithm(self):
        res = run_em_gmm(num_clusters=2, num_samples=80, max_iter=15)
        self.assertTrue(res['success'])
        self.assertEqual(len(res['final_parameters']['means']), 2)

    def test_hidden_markov_model(self):
        res = run_hidden_markov_model(['Walk', 'Shop', 'Clean'])
        self.assertTrue(res['success'])
        self.assertEqual(len(res['viterbi_decoding']['most_likely_states']), 3)
        self.assertGreater(res['forward_evaluation']['total_observation_probability'], 0.0)


class TestVirtualAssistant(unittest.TestCase):
    def test_assistant_algorithm_execution(self):
        from algorithms.assistant_agent import process_assistant_query
        res = process_assistant_query("Run BFS")
        self.assertEqual(res["category"], "algorithm_execution")
        self.assertEqual(res["action"], "visualize_bfs")

    def test_assistant_algorithm_theory(self):
        from algorithms.assistant_agent import process_assistant_query
        res = process_assistant_query("Explain A star")
        self.assertEqual(res["category"], "algorithm_explanation")
        self.assertEqual(res["action"], "load_learning_a_star")

    def test_assistant_direct_factual_answer(self):
        from algorithms.assistant_agent import process_assistant_query
        res = process_assistant_query("Who is Albert Einstein")
        self.assertEqual(res["category"], "answer")
        self.assertIn("Einstein", res["text"])

    def test_assistant_math_evaluation(self):
        from algorithms.assistant_agent import process_assistant_query
        res = process_assistant_query("What is 25 * 4")
        self.assertEqual(res["category"], "answer")
        self.assertIn("100", res["text"])

    def test_assistant_chrome_launcher(self):
        from algorithms.assistant_agent import process_assistant_query
        res = process_assistant_query("Open Github")
        self.assertEqual(res["action"], "open_url")
        self.assertIn("github.com", res["data"]["url"])


if __name__ == '__main__':
    unittest.main()
