/**
 * IntelliAssist Interactive Algorithm Visualizer Engine
 * Implements Canvas & DOM-based dynamic visualizations for all 13 AI algorithms:
 * Graph Traversals (DFS, BFS, IDS), Optimization (SA, Hill Climbing),
 * Classical Puzzles (Wumpus World, 8-Puzzle, Towers of Hanoi),
 * Informed Search (A*, D* Lite), and Probabilistic AI (Bayesian Net, EM, HMM).
 */

const VisualizerEngine = {
  activeAnimationTimer: null,
  stepIndex: 0,
  maxSteps: 0,
  isPlaying: false,

  // ===================================================================
  // 1. GRAPH TRAVERSAL VISUALIZER (DFS, BFS, IDS)
  // ===================================================================
  renderGraphSearch: function(canvasId, resultData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 700;
    const height = canvas.height = 420;

    const nodePositions = {
      'A': { x: width * 0.12, y: height * 0.45 },
      'B': { x: width * 0.32, y: height * 0.25 },
      'C': { x: width * 0.32, y: height * 0.65 },
      'D': { x: width * 0.52, y: height * 0.15 },
      'E': { x: width * 0.52, y: height * 0.38 },
      'F': { x: width * 0.52, y: height * 0.60 },
      'G': { x: width * 0.52, y: height * 0.82 },
      'H': { x: width * 0.72, y: height * 0.15 },
      'I': { x: width * 0.72, y: height * 0.32 },
      'J': { x: width * 0.72, y: height * 0.48 }, // Default Goal
      'K': { x: width * 0.72, y: height * 0.65 },
      'L': { x: width * 0.72, y: height * 0.82 }
    };

    const graph = resultData.graph || {
      'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F', 'G'],
      'D': ['H'], 'E': ['I', 'J'], 'F': ['K'], 'G': ['L']
    };

    const traversal = resultData.traversal_order || [];
    const finalPath = resultData.path || [];

    function draw(currentStep) {
      ctx.clearRect(0, 0, width, height);

      // Draw Edges
      for (const [node, neighbors] of Object.entries(graph)) {
        const p1 = nodePositions[node];
        if (!p1) continue;

        neighbors.forEach(nbr => {
          const p2 = nodePositions[nbr];
          if (!p2) return;

          // Check if edge is in final path
          let isPathEdge = false;
          for (let i = 0; i < finalPath.length - 1; i++) {
            if ((finalPath[i] === node && finalPath[i + 1] === nbr) || (finalPath[i] === nbr && finalPath[i + 1] === node)) {
              isPathEdge = true;
              break;
            }
          }

          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.lineWidth = isPathEdge ? 4 : 1.5;
          ctx.strokeStyle = isPathEdge ? '#06b6d4' : 'rgba(148, 163, 184, 0.25)';
          ctx.stroke();
        });
      }

      // Draw Nodes
      const visitedSoFar = traversal.slice(0, currentStep + 1);

      for (const [node, pos] of Object.entries(nodePositions)) {
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, 22, 0, Math.PI * 2);

        let fillColor = '#10172c';
        let strokeColor = '#475569';
        let textColor = '#cbd5e1';

        if (node === resultData.start) {
          strokeColor = '#10b981';
          fillColor = 'rgba(16, 185, 129, 0.25)';
        }
        if (node === resultData.goal) {
          strokeColor = '#f59e0b';
          fillColor = 'rgba(245, 158, 11, 0.25)';
        }
        if (visitedSoFar.includes(node)) {
          fillColor = 'rgba(124, 58, 237, 0.35)';
          strokeColor = '#7c3aed';
        }
        if (finalPath.includes(node) && currentStep >= traversal.length - 1) {
          fillColor = 'rgba(6, 182, 212, 0.35)';
          strokeColor = '#06b6d4';
          textColor = '#ffffff';
        }

        ctx.fillStyle = fillColor;
        ctx.fill();
        ctx.lineWidth = 2.5;
        ctx.strokeStyle = strokeColor;
        ctx.stroke();

        ctx.fillStyle = textColor;
        ctx.font = 'bold 14px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(node, pos.x, pos.y);
      }
    }

    // Interactive step-by-step animation
    let step = 0;
    draw(traversal.length); // Initial complete render
    return {
      play: function() {
        step = 0;
        clearInterval(VisualizerEngine.activeAnimationTimer);
        VisualizerEngine.activeAnimationTimer = setInterval(() => {
          if (step < traversal.length) {
            draw(step);
            step++;
          } else {
            clearInterval(VisualizerEngine.activeAnimationTimer);
          }
        }, 350);
      },
      showFull: function() {
        clearInterval(VisualizerEngine.activeAnimationTimer);
        draw(traversal.length);
      }
    };
  },

  // ===================================================================
  // 2. 8-PUZZLE VISUALIZER
  // ===================================================================
  renderEightPuzzle: function(containerId, steps) {
    const container = document.getElementById(containerId);
    if (!container || !steps || steps.length === 0) return;

    let currentStep = 0;

    function renderBoard(stepObj) {
      const board = stepObj.board;
      let html = `<div class="eight-puzzle-board">`;
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const val = board[r][c];
          if (val === 0) {
            html += `<div class="puzzle-tile blank"></div>`;
          } else {
            html += `<div class="puzzle-tile">${val}</div>`;
          }
        }
      }
      html += `</div>`;
      html += `
        <div style="margin-top:1rem; text-align:center;">
          <span class="metric-chip">Step: <b>${stepObj.step} / ${steps.length - 1}</b></span>
          <span class="metric-chip">Move: <b>${stepObj.move}</b></span>
          <span class="metric-chip">Manhattan Dist: <b>${stepObj.manhattan_dist}</b></span>
        </div>
      `;
      container.innerHTML = html;
    }

    renderBoard(steps[0]);

    return {
      stepNext: function() {
        if (currentStep < steps.length - 1) {
          currentStep++;
          renderBoard(steps[currentStep]);
        }
      },
      stepPrev: function() {
        if (currentStep > 0) {
          currentStep--;
          renderBoard(steps[currentStep]);
        }
      },
      play: function(onComplete) {
        clearInterval(VisualizerEngine.activeAnimationTimer);
        VisualizerEngine.activeAnimationTimer = setInterval(() => {
          if (currentStep < steps.length - 1) {
            currentStep++;
            renderBoard(steps[currentStep]);
          } else {
            clearInterval(VisualizerEngine.activeAnimationTimer);
            if (onComplete) onComplete();
          }
        }, 600);
      },
      reset: function() {
        clearInterval(VisualizerEngine.activeAnimationTimer);
        currentStep = 0;
        renderBoard(steps[0]);
      }
    };
  },

  // ===================================================================
  // 3. TOWERS OF HANOI VISUALIZER
  // ===================================================================
  renderTowersOfHanoi: function(containerId, steps, numDisks) {
    const container = document.getElementById(containerId);
    if (!container || !steps || steps.length === 0) return;

    let currentStep = 0;
    const colors = ["#f43f5e", "#f59e0b", "#10b981", "#06b6d4", "#6366f1", "#8b5cf6", "#ec4899"];

    function renderStage(stepObj) {
      const pegs = stepObj.pegs;
      let html = `<div class="hanoi-stage">`;

      ["A", "B", "C"].forEach(pegName => {
        const diskList = pegs[pegName] || [];
        html += `
          <div class="hanoi-peg-col">
            <div class="hanoi-peg-rod"></div>
            <div class="hanoi-disk-stack">
        `;
        diskList.forEach(d => {
          const widthPct = 25 + (d / numDisks) * 70;
          const bg = colors[(d - 1) % colors.length];
          html += `<div class="hanoi-disk" style="width:${widthPct}%; background:${bg};">${d}</div>`;
        });
        html += `
            </div>
            <div style="font-size:0.85rem; font-weight:bold; margin-top:8px; z-index:3;">Peg ${pegName}</div>
          </div>
        `;
      });

      html += `</div>`;
      html += `
        <div style="margin-top:1rem; display:flex; justify-content:center; gap:1rem;">
          <span class="metric-chip">Move: <b>${stepObj.step} / ${steps.length - 1}</b></span>
          <span class="metric-chip">Action: <b>${stepObj.action}</b></span>
        </div>
      `;
      container.innerHTML = html;
    }

    renderStage(steps[0]);

    return {
      stepNext: function() {
        if (currentStep < steps.length - 1) {
          currentStep++;
          renderStage(steps[currentStep]);
        }
      },
      stepPrev: function() {
        if (currentStep > 0) {
          currentStep--;
          renderStage(steps[currentStep]);
        }
      },
      play: function() {
        clearInterval(VisualizerEngine.activeAnimationTimer);
        VisualizerEngine.activeAnimationTimer = setInterval(() => {
          if (currentStep < steps.length - 1) {
            currentStep++;
            renderStage(steps[currentStep]);
          } else {
            clearInterval(VisualizerEngine.activeAnimationTimer);
          }
        }, 500);
      },
      reset: function() {
        clearInterval(VisualizerEngine.activeAnimationTimer);
        currentStep = 0;
        renderStage(steps[0]);
      }
    };
  },

  // ===================================================================
  // 4. WUMPUS WORLD VISUALIZER
  // ===================================================================
  renderWumpusWorld: function(containerId, worldData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const steps = worldData.steps || [];
    let currentStepIdx = 0;

    function renderGridAtStep(stepObj) {
      const agentPos = stepObj.agent_pos;
      const visited = stepObj.visited_cells.map(p => `${p[0]},${p[1]}`);
      const safe = stepObj.safe_cells.map(p => `${p[0]},${p[1]}`);

      const wumpus = worldData.wumpus_pos;
      const gold = worldData.gold_pos;
      const pits = worldData.pits.map(p => `${p[0]},${p[1]}`);

      let html = `<div style="display:flex; gap:1.5rem; flex-wrap:wrap; align-items:flex-start;">`;
      html += `<div class="wumpus-grid">`;

      // 4x4 grid (row 3 at top down to row 0 at bottom)
      for (let r = 3; r >= 0; r--) {
        for (let c = 0; c < 4; c++) {
          const coordKey = `${r},${c}`;
          const isAgent = agentPos[0] === r && agentPos[1] === c;
          const isWumpus = wumpus[0] === r && wumpus[1] === c;
          const isGold = gold[0] === r && gold[1] === c;
          const isPit = pits.includes(coordKey);
          const isVisited = visited.includes(coordKey);
          const isSafe = safe.includes(coordKey);

          let cellClass = "wumpus-cell";
          if (isVisited) cellClass += " visited";
          else if (isSafe) cellClass += " safe";

          html += `<div class="${cellClass}" title="Coord: (${r}, ${c})">`;
          html += `<span style="position:absolute; top:2px; left:4px; font-size:0.6rem; color:#64748b;">${r},${c}</span>`;

          if (isAgent) {
            html += `<span class="cell-agent">🤖</span>`;
          } else if (isGold && stepObj.has_gold === false) {
            html += `<span class="cell-gold">💰</span>`;
          } else if (isWumpus) {
            html += `<span class="cell-wumpus">👹</span>`;
          } else if (isPit) {
            html += `<span class="cell-pit">🕳️</span>`;
          }

          // Percept badges
          if (isVisited) {
            let clues = [];
            if (stepObj.percepts && isAgent) {
              if (stepObj.percepts.breeze) clues.push("💨 Breeze");
              if (stepObj.percepts.stench) clues.push("🦨 Stench");
              if (stepObj.percepts.glitter) clues.push("✨ Glitter");
            }
            if (clues.length > 0) {
              html += `<div style="font-size:0.55rem; color:#fcd34d; margin-top:2px;">${clues.join(" ")}</div>`;
            }
          }

          html += `</div>`;
        }
      }
      html += `</div>`;

      // Reasoning sidebar
      html += `
        <div style="flex:1; min-width:280px; background:rgba(7,10,19,0.85); border:1px solid rgba(148,163,184,0.15); border-radius:12px; padding:1.2rem;">
          <h4 style="color:#06b6d4; font-size:0.9rem; margin-bottom:0.75rem;">Step ${stepObj.step}: ${stepObj.action}</h4>
          <div style="font-size:0.8rem; margin-bottom:0.6rem;">
            Score: <b style="color:${stepObj.score >= 0 ? '#10b981':'#f43f5e'};">${stepObj.score}</b> |
            Status: <b>${stepObj.is_alive ? (stepObj.has_gold ? '🏆 WON!':'Active'):'💀 DEAD'}</b>
          </div>
          <div style="font-size:0.78rem; color:#94a3b8; margin-bottom:0.5rem;">Knowledge Base Deductions:</div>
          <ul style="font-size:0.78rem; line-height:1.45; padding-left:1.2rem; color:#cbd5e1;">
            ${(stepObj.reasoning || []).map(r => `<li>${r}</li>`).join("")}
          </ul>
        </div>
      `;
      html += `</div>`;

      container.innerHTML = html;
    }

    if (steps.length > 0) renderGridAtStep(steps[0]);

    return {
      stepNext: function() {
        if (currentStepIdx < steps.length - 1) {
          currentStepIdx++;
          renderGridAtStep(steps[currentStepIdx]);
        }
      },
      stepPrev: function() {
        if (currentStepIdx > 0) {
          currentStepIdx--;
          renderGridAtStep(steps[currentStepIdx]);
        }
      },
      play: function() {
        clearInterval(VisualizerEngine.activeAnimationTimer);
        VisualizerEngine.activeAnimationTimer = setInterval(() => {
          if (currentStepIdx < steps.length - 1) {
            currentStepIdx++;
            renderGridAtStep(steps[currentStepIdx]);
          } else {
            clearInterval(VisualizerEngine.activeAnimationTimer);
          }
        }, 1200);
      },
      reset: function() {
        clearInterval(VisualizerEngine.activeAnimationTimer);
        currentStepIdx = 0;
        renderGridAtStep(steps[0]);
      }
    };
  },

  // ===================================================================
  // 5. A* & D* 2D GRID PATHFINDING VISUALIZER
  // ===================================================================
  renderGridPath: function(canvasId, gridData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const rows = gridData.grid_rows || 10;
    const cols = gridData.grid_cols || 10;
    const size = Math.min(canvas.parentElement.clientWidth / cols, 42);
    canvas.width = cols * size;
    canvas.height = rows * size;

    const obstacles = (gridData.obstacles || gridData.initial_obstacles || []).map(p => `${p[0]},${p[1]}`);
    const path = (gridData.path || gridData.full_final_path || []).map(p => `${p[0]},${p[1]}`);
    const explored = (gridData.explored_nodes || []).map(p => `${p[0]},${p[1]}`);
    const dynObs = gridData.dynamic_obstacle ? `${gridData.dynamic_obstacle[0]},${gridData.dynamic_obstacle[1]}` : null;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const key = `${r},${c}`;
        const x = c * size;
        const y = r * size;

        let fill = '#0a0f21';
        let stroke = 'rgba(148, 163, 184, 0.12)';

        if (obstacles.includes(key)) {
          fill = '#1e1b4b'; // Obstacle wall
          stroke = '#4338ca';
        } else if (key === dynObs) {
          fill = '#e11d48'; // Dynamic obstacle
          stroke = '#f43f5e';
        } else if (r === gridData.start[0] && c === gridData.start[1]) {
          fill = '#10b981'; // Start
        } else if (r === gridData.goal[0] && c === gridData.goal[1]) {
          fill = '#f59e0b'; // Goal
        } else if (path.includes(key)) {
          fill = '#06b6d4'; // Path
        } else if (explored.includes(key)) {
          fill = 'rgba(124, 58, 237, 0.18)'; // Explored
        }

        ctx.fillStyle = fill;
        ctx.fillRect(x, y, size, size);
        ctx.strokeStyle = stroke;
        ctx.strokeRect(x, y, size, size);

        // Labels for Start and Goal
        if (r === gridData.start[0] && c === gridData.start[1]) {
          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 12px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText("S", x + size / 2, y + size / 2);
        } else if (r === gridData.goal[0] && c === gridData.goal[1]) {
          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 12px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText("G", x + size / 2, y + size / 2);
        }
      }
    }
  },

  // ===================================================================
  // 6. CONTINUOUS OPTIMIZATION / HILL CLIMBING LANDSCAPE
  // ===================================================================
  renderHillClimbingLandscape: function(canvasId, hillData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 700;
    const height = canvas.height = 360;

    const landscape = hillData.landscape || [];
    const steps = hillData.steps || [];

    const pad = 45;
    const plotW = width - pad * 2;
    const plotH = height - pad * 2;

    const minX = 0, maxX = 12;
    const minY = 0, maxY = 5.0;

    function toCanvasX(x) { return pad + ((x - minX) / (maxX - minX)) * plotW; }
    function toCanvasY(y) { return height - pad - ((y - minY) / (maxY - minY)) * plotH; }

    ctx.clearRect(0, 0, width, height);

    // Axes
    ctx.beginPath();
    ctx.moveTo(pad, pad);
    ctx.lineTo(pad, height - pad);
    ctx.lineTo(width - pad, height - pad);
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Draw Function Curve
    ctx.beginPath();
    landscape.forEach((pt, idx) => {
      const cx = toCanvasX(pt.x);
      const cy = toCanvasY(pt.y);
      if (idx === 0) ctx.moveTo(cx, cy);
      else ctx.lineTo(cx, cy);
    });
    ctx.strokeStyle = '#8b5cf6';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Fill under curve
    ctx.lineTo(toCanvasX(12), height - pad);
    ctx.lineTo(toCanvasX(0), height - pad);
    ctx.fillStyle = 'rgba(124, 58, 237, 0.08)';
    ctx.fill();

    // Plot Climber Path Steps
    steps.forEach((st, idx) => {
      const cx = toCanvasX(st.x);
      const cy = toCanvasY(st.y);

      ctx.beginPath();
      ctx.arc(cx, cy, idx === steps.length - 1 ? 7 : 4, 0, Math.PI * 2);
      ctx.fillStyle = idx === steps.length - 1 ? '#06b6d4' : '#f59e0b';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.stroke();
    });

    // Label Peak Classification
    ctx.fillStyle = '#06b6d4';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(`Result: ${hillData.status}`, width - pad, pad + 15);
  },

  // ===================================================================
  // 7. LINE CHART PLOTTER (Simulated Annealing & EM Log-Likelihood)
  // ===================================================================
  renderLineChart: function(canvasId, labels, dataPoints, title, color = '#06b6d4') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 650;
    const height = canvas.height = 300;

    const pad = 45;
    const plotW = width - pad * 2;
    const plotH = height - pad * 2;

    if (!dataPoints || dataPoints.length === 0) return;

    const minY = Math.min(...dataPoints);
    const maxY = Math.max(...dataPoints);
    const rangeY = (maxY - minY) || 1;

    function toX(i) { return pad + (i / (dataPoints.length - 1)) * plotW; }
    function toY(val) { return height - pad - ((val - minY) / rangeY) * plotH; }

    ctx.clearRect(0, 0, width, height);

    // Axes
    ctx.beginPath();
    ctx.moveTo(pad, pad);
    ctx.lineTo(pad, height - pad);
    ctx.lineTo(width - pad, height - pad);
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Curve
    ctx.beginPath();
    dataPoints.forEach((val, i) => {
      const cx = toX(i);
      const cy = toY(val);
      if (i === 0) ctx.moveTo(cx, cy);
      else ctx.lineTo(cx, cy);
    });
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Title & Min/Max
    ctx.fillStyle = '#cbd5e1';
    ctx.font = '12px sans-serif';
    ctx.fillText(`${title} (Min: ${minY.toFixed(1)}, Max: ${maxY.toFixed(1)})`, pad, pad - 10);
  }
};
