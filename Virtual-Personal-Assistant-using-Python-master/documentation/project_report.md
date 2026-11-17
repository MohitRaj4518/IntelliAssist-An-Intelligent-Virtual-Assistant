# PROJECT REPORT

---

## **INTELLIASSIST – AN INTELLIGENT VIRTUAL ASSISTANT USING CLASSICAL AI ALGORITHMS**

### **A Mini-Project Report Submitted in Partial Fulfillment of the Requirements for the Degree of Bachelor of Technology (B.Tech) in Computer Science & Engineering / Artificial Intelligence**

---

### **STUDENT DETAILS:**
- **Student Name:** [Your Name / Student Name Placeholder]
- **Roll Number / Registration No:** [Roll Number Placeholder]
- **Branch / Specialization:** B.Tech Computer Science & Engineering (Artificial Intelligence)
- **Semester / Year:** 6th Semester / 3rd Year
- **Academic Year:** 2025 – 2026

### **INSTITUTE DETAILS:**
- **Department:** Department of Computer Science & Engineering
- **Institution:** [College / University Name Placeholder]
- **Course Name:** Artificial Intelligence Laboratory (AI Lab)
- **Course Code:** [AI-Lab Course Code Placeholder]
- **Faculty Guide / Course Instructor:** [Professor / Teacher Name Placeholder]

---

## **CERTIFICATE OF ORIGINALITY**

This is to certify that the project entitled **"IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms"** is a bona fide record of academic work carried out by **[Your Name]** under my supervision and guidance for the Artificial Intelligence Laboratory mini-project submission.

To the best of my knowledge, the matter embodied in this report has not been submitted to any other University or Institute for the award of any degree or diploma.

\
**Faculty Guide / Evaluator Signature:** ___________________________  
**Date:** ___________________________  

---

## **ABSTRACT**

In contemporary artificial intelligence pedagogy, a significant gap frequently exists between theoretical textbook formulations of search and probabilistic algorithms and their dynamic visual execution. This academic project presents **IntelliAssist**, an intelligent, full-stack virtual assistant that provides an interactive, visual laboratory for exploring, executing, and analyzing **13 foundational AI algorithms** prescribed in the B.Tech Artificial Intelligence curriculum.

The system integrates four distinct algorithm groups:
1. **Uninformed Search & Optimization:** Depth First Search (DFS), Breadth First Search (BFS), Iterative Deepening Search (IDS), and Simulated Annealing (TSP).
2. **Classical AI Problem Spaces:** The Wumpus World problem (knowledge base and propositional logic reasoning), the 8-Puzzle sliding tile problem (A* search with Manhattan distance and parity inversion checking), and the Towers of Hanoi (recursive divide-and-conquer).
3. **Informed Search & Optimization:** A* Grid Navigation, D* Dynamic Replanning (handling real-time environmental obstacles), and Hill Climbing (steepest ascent, plateau, and local maxima detection).
4. **Probabilistic Artificial Intelligence:** Bayesian Belief Networks (exact inference by enumeration over conditional probability tables), Expectation-Maximization (EM for Gaussian Mixture Models), and Hidden Markov Models (Viterbi decoding and Forward evaluation).

Powered by a lightweight, cross-platform Python Flask backend and an interactive HTML5/Canvas/JavaScript frontend styled in a dark navy and purple glassmorphic theme, IntelliAssist pairs visual algorithms with a local virtual assistant supporting browser-based speech recognition and synthesis. The system eliminates reliance on external paid APIs while delivering verifiable mathematical outputs, step-by-step state traces, and runtime performance metrics.

---

## **TABLE OF CONTENTS**

1. Introduction
2. Problem Statement
3. Project Objectives
4. Software & Hardware Requirements
5. Technologies Used
6. System Architecture & Methodology
7. Module Descriptions
8. Detailed Technical Coverage of the 13 AI Topics
   - 8.1 Group 1: Search and Optimization Algorithms (DFS, BFS, IDS, Simulated Annealing)
   - 8.2 Group 2: Classical AI Problems (Wumpus World, 8-Puzzle, Towers of Hanoi)
   - 8.3 Group 3: Informed Search and Optimization (A*, D*, Hill Climbing)
   - 8.4 Group 4: Probabilistic Artificial Intelligence (Bayesian Network, EM, HMM)
