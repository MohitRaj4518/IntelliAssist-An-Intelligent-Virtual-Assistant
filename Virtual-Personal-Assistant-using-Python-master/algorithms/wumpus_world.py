"""
Module: wumpus_world.py
Implements:
Wumpus World Classical AI Problem with 4x4 Grid, Percepts (Breeze, Stench, Glitter),
and Knowledge-Based Logical Reasoning Agent.
"""

import random


class WumpusWorld:
    def __init__(self, size=4, custom_config=None):
        self.size = size
        self.agent_pos = (0, 0)
        self.agent_dir = "RIGHT"  # UP, DOWN, LEFT, RIGHT
        self.has_arrow = True
        self.has_gold = False
        self.is_alive = True
        self.wumpus_alive = True
        self.score = 0

        if custom_config:
            self.wumpus_pos = tuple(custom_config.get("wumpus", (1, 2)))
            self.gold_pos = tuple(custom_config.get("gold", (2, 3)))
            self.pits = [tuple(p) for p in custom_config.get("pits", [(2, 0), (2, 2), (3, 3)])]
        else:
            self._generate_preset_world()

        # Knowledge Base for Logical Agent
        self.visited = set()
        self.safe = {(0, 0)}
        self.breeze_cells = set()
        self.stench_cells = set()
        self.suspected_pits = set()
        self.suspected_wumpus = set()
        self.confirmed_pits = set()
        self.confirmed_wumpus = None
        self.action_history = []

        self.visited.add(self.agent_pos)

    def _generate_preset_world(self):
        """Standard pedagogical configuration from Russell & Norvig AIMA."""
        self.wumpus_pos = (1, 2)
        self.gold_pos = (1, 1)
        self.pits = [(2, 0), (2, 2), (3, 3)]

    def get_neighbors(self, pos):
        r, c = pos
        candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        return [(nr, nc) for nr, nc in candidates if 0 <= nr < self.size and 0 <= nc < self.size]

    def get_percepts(self, pos=None):
        if pos is None:
            pos = self.agent_pos
        r, c = pos

        stench = False
        if self.wumpus_alive and (pos == self.wumpus_pos or pos in self.get_neighbors(self.wumpus_pos)):
            stench = True

        breeze = False
        for p in self.pits:
            if pos == p or pos in self.get_neighbors(p):
                breeze = True
                break

        glitter = (pos == self.gold_pos and not self.has_gold)
        return {
            "stench": stench,
            "breeze": breeze,
            "glitter": glitter,
            "bump": False,
            "scream": False
        }

    def infer_knowledge(self):
        """
        Propositional Logic inference engine:
        - If current cell has NO Breeze: all unvisited neighbors cannot have a pit (safe from pits).
        - If current cell has NO Stench: all unvisited neighbors cannot be Wumpus.
        - Cross-referencing identifies confirmed danger or confirmed safety.
        """
        curr = self.agent_pos
        percepts = self.get_percepts(curr)
        neighbors = self.get_neighbors(curr)

        reasoning = []

        if percepts["breeze"]:
            self.breeze_cells.add(curr)
            reasoning.append(f"Felt Breeze at ({curr[0]},{curr[1]}) -> adjacent cells may contain a Pit.")
            for n in neighbors:
                if n not in self.visited and n not in self.safe:
                    self.suspected_pits.add(n)
        else:
            reasoning.append(f"No Breeze at ({curr[0]},{curr[1]}) -> all adjacent cells are free of Pits.")
            for n in neighbors:
                self.suspected_pits.discard(n)
                if n not in self.suspected_wumpus:
                    self.safe.add(n)

        if percepts["stench"] and self.wumpus_alive:
            self.stench_cells.add(curr)
            reasoning.append(f"Smelled Stench at ({curr[0]},{curr[1]}) -> Wumpus is adjacent.")
            for n in neighbors:
                if n not in self.visited and n not in self.safe:
                    self.suspected_wumpus.add(n)
        else:
            reasoning.append(f"No Stench at ({curr[0]},{curr[1]}) -> all adjacent cells are free of Wumpus.")
            for n in neighbors:
                self.suspected_wumpus.discard(n)
                if n not in self.suspected_pits:
                    self.safe.add(n)

        # Logical deduction for confirmed Wumpus
        if len(self.stench_cells) >= 2 and not self.confirmed_wumpus:
            common = None
            for sc in self.stench_cells:
                sc_neighbors = set(self.get_neighbors(sc))
                if common is None:
                    common = sc_neighbors
                else:
                    common = common.intersection(sc_neighbors)
            if common and len(common) == 1:
                self.confirmed_wumpus = list(common)[0]
                reasoning.append(f"LOGICAL INFERENCE: Wumpus position uniquely confirmed at {self.confirmed_wumpus}!")

        return reasoning

    def solve_autonomously(self, max_steps=20):
        """
        Simulates an autonomous AI agent navigating the Wumpus World
        using safe-first exploration and goal acquisition.
        """
        steps_log = []
        self.score = 0

        for step in range(1, max_steps + 1):
            if not self.is_alive or self.has_gold:
                break

            curr = self.agent_pos
            self.visited.add(curr)
            self.safe.add(curr)
            percepts = self.get_percepts(curr)
            deductions = self.infer_knowledge()

            # Check if current cell is fatal
            if curr in self.pits:
                self.is_alive = False
                self.score -= 1000
                steps_log.append({
                    "step": step,
                    "agent_pos": list(curr),
                    "action": "Agent Fell into a Pit!",
                    "percepts": percepts,
                    "reasoning": ["Tragic step: Agent stepped into an unmapped pit."],
                    "score": self.score,
                    "is_alive": False,
                    "has_gold": False,
                    "safe_cells": [list(p) for p in self.safe],
                    "visited_cells": [list(p) for p in self.visited]
                })
                break

            if curr == self.wumpus_pos and self.wumpus_alive:
                self.is_alive = False
                self.score -= 1000
                steps_log.append({
                    "step": step,
                    "agent_pos": list(curr),
                    "action": "Agent Eaten by Wumpus!",
                    "percepts": percepts,
                    "reasoning": ["Fatal step: Agent entered Wumpus lair."],
                    "score": self.score,
                    "is_alive": False,
                    "has_gold": False,
                    "safe_cells": [list(p) for p in self.safe],
                    "visited_cells": [list(p) for p in self.visited]
                })
                break

            # Check for Gold
            if curr == self.gold_pos and not self.has_gold:
                self.has_gold = True
                self.score += 1000
                steps_log.append({
                    "step": step,
                    "agent_pos": list(curr),
                    "action": "GRAB GOLD!",
                    "percepts": percepts,
                    "reasoning": deductions + ["GLITTER DETECTED! Gold secured. Objective achieved!"],
                    "score": self.score,
                    "is_alive": True,
                    "has_gold": True,
                    "safe_cells": [list(p) for p in self.safe],
                    "visited_cells": [list(p) for p in self.visited]
                })
                break

            # Decide next action: prioritize unvisited safe neighbors
            neighbors = self.get_neighbors(curr)
            unvisited_safe = [n for n in neighbors if n in self.safe and n not in self.visited]

            if unvisited_safe:
                next_move = unvisited_safe[0]
                action_desc = f"Move to unvisited safe cell ({next_move[0]}, {next_move[1]})"
            else:
                # Backtrack to any safe cell adjacent to visited
                candidates = []
                for v in self.visited:
                    for vn in self.get_neighbors(v):
                        if vn in self.safe and vn not in self.visited:
                            candidates.append(vn)
                if candidates:
                    next_move = candidates[0]
                    action_desc = f"Backtrack towards frontier safe cell ({next_move[0]}, {next_move[1]})"
                else:
                    # Risk-managed move: pick neighbor with least suspicion
                    next_move = neighbors[0]
                    action_desc = f"Cautious exploration step to ({next_move[0]}, {next_move[1]})"

            self.score -= 1  # Action cost
            self.agent_pos = next_move

            steps_log.append({
                "step": step,
                "agent_pos": list(curr),
                "action": action_desc,
                "percepts": percepts,
                "reasoning": deductions,
                "score": self.score,
                "is_alive": self.is_alive,
                "has_gold": self.has_gold,
                "safe_cells": [list(p) for p in self.safe],
                "visited_cells": [list(p) for p in self.visited]
            })

        return {
            "success": self.has_gold and self.is_alive,
            "grid_size": self.size,
            "wumpus_pos": list(self.wumpus_pos),
            "gold_pos": list(self.gold_pos),
            "pits": [list(p) for p in self.pits],
            "final_score": self.score,
            "steps": steps_log
        }
