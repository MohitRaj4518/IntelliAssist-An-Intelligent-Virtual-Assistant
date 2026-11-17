/**
 * IntelliAssist Core JavaScript
 * Manages Web Speech API, Voice Synthesis, Assistant Chat, and Settings.
 */

const AppState = {
  botName: window.APP_BOT_NAME || "IntelliAssist",
  voiceName: localStorage.getItem("intelli_voice") || window.APP_VOICE_NAME || "Samantha",
  voicePitch: parseFloat(localStorage.getItem("intelli_pitch") || window.APP_VOICE_PITCH || 1.1),
  voiceRate: parseFloat(localStorage.getItem("intelli_rate") || window.APP_VOICE_RATE || 1.05),
  speechEnabled: localStorage.getItem("intelli_speech_enabled") !== "false",
  isListening: false
};

// Global Speech Synthesis and Recognition references
let synth = window.speechSynthesis || null;
let recognition = null;
let availableVoices = [];

// Initialize Web Speech Synthesis & Recognition
function initSpeechSystem() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      AppState.isListening = true;
      updateMicUI(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const inputField = document.getElementById("chatInput");
      if (inputField) {
        inputField.value = transcript;
        sendChatMessage(transcript);
      }
    };

    recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      stopListening();
    };

    recognition.onend = () => {
      stopListening();
    };
  }

  // Load and populate available browser voices
  if (synth) {
    const populateVoices = () => {
      availableVoices = synth.getVoices();
      const voiceSelect = document.getElementById("voiceSelect");
      if (voiceSelect && availableVoices.length > 0) {
        voiceSelect.innerHTML = "";
        availableVoices.forEach((v) => {
          const opt = document.createElement("option");
          opt.value = v.name;
          opt.textContent = `${v.name} (${v.lang})`;
          if (v.name === AppState.voiceName) opt.selected = true;
          voiceSelect.appendChild(opt);
        });
      }
    };

    populateVoices();
    if (synth.onvoiceschanged !== undefined) {
      synth.onvoiceschanged = populateVoices;
    }
  }
}

function toggleSpeechListening() {
  if (!recognition) {
    alert("Speech recognition is not supported in this browser. Please type your query in the input bar.");
    return;
  }
  if (AppState.isListening) {
    recognition.stop();
    stopListening();
  } else {
    try {
      recognition.start();
    } catch (e) {
      console.error(e);
    }
  }
}

function stopListening() {
  AppState.isListening = false;
  updateMicUI(false);
}

function updateMicUI(listening) {
  const micBtns = document.querySelectorAll(".mic-toggle-btn");
  micBtns.forEach(btn => {
    if (listening) {
      btn.classList.add("listening");
      btn.title = "Listening... Speak your command";
    } else {
      btn.classList.remove("listening");
      btn.title = "Click to speak";
    }
  });
}