9. Mapping Syllabus Topics to IntelliAssist Features
10. Algorithm Pseudocode
11. Results, Outputs & Visualizations
12. Testing & Verification Suite
13. Advantages & Limitations
14. Future Scope
15. Conclusion
16. References

---

## **1. INTRODUCTION**

Classical Artificial Intelligence (symbolic, heuristic, and probabilistic AI) forms the foundational bedrock of modern machine intelligence. While modern developments in deep learning and large language models receive significant public attention, real-world autonomous systems—from Mars rovers and industrial robot manipulators to automated logistics dispatchers and medical diagnostic networks—rely fundamentally on rigorous heuristic search, dynamic replanning, and probabilistic graphical models.

**IntelliAssist** bridges theoretical instruction and practical laboratory implementation. It acts as both a hands-on simulation workbench and an intelligent virtual assistant capable of answering questions, running live algorithmic traces, and explaining foundational concepts.

---

## **2. PROBLEM STATEMENT**

In conventional university AI laboratory assignments:
1. Algorithms are often implemented as isolated command-line scripts lacking visual intuition.
2. Students often struggle to conceptualize how heuristics guide search frontiers or how probabilistic belief updates propagate across directed acyclic graphs.
3. Chatbot projects frequently resort to superficial pre-trained black-box APIs without implementing the core AI algorithms covered in their curriculum.

**The Goal:** Build an end-to-end, localized web platform titled **"IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms"** that unifies all 13 syllabus algorithms into an interactive, visual environment controlled via text and voice commands.

---

## **3. PROJECT OBJECTIVES**

1. **Complete Syllabus Implementation:** Fully implement all 13 algorithms in modular Python files without relying on mock or hardcoded outputs.
2. **Interactive Visualizations:** Create dynamic HTML5 Canvas and CSS visualizers showing step-by-step node expansions, sliding puzzle tiles, peg disk movements, optimization landscapes, and probabilistic trellis matrices.
3. **Conversational Assistant Integration:** Build a virtual assistant that comprehends student commands (e.g., *"Run BFS"*, *"Solve 8 puzzle"*, *"Explain A star"*), answers academic questions, and triggers simulations.
4. **Voice Interaction:** Integrate native browser Web Speech API for speech-to-text input and text-to-speech feedback with customizable voices.
5. **Academic Rigor:** Include solvability checks (inversion parity), formal recurrence relations, time/space complexity proofs, and viva interview questions.

---

## **4. SOFTWARE & HARDWARE REQUIREMENTS**

### **4.1 Software Requirements:**
- **Operating System:** Cross-platform (Windows 10/11, macOS, Ubuntu/Debian Linux)
- **Programming Language:** Python 3.9+ (Tested on Python 3.11 / 3.14)
- **Backend Framework:** Flask 3.x
- **Scientific Libraries:** NumPy, Pandas, Scikit-Learn, Matplotlib
- **Web Browser:** Google Chrome, Mozilla Firefox, Microsoft Edge, or Apple Safari (supporting Web Speech API and HTML5 Canvas)
- **Version Control:** Git & GitHub

### **4.2 Hardware Requirements:**
- **Processor:** Intel Core i3 / AMD Ryzen 3 / Apple Silicon M-series or higher
- **RAM:** Minimum 4 GB (8 GB recommended)
- **Disk Space:** Less than 200 MB for complete application and virtual environment
- **Audio:** Microphone and speaker/headphones for speech recognition and voice synthesis

---

## **5. TECHNOLOGIES USED**

