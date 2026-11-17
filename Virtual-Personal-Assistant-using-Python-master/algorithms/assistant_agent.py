"""
Module: assistant_agent.py
IntelliAssist Intelligent Virtual Assistant Engine
Interprets user natural language queries, executes AI algorithms,
explains syllabus concepts, and provides interactive voice/text guidance.
"""

import re
import assistant_engine
from algorithms.knowledge_base import ALGORITHM_KNOWLEDGE
from algorithms.search_algorithms import depth_first_search, breadth_first_search, iterative_deepening_search
from algorithms.optimization_algorithms import simulated_annealing_tsp, hill_climbing
from algorithms.wumpus_world import WumpusWorld
from algorithms.eight_puzzle import solve_eight_puzzle
from algorithms.towers_of_hanoi import solve_towers_of_hanoi
from algorithms.informed_search import a_star_grid, d_star_dynamic_replan
from algorithms.bayesian_network import run_bayesian_network
from algorithms.em_algorithm import run_em_gmm
from algorithms.hidden_markov_model import run_hidden_markov_model


BOT_NAME = "IntelliAssist"

INTENT_MAP = {
    "dfs": ["dfs", "depth first search", "depth-first"],
    "bfs": ["bfs", "breadth first search", "breadth-first"],
    "ids": ["ids", "iterative deepening", "iddfs"],
    "simulated_annealing": ["simulated annealing", "annealing", "tsp optimization"],
    "wumpus_world": ["wumpus", "wumpus world"],
    "eight_puzzle": ["8 puzzle", "eight puzzle", "sliding tile"],
    "towers_of_hanoi": ["towers of hanoi", "hanoi", "tower of hanoi"],
    "a_star": ["a*", "a star", "a-star"],
    "d_star": ["d*", "d star", "d-star", "dynamic a*"],
    "hill_climbing": ["hill climbing", "hill climb", "local search"],
    "bayesian_network": ["bayesian network", "bayes net", "bbn", "rain sprinkler"],
    "em_algorithm": ["em algorithm", "expectation maximization", "gmm", "gaussian mixture"],
    "hidden_markov_model": ["hmm", "hidden markov", "viterbi", "markov model"]
}


def process_assistant_query(query_text):
    """
    Analyzes natural language query, detects intent, and either:
    1. Triggers algorithm execution with rich visualization payload.
    2. Explains an algorithm (definition, pseudocode, complexities, viva).
    3. Guides the user across syllabus modules.
    4. Responds to conversational greetings.
    """
    if not query_text or not query_text.strip():
        return {
            "text": "Hello! I am IntelliAssist. Ask me to run an algorithm, explain an AI concept, or solve a puzzle.",
            "category": "greeting",
            "action": None,
            "data": None
        }

    q = query_text.lower().strip()

    # Conversational Greetings & Identity (word-boundary matched to avoid substrings like 'hi' in 'delhi')
    if re.search(r'\b(hello|hi|hey|greetings|good morning|good evening|good afternoon)\b', q) and not any(cmd in q for cmd in ['weather', 'search', 'open', 'run', 'solve', 'calculate']):
        return {
            "text": f"Greetings! I am {BOT_NAME}, your AI Lab Virtual Assistant. I can demonstrate and explain all 13 classical AI algorithms from your syllabus, answer general knowledge questions, and launch system/web tools. Try saying 'Run BFS', 'Solve 8 puzzle', 'Explain A star', or ask any general question!",
            "category": "greeting",
            "action": None,
            "data": None
        }

    if any(k in q for k in ["how are you", "how are you doing", "how do you do"]):
        return {
            "text": "I am operating smoothly at peak efficiency, ready to demonstrate AI algorithms and assist you with anything you need!",
            "category": "conversation",
            "action": None,
            "data": None
        }

    if any(k in q for k in ["thank you", "thanks", "thank u"]):
        return {
            "text": "You are very welcome! Let me know if you would like to run another algorithm simulation or explore more AI theory.",
            "category": "conversation",
            "action": None,
            "data": None
        }

    if any(k in q for k in ["who made you", "who created you", "who developed you"]):
        return {
            "text": "I was developed for the B.Tech Artificial Intelligence Lab mini-project submission: 'IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms'.",
            "category": "about",
            "action": None,
            "data": None
        }

    if any(k in q for k in ["who are you", "what is your name", "your topic", "project title", "about project"]):
        return {
            "text": (
                "Project Title: 'IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms'. "
                "I am built for your B.Tech AI Lab mini-project to demonstrate 13 core algorithms across Search, "
                "Optimization, Classical Puzzles, and Probabilistic AI."
            ),
            "category": "about",
            "action": None,
            "data": {
                "title": "IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms",
                "total_algorithms": 13,
                "groups": ["Search Algorithms", "Classical AI Puzzles", "Informed Search", "Probabilistic AI"]
            }
        }

    if any(k in q for k in ["syllabus", "algorithms list", "what can you do", "help", "topics"]):
        return {
            "text": (
                "My syllabus covers 4 groups (13 algorithms):\n"
                "1. Search & Optimization: DFS, BFS, IDS, Simulated Annealing\n"
                "2. Classical AI Puzzles: Wumpus World, 8-Puzzle, Towers of Hanoi\n"
                "3. Informed Search: A*, D* Dynamic Replanning, Hill Climbing\n"
                "4. Probabilistic AI: Bayesian Network, EM Algorithm, Hidden Markov Model (HMM)."
            ),
            "category": "help",
            "action": None,
            "data": list(ALGORITHM_KNOWLEDGE.keys())
        }

    # Detect Algorithm Target
    detected_algo = None
    for algo_id, triggers in INTENT_MAP.items():
        if any(tr in q for tr in triggers):
            detected_algo = algo_id
            break

    # Check for Action: "Run" / "Solve" / "Start" vs "Explain" / "What is"
    is_run_action = any(k in q for k in ["run", "execute", "solve", "start", "open", "demonstrate", "visualize", "play", "show"])
    is_explain_action = any(k in q for k in ["explain", "what is", "definition", "how does", "pseudocode", "complexity", "viva", "theory"])

    if detected_algo:
        info = ALGORITHM_KNOWLEDGE[detected_algo]

        # If user explicitly wants execution OR default if they said "run/solve"
        if is_run_action and not is_explain_action:
            exec_res = execute_algorithm_by_id(detected_algo)
            return {
                "text": f"Executing {info['name']}. Results and interactive visualization are ready below!",
                "category": "algorithm_execution",
                "action": f"visualize_{detected_algo}",
                "algorithm_id": detected_algo,
                "algorithm_name": info["name"],
                "data": exec_res
            }
        else:
            # Explanation & Theory
            summary = (
                f"**{info['name']}**\n\n"
                f"• **Definition:** {info['definition']}\n\n"
                f"• **Principle:** {info['working_principle']}\n\n"
                f"• **Complexity:** Time: {info['time_complexity']} | Space: {info['space_complexity']}\n\n"
                f"Say 'Run {info['name']}' to see a live visual simulation!"
            )
            return {
                "text": summary,
                "category": "algorithm_explanation",
                "action": f"load_learning_{detected_algo}",
                "algorithm_id": detected_algo,
                "algorithm_name": info["name"],
                "data": info
            }

    # Seamless General Assistant & Direct Answer Engine (Answers EVERY question!)
    try:
        gen_res = assistant_engine.handle_command(query_text)
        return {
            "text": gen_res.get("text", "I am here to assist you."),
            "category": gen_res.get("category", "general"),
            "action": gen_res.get("action"),
            "data": gen_res.get("data")
        }
    except Exception as e:
        return {
            "text": f"I processed your request, but encountered: {str(e)}",
            "category": "error",
            "action": None,
            "data": None
        }