// Speak text using SpeechSynthesis
function speakAssistantResponse(text) {
  if (!AppState.speechEnabled || !synth) return;
  synth.cancel();

  // Strip markdown formatting before speaking
  const plainText = text.replace(/[*_#`]/g, '').replace(/\[.*?\]\(.*?\)/g, '');
  const utterance = new SpeechSynthesisUtterance(plainText);
  utterance.pitch = AppState.voicePitch;
  utterance.rate = AppState.voiceRate;

  if (availableVoices.length > 0) {
    const selected = availableVoices.find(v => v.name === AppState.voiceName);
    if (selected) {
      utterance.voice = selected;
    } else {
      // Fallback: preferred natural/english female voice
      const preferred = availableVoices.find(v => 
        v.lang.startsWith("en") && (v.name.includes("Samantha") || v.name.includes("Victoria") || v.name.includes("Natural") || v.name.includes("Google"))
      );
      if (preferred) utterance.voice = preferred;
    }
  }

  synth.speak(utterance);
}

// Toggle Voice Speech On/Off
function toggleSpeechAudio() {
  AppState.speechEnabled = !AppState.speechEnabled;
  localStorage.setItem("intelli_speech_enabled", AppState.speechEnabled);
  const btn = document.getElementById("speechToggleBtn");
  if (btn) {
    btn.innerHTML = AppState.speechEnabled ? "🔊 Voice: <b>ON</b>" : "🔇 Voice: <b>OFF</b>";
    btn.classList.toggle("active", AppState.speechEnabled);
  }
  if (!AppState.speechEnabled && synth) {
    synth.cancel();
  }
}

// Open / Close Settings Modal
function openSettingsModal() {
  const modal = document.getElementById("settingsModal");
  if (modal) modal.style.display = "flex";
  const nameInput = document.getElementById("settingBotName");
  if (nameInput) nameInput.value = AppState.botName;
}

function closeSettingsModal() {
  const modal = document.getElementById("settingsModal");
  if (modal) modal.style.display = "none";
}

function saveAssistantSettings() {
  const nameInput = document.getElementById("settingBotName");
  const voiceSelect = document.getElementById("voiceSelect");
  const pitchInput = document.getElementById("settingPitch");
  const rateInput = document.getElementById("settingRate");

  if (nameInput && nameInput.value.trim()) {
    AppState.botName = nameInput.value.trim();
  }
  if (voiceSelect && voiceSelect.value) {
    AppState.voiceName = voiceSelect.value;
    localStorage.setItem("intelli_voice", AppState.voiceName);
  }
  if (pitchInput) {
    AppState.voicePitch = parseFloat(pitchInput.value);
    localStorage.setItem("intelli_pitch", AppState.voicePitch);
  }
  if (rateInput) {
    AppState.voiceRate = parseFloat(rateInput.value);
    localStorage.setItem("intelli_rate", AppState.voiceRate);
  }

  // Sync with backend API
  fetch("/api/config", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      bot_name: AppState.botName,
      voice_name: AppState.voiceName,
      voice_pitch: AppState.voicePitch,
      voice_rate: AppState.voiceRate
    })
  }).catch(e => console.warn(e));

  closeSettingsModal();
  speakAssistantResponse(`Configuration updated. I am ${AppState.botName}, operating with audio synthesizer ${AppState.voiceName}.`);
  
  // Update UI brand labels
  document.querySelectorAll(".bot-name-label").forEach(el => el.textContent = AppState.botName);
}

function testAssistantVoice() {
  const nameInput = document.getElementById("settingBotName");
  const voiceSelect = document.getElementById("voiceSelect");
  const pitchInput = document.getElementById("settingPitch");
  const rateInput = document.getElementById("settingRate");

  const testName = (nameInput && nameInput.value.trim()) || AppState.botName;
  const testVoice = (voiceSelect && voiceSelect.value) || AppState.voiceName;
  const testPitch = pitchInput ? parseFloat(pitchInput.value) : AppState.voicePitch;
  const testRate = rateInput ? parseFloat(rateInput.value) : AppState.voiceRate;

  if (!synth) return;
  synth.cancel();

  const phrase = `Hello! I am ${testName}, your AI Lab Virtual Assistant. Ready to demonstrate search and probabilistic algorithms.`;
  const utt = new SpeechSynthesisUtterance(phrase);
  utt.pitch = testPitch;
  utt.rate = testRate;
  if (availableVoices.length > 0) {
    const v = availableVoices.find(voice => voice.name === testVoice);
    if (v) utt.voice = v;
  }
  synth.speak(utt);
}

// Chat Assistant Messaging
async function sendChatMessage(customQuery) {
  const input = document.getElementById("chatInput");
  const query = customQuery || (input ? input.value.trim() : "");
  if (!query) return;

  if (input) input.value = "";
  appendChatBubble("user", query);

  const history = document.getElementById("chatHistory");
  if (history) history.scrollTop = history.scrollHeight;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query })
    });
    const data = await response.json();

    if (data.status === "success" && data.response) {
      appendChatBubble("bot", data.response.text, data.response);
      speakAssistantResponse(data.response.text);
    } else {
      appendChatBubble("bot", "I encountered an error processing your query.");
    }
  } catch (err) {
    appendChatBubble("bot", "Network connection error with assistant backend: " + err.message);
  }

  if (history) history.scrollTop = history.scrollHeight;
}