- **Python 3:** Core programming language executing all mathematical and logical algorithms.
- **Flask:** Lightweight WSGI web application framework facilitating RESTful API communication between algorithm engines and the frontend.
- **HTML5 & CSS3:** Responsive UI designed with custom dark navy and purple glassmorphism, flexbox, and CSS grid layouts.
- **JavaScript (ES6+):** Client-side state management, interactive canvas rendering, and animation loops.
- **Web Speech API:** Browser-native `webkitSpeechRecognition` for voice queries and `speechSynthesis` for spoken responses.
- **NumPy & Scikit-Learn:** Matrix manipulation, sample Gaussian generation, and data verification.

---

## **6. SYSTEM ARCHITECTURE & METHODOLOGY**

The architecture follows a decoupled Model-View-Controller (MVC) pattern:

```
+----------------------------------------------------------------------+
|                     CLIENT-SIDE PRESENTATION LAYER                   |
|  - Modern Dark Navy & Purple Glassmorphic UI                         |
|  - HTML5 Canvas Visualizers (Graph, 8-Puzzle, Hanoi, Grids)          |
|  - Web Speech API (Voice Recognition & Voice Synthesizer)            |
+-----------------------------------^----------------------------------+
                                    | HTTP / JSON REST APIs
+-----------------------------------v----------------------------------+
|                     FLASK APPLICATION CONTROLLER                     |
|  - Route Dispatcher (/, /algorithms, /puzzles, /learning, /chatbot)  |
|  - REST Endpoints (/api/run_algorithm, /api/chat, /api/config)       |
+-----------------------------------^----------------------------------+
                                    | Modular Execution Calls
+-----------------------------------v----------------------------------+
|                  CORE PYTHON AI ALGORITHM ENGINES                    |
|  1. search_algorithms.py        (DFS, BFS, IDS)                      |
|  2. optimization_algorithms.py  (Simulated Annealing, Hill Climbing) |
|  3. wumpus_world.py             (Propositional Logic Agent)          |
|  4. eight_puzzle.py             (A* Manhattan Solver)                |
|  5. towers_of_hanoi.py          (Recursive Hanoi Engine)             |
|  6. informed_search.py          (A* Grid & D* Dynamic Replanning)    |
|  7. bayesian_network.py         (Exact Enumeration BBN)              |
|  8. em_algorithm.py             (Gaussian Mixture Model EM)          |
|  9. hidden_markov_model.py      (Viterbi & Forward Algorithm)        |
|  10. knowledge_base.py          (Theory, Complexities, Viva Q&A)     |
+----------------------------------------------------------------------+
```

---

## **7. MODULE DESCRIPTIONS**

1. **Dashboard Module (`/`):** Displays overall project metadata, syllabus group cards, core metrics, and quick demonstration links.
2. **Algorithm Laboratory (`/algorithms`):** Allows users to select any search, informed search, or probabilistic algorithm, configure parameters, execute the simulation, and view dynamic Canvas graphs, convergence curves, and step feeds.
3. **Classical AI Puzzles (`/puzzles`):** Houses dedicated simulation environments for Wumpus World, 8-Puzzle, and Towers of Hanoi with interactive stepping and animation controls.
4. **Algorithm Learning Section (`/learning`):** Provides academic reference documentation for all 13 algorithms, including definitions, working principles, pseudocode, complexities, and viva interview questions.
5. **Virtual Assistant (`/chatbot`):** Interactive voice and text interface that interprets student requests, explains algorithms, and triggers real-time execution.

---

## **8. DETAILED TECHNICAL COVERAGE OF THE 13 AI TOPICS**

### **8.1 Group 1: Search and Optimization Algorithms**

#### **1. Depth First Search (DFS)**
- **Principle:** Explores the deepest unexpanded node first using a LIFO stack.
- **Time Complexity:** $O(b^m)$ where $b$ is the branching factor and $m$ is the maximum depth.
- **Space Complexity:** $O(bm)$, maintaining linear memory consumption.
- **Completeness & Optimality:** Complete in finite spaces with cycle checking; not optimal.

