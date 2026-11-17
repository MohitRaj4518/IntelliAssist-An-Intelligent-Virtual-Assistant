"""
JARVIS Virtual Personal Assistant
CLI & Web Entrypoint supporting Cross-Platform Execution (macOS, Windows, Linux).
"""

from datetime import datetime
import os
import sys
from random import choice
from decouple import config
from pprint import pprint

import assistant_engine
from utils import opening_text
from functions.online_ops import (
    find_my_ip,
    get_latest_news,
    get_random_advice,
    get_random_joke,
    get_trending_movies,
    get_weather_report,
    play_on_youtube,
    search_on_google,
    search_on_wikipedia,
    send_email,
    send_whatsapp_message,
)
from functions.os_ops import (
    open_calculator,
    open_camera,
    open_cmd,
    open_notepad,
    open_discord,
)

USERNAME = config('USER', default='User')
BOTNAME = config('BOTNAME', default='JARVIS')

# Initialize Text-to-Speech Engine safely across platforms
engine = None
try:
    import pyttsx3
    if sys.platform == 'win32':
        engine = pyttsx3.init('sapi5')
    elif sys.platform == 'darwin':
        engine = pyttsx3.init('nsss')
    else:
        engine = pyttsx3.init('espeak')
    
    engine.setProperty('rate', 190)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    if voices and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
except Exception:
    engine = None


def speak(text):
    """Speaks text using pyttsx3, macOS say, or terminal print fallback."""
    print(f"[{BOTNAME}]: {text}")
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
            return
        except Exception:
            pass

    # macOS native TTS fallback
    if sys.platform == 'darwin':
        try:
            import subprocess
            subprocess.run(['say', text], check=False)
            return
        except Exception:
            pass


def greet_user():
    """Greets the user according to the time of day."""
    greeting = assistant_engine.get_greeting()
    speak(greeting)


def take_user_input():
    """Takes input via microphone if available, or falls back to keyboard input."""
    # Attempt Speech Recognition
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('\n[Mic] Listening....')
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=10)

        print('[Mic] Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        if not ('exit' in query.lower() or 'stop' in query.lower()):
            speak(choice(opening_text))
        return query
    except Exception:
        # Fallback to keyboard input
        pass

    try:
        query = input(f"\n[{USERNAME}]: ")
        return query
    except (EOFError, KeyboardInterrupt):
        return "exit"


def run_cli():
    """Runs the assistant in interactive CLI mode."""
    greet_user()
    while True:
        query = take_user_input().lower().strip()

        if not query or query == 'none':
            continue

        if 'exit' in query or 'stop' in query or 'quit' in query or 'bye' in query:
            hour = datetime.now().hour
            if 21 <= hour or hour < 6:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day sir!")
            break

        # Process through the assistant engine
        res = assistant_engine.handle_command(query)
        speak(res['text'])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        from app import app, HOST, PORT
        print(f"Starting JARVIS Web Server on http://{HOST}:{PORT}")
        app.run(host=HOST, port=PORT, debug=False)
    else:
        # By default, ask user or start web app if web flag or interactive
        print("=" * 60)
        print(f"  {BOTNAME} Virtual Personal Assistant")
        print("  1. Run in Localhost (Web Interface) -> python3 app.py")
        print("  2. Run in Terminal (CLI Mode)       -> python3 main.py")
        print("=" * 60)
        run_cli()
