"""
Module: towers_of_hanoi.py
Implements:
Towers of Hanoi Classical AI Problem with Recursive Divide-and-Conquer Solution,
Full Peg-State Snapshots for Step-by-Step Animation, and Mathematical Analysis.
"""

import time


def solve_towers_of_hanoi(num_disks=3, source="A", auxiliary="B", destination="C"):
    """
    Solves Towers of Hanoi recursively.
    Tracks state of all 3 pegs at each step for step-by-step visual playback.
    """
    start_time = time.perf_counter()

    if num_disks < 1:
        num_disks = 3
    if num_disks > 7:
        num_disks = 7  # Cap for interactive browser animation speed

    # Initialize peg states: larger disk numbers represent larger physical disks
    pegs = {
        source: list(range(num_disks, 0, -1)),
        auxiliary: [],
        destination: []
    }

    steps = [{
        "step": 0,
        "action": "Initial State",
        "disk": None,
        "from_peg": None,
        "to_peg": None,
        "pegs": {k: list(v) for k, v in pegs.items()}
    }]

    move_count = 0

    def hanoi_recursive(n, src, aux, dst):
        nonlocal move_count
        if n == 1:
            move_count += 1
            disk = pegs[src].pop()
            pegs[dst].append(disk)
            steps.append({
                "step": move_count,
                "action": f"Move disk {disk} from {src} to {dst}",
                "disk": disk,
                "from_peg": src,
                "to_peg": dst,
                "pegs": {k: list(v) for k, v in pegs.items()}
            })
            return

        # 1. Move top n-1 disks from source to auxiliary using destination
        hanoi_recursive(n - 1, src, dst, aux)

        # 2. Move the nth disk from source to destination
        move_count += 1
        disk = pegs[src].pop()
        pegs[dst].append(disk)
        steps.append({
            "step": move_count,
            "action": f"Move disk {disk} from {src} to {dst}",
            "disk": disk,
            "from_peg": src,
            "to_peg": dst,
            "pegs": {k: list(v) for k, v in pegs.items()}
        })

        # 3. Move the n-1 disks from auxiliary to destination using source
        hanoi_recursive(n - 1, aux, src, dst)

    hanoi_recursive(num_disks, source, auxiliary, destination)
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": True,
        "algorithm": "Towers of Hanoi (Recursive Divide-and-Conquer)",
        "num_disks": num_disks,
        "total_moves": move_count,
        "theoretical_minimum_moves": (2 ** num_disks) - 1,
        "recurrence_relation": "T(n) = 2T(n-1) + 1  ==>  T(n) = 2^n - 1",
        "time_complexity": "O(2^n)",
        "space_complexity": "O(n) call stack depth",
        "steps": steps,
        "execution_time_ms": elapsed_ms
    }