#### **2. Breadth First Search (BFS)**
- **Principle:** Explores the shallowest unexpanded node first using a FIFO queue.
- **Time Complexity:** $O(b^d)$ where $d$ is the shallowest goal depth.
- **Space Complexity:** $O(b^d)$, storing all frontier nodes in memory.
- **Completeness & Optimality:** Complete if $b$ is finite; optimal for unweighted step costs.

#### **3. Iterative Deepening Search (IDS)**
- **Principle:** Repeatedly runs Depth-Limited Search (DLS) with depth limits $0, 1, 2, \dots$
- **Time Complexity:** $O(b^d)$ — asymptotically identical to BFS.
- **Space Complexity:** $O(bd)$ — identical to DFS linear space.
- **Advantage:** Combines the completeness and optimality of BFS with the linear memory efficiency of DFS.

#### **4. Simulated Annealing**
- **Principle:** Probabilistic metaheuristic inspired by metallurgy. Better moves are always accepted ($\Delta E < 0$); worse moves are accepted with Boltzmann probability $P = e^{-\Delta E / T}$.
- **Cooling Schedule:** Temperature decreases geometrically: $T_{k+1} = \alpha T_k$.
- **Application in Project:** Traveling Salesperson Problem (TSP) optimizing route distance.

---

### **8.2 Group 2: Classical AI Problems**

#### **5. Wumpus World Problem**
- **Environment:** 4x4 grid with pits, gold, and the Wumpus. Partially observable.
- **Percepts:** Stench, Breeze, Glitter, Bump, Scream.
- **Knowledge Base:** Uses propositional logic deductions:
  $$\neg \text{Breeze}(x, y) \implies \forall (nx, ny) \in \text{Neighbors}(x, y), \neg \text{Pit}(nx, ny)$$
  $$\neg \text{Stench}(x, y) \implies \forall (nx, ny) \in \text{Neighbors}(x, y), \neg \text{Wumpus}(nx, ny)$$

#### **6. 8-Puzzle Problem**
- **Mathematical Parity Verification:** A configuration is solvable if and only if the number of inversions is even.
- **Search Strategy:** A* search utilizing the Manhattan Distance heuristic:
  $$h(n) = \sum_{i=1}^8 \left( |x_i - x_{i,\text{goal}}| + |y_i - y_{i,\text{goal}}| \right)$$
- **Admissibility:** Proved admissible because tiles can move at most one square per step ($h(n) \le h^*(n)$).

#### **7. Towers of Hanoi Problem**
- **Principle:** Recursive divide-and-conquer moving $n$ disks between three pegs.
- **Recurrence Relation:** $T(n) = 2T(n-1) + 1$, yielding the exact minimum moves $T(n) = 2^n - 1$.
- **Complexity:** Time $O(2^n)$, Space $O(n)$ call stack depth.

---

### **8.3 Group 3: Informed Search and Optimization**

#### **8. A* Search Algorithm**
- **Evaluation Function:** $f(n) = g(n) + h(n)$
  - $g(n)$: Exact path cost from start to node $n$.
  - $h(n)$: Admissible heuristic estimate from node $n$ to goal.
- **Grid Navigation:** Demonstrates obstacle avoidance on a 2D coordinate grid with open and closed list tracking.

#### **9. D* Search Algorithm (Dynamic Replanning)**
- **Principle:** When an obstacle appears along an active planned route, standard A* re-computes the entire search space. D* Lite updates only affected edge costs and replans locally from the agent's current coordinates.
- **Demonstration:** Dynamic obstacle dynamically placed on the planned path, triggering local path repair.

#### **10. Hill Climbing Algorithm**
- **Principle:** Greedy local search moving continuously in the direction of steepest elevation.
- **Failure Modes Demonstrated:**
  1. **Local Maxima:** Suboptimal peaks where all neighbors are worse.
  2. **Plateaus / Shoulders:** Flat regions where all neighbors have equal value.
  3. **Random-Restart:** Running multiple random initializations to reach the global maximum.

---

### **8.4 Group 4: Probabilistic Artificial Intelligence**

