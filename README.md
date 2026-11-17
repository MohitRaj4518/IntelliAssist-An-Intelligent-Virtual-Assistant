# 🧠 IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask&logoColor=white)
![AI Syllabus](https://img.shields.io/badge/AI%20Lab-13%20Algorithms-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-emerald?style=for-the-badge)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

> **College Mini-Project Submission:**  
> **Topic:** *"IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms"*  
> **Course:** B.Tech Artificial Intelligence Laboratory  

---

## 📌 Project Overview
 DEMO LINK : 
https://intelliassist-an-intelligent-virtual-sdb8.onrender.com
**IntelliAssist** is an intelligent, full-stack virtual assistant and educational simulation platform built to demonstrate, analyze, and visualize all **13 classical Artificial Intelligence algorithms** from the university AI Lab syllabus. 

Unlike generic chatbots, **IntelliAssist** features real computational algorithm engines written in Python, dynamic step-by-step Canvas/DOM visualizers, and a localized virtual assistant supporting browser-native speech recognition and speech synthesis.

---

## 📚 AI Syllabus Coverage Table

| Group | # | Algorithm / Problem | Category | Implementation File | Interactive Visualization |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Group 1** | 1 | **Depth First Search (DFS)** | Uninformed Search | `algorithms/search_algorithms.py` | Step-by-step graph traversal & LIFO stack order |
| | 2 | **Breadth First Search (BFS)** | Uninformed Search | `algorithms/search_algorithms.py` | Level-by-level FIFO frontier & shortest path |
| | 3 | **Iterative Deepening Search (IDS)** | Uninformed Search | `algorithms/search_algorithms.py` | Depth limit iterations log & path cost |
| | 4 | **Simulated Annealing** | Metaheuristic Optimization | `algorithms/optimization_algorithms.py` | TSP route mapping & thermal cooling energy curve |
| **Group 2** | 5 | **Wumpus World Problem** | Classical AI Problem | `algorithms/wumpus_world.py` | 4x4 Grid (Agent, Wumpus, Pit, Gold, Percepts) |
| | 6 | **8-Puzzle Problem** | Classical AI Problem | `algorithms/eight_puzzle.py` | 3x3 Sliding tiles, parity checker & A* player |
| | 7 | **Towers of Hanoi** | Classical AI Problem | `algorithms/towers_of_hanoi.py` | 3 Pegs with animated disk movements ($2^n - 1$) |
| **Group 3** | 8 | **A* Search Algorithm** | Informed Search | `algorithms/informed_search.py` | 2D Grid with obstacle avoidance ($f=g+h$) |
| | 9 | **D* Search Algorithm** | Dynamic Replanning | `algorithms/informed_search.py` | Real-time dynamic obstacle detour replanning |
| | 10 | **Hill Climbing Algorithm** | Local Optimization | `algorithms/optimization_algorithms.py` | Multimodal landscape (local maxima & plateau) |
| **Group 4** | 11 | **Bayesian Network** | Probabilistic AI | `algorithms/bayesian_network.py` | DAG nodes, CPTs, and exact Bayes inference |
| | 12 | **Expectation Maximization (EM)** | Probabilistic AI | `algorithms/em_algorithm.py` | GMM clustering & log-likelihood convergence curve |
| | 13 | **Hidden Markov Model (HMM)** | Probabilistic AI | `algorithms/hidden_markov_model.py` | Viterbi Trellis matrix & Forward evaluation |

---

## ✨ Key Features

- 🎨 **Modern Dark Navy & Purple UI:** Glassmorphism cards, glowing accents, and clean responsive sidebar navigation.
- 🎙️ **Voice & Direct Answer Virtual Assistant:** Direct factual question answering (Science, Tech, AI, Personalities, History), instant math expression solver, speech-to-text mic input, and customizable voice speech synthesis.
- 🌐 **Web & System Automation:** Launch any website in Google Chrome, search Google Chrome directly, play YouTube videos, and launch system tools (Calculator, Camera, Terminal, Notepad).
- 📊 **Real Calculated Outputs:** Every result is computed live with mathematical verification (no fake hardcoded outputs).
- 🧩 **Interactive Puzzles:** Autonomous Wumpus World explorer, solvable/unsolvable 8-Puzzle tester, and recursive Hanoi animator.
- 📖 **Comprehensive Learning Section:** Theory, pseudocode, time/space complexities, pros/cons, and viva Q&A for every algorithm.
- 🧪 **Automated Test Suite:** 19 comprehensive unit tests in `tests/test_algorithms.py` validating 100% algorithm accuracy and assistant query resolution.
- 🔒 **100% Local & Free:** Complete offline functionality with built-in knowledge engine; optional free Gemini/Groq API expansion.

---

## 📂 Folder Structure

```
IntelliAssist/
├── app.py                          # Flask backend server & REST API
├── requirements.txt                # Production Python dependencies
├── README.md                       # Comprehensive project documentation
├── .gitignore                      # Git configuration avoiding unnecessary uploads
│
├── algorithms/                     # Modular Python AI algorithm engines
│   ├── __init__.py
│   ├── search_algorithms.py        # DFS, BFS, IDS
│   ├── optimization_algorithms.py  # Simulated Annealing, Hill Climbing
│   ├── wumpus_world.py             # Wumpus World propositional logic agent
│   ├── eight_puzzle.py             # 8-Puzzle A* Manhattan solver
│   ├── towers_of_hanoi.py          # Towers of Hanoi recursive solver
│   ├── informed_search.py          # A* Search & D* Dynamic Replanning
│   ├── bayesian_network.py         # Exact inference Bayesian Network
│   ├── em_algorithm.py             # Expectation-Maximization for GMM
│   ├── hidden_markov_model.py      # HMM Viterbi decoding & Forward algorithm
│   ├── knowledge_base.py           # Academic theory, pseudocode, and viva questions
│   └── assistant_agent.py          # Virtual Assistant natural language processor
│
├── templates/                      # Responsive HTML5 Templates
│   ├── base.html                   # Common layout with sidebar & voice settings
│   ├── index.html                  # Main project dashboard
│   ├── algorithms.html             # Interactive Algorithm Laboratory
│   ├── puzzles.html                # Classical AI Problems (Wumpus, 8-Puzzle, Hanoi)
│   ├── learning.html               # Algorithm Learning Section & Viva Q&A
│   └── chatbot.html                # IntelliAssist Virtual Assistant Interface
│
├── static/                         # Frontend Styling & JavaScript
│   ├── css/
│   │   └── main.css                # Dark navy and purple glassmorphic stylesheet
│   └── js/
│       ├── main.js                 # Web Speech API, voice controls, and assistant
│       └── visualizers.js          # Canvas engines for graphs, grids, charts, and tiles
│
├── documentation/                  # Academic Submission Documentation
│   ├── project_report.md           # Formal college mini-project report
│   └── viva_questions.md           # Top 50 AI Lab viva voce questions & answers
│
└── tests/                          # Automated Unit Test Suite
    └── test_algorithms.py          # Unittest suite covering all 13 algorithms
```

---

## 🚀 Installation & Execution Instructions

### 1. Prerequisites
- Python 3.9 or higher installed on your system.
- Modern web browser (Chrome, Edge, Firefox, or Safari).

### 2. Clone the Repository
```bash
git clone https://github.com/[YOUR-USERNAME]/[YOUR-REPOSITORY].git
cd IntelliAssist
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Web Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:5050
```

---

## 🧪 Running Automated Unit Tests

To verify that all 13 algorithms pass formal test cases:
```bash
python -m unittest discover tests
```
*Expected Output:*
```
Ran 14 tests in 0.020s
OK
```

---

## 🤖 Virtual Assistant Voice Commands

You can speak or type the following commands into the Virtual Assistant:
- *"Run BFS"*
- *"Run DFS"*
- *"Solve 8 puzzle"*
- *"Start Wumpus World"*
- *"Run A star"*
- *"Show Bayesian Network"*
- *"Run Simulated Annealing"*
- *"Explain Hidden Markov Model"*
- *"Explain EM Algorithm"*
- *"What is your project title?"*

---

## 📸 Screenshots Section

| Dashboard & Overview | Algorithm Laboratory |
| :---: | :---: |
| *(Interactive statistics & syllabus breakdown)* | *(Real-time canvas graph search & heuristic grids)* |

| Classical AI Puzzles | Virtual Assistant |
| :---: | :---: |
| *(Wumpus 4x4, 8-Puzzle tile sliding, Hanoi pegs)* | *(Voice-enabled conversational AI agent)* |

---

## 🎓 Academic Submission Details

- **Student Name:** [Your Name]
- **Roll Number:** [Your Roll Number]
- **Class / Semester:** B.Tech CSE (AI) - 6th Semester
- **Lab Course:** Artificial Intelligence Laboratory
- **GitHub Repository URL:** `https://github.com/[YOUR-USERNAME]/intelliassist-ai-assistant`

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
