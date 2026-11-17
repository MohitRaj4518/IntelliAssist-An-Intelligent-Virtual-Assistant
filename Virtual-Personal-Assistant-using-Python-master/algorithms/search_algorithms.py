"""
Module: search_algorithms.py
Implements:
1. Depth First Search (DFS)
2. Breadth First Search (BFS)
3. Iterative Deepening Search (IDS)
"""

import time
from collections import deque


DEFAULT_GRAPH = {
    'A': [('B', 1), ('C', 2)],
    'B': [('A', 1), ('D', 3), ('E', 1)],
    'C': [('A', 2), ('F', 2), ('G', 4)],
    'D': [('B', 3), ('H', 2)],
    'E': [('B', 1), ('I', 3), ('J', 2)],
    'F': [('C', 2), ('K', 1)],
    'G': [('C', 4), ('L', 2)],
    'H': [('D', 2)],
    'I': [('E', 3)],
    'J': [('E', 2)],
    'K': [('F', 1)],
    'L': [('G', 2)]
}

DEFAULT_GRAPH_SIMPLE = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B', 'H'],
    'E': ['B', 'I', 'J'],
    'F': ['C', 'K'],
    'G': ['C', 'L'],
    'H': ['D'],
    'I': ['E'],
    'J': ['E'],
    'K': ['F'],
    'L': ['G']
}


def normalize_graph(graph=None):
    """Ensures graph has edge weights: node -> list of (neighbor, weight)."""
    if not graph:
        return DEFAULT_GRAPH
    normalized = {}
    for node, neighbors in graph.items():
        norm_neighbors = []
        for n in neighbors:
            if isinstance(n, (list, tuple)):
                norm_neighbors.append((str(n[0]), float(n[1])))
            else:
                norm_neighbors.append((str(n), 1.0))
        normalized[str(node)] = norm_neighbors
    return normalized


def depth_first_search(graph=None, start='A', goal='J'):
    """
    Executes Depth First Search (DFS).
    Uses an explicit stack and maintains full exploration trace.
    """
    start_time = time.perf_counter()
    g = normalize_graph(graph)

    if start not in g:
        return {"error": f"Start node '{start}' not in graph.", "success": False}
    if goal not in g:
        return {"error": f"Goal node '{goal}' not in graph.", "success": False}

    stack = [(start, [start], 0.0)]
    visited = set()
    traversal_order = []
    steps = []
    found_path = None
    final_cost = 0.0

    while stack:
        current, path, cost = stack.pop()

        if current not in visited:
            visited.add(current)
            traversal_order.append(current)

            steps.append({
                "step": len(traversal_order),
                "action": f"Visited node '{current}'",
                "current": current,
                "path_so_far": list(path),
                "stack": [item[0] for item in stack],
                "visited": list(traversal_order)
            })

            if current == goal:
                found_path = path
                final_cost = cost
                break

            # Add neighbors in reverse to visit in natural alphabetical order
            neighbors = g.get(current, [])
            for neighbor, weight in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], cost + weight))

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": found_path is not None,
        "algorithm": "Depth First Search (DFS)",
        "start": start,
        "goal": goal,
        "path": found_path if found_path else [],
        "traversal_order": traversal_order,
        "visited_count": len(visited),
        "path_cost": final_cost,
        "path_length": len(found_path) if found_path else 0,
        "execution_time_ms": elapsed_ms,
        "steps": steps,
        "graph": {k: [n[0] for n in v] for k, v in g.items()}
    }


def breadth_first_search(graph=None, start='A', goal='J'):
    """
    Executes Breadth First Search (BFS).
    Uses a FIFO queue to explore nodes level-by-level, finding the shortest edge-count path.
    """
    start_time = time.perf_counter()
    g = normalize_graph(graph)

    if start not in g:
        return {"error": f"Start node '{start}' not in graph.", "success": False}
    if goal not in g:
        return {"error": f"Goal node '{goal}' not in graph.", "success": False}

    queue = deque([(start, [start], 0.0)])
    visited = {start}
    traversal_order = []
    steps = []
    found_path = None
    final_cost = 0.0

    while queue:
        current, path, cost = queue.popleft()
        traversal_order.append(current)

        steps.append({
            "step": len(traversal_order),
            "action": f"Expanded node '{current}'",
            "current": current,
            "path_so_far": list(path),
            "queue": [item[0] for item in queue],
            "visited": list(traversal_order)
        })

        if current == goal:
            found_path = path
            final_cost = cost
            break

        neighbors = g.get(current, [])
        for neighbor, weight in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], cost + weight))

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": found_path is not None,
        "algorithm": "Breadth First Search (BFS)",
        "start": start,
        "goal": goal,
        "path": found_path if found_path else [],
        "traversal_order": traversal_order,
        "visited_count": len(traversal_order),
        "path_cost": final_cost,
        "path_length": len(found_path) if found_path else 0,
        "execution_time_ms": elapsed_ms,
        "steps": steps,
        "graph": {k: [n[0] for n in v] for k, v in g.items()}
    }


def iterative_deepening_search(graph=None, start='A', goal='J', max_depth=10):
    """
    Executes Iterative Deepening Search (IDS / IDDFS).
    Repeatedly applies Depth-Limited Search (DLS) with increasing depth limits.
    Combines BFS's optimality (for unweighted) with DFS's space efficiency.
    """
    start_time = time.perf_counter()
    g = normalize_graph(graph)

    if start not in g:
        return {"error": f"Start node '{start}' not in graph.", "success": False}
    if goal not in g:
        return {"error": f"Goal node '{goal}' not in graph.", "success": False}

    overall_traversal = []
    depth_iterations = []
    found_path = None
    final_cost = 0.0

    for depth_limit in range(max_depth + 1):
        iter_visited = []
        iter_steps = []

        def dls(current, path, cost, current_depth):
            nonlocal found_path, final_cost
            iter_visited.append(current)
            overall_traversal.append(current)

            iter_steps.append({
                "depth": current_depth,
                "node": current,
                "path": list(path)
            })

            if current == goal:
                found_path = path
                final_cost = cost
                return True

            if current_depth >= depth_limit:
                return False

            neighbors = g.get(current, [])
            for neighbor, weight in neighbors:
                if neighbor not in path:  # avoid cycles along current branch
                    if dls(neighbor, path + [neighbor], cost + weight, current_depth + 1):
                        return True
            return False

        goal_found = dls(start, [start], 0.0, 0)

        depth_iterations.append({
            "depth_limit": depth_limit,
            "nodes_visited": list(iter_visited),
            "visited_count": len(iter_visited),
            "goal_found": goal_found
        })

        if goal_found:
            break

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": found_path is not None,
        "algorithm": "Iterative Deepening Search (IDS)",
        "start": start,
        "goal": goal,
        "depth_reached": len(depth_iterations) - 1,
        "path": found_path if found_path else [],
        "traversal_order": overall_traversal,
        "total_nodes_expanded": len(overall_traversal),
        "path_cost": final_cost,
        "path_length": len(found_path) if found_path else 0,
        "depth_iterations": depth_iterations,
        "execution_time_ms": elapsed_ms,
        "graph": {k: [n[0] for n in v] for k, v in g.items()}
    }