function appendChatBubble(sender, text, responsePayload = null) {
  const history = document.getElementById("chatHistory");
  if (!history) return;

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender === "user" ? "user-bubble" : "bot-bubble"}`;

  const author = document.createElement("div");
  author.className = "bubble-author";
  author.textContent = sender === "user" ? "You (Student)" : AppState.botName;
  bubble.appendChild(author);

  const textNode = document.createElement("div");
  textNode.innerHTML = formatMarkdownText(text);
  bubble.appendChild(textNode);

  // If algorithm was executed, embed action buttons or results preview
  if (responsePayload && responsePayload.category === "algorithm_execution" && responsePayload.data) {
    const actionCard = document.createElement("div");
    actionCard.style.marginTop = "0.75rem";
    actionCard.style.padding = "0.75rem";
    actionCard.style.background = "rgba(7, 10, 19, 0.75)";
    actionCard.style.borderRadius = "8px";
    actionCard.style.borderLeft = "3px solid #06b6d4";

    const algoId = responsePayload.algorithm_id;
    const isPuzzle = ["wumpus_world", "eight_puzzle", "towers_of_hanoi"].includes(algoId);
    const targetUrl = isPuzzle ? `/puzzles?puzzle=${algoId}` : `/algorithms?id=${algoId}`;

    actionCard.innerHTML = `
      <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:0.4rem;">
        Execution Completed in <b>${responsePayload.data.execution_time_ms || 1.2} ms</b>
      </div>
      <a href="${targetUrl}" class="btn-pill btn-primary" style="font-size:0.78rem; padding:0.35rem 0.8rem;">
        🚀 Open Full Interactive Visualizer
      </a>
    `;
    bubble.appendChild(actionCard);
  }

  // Google Search & Verified Knowledge Source Card
  if (responsePayload && responsePayload.data && responsePayload.data.google_url && !responsePayload.data.url) {
    const gCard = document.createElement("div");
    gCard.style.marginTop = "0.75rem";
    gCard.style.padding = "0.55rem 0.85rem";
    gCard.style.background = "rgba(59, 130, 246, 0.08)";
    gCard.style.borderRadius = "8px";
    gCard.style.border = "1px solid rgba(59, 130, 246, 0.25)";
    const sourceName = responsePayload.data.source || "Web & Google Knowledge";
    gCard.innerHTML = `
      <div style="font-size:0.78rem; color:#93c5fd; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.4rem;">
        <span>🔍 <b>Source:</b> ${sourceName}</span>
        <a href="${responsePayload.data.google_url}" target="_blank" style="color:#60a5fa; text-decoration:underline; font-weight:600;">
          🌐 View on Google Search →
        </a>
      </div>
    `;
    bubble.appendChild(gCard);
  }

  // URL link card (Websites & Chrome searches)
  if (responsePayload && responsePayload.data && responsePayload.data.url) {
    const urlCard = document.createElement("div");
    urlCard.style.marginTop = "0.75rem";
    urlCard.style.padding = "0.6rem 0.85rem";
    urlCard.style.background = "rgba(6, 182, 212, 0.1)";
    urlCard.style.borderRadius = "8px";
    urlCard.style.border = "1px solid rgba(6, 182, 212, 0.3)";
    urlCard.innerHTML = `🌐 <b>Link:</b> <a href="${responsePayload.data.url}" target="_blank" style="color:#06b6d4; text-decoration:underline; word-break:break-all; margin-left:0.3rem;">${responsePayload.data.url}</a>`;
    bubble.appendChild(urlCard);
    if (responsePayload.action === "open_url") {
      try { window.open(responsePayload.data.url, "_blank"); } catch (e) {}
    }
  }

  // Weather card
  if (responsePayload && responsePayload.data && responsePayload.data.temperature) {
    const wCard = document.createElement("div");
    wCard.style.marginTop = "0.75rem";
    wCard.style.padding = "0.75rem";
    wCard.style.background = "rgba(16, 185, 129, 0.1)";
    wCard.style.borderRadius = "8px";
    wCard.style.border = "1px solid rgba(16, 185, 129, 0.3)";
    wCard.innerHTML = `
      <div style="font-size:0.85rem; color:#6ee7b7; font-weight:bold;">🌦️ Weather in ${responsePayload.data.city}:</div>
      <div style="font-size:0.8rem; color:#cbd5e1; margin-top:0.3rem;">
        Condition: <b>${responsePayload.data.description}</b> | Temp: <b>${responsePayload.data.temperature}</b> (Feels like: ${responsePayload.data.feels_like})
      </div>
    `;
    bubble.appendChild(wCard);
  }

  // News headlines card
  if (responsePayload && responsePayload.data && responsePayload.data.headlines) {
    const nCard = document.createElement("div");
    nCard.style.marginTop = "0.75rem";
    nCard.style.padding = "0.75rem";
    nCard.style.background = "rgba(124, 58, 237, 0.1)";
    nCard.style.borderRadius = "8px";
    nCard.style.border = "1px solid rgba(124, 58, 237, 0.3)";
    nCard.innerHTML = `
      <div style="font-size:0.85rem; color:#c4b5fd; font-weight:bold; margin-bottom:0.4rem;">📰 Top Headlines:</div>
      <ul style="padding-left:1.2rem; font-size:0.8rem; line-height:1.5; color:#cbd5e1;">
        ${responsePayload.data.headlines.map(h => `<li>${h}</li>`).join("")}
      </ul>
    `;
    bubble.appendChild(nCard);
  }

  // Trending Movies card
  if (responsePayload && responsePayload.data && responsePayload.data.movies) {
    const mCard = document.createElement("div");
    mCard.style.marginTop = "0.75rem";
    mCard.style.padding = "0.75rem";
    mCard.style.background = "rgba(245, 158, 11, 0.1)";
    mCard.style.borderRadius = "8px";
    mCard.style.border = "1px solid rgba(245, 158, 11, 0.3)";
    mCard.innerHTML = `
      <div style="font-size:0.85rem; color:#fcd34d; font-weight:bold; margin-bottom:0.4rem;">🎬 Trending Releases:</div>
      <ul style="padding-left:1.2rem; font-size:0.8rem; line-height:1.5; color:#cbd5e1;">
        ${responsePayload.data.movies.map((m, i) => `<li><b>#${i+1}</b> ${m}</li>`).join("")}
      </ul>
    `;
    bubble.appendChild(mCard);
  }

  // IP Address card
  if (responsePayload && responsePayload.data && responsePayload.data.ip) {
    const ipCard = document.createElement("div");
    ipCard.style.marginTop = "0.5rem";
    ipCard.style.padding = "0.4rem 0.6rem";
    ipCard.style.background = "rgba(7, 10, 19, 0.7)";
    ipCard.style.borderRadius = "6px";
    ipCard.innerHTML = `🌐 <b>IP Address:</b> <code>${responsePayload.data.ip}</code>`;
    bubble.appendChild(ipCard);
  }

  const timeEl = document.createElement("div");
  timeEl.className = "bubble-time";
  timeEl.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  bubble.appendChild(timeEl);

  history.appendChild(bubble);
}

function formatMarkdownText(txt) {
  // Simple markdown renderer for bold, lists, and line breaks
  return txt
    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>')
    .replace(/• (.*?)(<br>|$)/g, '<li>$1</li>');
}

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  initSpeechSystem();

  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("chatSendBtn");

  if (sendBtn) {
    sendBtn.addEventListener("click", () => sendChatMessage());
  }
  if (chatInput) {
    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") sendChatMessage();
    });
  }
});
