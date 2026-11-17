# 🎓 INTELLIASSIST – VIVA VOCE PREPARATION GUIDE
## Top 50 Academic Viva Questions & Detailed Answers for AI Laboratory

---

### **SECTION A: GENERAL PROJECT QUESTIONS**

#### **Q1. What is the title and objective of your AI Lab project?**
**Answer:** The project is titled **"IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms"**. The objective is to build an intelligent, interactive virtual assistant and web platform that demonstrates, visualizes, and executes the 13 core classical AI algorithms prescribed in our B.Tech curriculum across search, optimization, classical problem spaces, and probabilistic machine learning.

#### **Q2. Why did you choose Classical AI algorithms instead of simply using a modern LLM API?**
**Answer:** Classical AI algorithms represent the mathematical foundation of autonomous decision making, path planning, and probabilistic reasoning. They provide provable optimality, formal time/space complexity guarantees, and complete interpretability, which black-box neural networks cannot provide. Furthermore, this project is designed for the academic Artificial Intelligence Laboratory curriculum.

#### **Q3. What technology stack does IntelliAssist use?**
**Answer:**
- **Backend:** Python 3, Flask framework.
- **Scientific Libraries:** NumPy, Pandas, Scikit-Learn, Matplotlib.
- **Frontend:** HTML5, CSS3 (custom dark navy & purple glassmorphism theme), JavaScript (ES6+).
- **Visualization:** HTML5 Canvas, SVG, dynamic DOM rendering.
- **Voice System:** Browser-native Web Speech API (`SpeechRecognition` & `SpeechSynthesis`).

---

### **SECTION B: GROUP 1 – SEARCH & OPTIMIZATION**

#### **Q4. What is the fundamental difference between DFS and BFS?**
**Answer:** DFS uses a LIFO (Stack) data structure and explores deep down a branch before backtracking; its space complexity is linear $O(bm)$, but it is not optimal. BFS uses a FIFO (Queue) data structure and expands nodes level-by-level; it is optimal for unweighted graphs, but its space complexity is exponential $O(b^d)$, making it memory-intensive.

#### **Q5. Why is Iterative Deepening Search (IDS) considered the preferred uninformed search strategy?**
**Answer:** IDS combines the benefits of both: it achieves the completeness and optimality of BFS while maintaining the low linear memory complexity of DFS ($O(bd)$). The overhead of re-expanding top nodes is minimal because in an exponential tree, the vast majority of nodes reside in the deepest level.

#### **Q6. In Simulated Annealing, why do we accept worse moves ($\Delta E > 0$)?**
**Answer:** To escape local optima (peaks or valleys). If an algorithm only accepts improvements (like Hill Climbing), it gets trapped in the first local optimum it encounters. By accepting worse moves with probability $P = e^{-\Delta E / T}$, Simulated Annealing can jump out of local traps.

#### **Q7. What happens to Simulated Annealing as the temperature $T$ approaches 0?**
**Answer:** As $T \to 0$, $-\Delta E / T \to -\infty$, meaning $P = e^{-\Delta E / T} \to 0$. Therefore, the probability of accepting worse moves vanishes, and the algorithm transforms into standard greedy local search.

---

### **SECTION C: GROUP 2 – CLASSICAL AI PROBLEMS**

#### **Q8. What makes the Wumpus World environment challenging for an AI agent?**
**Answer:** It is a **partially observable**, **discrete**, **static**, and **deterministic** environment. The agent cannot observe hazards directly; it must use propositional logic inference over percepts (breeze, stench, glitter) to deduce safe squares.

#### **Q9. How do you mathematically determine if an 8-Puzzle configuration is solvable?**
**Answer:** By calculating the **inversion count** of the tiles (ignoring the blank space). An inversion is any pair of tiles $(a, b)$ such that $a > b$ but $a$ appears before $b$ in the row-major sequence. For an 8-puzzle with the blank in the bottom-right of the goal, the puzzle is solvable **if and only if the inversion count is EVEN**. If odd, reaching the goal is mathematically impossible.

#### **Q10. Why is Manhattan Distance an admissible heuristic for the 8-Puzzle?**
**Answer:** An admissible heuristic never overestimates the true cost to reach the goal ($h(n) \le h^*(n)$). In the 8-puzzle, each tile must make at least as many horizontal and vertical moves as its Manhattan distance from its goal square (assuming no other tiles blocked it). Because tiles cannot move diagonally or jump, the true number of moves is always greater than or equal to the Manhattan distance.

