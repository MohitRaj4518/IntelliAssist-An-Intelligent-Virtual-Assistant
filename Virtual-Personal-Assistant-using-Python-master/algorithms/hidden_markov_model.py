"""
Module: hidden_markov_model.py
Implements:
Hidden Markov Model (HMM) with:
1. Viterbi Algorithm (Decoding Problem - Most likely hidden state sequence)
2. Forward Algorithm (Evaluation Problem - Total probability of observation sequence)
Pedagogical Example: Weather (Hidden: Sunny, Rainy) -> Activity (Observed: Walk, Shop, Clean).
"""

import math
import time
import numpy as np


class HiddenMarkovModel:
    def __init__(self, states=None, observations=None, start_prob=None, trans_prob=None, emit_prob=None):
        # Default Academic Example (Rabiner / AIMA Weather-Activity model)
        self.states = states if states else ['Sunny', 'Rainy']
        self.observations = observations if observations else ['Walk', 'Shop', 'Clean']

        # Initial State Distribution pi
        self.start_prob = start_prob if start_prob else {
            'Sunny': 0.60,
            'Rainy': 0.40
        }

        # State Transition Matrix A: P(State_t | State_{t-1})
        self.trans_prob = trans_prob if trans_prob else {
            'Sunny': {'Sunny': 0.70, 'Rainy': 0.30},
            'Rainy': {'Sunny': 0.40, 'Rainy': 0.60}
        }

        # Emission Matrix B: P(Observation_t | State_t)
        self.emit_prob = emit_prob if emit_prob else {
            'Sunny': {'Walk': 0.60, 'Shop': 0.30, 'Clean': 0.10},
            'Rainy': {'Walk': 0.10, 'Shop': 0.40, 'Clean': 0.50}
        }

    def viterbi(self, obs_sequence):
        """
        Viterbi Algorithm: Finds the single most likely hidden state sequence.
        v_t(j) = max_i [ v_{t-1}(i) * a_{ij} ] * b_j(o_t)
        """
        if not obs_sequence:
            return {"error": "Observation sequence is empty."}

        T = len(obs_sequence)
        N = len(self.states)

        # viterbi_table[t][state] = (prob, backpointer)
        v_table = [{}]
        for s in self.states:
            prob = self.start_prob[s] * self.emit_prob[s].get(obs_sequence[0], 0.0)
            v_table[0][s] = {"prob": prob, "prev": None}

        # Dynamic programming forward pass
        for t in range(1, T):
            v_table.append({})
            obs = obs_sequence[t]

            for curr_s in self.states:
                max_tr_prob = -1.0
                best_prev = None

                for prev_s in self.states:
                    tr_prob = v_table[t - 1][prev_s]["prob"] * self.trans_prob[prev_s][curr_s]
                    if tr_prob > max_tr_prob:
                        max_tr_prob = tr_prob
                        best_prev = prev_s

                emission = self.emit_prob[curr_s].get(obs, 0.0)
                curr_prob = max_tr_prob * emission
                v_table[t][curr_s] = {"prob": curr_prob, "prev": best_prev}

        # Backtrack best path
        best_last_state = max(self.states, key=lambda s: v_table[-1][s]["prob"])
        best_path_prob = v_table[-1][best_last_state]["prob"]

        best_path = [best_last_state]
        curr_state = best_last_state
        for t in range(T - 1, 0, -1):
            curr_state = v_table[t][curr_state]["prev"]
            best_path.insert(0, curr_state)

        # Trellis matrix for visualization
        trellis = []
        for t in range(T):
            row = {"time": t + 1, "observation": obs_sequence[t], "state_probs": {}}
            for s in self.states:
                row["state_probs"][s] = round(v_table[t][s]["prob"], 6)
            trellis.append(row)

        return {
            "most_likely_states": best_path,
            "path_probability": round(best_path_prob, 8),
            "trellis_table": trellis
        }

    def forward_algorithm(self, obs_sequence):
        """
        Forward Algorithm: Computes total probability P(O | lambda).
        alpha_t(j) = sum_i [ alpha_{t-1}(i) * a_{ij} ] * b_j(o_t)
        """
        if not obs_sequence:
            return {"error": "Observation sequence is empty."}

        T = len(obs_sequence)
        alpha = [{}]

        # Base case t = 0
        for s in self.states:
            alpha[0][s] = self.start_prob[s] * self.emit_prob[s].get(obs_sequence[0], 0.0)

        # Induction step
        for t in range(1, T):
            alpha.append({})
            obs = obs_sequence[t]
            for curr_s in self.states:
                sum_trans = sum(alpha[t - 1][prev_s] * self.trans_prob[prev_s][curr_s] for prev_s in self.states)
                emission = self.emit_prob[curr_s].get(obs, 0.0)
                alpha[t][curr_s] = sum_trans * emission

        # Total observation likelihood
        total_likelihood = sum(alpha[-1][s] for s in self.states)

        forward_table = []
        for t in range(T):
            forward_table.append({
                "time": t + 1,
                "observation": obs_sequence[t],
                "alpha_values": {s: round(alpha[t][s], 6) for s in self.states}
            })

        return {
            "total_observation_probability": round(total_likelihood, 8),
            "forward_table": forward_table
        }


def run_hidden_markov_model(obs_sequence=None):
    """
    Executes both Viterbi Decoding and Forward Probability calculation for HMM.
    """
    start_time = time.perf_counter()
    if obs_sequence is None:
        obs_sequence = ['Walk', 'Shop', 'Clean']

    hmm = HiddenMarkovModel()
    viterbi_res = hmm.viterbi(obs_sequence)
    forward_res = hmm.forward_algorithm(obs_sequence)

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "success": True,
        "algorithm": "Hidden Markov Model (Viterbi Decoding & Forward Evaluation)",
        "observations_input": obs_sequence,
        "hidden_states": hmm.states,
        "observation_symbols": hmm.observations,
        "initial_state_distribution": hmm.start_prob,
        "transition_matrix": hmm.trans_prob,
        "emission_matrix": hmm.emit_prob,
        "viterbi_decoding": viterbi_res,
        "forward_evaluation": forward_res,
        "execution_time_ms": elapsed_ms
    }
