"""
IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms
Flask Web Application Server
"""

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, render_template, request

from algorithms.knowledge_base import ALGORITHM_KNOWLEDGE
from algorithms.assistant_agent import process_assistant_query, execute_algorithm_by_id

app = Flask(__name__)

PROJECT_TITLE = "IntelliAssist – An Intelligent Virtual Assistant Using Classical AI Algorithms"
BOT_NAME = os.environ.get("BOT_NAME", "IntelliAssist")
VOICE_NAME = os.environ.get("VOICE_NAME", "Samantha")
VOICE_PITCH = float(os.environ.get("VOICE_PITCH", 1.1))
VOICE_RATE = float(os.environ.get("VOICE_RATE", 1.05))
PORT = int(os.environ.get("PORT", 5050))
HOST = os.environ.get("HOST", "0.0.0.0")


@app.context_processor
def inject_common_variables():
    return {
        "project_title": PROJECT_TITLE,
        "bot_name": BOT_NAME,
        "voice_name": VOICE_NAME,
        "voice_pitch": VOICE_PITCH,
        "voice_rate": VOICE_RATE,
        "total_algorithms": 13,
        "algorithm_groups": [
            {"id": 1, "name": "Search & Optimization", "count": 4, "badge": "DFS, BFS, IDS, SA"},
            {"id": 2, "name": "Classical AI Problems", "count": 3, "badge": "Wumpus, 8-Puzzle, Hanoi"},
            {"id": 3, "name": "Informed Search & Optimization", "count": 3, "badge": "A*, D*, Hill Climbing"},
            {"id": 4, "name": "Probabilistic Artificial Intelligence", "count": 3, "badge": "Bayes Net, EM, HMM"}
        ]
    }


# =====================================================================
# PAGE ROUTES
# =====================================================================

@app.route("/")
def index():
    """Main Dashboard with stats, syllabus breakdown, and quick access."""
    return render_template("index.html", active_page="dashboard")


@app.route("/algorithms")
def algorithms_page():
    """Interactive Algorithm Lab for Search, Informed Search, and Probabilistic AI."""
    selected_id = request.args.get("id", "bfs")
    return render_template("algorithms.html", active_page="algorithms", selected_algo=selected_id)


@app.route("/puzzles")
def puzzles_page():
    """Interactive Classic AI Problems: Wumpus World, 8-Puzzle, and Towers of Hanoi."""
    selected_puzzle = request.args.get("puzzle", "wumpus")
    return render_template("puzzles.html", active_page="puzzles", selected_puzzle=selected_puzzle)


@app.route("/learning")
def learning_page():
    """Comprehensive Algorithm Learning Portal with Pseudocode, Complexities & Viva Q&A."""
    selected_id = request.args.get("id", "bfs")
    return render_template(
        "learning.html",
        active_page="learning",
        all_algorithms=ALGORITHM_KNOWLEDGE,
        selected_id=selected_id
    )


@app.route("/chatbot")
def chatbot_page():
    """IntelliAssist Virtual Assistant Chat Interface."""
    return render_template("chatbot.html", active_page="chatbot")


# =====================================================================
# REST API ENDPOINTS
# =====================================================================

@app.route("/api/run_algorithm", methods=["POST"])
def api_run_algorithm():
    """Executes any algorithm and returns rich JSON execution trace for visualization."""
    data = request.get_json(silent=True) or {}
    algo_id = data.get("algorithm_id", "").lower().strip()
    params = data.get("params", {})

    if not algo_id:
        return jsonify({"status": "error", "message": "Missing 'algorithm_id' parameter."}), 400

    try:
        result = execute_algorithm_by_id(algo_id, params)
        return jsonify({
            "status": "success",
            "algorithm_id": algo_id,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Execution error in {algo_id}: {str(e)}"
        }), 500


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Processes natural language query from Virtual Assistant."""
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or data.get("message") or "").strip()

    if not query:
        return jsonify({"status": "error", "message": "Query cannot be empty."}), 400

    response_data = process_assistant_query(query)
    return jsonify({
        "status": "success",
        "query": query,
        "bot_name": BOT_NAME,
        "response": response_data
    })


@app.route("/api/algorithm_info/<algo_id>", methods=["GET"])
def api_algorithm_info(algo_id):
    """Fetches theoretical metadata, pseudocode, and viva Q&A for an algorithm."""
    clean_id = algo_id.lower().strip()
    if clean_id in ALGORITHM_KNOWLEDGE:
        return jsonify({
            "status": "success",
            "data": ALGORITHM_KNOWLEDGE[clean_id]
        })
    return jsonify({"status": "error", "message": f"Algorithm '{algo_id}' not found."}), 404


@app.route("/api/config", methods=["POST"])
def api_config():
    """Updates Assistant Name and Voice Settings."""
    global BOT_NAME, VOICE_NAME, VOICE_PITCH, VOICE_RATE
    data = request.get_json(silent=True) or {}
    new_name = data.get("bot_name", "").strip()
    new_voice = data.get("voice_name", "").strip()
    new_pitch = data.get("voice_pitch")
    new_rate = data.get("voice_rate")

    if new_name:
        BOT_NAME = new_name
    if new_voice:
        VOICE_NAME = new_voice
    if new_pitch is not None:
        try: VOICE_PITCH = float(new_pitch)
        except Exception: pass
    if new_rate is not None:
        try: VOICE_RATE = float(new_rate)
        except Exception: pass

    return jsonify({
        "status": "success",
        "bot_name": BOT_NAME,
        "voice_name": VOICE_NAME,
        "voice_pitch": VOICE_PITCH,
        "voice_rate": VOICE_RATE
    })


@app.route("/api/stats", methods=["GET"])
def api_stats():
    """Returns application metrics."""
    return jsonify({
        "project_title": PROJECT_TITLE,
        "total_algorithms": 13,
        "algorithm_groups": 4,
        "status": "operational",
        "bot_name": BOT_NAME,
        "version": "1.0.0"
    })


if __name__ == "__main__":
    print("=" * 70)
    print(f"  {PROJECT_TITLE}")
    print(f"  Server starting on http://127.0.0.1:{PORT}")
    print(f"  Virtual Assistant: {BOT_NAME} (Voice: {VOICE_NAME})")
    print("=" * 70)
    app.run(host=HOST, port=PORT, debug=False)
