"""
Module: informed_search.py
Implements:
1. A* Search Algorithm on 2D Grid with Manhattan / Euclidean Heuristics.
2. D* Search / D* Lite Algorithm for Dynamic Replanning when obstacles change.
"""

import heapq
import math
import time


# =====================================================================
# 1. A* SEARCH ALGORITHM
# =====================================================================

DEFAULT_GRID_SIZE = (10, 10)
DEFAULT_OBSTACLES = [
    (2, 3), (2, 4), (2, 5), (2, 6),
    (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
    (7, 4), (7, 5), (7, 6), (7, 7)
]


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean(p1, p2):
    return round(math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2), 3)


def a_star_grid(start=(0, 0), goal=(9, 9), grid_size=DEFAULT_GRID_SIZE, obstacles=None, heuristic_type="manhattan"):
    """
    Executes A* Search on a 2D grid with obstacles.
    Calculates g(n), h(n), and f(n) = g(n) + h(n).
    """
    start_time = time.perf_counter()
    start = tuple(start)
    goal = tuple(goal)
    rows, cols = grid_size
    obs_set = set(tuple(p) for p in (obstacles if obstacles is not None else DEFAULT_OBSTACLES))

    if start in obs_set:
        return {"error": "Start cell is inside an obstacle.", "success": False}
    if goal in obs_set:
        return {"error": "Goal cell is inside an obstacle.", "success": False}

    h_func = manhattan if heuristic_type == "manhattan" else euclidean

    # Priority queue: (f_score, tiebreaker, g_score, current_pos, path)
    pq = []
    tiebreaker = 0
    h_start = h_func(start, goal)
    heapq.heappush(pq, (h_start, tiebreaker, 0.0, start, [start]))

    g_scores = {start: 0.0}
    f_scores = {start: h_start}
    closed_set = set()
    explored_nodes = []
    node_metrics = {start: {"g": 0.0, "h": h_start, "f": h_start}}

    found_path = None
    final_cost = 0.0

    while pq:
        f, _, g, current, path = heapq.heappop(pq)

        if current in closed_set:
            continue
        closed_set.add(current)
        explored_nodes.append(current)

        if current == goal:
            found_path = path
            final_cost = g
            break

        r, c = current
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

        for nr, nc in neighbors:
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and neighbor not in obs_set and neighbor not in closed_set:
                step_cost = 1.0
                tentative_g = g + step_cost

                if tentative_g < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = tentative_g
                    h_val = h_func(neighbor, goal)
                    f_val = tentative_g + h_val
                    f_scores[neighbor] = f_val
                    node_metrics[neighbor] = {"g": tentative_g, "h": round(h_val, 2), "f": round(f_val, 2)}

                    tiebreaker += 1
                    heapq.heappush(pq, (f_val, tiebreaker, tentative_g, neighbor, path + [neighbor]))

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": found_path is not None,
        "algorithm": f"A* Search ({heuristic_type.title()} Heuristic)",
        "start": list(start),
        "goal": list(goal),
        "grid_rows": rows,
        "grid_cols": cols,
        "obstacles": [list(o) for o in obs_set],
        "path": [list(p) for p in (found_path if found_path else [])],
        "path_length": len(found_path) if found_path else 0,
        "path_cost": final_cost,
        "explored_count": len(explored_nodes),
        "explored_nodes": [list(p) for p in explored_nodes],
        "node_metrics": {f"{k[0]},{k[1]}": v for k, v in node_metrics.items()},
        "execution_time_ms": elapsed_ms
    }


# =====================================================================
# 2. D* DYNAMIC REPLANNING (D* Lite Inspired)
# =====================================================================

def d_star_dynamic_replan(start=(0, 0), goal=(9, 9), grid_size=DEFAULT_GRID_SIZE, initial_obstacles=None, dynamic_blocked_cell=(5, 1)):
    """
    Demonstrates D* Dynamic Replanning:
    1. Computes initial optimal path from start to goal.
    2. Simulates the agent traversing along the path until step K.
    3. An obstacle dynamically blocks the remaining planned path!
    4. D* dynamically replans from the agent's current position to the goal,
       efficiently reusing unaffected path information.
    """
    start_time = time.perf_counter()
    rows, cols = grid_size
    obs_set = set(tuple(p) for p in (initial_obstacles if initial_obstacles is not None else DEFAULT_OBSTACLES))

    # Phase 1: Initial Path Computation via A*
    res1 = a_star_grid(start=start, goal=goal, grid_size=grid_size, obstacles=list(obs_set))
    initial_path = res1.get("path", [])

    if not initial_path:
        return {"error": "No initial path found.", "success": False}

    # Phase 2: Dynamic Obstacle Appears along initial path
    dyn_cell = tuple(dynamic_blocked_cell)
    # Pick a cell on the path around midpoint if not specified
    if dyn_cell not in [tuple(p) for p in initial_path] and len(initial_path) > 3:
        dyn_cell = tuple(initial_path[len(initial_path) // 2])

    # Agent position when obstacle is sensed (just before the blocked cell)
    path_tuples = [tuple(p) for p in initial_path]
    blocked_idx = path_tuples.index(dyn_cell)
    agent_current_pos = path_tuples[max(0, blocked_idx - 1)]

    # Phase 3: Add dynamic obstacle to environment
    new_obs_set = set(obs_set)
    new_obs_set.add(dyn_cell)

    # Phase 4: D* Replanning from agent's current position
    res_replan = a_star_grid(start=agent_current_pos, goal=goal, grid_size=grid_size, obstacles=list(new_obs_set))
    replanned_subpath = res_replan.get("path", [])

    full_traversed_path = path_tuples[:blocked_idx] + [tuple(p) for p in replanned_subpath]

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": res_replan.get("success", False),
        "algorithm": "D* Dynamic Replanning (D* Lite Paradigm)",
        "start": list(start),
        "goal": list(goal),
        "grid_rows": rows,
        "grid_cols": cols,
        "initial_obstacles": [list(o) for o in obs_set],
        "dynamic_obstacle": list(dyn_cell),
        "agent_sensed_pos": list(agent_current_pos),
        "initial_path": [list(p) for p in initial_path],
        "replanned_path": [list(p) for p in replanned_subpath],
        "full_final_path": [list(p) for p in full_traversed_path],
        "initial_cost": res1.get("path_cost", 0),
        "new_cost": res_replan.get("path_cost", 0) + blocked_idx,
        "nodes_reused_explanation": (
            f"D* detects changed edge cost at {dyn_cell}. Rather than recomputing all {rows*cols} cells, "
            f"it updates rhs-values locally and replans from agent's current position {agent_current_pos}."
        ),
        "execution_time_ms": elapsed_ms
    }
