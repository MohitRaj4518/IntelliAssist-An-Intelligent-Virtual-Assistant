"""
Module: bayesian_network.py
Implements:
Bayesian Belief Network (BBN) with Exact Inference by Variable Elimination / Enumeration.
Pedagogical Example: Cloudy -> Sprinkler, Rain -> Wet Grass.
"""


class BayesianNetwork:
    """
    Standard Russell & Norvig Bayesian Network:
    - Cloudy (C)
    - Sprinkler (S) given Cloudy
    - Rain (R) given Cloudy
    - WetGrass (W) given Sprinkler & Rain
    """
    def __init__(self):
        # Prior P(Cloudy)
        self.p_cloudy = {True: 0.50, False: 0.50}

        # Conditional P(Sprinkler | Cloudy)
        self.p_sprinkler = {
            True: {True: 0.10, False: 0.90},   # P(S | C=True)
            False: {True: 0.50, False: 0.50}   # P(S | C=False)
        }

        # Conditional P(Rain | Cloudy)
        self.p_rain = {
            True: {True: 0.80, False: 0.20},   # P(R | C=True)
            False: {True: 0.20, False: 0.80}   # P(R | C=False)
        }

        # Conditional P(WetGrass | Sprinkler, Rain)
        self.p_wetgrass = {
            (True, True): {True: 0.99, False: 0.01},
            (True, False): {True: 0.90, False: 0.10},
            (False, True): {True: 0.90, False: 0.10},
            (False, False): {True: 0.00, False: 1.00}
        }

        self.nodes = [
            {"id": "Cloudy", "label": "Cloudy (C)", "type": "root", "parents": []},
            {"id": "Sprinkler", "label": "Sprinkler (S)", "type": "intermediate", "parents": ["Cloudy"]},
            {"id": "Rain", "label": "Rain (R)", "type": "intermediate", "parents": ["Cloudy"]},
            {"id": "WetGrass", "label": "Wet Grass (W)", "type": "leaf", "parents": ["Sprinkler", "Rain"]}
        ]

        self.edges = [
            {"from": "Cloudy", "to": "Sprinkler"},
            {"from": "Cloudy", "to": "Rain"},
            {"from": "Sprinkler", "to": "WetGrass"},
            {"from": "Rain", "to": "WetGrass"}
        ]

    def joint_probability(self, c, s, r, w):
        """Calculates P(C=c, S=s, R=r, W=w) = P(C)*P(S|C)*P(R|C)*P(W|S,R)."""
        p_c = self.p_cloudy[c]
        p_s = self.p_sprinkler[c][s]
        p_r = self.p_rain[c][r]
        p_w = self.p_wetgrass[(s, r)][w]
        return p_c * p_s * p_r * p_w

    def get_full_joint_distribution(self):
        """Generates all 16 rows of the joint distribution table."""
        table = []
        for c in [True, False]:
            for s in [True, False]:
                for r in [True, False]:
                    for w in [True, False]:
                        prob = round(self.joint_probability(c, s, r, w), 5)
                        table.append({
                            "Cloudy": c,
                            "Sprinkler": s,
                            "Rain": r,
                            "WetGrass": w,
                            "probability": prob
                        })
        return table

    def query_posterior(self, query_var="Rain", evidence=None):
        """
        Calculates P(query_var | evidence) using exact enumeration over hidden variables.
        evidence dict: e.g. {"WetGrass": True, "Sprinkler": False}
        """
        if evidence is None:
            evidence = {"WetGrass": True}

        var_names = ["Cloudy", "Sprinkler", "Rain", "WetGrass"]
        if query_var not in var_names:
            return {"error": f"Invalid query variable '{query_var}'.", "success": False}

        results = {}
        for q_val in [True, False]:
            sum_prob = 0.0
            # Enumerate over all states consistent with query and evidence
            for c in [True, False]:
                for s in [True, False]:
                    for r in [True, False]:
                        for w in [True, False]:
                            assignment = {"Cloudy": c, "Sprinkler": s, "Rain": r, "WetGrass": w}
                            # Check query match
                            if assignment[query_var] != q_val:
                                continue
                            # Check evidence match
                            matches_evidence = True
                            for e_key, e_val in evidence.items():
                                if assignment.get(e_key) != e_val:
                                    matches_evidence = False
                                    break
                            if matches_evidence:
                                sum_prob += self.joint_probability(c, s, r, w)
            results[q_val] = sum_prob

        # Normalize probabilities
        norm_factor = results[True] + results[False]
        if norm_factor > 0:
            p_true = round(results[True] / norm_factor, 4)
            p_false = round(results[False] / norm_factor, 4)
        else:
            p_true, p_false = 0.0, 0.0

        # Mathematical derivation explanation
        evidence_str = ", ".join([f"{k} = {v}" for k, v in evidence.items()])
        formula = f"P({query_var}=True | {evidence_str}) = α · Σ_{{hidden}} P({query_var}=True, Evidence, Hidden)"

        return {
            "success": True,
            "query": query_var,
            "evidence": evidence,
            "posterior_probabilities": {
                "True": p_true,
                "False": p_false
            },
            "percentage_true": round(p_true * 100, 2),
            "percentage_false": round(p_false * 100, 2),
            "formula_derivation": formula,
            "unnormalized_weights": {
                "True": round(results[True], 6),
                "False": round(results[False], 6)
            },
            "cpt_tables": {
                "Cloudy": [{"Condition": "P(C)", "True": 0.50, "False": 0.50}],
                "Sprinkler": [
                    {"Given": "Cloudy=True", "P(S=True)": 0.10, "P(S=False)": 0.90},
                    {"Given": "Cloudy=False", "P(S=True)": 0.50, "P(S=False)": 0.50}
                ],
                "Rain": [
                    {"Given": "Cloudy=True", "P(R=True)": 0.80, "P(R=False)": 0.20},
                    {"Given": "Cloudy=False", "P(R=True)": 0.20, "P(R=False)": 0.80}
                ],
                "WetGrass": [
                    {"Sprinkler": True, "Rain": True, "P(W=True)": 0.99, "P(W=False)": 0.01},
                    {"Sprinkler": True, "Rain": False, "P(W=True)": 0.90, "P(W=False)": 0.10},
                    {"Sprinkler": False, "Rain": True, "P(W=True)": 0.90, "P(W=False)": 0.10},
                    {"Sprinkler": False, "Rain": False, "P(W=True)": 0.00, "P(W=False)": 1.00}
                ]
            },
            "network_structure": {
                "nodes": self.nodes,
                "edges": self.edges
            }
        }


def run_bayesian_network(query_var="Rain", evidence=None):
    bn = BayesianNetwork()
    return bn.query_posterior(query_var, evidence)