def execute_algorithm_by_id(algo_id, params=None):
    """Executes the requested algorithm with optional user parameters."""
    params = params or {}

    if algo_id == "dfs":
        start = params.get("start", "A")
        goal = params.get("goal", "J")
        return depth_first_search(start=start, goal=goal)

    elif algo_id == "bfs":
        start = params.get("start", "A")
        goal = params.get("goal", "J")
        return breadth_first_search(start=start, goal=goal)

    elif algo_id == "ids":
        start = params.get("start", "A")
        goal = params.get("goal", "J")
        max_depth = int(params.get("max_depth", 8))
        return iterative_deepening_search(start=start, goal=goal, max_depth=max_depth)

    elif algo_id == "simulated_annealing":
        initial_temp = float(params.get("initial_temp", 1000.0))
        cooling_rate = float(params.get("cooling_rate", 0.95))
        max_iter = int(params.get("max_iter", 300))
        return simulated_annealing_tsp(initial_temp=initial_temp, cooling_rate=cooling_rate, max_iter=max_iter)

    elif algo_id == "wumpus_world":
        ww = WumpusWorld()
        return ww.solve_autonomously(max_steps=20)

    elif algo_id == "eight_puzzle":
        board = params.get("board")
        heuristic = params.get("heuristic", "manhattan")
        return solve_eight_puzzle(initial_board=board, heuristic=heuristic)

    elif algo_id == "towers_of_hanoi":
        num_disks = int(params.get("num_disks", 3))
        return solve_towers_of_hanoi(num_disks=num_disks)

    elif algo_id == "a_star":
        heuristic = params.get("heuristic", "manhattan")
        return a_star_grid(heuristic_type=heuristic)

    elif algo_id == "d_star":
        dyn_cell = params.get("dynamic_cell", (5, 1))
        return d_star_dynamic_replan(dynamic_blocked_cell=dyn_cell)

    elif algo_id == "hill_climbing":
        start_x = float(params.get("start_x", 1.5))
        variant = params.get("variant", "steepest")
        return hill_climbing(start_x=start_x, variant=variant)

    elif algo_id == "bayesian_network":
        query_var = params.get("query_var", "Rain")
        evidence = params.get("evidence", {"WetGrass": True})
        return run_bayesian_network(query_var=query_var, evidence=evidence)

    elif algo_id == "em_algorithm":
        num_clusters = int(params.get("num_clusters", 2))
        return run_em_gmm(num_clusters=num_clusters, max_iter=25)

    elif algo_id == "hidden_markov_model":
        obs = params.get("observations", ["Walk", "Shop", "Clean"])
        return run_hidden_markov_model(obs_sequence=obs)

    return {"error": f"Unknown algorithm ID '{algo_id}'.", "success": False}