#### **Q11. What is the recurrence relation and minimum moves for Towers of Hanoi with $n$ disks?**
**Answer:** The recurrence relation is $T(n) = 2T(n-1) + 1$, with base case $T(1) = 1$. This solves to $T(n) = 2^n - 1$ moves. For 3 disks, $2^3 - 1 = 7$ moves; for 4 disks, $2^4 - 1 = 15$ moves.

---

### **SECTION D: GROUP 3 – INFORMED SEARCH & OPTIMIZATION**

#### **Q12. What does $f(n) = g(n) + h(n)$ mean in A* search?**
**Answer:**
- $g(n)$: The exact cost incurred to reach node $n$ from the start node.
- $h(n)$: The estimated (heuristic) cost from node $n$ to the goal.
- $f(n)$: The estimated total cost of the cheapest solution passing through node $n$.

#### **Q13. What is the difference between an admissible heuristic and a consistent heuristic?**
**Answer:**
- **Admissibility:** $h(n) \le h^*(n)$ for all $n$ (never overestimates). Guarantees optimality in tree search.
- **Consistency (Monotonicity):** For every node $n$ and neighbor $n'$ generated by action $a$, $h(n) \le c(n, a, n') + h(n')$, satisfying the triangle inequality. Consistency guarantees that the first time a node is expanded in graph search, its path is optimal (no need to reopen closed nodes).

#### **Q14. How does D* Lite differ from A*?**
**Answer:** A* assumes a static environment; if an obstacle appears on the planned path, A* must re-run the entire search from scratch. D* Lite is an incremental heuristic search algorithm that reuses previous search information, updating only affected nodes locally and replanning the path in real-time.

#### **Q15. What are the three main limitations of Hill Climbing?**
**Answer:**
1. **Local Maxima:** Peaks that are higher than all neighbors but lower than the global maximum.
2. **Plateaus / Shoulders:** Flat areas where evaluation function is constant, leaving the agent without directional gradient.
3. **Ridges:** Narrow slopes requiring simultaneous steps in multiple dimensions.

---

### **SECTION E: GROUP 4 – PROBABILISTIC ARTIFICIAL INTELLIGENCE**

#### **Q16. What is a Bayesian Network?**
**Answer:** A Bayesian Network is a Directed Acyclic Graph (DAG) where nodes represent random variables, and directed edges represent conditional probabilistic dependencies. Each node is annotated with a Conditional Probability Table (CPT) specifying $P(\text{Node} \mid \text{Parents})$.

#### **Q17. State Bayes' Theorem and its components.**
**Answer:**
$$P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B)}$$
- $P(A \mid B)$: Posterior probability (probability of hypothesis $A$ given evidence $B$).
- $P(B \mid A)$: Likelihood (probability of evidence $B$ if hypothesis $A$ is true).
- $P(A)$: Prior probability of hypothesis $A$.
- $P(B)$: Marginal probability of evidence $B$.

#### **Q18. What are the E-step and M-step in the Expectation-Maximization (EM) algorithm?**
**Answer:**
- **E-Step (Expectation):** Computes the expected values of latent (hidden) variables given current parameters. In Gaussian Mixture Models, this calculates the soft responsibilities $\gamma_{ik}$ (probability that data point $i$ came from Gaussian component $k$).
- **M-Step (Maximization):** Updates model parameters (means $\mu_k$, covariances $\Sigma_k$, mixture weights $\pi_k$) to maximize the expected log-likelihood calculated in the E-step.

#### **Q19. What is a Hidden Markov Model (HMM) and what are its three fundamental problems?**
**Answer:** An HMM is a double-embedded stochastic process where states are unobservable (hidden), but each state emits observable symbols according to an emission probability distribution.
The three fundamental problems are:
1. **Evaluation:** Given observation sequence $O$ and model $\lambda$, find $P(O \mid \lambda)$ using the **Forward Algorithm**.
2. **Decoding:** Given $O$ and $\lambda$, find the most likely sequence of hidden states using the **Viterbi Algorithm**.
3. **Learning:** Given $O$, estimate model parameters $\lambda = (A, B, \pi)$ using the **Baum-Welch (EM) Algorithm**.

#### **Q20. What is the time complexity of the Viterbi Algorithm compared to brute force?**
**Answer:**
- **Viterbi Algorithm:** $O(T \cdot N^2)$, where $T$ is sequence length and $N$ is number of states, thanks to dynamic programming trellis memoization.
- **Brute Force:** $O(N^T)$, which is exponentially intractable.
