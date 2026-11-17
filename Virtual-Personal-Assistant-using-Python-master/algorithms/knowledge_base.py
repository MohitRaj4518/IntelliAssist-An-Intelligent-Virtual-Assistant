"""
Module: knowledge_base.py
Comprehensive Academic Knowledge Base for all 13 AI Algorithms.
Provides complete theory, pseudocode, complexity, applications, and viva Q&A.
Powers both the Learning Portal and the IntelliAssist Virtual Assistant.
"""

ALGORITHM_KNOWLEDGE = {
    "dfs": {
        "id": "dfs",
        "name": "Depth First Search (DFS)",
        "group": "Search and Optimization",
        "group_id": 1,
        "definition": "Depth First Search (DFS) is an uninformed graph/tree traversal algorithm that explores as deep as possible along each branch before backtracking.",
        "working_principle": "DFS operates on a LIFO (Last-In, First-Out) principle using a Stack (or function recursion). Starting at the root or initial node, it proceeds down a path until a dead end or the goal state is reached, then backtracks to the most recent node with unexplored branches.",
        "steps": [
            "Push the initial start node onto the stack and mark it as visited.",
            "While the stack is not empty, pop the top node.",
            "If the popped node is the goal state, terminate and reconstruct the path.",
            "Otherwise, retrieve all unvisited adjacent neighbors of the current node.",
            "Push unvisited neighbors onto the stack and mark them visited.",
            "Repeat until the goal is found or the stack is empty."
        ],
        "pseudocode": """procedure DFS(Graph, start_node, goal_node):
    stack = [start_node]
    visited = {start_node}
    parent = {}
    
    while stack is not empty:
        current = stack.pop()
        if current == goal_node:
            return reconstruct_path(parent, current)
        
        for neighbor in Graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.push(neighbor)
    return failure""",
        "time_complexity": "O(b^m) where b is branching factor and m is maximum depth of the state space.",
        "space_complexity": "O(b * m) linear space (highly memory efficient compared to BFS).",
        "optimality": "Not optimal. It may return a sub-optimal long path before discovering a shorter one.",
        "completeness": "Complete in finite state spaces with loop-checking. Incomplete in infinite spaces with cycles without cycle detection.",
        "advantages": [
            "Significantly lower memory requirement O(bm) than BFS O(b^d).",
            "Fast when solutions are dense and located deep down a branch.",
            "Natural fit for backtracking problems like mazes and constraint satisfaction."
        ],
        "disadvantages": [
            "Can get trapped in infinite loops or very deep paths.",
            "Does not guarantee finding the shortest path.",
            "Sensitive to the order of branch expansion."
        ],
        "applications": [
            "Topological sorting in compilers and dependency resolution.",
            "Detecting cycles in directed and undirected graphs.",
            "Solving mazes, sudoku, and constraint satisfaction problems."
        ],
        "viva_questions": [
            {"q": "What data structure is used by DFS?", "a": "A LIFO Stack (explicit stack or system call stack in recursive implementation)."},
            {"q": "Is DFS optimal?", "a": "No, DFS is not guaranteed to find the shortest path; it takes the first path found."},
            {"q": "What is the space complexity of DFS?", "a": "O(bm), where b is branching factor and m is maximum tree depth."}
        ]
    },

    "bfs": {
        "id": "bfs",
        "name": "Breadth First Search (BFS)",
        "group": "Search and Optimization",
        "group_id": 1,
        "definition": "Breadth First Search (BFS) is an uninformed search algorithm that explores a graph level-by-level, visiting all neighbor nodes at the current depth before moving deeper.",
        "working_principle": "BFS operates on a FIFO (First-In, First-Out) principle using a Queue. It expands the shallowest unexpanded node first, guaranteeing the shortest path in unweighted graphs.",
        "steps": [
            "Enqueue the start node into a FIFO queue and mark it as visited.",
            "While the queue is not empty, dequeue the front node.",
            "If the dequeued node is the goal, reconstruct and return the path.",
            "For each adjacent unvisited neighbor, mark it as visited, record its parent, and enqueue it.",
            "Repeat until the goal is found or the queue is exhausted."
        ],
        "pseudocode": """procedure BFS(Graph, start_node, goal_node):
    queue = [start_node]
    visited = {start_node}
    parent = {}
    
    while queue is not empty:
        current = queue.dequeue()
        if current == goal_node:
            return reconstruct_path(parent, current)
            
        for neighbor in Graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.enqueue(neighbor)
    return failure""",
        "time_complexity": "O(b^d) where b is branching factor and d is depth of the shallowest solution.",
        "space_complexity": "O(b^d) exponential space requirement to maintain all frontier nodes.",
        "optimality": "Optimal for unweighted graphs (guarantees finding the path with minimum number of transitions).",
        "completeness": "Complete if branching factor b is finite.",
        "advantages": [
            "Guaranteed to find the shallowest/shortest path in unweighted graphs.",
            "Never gets trapped down an infinite single branch.",
            "Simple to implement and verify."
        ],
        "disadvantages": [
            "Massive exponential memory consumption O(b^d).",
            "Slow if the goal is located at a deep level in a wide graph."
        ],
        "applications": [
            "Finding shortest path in unweighted networks (GPS, peer-to-peer routing).",
            "Web crawlers indexing pages level by level.",
            "Social network distance (degrees of separation on LinkedIn/Facebook)."
        ],
        "viva_questions": [
            {"q": "What data structure is used by BFS?", "a": "A FIFO (First-In-First-Out) Queue."},
            {"q": "When is BFS guaranteed to be optimal?", "a": "When all step costs are equal or in an unweighted graph."},
            {"q": "Why is BFS rarely used on very large search spaces?", "a": "Because its space complexity O(b^d) rapidly exhausts physical memory."}
        ]
    },

    "ids": {
        "id": "ids",
        "name": "Iterative Deepening Search (IDS)",
        "group": "Search and Optimization",
        "group_id": 1,
        "definition": "Iterative Deepening Search (IDS / IDDFS) is a state space search algorithm that repeatedly applies depth-limited search with increasing depth limits (0, 1, 2, ...).",
        "working_principle": "Combines the benefits of BFS (completeness and optimality) with the memory efficiency of DFS (linear space O(bd)). Although states near the top are visited multiple times, the overhead is negligible because the majority of nodes in an exponential tree reside in the bottom layer.",
        "steps": [
            "Set depth limit = 0.",
            "Execute Depth-Limited Search (DLS) from start node up to the current depth limit.",
            "If the goal is found, return the path.",
            "If DLS reports cutoff without goal, increment depth limit by 1.",
            "Repeat until goal is found or max allowed depth is exceeded."
        ],
        "pseudocode": """procedure IDS(root, goal):
    depth = 0
    while True:
        result = DLS(root, goal, depth)
        if result != CUTOFF:
            return result
        depth = depth + 1

procedure DLS(node, goal, limit):
    if node == goal: return node
    if limit <= 0: return CUTOFF
    for child in node.children():
        res = DLS(child, goal, limit - 1)
        if res != CUTOFF and res != FAILURE: return res
    return CUTOFF""",
        "time_complexity": "O(b^d) — asymptotically the same as BFS despite re-generating top nodes.",
        "space_complexity": "O(b * d) linear space — same as DFS.",
        "optimality": "Optimal for uniform step costs.",
        "completeness": "Complete if branching factor b is finite.",
        "advantages": [
            "Combines optimal path guarantees of BFS with linear space complexity of DFS.",
            "Preferred uninformed search method when tree depth is large and unknown.",
            "Very low memory footprint O(bd)."
        ],
        "disadvantages": [
            "Repeated generation of upper-level nodes across iterations.",
            "Inefficient for graphs with large numbers of alternative cycles unless path history is tracked."
        ],
        "applications": [
            "Game tree searching (Chess, Checkers) within fixed time slices.",
            "Automated theorem proving and logic puzzle solving."
        ],
        "viva_questions": [
            {"q": "Why is the repeated expansion of nodes in IDS acceptable?", "a": "Because in an exponential tree with branching factor b, the bottom level contains (b-1)/b of total nodes (~80-90%), so overhead is only a small constant fraction."},
            {"q": "What are the time and space complexities of IDS?", "a": "Time is O(b^d) and Space is O(bd)."},
            {"q": "How does IDS compare to BFS in memory?", "a": "BFS requires exponential memory O(b^d) while IDS requires only linear memory O(bd)."}
        ]
    },

    "simulated_annealing": {
        "id": "simulated_annealing",
        "name": "Simulated Annealing",
        "group": "Search and Optimization",
        "group_id": 1,
        "definition": "Simulated Annealing is a probabilistic metaheuristic optimization algorithm inspired by the physical annealing process in metallurgy, where controlled cooling minimizes crystal lattice defects.",
        "working_principle": "At high temperatures, the algorithm frequently accepts worse moves to explore the state space and escape local optima. As the temperature drops according to a cooling schedule T = T * alpha, the probability of accepting worse moves P = exp(-delta_E / T) approaches zero, causing the algorithm to settle into a deep global minimum.",
        "steps": [
            "Initialize current state S and temperature T = T_0.",
            "While T > T_min and max iterations not exceeded:",
            "  Generate a candidate neighbor state S'.",
            "  Compute energy difference delta_E = Cost(S') - Cost(S).",
            "  If delta_E < 0 (improvement), accept S' unconditionally (S = S').",
            "  Else (worse solution), accept S' with probability P = exp(-delta_E / T).",
            "  Update T according to cooling rate (e.g. T = alpha * T).",
            "Return the best solution found throughout the cooling process."
        ],
        "pseudocode": """procedure SimulatedAnnealing(problem, schedule):
    current = problem.initial_state
    T = schedule.initial_temp
    
    while T > schedule.min_temp:
        neighbor = random_neighbor(current)
        delta_E = cost(neighbor) - cost(current)
        
        if delta_E < 0:
            current = neighbor
        elif random(0, 1) < exp(-delta_E / T):
            current = neighbor
            
        T = T * schedule.cooling_rate
    return current""",
        "time_complexity": "Dependent on cooling schedule and problem; typically O(k * N) where k is cooling steps.",
        "space_complexity": "O(1) auxiliary space beyond state representation.",
        "optimality": "Theoretically guaranteed to converge to the global optimum if cooled sufficiently slowly (logarithmic cooling).",
        "completeness": "Heuristic; not guaranteed within finite practical runtimes.",
        "advantages": [
            "Effectively escapes local minima and plateaus.",
            "Independent of gradient information (works on non-differentiable surfaces).",
            "Versatile and easily adapted to combinatorial optimization."
        ],
        "disadvantages": [
            "Hyperparameter sensitive: initial temperature and cooling rate drastically impact performance.",
            "Can be slow if cooling schedule is too conservative."
        ],
        "applications": [
            "VLSI circuit design and chip floorplanning.",
            "Traveling Salesperson Problem (TSP) and logistics routing.",
            "Job shop scheduling and protein structure prediction."
        ],
        "viva_questions": [
            {"q": "What is the acceptance probability formula in Simulated Annealing?", "a": "P = exp(-ΔE / T), where ΔE is the cost difference and T is current temperature."},
            {"q": "Why does Simulated Annealing accept worse states?", "a": "To escape local minima and explore promising alternative regions of the search landscape."},
            {"q": "What happens as temperature T approaches 0?", "a": "The acceptance probability for worse moves approaches 0, turning the algorithm into greedy local hill climbing."}
        ]
    },

    "wumpus_world": {
        "id": "wumpus_world",
        "name": "Wumpus World Problem",
        "group": "Classical AI Problems",
        "group_id": 2,
        "definition": "The Wumpus World is a classical grid-based benchmark problem in Artificial Intelligence used to illustrate knowledge-based, reasoning, and logical inference agents in partially observable environments.",
        "working_principle": "The agent operates in a 4x4 grid containing pits, gold, and a monster (Wumpus). The agent cannot see hazards directly but perceives local environmental clues (Breeze adjacent to pits, Stench adjacent to the Wumpus, Glitter in the gold cell). By maintaining a Propositional Logic Knowledge Base, the agent infers safe cells.",
        "steps": [
            "Agent begins at cell (0, 0), facing RIGHT, holding 1 arrow.",
            "Sense percepts [Stench, Breeze, Glitter, Bump, Scream].",
            "Apply logical deduction: No Breeze => adjacent cells safe from pits. No Stench => adjacent cells safe from Wumpus.",
            "If Glitter is perceived: execute GRAB gold action.",
            "Prioritize movement into unvisited cells proven to be SAFE.",
            "If Wumpus location is uniquely inferred and blocks the path: shoot the arrow."
        ],
        "pseudocode": """procedure WumpusAgent(percept):
    TELL(KB, MakePerceptSentence(percept, current_time))
    
    // Logical inference of safety
    for each cell adjacent to current:
        if ASK(KB, ~Pit(cell) and ~Wumpus(cell)):
            SafeCells.add(cell)
            
    if Glitter:
        return 'GRAB'
    if SafeUnvisitedCells:
        return PlanMovesTo(SafeUnvisitedCells.pop())
    return Backtrack()""",
        "time_complexity": "NP-complete in worst-case propositional theorem proving; fast with Horn clauses.",
        "space_complexity": "O(N^2) where N is grid dimension.",
        "optimality": "Finds safe optimal moves when guaranteed deductions exist.",
        "completeness": "Sound inference under propositional logic.",
        "advantages": [
            "Exemplifies reasoning under uncertainty and partial observability.",
            "Combines knowledge representation, inference, and sequential planning."
        ],
        "disadvantages": [
            "May encounter situations requiring probabilistic risk assessment when no cell is proven 100% safe."
        ],
        "applications": [
            "Autonomous planetary rover navigation (Mars Curiosity / Perseverance).",
            "Mine clearance and hazardous material rescue robots."
        ],
        "viva_questions": [
            {"q": "What environmental clues does the agent perceive in Wumpus World?", "a": "Stench (near Wumpus), Breeze (near Pits), Glitter (at Gold), Bump (hitting wall), Scream (Wumpus killed)."},
            {"q": "Is the Wumpus World environment fully observable or partially observable?", "a": "Partially observable, as the agent only senses local percepts in its current square."},
            {"q": "How does the agent prove a square is safe?", "a": "If an adjacent square had neither breeze nor stench, all of its orthogonal neighbors are proven free of pits and Wumpus."}
        ]
    },

    "eight_puzzle": {
        "id": "eight_puzzle",
        "name": "8 Puzzle Problem",
        "group": "Classical AI Problems",
        "group_id": 2,
        "definition": "The 8 Puzzle is a classic sliding tile puzzle consisting of a 3x3 frame with 8 numbered tiles (1-8) and one empty space, aiming to reach a target configuration from a given start state.",
        "working_principle": "Solvability is first verified via inversion counts. The state space has 9!/2 = 181,440 reachable states. The problem is solved using A* search with admissible heuristics such as Manhattan Distance (sum of horizontal and vertical distances of tiles from target positions).",
        "steps": [
            "Verify solvability: count inversions in flattened puzzle (excluding blank). If odd, puzzle is UNSOLVABLE.",
            "Initialize A* priority queue with start state, g=0, and h=ManhattanDistance(start).",
            "Pop state with lowest f(n) = g(n) + h(n).",
            "If state matches goal: reconstruct sequence of tile moves.",
            "Generate valid sliding moves (UP, DOWN, LEFT, RIGHT of blank space).",
            "Compute new g(n) and h(n) for each successor and push into priority queue."
        ],
        "pseudocode": """procedure Solve8Puzzle(start_board, goal_board):
    if count_inversions(start_board) % 2 != 0:
        return "UNSOLVABLE"
        
    pq = PriorityQueue()
    pq.push(f=h(start), g=0, state=start, path=[])
    visited = {start: 0}
    
    while pq is not empty:
        f, g, state, path = pq.pop()
        if state == goal:
            return path
            
        for neighbor, move in get_neighbors(state):
            if g + 1 < visited.get(neighbor, infinity):
                visited[neighbor] = g + 1
                h_val = manhattan_distance(neighbor, goal)
                pq.push(f=g+1+h_val, g=g+1, state=neighbor, path=path+[move])""",
        "time_complexity": "O(b^d) worst-case; vastly reduced by Manhattan heuristic.",
        "space_complexity": "O(b^d) storing explored states in closed list.",
        "optimality": "Optimal when using admissible heuristic (Manhattan distance h(n) <= h*(n)).",
        "completeness": "Complete for all solvable configurations.",
        "advantages": [
            "Demonstrates heuristic search power over brute force.",
            "Proves admissibility and consistency of heuristics."
        ],
        "disadvantages": [
            "Scales exponentially: 15-puzzle has 10^13 states; 24-puzzle requires IDA*."
        ],
        "applications": [
            "Automated warehouse robot routing and container reshuffling in shipping ports.",
            "DNA fragment assembly and sequence alignment."
        ],
        "viva_questions": [
            {"q": "How can you determine if an 8-puzzle configuration is solvable?", "a": "Count the number of inversions (pairs of tiles where a larger number precedes a smaller one, ignoring blank). If the inversion count is EVEN, it is solvable; if ODD, it is impossible to reach standard goal."},
            {"q": "What is the Manhattan distance heuristic?", "a": "The sum of absolute horizontal and vertical differences between current and goal coordinates: |x - x_goal| + |y - y_goal|."},
            {"q": "Why is Manhattan distance admissible?", "a": "Because every tile must move at least its Manhattan distance to reach goal, so h(n) never overestimates true cost h*(n)."}
        ]
    },

    "towers_of_hanoi": {
        "id": "towers_of_hanoi",
        "name": "Towers of Hanoi Problem",
        "group": "Classical AI Problems",
        "group_id": 2,
        "definition": "Towers of Hanoi is a classical mathematical and AI puzzle consisting of three rods and n disks of different sizes, governed by strict movement rules.",
        "working_principle": "Solved via recursive divide-and-conquer. Moving n disks from Source to Destination requires: 1) moving n-1 disks to Auxiliary, 2) moving the nth (largest) disk directly to Destination, and 3) moving the n-1 disks from Auxiliary to Destination.",
        "steps": [
            "Base case: if n == 1, move disk 1 directly from Source to Destination.",
            "Recursive step 1: Move top n-1 disks from Source to Auxiliary peg using Destination as buffer.",
            "Recursive step 2: Move disk n from Source to Destination peg.",
            "Recursive step 3: Move n-1 disks from Auxiliary to Destination peg using Source as buffer.",
            "Total moves required: 2^n - 1."
        ],
        "pseudocode": """procedure Hanoi(n, source, auxiliary, destination):
    if n == 1:
        print("Move disk 1 from", source, "to", destination)
        return
        
    Hanoi(n - 1, source, destination, auxiliary)
    print("Move disk", n, "from", source, "to", destination)
    Hanoi(n - 1, auxiliary, source, destination)""",
        "time_complexity": "O(2^n) exponential time complexity (T(n) = 2T(n-1) + 1).",
        "space_complexity": "O(n) auxiliary call stack depth.",
        "optimality": "Strictly optimal: 2^n - 1 is the theoretical minimum number of moves.",
        "completeness": "Complete: guaranteed to solve for any n >= 1.",
        "advantages": [
            "Perfect educational demonstration of recursive decomposition and induction.",
            "Deterministic and mathematically optimal."
        ],
        "disadvantages": [
            "Exponential explosion: 64 disks would take 2^64 - 1 moves (~585 billion years)."
        ],
        "applications": [
            "Recursive algorithm benchmarking in computer architectures.",
            "Backup rotation schemes (Grandfather-Father-Son tape backup schedule).",
            "Cognitive psychology testing (executive brain function assessment)."
        ],
        "viva_questions": [
            {"q": "What is the recurrence relation for Towers of Hanoi?", "a": "T(n) = 2T(n-1) + 1 with T(1) = 1, which solves to T(n) = 2^n - 1."},
            {"q": "What are the three fundamental rules of Towers of Hanoi?", "a": "1) Only one disk can be moved at a time, 2) each move takes the upper disk from a peg, 3) no disk may be placed on top of a smaller disk."},
            {"q": "How many moves are needed for 4 disks?", "a": "2^4 - 1 = 15 moves."}
        ]
    },

    "a_star": {
        "id": "a_star",
        "name": "A* Search Algorithm",
        "group": "Informed Search and Optimization",
        "group_id": 3,
        "definition": "A* Search is the most widely used informed best-first pathfinding algorithm, evaluating nodes using evaluation function f(n) = g(n) + h(n).",
        "working_principle": "Balances the exact path cost incurred so far g(n) with the estimated heuristic remaining cost h(n) to the goal. By maintaining an open set priority queue, it expands the node with minimum f(n), guaranteeing the shortest path when h(n) is admissible and consistent.",
        "steps": [
            "Initialize open set priority queue with start node (g=0, f=h(start)).",
            "Maintain closed set of expanded nodes.",
            "While open set is not empty, pop node with lowest f(n).",
            "If node is goal, reconstruct path from parent pointers and return.",
            "Add current node to closed set.",
            "For each valid neighbor, compute tentative_g = g(current) + step_cost.",
            "If neighbor is in closed set and tentative_g >= g(neighbor), skip.",
            "If tentative_g < g(neighbor), record parent and update f(neighbor) = tentative_g + h(neighbor)."
        ],
        "pseudocode": """procedure A_Star(start, goal, heuristic):
    open_set = PriorityQueue()
    open_set.push(start, priority=heuristic(start, goal))
    
    g_score = {start: 0}
    parent = {}
    
    while open_set is not empty:
        current = open_set.pop()
        if current == goal:
            return reconstruct_path(parent, current)
            
        for neighbor in get_neighbors(current):
            tentative_g = g_score[current] + cost(current, neighbor)
            if tentative_g < g_score.get(neighbor, infinity):
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                open_set.push(neighbor, priority=f_score)
    return failure""",
        "time_complexity": "O(b^d) worst-case; O(d) in best-case with perfect heuristic.",
        "space_complexity": "O(b^d) keeping all visited and open nodes in memory.",
        "optimality": "Optimal if h(n) is admissible (tree search) or consistent/monotonic (graph search).",
        "completeness": "Complete on finite graphs with positive step costs.",
        "advantages": [
            "Universally accepted benchmark for optimal pathfinding.",
            "Explores far fewer nodes than Dijkstra while guaranteeing optimality."
        ],
        "disadvantages": [
            "Substantial memory consumption on large grid maps."
        ],
        "applications": [
            "Video game NPC movement and pathfinding (Unreal/Unity engines).",
            "Autonomous self-driving vehicle route planning (Google Maps, Waymo).",
            "Robotic arm trajectory synthesis."
        ],
        "viva_questions": [
            {"q": "What does f(n) = g(n) + h(n) represent in A*?", "a": "g(n) is the exact cost from start to current node n; h(n) is the estimated heuristic cost from n to goal; f(n) is total estimated path cost."},
            {"q": "What makes a heuristic admissible?", "a": "A heuristic is admissible if it never overestimates the true cost to reach the goal: h(n) <= h*(n)."},
            {"q": "What happens if h(n) = 0 for all nodes?", "a": "A* reduces exactly to Dijkstra's Algorithm (Uniform Cost Search)."}
        ]
    },

    "d_star": {
        "id": "d_star",
        "name": "D* Search Algorithm",
        "group": "Informed Search and Optimization",
        "group_id": 3,
        "definition": "D* (Dynamic A*) and D* Lite are informed incremental heuristic search algorithms designed for path planning in dynamic, partially known, or changing environments.",
        "working_principle": "When an agent moving along a planned path encounters a newly blocked cell or changed edge cost, standard A* would have to replan from scratch. D* instead maintains rhs-values and key comparisons, propagating cost updates only to affected states to replan in real-time.",
        "steps": [
            "Perform initial search backwards from goal to start so distance-to-goal estimates are preserved.",
            "Agent begins executing movement along the computed path.",
            "Sensors detect an obstacle dynamically blocking an upcoming cell.",
            "Update edge cost of the blocked transition to infinity.",
            "Insert affected nodes into an inconsistency priority queue.",
            "Propagate cost changes locally until the agent's current position is consistent again.",
            "Continue moving along the newly replanned path."
        ],
        "pseudocode": """procedure DStarLite():
    Initialize()
    ComputeShortestPath()
    
    while current_node != goal_node:
        if current_node == goal: return success
        current_node = argmin_{neighbor}(cost(current, neighbor) + g(neighbor))
        MoveTo(current_node)
        
        ScanForChangedEdges()
        if changed_edges:
            for (u, v) in changed_edges:
                UpdateEdgeCost(u, v, new_cost)
                UpdateVertex(u)
            ComputeShortestPath()""",
        "time_complexity": "Orders of magnitude faster than re-running A* from scratch in dynamic settings.",
        "space_complexity": "O(N) where N is number of grid cells.",
        "optimality": "Maintains provably optimal paths after each replanning step.",
        "completeness": "Complete in finite graphs.",
        "advantages": [
            "Dramatically reduces replanning time in real-time robotics.",
            "Reuses previously explored path trees efficiently."
        ],
        "disadvantages": [
            "More complex bookkeeping with rhs-values and double-key priority queues."
        ],
        "applications": [
            "NASA Mars Exploration Rovers (Spirit, Opportunity) autonomous navigation.",
            "Automated Guided Vehicles (AGVs) in dynamic automated factory floors.",
            "Drone flight navigation around sudden aerial obstacles."
        ],
        "viva_questions": [
            {"q": "How does D* differ from standard A*?", "a": "A* plans in static environments and must restart from scratch if an obstacle changes; D* updates only affected nodes incrementally and replans rapidly."},
            {"q": "Why does D* search backward from goal to start?", "a": "Because when the robot moves, its current position changes constantly while the goal position remains static, making goal-directed heuristic updates much cheaper."},
            {"q": "Where has D* been famously deployed in real life?", "a": "On the NASA Mars rovers for autonomous hazard avoidance."}
        ]
    },

    "hill_climbing": {
        "id": "hill_climbing",
        "name": "Hill Climbing Algorithm",
        "group": "Informed Search and Optimization",
        "group_id": 3,
        "definition": "Hill Climbing is an iterative local search algorithm that continually moves in the direction of increasing value (steepest gradient) until no higher neighbor can be found.",
        "working_principle": "Operates like climbing a mountain in a dense fog: at every step, it checks immediate neighbors and climbs upward. It does not look ahead or remember past states, making it greedy and vulnerable to local maxima, plateaus, and ridges.",
        "steps": [
            "Evaluate initial state. Set current = start.",
            "Loop:",
            "  Generate neighbor states of current.",
            "  Select neighbor with highest evaluation value.",
            "  If best neighbor value <= current value, terminate (peak/plateau reached).",
            "  Else, current = best neighbor.",
            "Return current state as solution."
        ],
        "pseudocode": """procedure HillClimbing(problem):
    current = problem.initial_state
    
    while True:
        neighbors = problem.get_neighbors(current)
        best_neighbor = argmax_{n in neighbors}(heuristic(n))
        
        if heuristic(best_neighbor) <= heuristic(current):
            return current // Peak reached
        current = best_neighbor""",
        "time_complexity": "O(d * b) where d is steps to peak and b is number of neighbors.",
        "space_complexity": "O(1) keeps only current state.",
        "optimality": "Not optimal; frequently terminates at suboptimal local maxima.",
        "completeness": "Incomplete; can get stuck in local maxima or loops on plateaus.",
        "advantages": [
            "Virtually zero memory requirement O(1).",
            "Finds good solutions very quickly in convex/unimodal landscapes."
        ],
        "disadvantages": [
            "Prone to getting stuck in Local Maxima.",
            "Wanders aimlessly on Flat Plateaus and Shoulders.",
            "Cannot navigate narrow diagonal Ridges effectively."
        ],
        "applications": [
            "Optimizing parameters in machine learning models without gradient access.",
            "N-Queens problem solution generation.",
            "Integrated circuit layout routing."
        ],
        "viva_questions": [
            {"q": "What are the three main failure modes of Hill Climbing?", "a": "1) Local Maxima (peaks lower than global max), 2) Plateaus/Shoulders (flat areas where all neighbors have equal value), 3) Ridges (steep slopes requiring diagonal navigation)."},
            {"q": "How can Hill Climbing overcome local maxima?", "a": "By using Random-Restart Hill Climbing (launching multiple runs from randomized starting points) or Simulated Annealing."},
            {"q": "What is the difference between Simple and Steepest-Ascent Hill Climbing?", "a": "Simple moves to the first neighbor that improves the evaluation function; Steepest Ascent examines ALL neighbors and moves to the one with the maximum improvement."}
        ]
    },

    "bayesian_network": {
        "id": "bayesian_network",
        "name": "Bayesian Network",
        "group": "Probabilistic AI",
        "group_id": 4,
        "definition": "A Bayesian Belief Network (BBN) is a probabilistic graphical model that represents a set of variables and their conditional dependencies via a Directed Acyclic Graph (DAG).",
        "working_principle": "Nodes represent random variables; directed edges represent direct causal or probabilistic influences. Each node has an associated Conditional Probability Table (CPT) quantifying P(Node | Parents). The joint distribution factorizes as P(X1,...,Xn) = product_i P(Xi | Parents(Xi)). Inference is performed using Bayes' Theorem.",
        "steps": [
            "Define domain variables and establish topological causal edges.",
            "Specify conditional probability tables (CPTs) for every node given its parents.",
            "Apply Bayes' Rule: P(A | B) = [P(B | A) * P(A)] / P(B).",
            "Compute posterior probabilities given observed evidence via variable elimination or enumeration over hidden variables."
        ],
        "pseudocode": """procedure ExactInference(QueryVar, Evidence, BayesianNet):
    factors = []
    for var in BayesianNet.topological_order():
        factors.append(MakeFactor(var, Evidence))
        if var is hidden:
            factors = SumOut(var, factors)
    return Normalize(MultiplyFactors(factors))""",
        "time_complexity": "Exact inference in general BBNs is NP-hard; linear in polytrees.",
        "space_complexity": "Compact O(n * 2^k) where k is maximum number of parents per node.",
        "optimality": "Produces exact mathematical posterior probabilities.",
        "completeness": "Sound probabilistic reasoning.",
        "advantages": [
            "Handles incomplete and uncertain information systematically.",
            "Models causal relationships naturally rather than pure correlation.",
            "Dramatically reduces parameters needed to represent full joint distribution."
        ],
        "disadvantages": [
            "Exact inference becomes computationally intractable in dense graphs.",
            "Requires domain expertise to formulate accurate prior CPTs."
        ],
        "applications": [
            "Medical diagnostic decision support systems (PathFinder, QMR-DT).",
            "Credit card fraud detection and risk scoring.",
            "Weather forecasting and environmental sensor networks."
        ],
        "viva_questions": [
            {"q": "What is the chain rule formula for a Bayesian Network?", "a": "P(X1, X2, ..., Xn) = Π_{i=1}^n P(Xi | Parents(Xi))."},
            {"q": "What is d-separation in Bayesian Networks?", "a": "A graphical criterion that determines whether two variables are conditionally independent given a set of evidence variables."},
            {"q": "Why is a Bayesian Network more compact than a full joint distribution?", "a": "Full joint distribution requires 2^n - 1 parameters; a Bayesian Network requires only Σ 2^(parents(Xi)), exploiting conditional independence."}
        ]
    },

    "em_algorithm": {
        "id": "em_algorithm",
        "name": "Expectation Maximization (EM) Algorithm",
        "group": "Probabilistic AI",
        "group_id": 4,
        "definition": "Expectation-Maximization (EM) is an iterative optimization algorithm used to find Maximum Likelihood Estimates (MLE) of parameters in probabilistic models with unobserved latent variables.",
        "working_principle": "Alternates between two steps: the E-step (Expectation), which calculates expected values of the latent variables given current parameters (soft responsibility assignments), and the M-step (Maximization), which updates model parameters to maximize the expected log-likelihood. Guarantees monotonic increase in likelihood.",
        "steps": [
            "Initialize parameters: means, covariances, and mixture weights.",
            "Repeat until convergence:",
            "  E-Step: Compute responsibilities gamma(i, k) = P(Z_i = k | x_i, theta).",
            "  M-Step: Update parameters using responsibilities (mean_k, variance_k, weight_k).",
            "  Evaluate Log-Likelihood: ln P(X | theta).",
            "  If change in log-likelihood < epsilon, terminate."
        ],
        "pseudocode": """procedure ExpectationMaximization(Data, K, max_iter):
    Initialize weights, means, variances for K components
    
    for iter = 1 to max_iter:
        // E-Step
        for each data point x_i and component k:
            gamma[i][k] = weight[k] * N(x_i | mean[k], var[k]) / sum_j(...)
            
        // M-Step
        for each component k:
            N_k = sum_i(gamma[i][k])
            mean[k] = sum_i(gamma[i][k] * x_i) / N_k
            var[k]  = sum_i(gamma[i][k] * (x_i - mean[k])^2) / N_k
            weight[k] = N_k / N
            
        if abs(log_likelihood - prev_ll) < tolerance:
            break""",
        "time_complexity": "O(iterations * N * K * D) where N is samples, K is clusters, D is dimensions.",
        "space_complexity": "O(N * K) storing responsibilities matrix.",
        "optimality": "Guaranteed to converge to a local maximum of the likelihood function.",
        "completeness": "Always converges monotonically.",
        "advantages": [
            "Performs soft clustering (data points belong probabilistically to multiple clusters).",
            "Mathematically principled approach for incomplete data and latent models.",
            "Guaranteed non-decreasing log-likelihood at every iteration."
        ],
        "disadvantages": [
            "Can converge to local optima depending on initial parameter guesses.",
            "Slower convergence than K-Means.",
            "Requires specifying number of components K in advance."
        ],
        "applications": [
            "Gaussian Mixture Model (GMM) clustering.",
            "Speech recognition acoustic modeling and natural language processing.",
            "Image segmentation and medical MRI tissue classification."
        ],
        "viva_questions": [
            {"q": "What are the two steps of the EM algorithm?", "a": "E-step (Expectation): computes expectations of missing latent variables (responsibilities); M-step (Maximization): updates model parameters to maximize expected log-likelihood."},
            {"q": "How does EM differ from K-Means clustering?", "a": "K-Means performs hard clustering (each point belongs strictly to 1 cluster); EM performs soft probabilistic clustering with Gaussian distributions (points have fractional membership)."},
            {"q": "Is EM guaranteed to find the global maximum likelihood?", "a": "No, it is guaranteed to converge to a local maximum, making good initialization important."}
        ]
    },

    "hidden_markov_model": {
        "id": "hidden_markov_model",
        "name": "Hidden Markov Model (HMM)",
        "group": "Probabilistic AI",
        "group_id": 4,
        "definition": "A Hidden Markov Model (HMM) is a statistical Markov model in which the system is modeled as a Markov process with unobservable (hidden) states that emit observable symbols.",
        "working_principle": "Characterized by 5 components: States S, Observations V, Initial distribution pi, Transition probability matrix A, and Emission probability matrix B. Solves three fundamental tasks: 1) Evaluation (Forward Algorithm), 2) Decoding (Viterbi Algorithm), and 3) Learning (Baum-Welch / EM Algorithm).",
        "steps": [
            "Define Hidden States (e.g. Sunny, Rainy) and Observed Symbols (e.g. Walk, Shop, Clean).",
            "Initialize matrices: pi (initial state vector), A (transition matrix), B (emission matrix).",
            "For Decoding: Apply Viterbi dynamic programming to find most probable hidden state sequence.",
            "For Evaluation: Apply Forward algorithm to compute total observation sequence probability P(O | lambda)."
        ],
        "pseudocode": """procedure Viterbi(Observations, States, pi, A, B):
    T = length(Observations)
    Initialize viterbi_matrix[T, States] and backpointer[T, States]
    
    for each state s:
        viterbi_matrix[0, s] = pi[s] * B[s, Observations[0]]
        
    for t = 1 to T - 1:
        for each state s:
            viterbi_matrix[t, s] = max_{s'}(viterbi_matrix[t-1, s'] * A[s', s]) * B[s, Observations[t]]
            backpointer[t, s]    = argmax_{s'}(viterbi_matrix[t-1, s'] * A[s', s])
            
    best_last = argmax_{s}(viterbi_matrix[T-1, s])
    best_path = Backtrack(backpointer, best_last)
    return best_path""",
        "time_complexity": "Viterbi: O(T * N^2) where T is sequence length and N is number of hidden states.",
        "space_complexity": "O(T * N) trellis storage table.",
        "optimality": "Viterbi is provably optimal for finding the single best state sequence.",
        "completeness": "Sound dynamic programming evaluation.",
        "advantages": [
            "Rigorous temporal modeling of sequential and time-series data.",
            "Polynomial time inference O(TN^2) via dynamic programming vs O(N^T) brute force."
        ],
        "disadvantages": [
            "First-order Markov assumption (current state depends only on immediate predecessor).",
            "Observations assumed conditionally independent of previous observations."
        ],
        "applications": [
            "Speech recognition (phoneme acoustic modeling).",
            "Bioinformatics (DNA sequence alignment and gene prediction).",
            "Part-of-Speech (POS) tagging and handwriting recognition."
        ],
        "viva_questions": [
            {"q": "What are the three fundamental problems of HMMs?", "a": "1) Evaluation: Compute P(O|λ) via Forward/Backward algorithm; 2) Decoding: Find best hidden state sequence via Viterbi algorithm; 3) Learning: Estimate model parameters λ=(A,B,π) via Baum-Welch (EM) algorithm."},
            {"q": "What is the time complexity of the Viterbi algorithm?", "a": "O(T * N^2), where T is sequence length and N is number of hidden states (compared to O(N^T) for brute force)."},
            {"q": "What is the difference between Markov Chains and Hidden Markov Models?", "a": "In a Markov Chain, the states are directly visible to the observer; in an HMM, the states are hidden, and only emitted outputs are observable."}
        ]
    }
}
