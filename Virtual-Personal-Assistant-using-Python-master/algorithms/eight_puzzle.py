"""
Module: eight_puzzle.py
Implements:
8-Puzzle Solver using A* Search with Manhattan Distance Heuristic.
Includes Inversion Count Solvability Verification.
"""

import heapq
import time

GOAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

GOAL_POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}


def to_tuple(board):
    """Converts 2D list or 1D list to standard immutable tuple of tuples."""
    if isinstance(board[0], (list, tuple)):
        return tuple(tuple(row) for row in board)
    return (
        tuple(board[0:3]),
        tuple(board[3:6]),
        tuple(board[6:9])
    )


def count_inversions(flat_board):
    """
    Counts tile inversions excluding the blank space (0).
    A standard 8-puzzle configuration is solvable iff inversion count is EVEN.
    """
    tiles = [x for x in flat_board if x != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions


def is_solvable(board):
    flat = [tile for row in to_tuple(board) for tile in row]
    inv = count_inversions(flat)
    return (inv % 2 == 0), inv


def manhattan_distance(board):
    """Computes total Manhattan distance heuristic h(n)."""
    dist = 0
    for r in range(3):
        for c in range(3):
            val = board[r][c]
            if val != 0:
                goal_r, goal_c = GOAL_POSITIONS[val]
                dist += abs(r - goal_r) + abs(c - goal_c)
    return dist


def misplaced_tiles(board):
    """Computes count of misplaced tiles heuristic."""
    count = 0
    for r in range(3):
        for c in range(3):
            val = board[r][c]
            if val != 0 and val != GOAL_STATE[r][c]:
                count += 1
    return count


def get_neighbors(board):
    """Generates valid sliding tile moves."""
    # Find blank tile (0)
    blank_r, blank_c = 0, 0
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                blank_r, blank_c = r, c
                break

    moves = []
    directions = [
        (-1, 0, "UP"),
        (1, 0, "DOWN"),
        (0, -1, "LEFT"),
        (0, 1, "RIGHT")
    ]

    for dr, dc, move_name in directions:
        nr, nc = blank_r + dr, blank_c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_board = [list(row) for row in board]
            new_board[blank_r][blank_c], new_board[nr][nc] = new_board[nr][nc], new_board[blank_r][blank_c]
            moves.append((to_tuple(new_board), move_name))

    return moves


def solve_eight_puzzle(initial_board=None, heuristic="manhattan", max_nodes=5000):
    """
    Solves 8-Puzzle using A* Search.
    Verifies solvability upfront to prevent infinite loops on impossible inputs.
    """
    start_time = time.perf_counter()

    if initial_board is None:
        # Default interesting solvable puzzle (5 moves away)
        initial_board = (
            (1, 2, 3),
            (4, 0, 6),
            (7, 5, 8)
        )
    else:
        initial_board = to_tuple(initial_board)

    solvable, inv_count = is_solvable(initial_board)
    if not solvable:
        return {
            "success": False,
            "error": "The given puzzle configuration is mathematically UNSOLVABLE (Odd number of inversions).",
            "inversion_count": inv_count,
            "initial_board": [list(r) for r in initial_board],
            "goal_board": [list(r) for r in GOAL_STATE]
        }

    h_func = manhattan_distance if heuristic == "manhattan" else misplaced_tiles

    h0 = h_func(initial_board)
    # Priority Queue: (f_score, tiebreaker_id, g_score, current_board, path_states, moves)
    pq = []
    tiebreaker = 0
    heapq.heappush(pq, (h0, tiebreaker, 0, initial_board, [initial_board], []))

    visited_costs = {initial_board: 0}
    nodes_explored = 0

    solution_path = None
    solution_moves = None

    while pq and nodes_explored < max_nodes:
        f, _, g, current, path, moves = heapq.heappop(pq)
        nodes_explored += 1

        if current == GOAL_STATE:
            solution_path = path
            solution_moves = moves
            break

        if g > visited_costs.get(current, float('inf')):
            continue

        for neighbor_board, move_name in get_neighbors(current):
            new_g = g + 1
            if new_g < visited_costs.get(neighbor_board, float('inf')):
                visited_costs[neighbor_board] = new_g
                h = h_func(neighbor_board)
                tiebreaker += 1
                heapq.heappush(
                    pq,
                    (new_g + h, tiebreaker, new_g, neighbor_board, path + [neighbor_board], moves + [move_name])
                )

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    if solution_path:
        formatted_steps = []
        for idx, (board_state, move) in enumerate(zip(solution_path, ["START"] + solution_moves)):
            formatted_steps.append({
                "step": idx,
                "move": move,
                "board": [list(r) for r in board_state],
                "manhattan_dist": manhattan_distance(board_state)
            })

        return {
            "success": True,
            "algorithm": f"A* 8-Puzzle Solver ({heuristic.title()} Heuristic)",
            "solvable": True,
            "inversion_count": inv_count,
            "total_moves": len(solution_moves),
            "nodes_explored": nodes_explored,
            "moves": solution_moves,
            "steps": formatted_steps,
            "execution_time_ms": elapsed_ms
        }
    else:
        return {
            "success": False,
            "error": "Max node exploration threshold exceeded.",
            "nodes_explored": nodes_explored,
            "execution_time_ms": elapsed_ms
        }