#### **11. Bayesian Network**
- **Model:** Cloudy ($C$), Sprinkler ($S$), Rain ($R$), Wet Grass ($W$).
- **Chain Rule:** $P(C, S, R, W) = P(C) P(S | C) P(R | C) P(W | S, R)$
- **Inference:** Exact calculation of posterior probabilities given observed evidence via enumeration:
  $$P(R = \text{True} \mid W = \text{True}) = \frac{\sum_{C, S} P(C, S, R=\text{True}, W=\text{True})}{\sum_{C, S, R} P(C, S, R, W=\text{True})} \approx 0.7079$$

#### **12. Expectation Maximization (EM) Algorithm**
- **Model:** Gaussian Mixture Model (GMM) clustering on multi-modal continuous data.
- **E-Step:** Compute soft responsibilities $\gamma_{ik}$:
  $$\gamma_{ik} = \frac{\pi_k \mathcal{N}(x_i \mid \mu_k, \sigma_k^2)}{\sum_{j=1}^K \pi_j \mathcal{N}(x_i \mid \mu_j, \sigma_j^2)}$$
- **M-Step:** Update weights $\pi_k$, means $\mu_k$, and variances $\sigma_k^2$.
- **Log-Likelihood:** Tracks monotonic convergence of $\ln P(X \mid \theta)$.

#### **13. Hidden Markov Model (HMM)**
- **Model:** Hidden weather states (Sunny, Rainy) emitting observable activities (Walk, Shop, Clean).
- **Viterbi Decoding:** Solves the decoding problem via dynamic programming:
  $$v_t(j) = \max_i \left[ v_{t-1}(i) \cdot a_{ij} \right] \cdot b_j(o_t)$$
- **Forward Algorithm:** Computes total observation likelihood $P(O \mid \lambda) = \sum_i \alpha_T(i)$.

---

## **9. MAPPING SYLLABUS TOPICS TO INTELLIASSIST FEATURES**

| Syllabus Topic | Underlying Python Engine | IntelliAssist Visual Feature | Interactive Controls |
| :--- | :--- | :--- | :--- |
| **1. DFS** | `search_algorithms.py` | Graph Canvas (order pulses, stack state) | Start/Goal Node, Step Playback |
| **2. BFS** | `search_algorithms.py` | Level-by-level queue frontier expansion | Start/Goal Node, Step Playback |
| **3. IDS** | `search_algorithms.py` | Depth limit iterations log & path | Max Depth slider, Start/Goal Node |
| **4. Simulated Annealing** | `optimization_algorithms.py` | TSP Tour path & Energy cooling curve | $T_0$, Cooling Rate $\alpha$, Iterations |
| **5. Wumpus World** | `wumpus_world.py` | 4x4 Grid (Agent, Wumpus, Pit, Gold) | Autonomous Run, Step Playback |
| **6. 8-Puzzle** | `eight_puzzle.py` | 3x3 Animated Tile Board | Solvable Preset, Inversion Checker |
| **7. Towers of Hanoi** | `towers_of_hanoi.py` | 3 Pegs with proportional disk stacks | Number of Disks (2-6), Step Slider |
| **8. A* Search** | `informed_search.py` | 2D Grid with Obstacles & $f(n)$ metrics | Manhattan vs. Euclidean Heuristics |
| **9. D* Replanning** | `informed_search.py` | Dynamic blocked cell & detour path | Dynamic Obstacle Trigger |
| **10. Hill Climbing** | `optimization_algorithms.py` | Multimodal landscape curve with peak labels | Simple, Steepest, Random-Restart |
| **11. Bayesian Network** | `bayesian_network.py` | DAG nodes, CPT tables & Posterior bar | Evidence selector (WetGrass, Sprinkler) |
| **12. EM Algorithm** | `em_algorithm.py` | Gaussian distribution curve & LL plot | Number of Clusters ($K=2,3,4$) |
| **13. HMM** | `hidden_markov_model.py` | Viterbi Trellis DP table & state path | Observation Sequence Selector |

---

