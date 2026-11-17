"""
Module: optimization_algorithms.py
Implements:
1. Simulated Annealing (Traveling Salesperson Problem & Continuous Multi-modal Landscape)
2. Hill Climbing (Simple, Steepest Ascent, and Random-Restart with Local Maxima / Plateau detection)
"""

import math
import random
import time


# =====================================================================
# 1. SIMULATED ANNEALING
# =====================================================================

DEFAULT_TSP_CITIES = {
    'A': (60, 200),
    'B': (180, 200),
    'C': (80, 180),
    'D': (140, 180),
    'E': (20, 160),
    'F': (100, 160),
    'G': (200, 160),
    'H': (140, 140),
    'I': (40, 120),
    'J': (100, 120)
}


def euclidean_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def calculate_tsp_tour_cost(tour, cities):
    total = 0.0
    n = len(tour)
    for i in range(n):
        c1, c2 = tour[i], tour[(i + 1) % n]
        total += euclidean_dist(cities[c1], cities[c2])
    return round(total, 2)


def simulated_annealing_tsp(initial_temp=1000.0, cooling_rate=0.95, stopping_temp=1.0, max_iter=500, custom_cities=None):
    """
    Solves Traveling Salesperson Problem (TSP) using Simulated Annealing.
    Demonstrates thermal cooling, probabilistic acceptance of worse states, and convergence.
    """
    start_time = time.perf_counter()
    cities = custom_cities if custom_cities else DEFAULT_TSP_CITIES
    city_names = list(cities.keys())

    # Random initial tour
    current_tour = list(city_names)
    random.seed(42)  # Deterministic seed for reproducible academic demonstration
    random.shuffle(current_tour)

    current_cost = calculate_tsp_tour_cost(current_tour, cities)
    best_tour = list(current_tour)
    best_cost = current_cost

    temp = float(initial_temp)
    iteration = 0

    history = []
    temperature_curve = []
    energy_curve = []
    best_energy_curve = []

    while temp > stopping_temp and iteration < max_iter:
        iteration += 1

        # Generate neighbor via 2-opt sub-tour reversal
        i, j = sorted(random.sample(range(len(current_tour)), 2))
        neighbor_tour = current_tour[:i] + list(reversed(current_tour[i:j + 1])) + current_tour[j + 1:]
        neighbor_cost = calculate_tsp_tour_cost(neighbor_tour, cities)

        delta_e = neighbor_cost - current_cost
        accepted = False
        acceptance_prob = 1.0

        if delta_e < 0:
            # Better solution: always accept
            accepted = True
            current_tour = neighbor_tour
            current_cost = neighbor_cost
        else:
            # Worse solution: accept with probability P = exp(-delta_e / T)
            acceptance_prob = math.exp(-delta_e / max(temp, 1e-8))
            if random.random() < acceptance_prob:
                accepted = True
                current_tour = neighbor_tour
                current_cost = neighbor_cost

        if current_cost < best_cost:
            best_cost = current_cost
            best_tour = list(current_tour)

        # Log periodic snapshots (up to 80 points for smooth frontend plotting)
        if iteration % max(1, (max_iter // 60)) == 0 or iteration == 1:
            temperature_curve.append(round(temp, 2))
            energy_curve.append(round(current_cost, 2))
            best_energy_curve.append(round(best_cost, 2))
            history.append({
                "iteration": iteration,
                "temperature": round(temp, 2),
                "current_cost": round(current_cost, 2),
                "best_cost": round(best_cost, 2),
                "delta_e": round(delta_e, 2),
                "prob": round(acceptance_prob, 4),
                "accepted": accepted
            })

        temp *= cooling_rate

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": True,
        "algorithm": "Simulated Annealing (TSP Optimization)",
        "initial_temp": initial_temp,
        "cooling_rate": cooling_rate,
        "stopping_temp": stopping_temp,
        "total_iterations": iteration,
        "final_temp": round(temp, 4),
        "initial_cost": energy_curve[0] if energy_curve else current_cost,
        "best_cost": round(best_cost, 2),
        "best_tour": best_tour,
        "cities": cities,
        "temperature_curve": temperature_curve,
        "energy_curve": energy_curve,
        "best_energy_curve": best_energy_curve,
        "sample_history": history[:30],
        "execution_time_ms": elapsed_ms
    }


# =====================================================================
# 2. HILL CLIMBING ALGORITHM
# =====================================================================

def landscape_function(x):
    """
    Multimodal function designed for pedagogical demonstration:
    Features a Global Maximum at ~6.5, Local Maxima at ~2.2 and ~9.8,
    and a Plateau region between 4.0 and 4.8.
    """
    # Mathematical landscape with known features:
    # Global Max around x ~ 6.5, Local Maxima around x ~ 2.1 and x ~ 9.8
    if 4.0 <= x <= 4.8:
        # Plateau zone
        return 3.20 + 0.005 * math.sin(x * 10)
    return round(math.sin(x) + 0.8 * math.sin(2.5 * x) + 0.4 * math.cos(0.8 * x) + 2.5, 4)


def hill_climbing(start_x=1.5, step_size=0.1, max_steps=100, variant="steepest"):
    """
    Executes Hill Climbing on a multimodal landscape.
    Detects and labels: Local Maximum, Plateau, or Global Maximum.
    Variants: 'simple', 'steepest', 'random_restart'.
    """
    start_time = time.perf_counter()

    # Pre-generate landscape data curve for frontend charting (x from 0 to 12)
    landscape_points = []
    cur_x = 0.0
    while cur_x <= 12.0:
        landscape_points.append({"x": round(cur_x, 2), "y": landscape_function(cur_x)})
        cur_x += 0.1

    def single_run(initial_x):
        current_x = initial_x
        current_val = landscape_function(current_x)
        steps_log = [{"step": 0, "x": round(current_x, 3), "y": round(current_val, 4), "action": "Start"}]

        status = "In Progress"

        for step in range(1, max_steps + 1):
            left_x = round(current_x - step_size, 3)
            right_x = round(current_x + step_size, 3)

            left_val = landscape_function(left_x) if left_x >= 0 else -999
            right_val = landscape_function(right_x) if right_x <= 12.0 else -999

            if variant == "simple":
                # First neighbor that improves
                if left_val > current_val:
                    current_x, current_val = left_x, left_val
                    steps_log.append({"step": step, "x": current_x, "y": current_val, "action": "Moved Left"})
                    continue
                elif right_val > current_val:
                    current_x, current_val = right_x, right_val
                    steps_log.append({"step": step, "x": current_x, "y": current_val, "action": "Moved Right"})
                    continue
                else:
                    # Check plateau vs local maximum
                    if abs(left_val - current_val) < 0.01 and abs(right_val - current_val) < 0.01:
                        status = "Plateau / Shoulder Encountered"
                    else:
                        status = "Local Maximum Reached"
                    break

            else:  # Steepest ascent
                best_neighbor_x = current_x
                best_neighbor_val = current_val

                if left_val > best_neighbor_val:
                    best_neighbor_x = left_x
                    best_neighbor_val = left_val
                if right_val > best_neighbor_val:
                    best_neighbor_x = right_x
                    best_neighbor_val = right_val

                if best_neighbor_val > current_val + 1e-4:
                    direction = "Left" if best_neighbor_x < current_x else "Right"
                    current_x = best_neighbor_x
                    current_val = best_neighbor_val
                    steps_log.append({"step": step, "x": current_x, "y": current_val, "action": f"Steepest Move {direction}"})
                elif abs(left_val - current_val) < 0.01 and abs(right_val - current_val) < 0.01:
                    status = "Plateau / Flat Shoulder Encountered"
                    break
                else:
                    # Check if close to true global maximum (around x=6.5, y~4.4)
                    if abs(current_x - 6.5) < 0.5:
                        status = "Global Maximum Achieved!"
                    else:
                        status = "Stuck in Local Maximum"
                    break

        return current_x, current_val, status, steps_log

    if variant == "random_restart":
        restarts_count = 5
        best_overall_x = None
        best_overall_y = -999
        all_restarts = []

        for r in range(restarts_count):
            rx = round(random.uniform(0.5, 11.5), 2)
            final_x, final_y, st, run_steps = single_run(rx)
            all_restarts.append({
                "restart_id": r + 1,
                "start_x": rx,
                "final_x": final_x,
                "final_y": final_y,
                "status": st,
                "steps": run_steps
            })
            if final_y > best_overall_y:
                best_overall_y = final_y
                best_overall_x = final_x

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)
        return {
            "success": True,
            "algorithm": "Random-Restart Hill Climbing",
            "variant": variant,
            "best_x": best_overall_x,
            "best_y": best_overall_y,
            "restarts": all_restarts,
            "landscape": landscape_points,
            "execution_time_ms": elapsed_ms
        }
    else:
        final_x, final_y, status, steps_log = single_run(start_x)
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

        return {
            "success": True,
            "algorithm": f"Hill Climbing ({variant.title()} Ascent)",
            "variant": variant,
            "start_x": start_x,
            "final_x": final_x,
            "final_y": final_y,
            "status": status,
            "total_steps": len(steps_log) - 1,
            "steps": steps_log,
            "landscape": landscape_points,
            "execution_time_ms": elapsed_ms
        }