## **10. ALGORITHM PSEUDOCODE**

*(Please see Section 8 and `algorithms/knowledge_base.py` for comprehensive pseudocode blocks corresponding to each algorithm).*

---

## **11. RESULTS & OUTPUTS**

The application produces verifiable mathematical outputs:
- **DFS / BFS / IDS:** Successfully finds optimal paths on unweighted benchmarks with sub-millisecond execution times.
- **8-Puzzle:** Resolves solvable boards within 2 to 24 moves, rejecting unsolvable boards based on odd inversion count.
- **Towers of Hanoi:** Generates exactly $2^n - 1$ steps (e.g. 7 moves for $n=3$, 15 moves for $n=4$).
- **Bayesian Network:** Computes exact posterior $P(\text{Rain} = \text{True} \mid \text{WetGrass} = \text{True}) = 70.79\%$.
- **HMM:** Correctly identifies the optimal hidden state sequence for observation sequences like `['Walk', 'Shop', 'Clean']` using Viterbi dynamic programming.

---

## **12. TESTING & VERIFICATION SUITE**

Automated unit tests are implemented in `tests/test_algorithms.py` utilizing Python's built-in `unittest` module.

### **Test Results:**
- `test_dfs`, `test_bfs`, `test_ids`: Passed (100% path accuracy).
- `test_simulated_annealing`: Passed ($\text{BestCost} \le \text{InitialCost}$).
- `test_eight_puzzle_solvability`: Passed (even parity solved, odd parity flagged).
- `test_towers_of_hanoi`: Passed (verified $T(n) = 2^n - 1$ for all test depths).
- `test_bayesian_network`: Passed (verified $P(\text{Rain} \mid \text{WetGrass}) = 0.7079$).
- `test_em_algorithm`: Passed (verified convergence of Gaussian mixture parameters).
- `test_hidden_markov_model`: Passed (verified Viterbi state sequence and Forward probability).

---

## **13. ADVANTAGES & LIMITATIONS**

### **Advantages:**
1. **100% Offline & Free:** Operates completely without API keys, paid credits, or external cloud latency.
2. **Unified UI/UX:** Dark navy and purple visual interface with responsive controls.
3. **Voice Enabled:** Speech-to-text and text-to-speech built into the virtual assistant.
4. **Academically Rigorous:** Uses exact algorithms rather than simulated or mock responses.

### **Limitations:**
1. The virtual assistant uses structured keyword and intent matching rather than an unrestricted generative large language model.
2. Grid sizes for pathfinding are optimized for classroom demonstrations (10x10) rather than planetary scale.

---

## **14. FUTURE SCOPE**

1. Integration of local open-weights Small Language Models (SLMs) such as LLaMA-3-1B or Phi-3 via ONNX/WebGPU.
2. Extension to Adversarial Search algorithms (Alpha-Beta Pruning, Minimax in Connect-4 and Chess).
3. 3D WebGL visualizations for continuous robotic configuration space planning.

---

## **15. CONCLUSION**

**IntelliAssist** successfully demonstrates that classical AI algorithms remain vital, mathematically elegant, and practical. By uniting uninformed search, informed heuristics, classical AI problem spaces, and probabilistic machine learning under a single voice-guided virtual assistant, the project fulfills all academic requirements of the B.Tech Artificial Intelligence Laboratory syllabus.

---

## **16. REFERENCES**

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
2. Rich, E., Knight, K., & Nair, S. B. (2009). *Artificial Intelligence* (3rd ed.). Tata McGraw-Hill.
3. Rabiner, L. R. (1989). "A tutorial on hidden Markov models and selected applications in speech recognition." *Proceedings of the IEEE*, 77(2), 257-286.
4. Koenig, S., & Likhachev, M. (2002). "D* Lite." *Eighteenth National Conference on Artificial Intelligence (AAAI)*, 476-483.
5. Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977). "Maximum likelihood from incomplete data via the EM algorithm." *Journal of the Royal Statistical Society: Series B*, 39(1), 1-38.
