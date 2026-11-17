"""
Core Assistant Engine for JARVIS Virtual Personal Assistant.
Handles command interpretation, execution, and response generation.
"""

from datetime import datetime
import os
import random
import re
import sys
from decouple import config
from utils import opening_text
from functions.online_ops import (
    find_my_ip,
    fetch_web_google_answer,
    get_direct_answer,
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
    open_discord,
    open_notepad,
    open_in_chrome,
    resolve_website_url,
    search_on_chrome,
    COMMON_WEBSITES,
)

USERNAME = config('USER', default='User')
BOTNAME = config('BOTNAME', default='IntelliAssist')


def get_greeting():
    """Generates a context-aware greeting based on the current hour."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        period = "Good morning"
    elif 12 <= hour < 17:
        period = "Good afternoon"
    elif 17 <= hour < 22:
        period = "Good evening"
    else:
        period = "Hello"
    return f"{period} {USERNAME}! I am {BOTNAME}, your virtual personal assistant. How may I assist you today?"


def handle_command(query_text: str) -> dict:
    """
    Analyzes and executes the given command query.
    Returns a dict with 'text', 'category', 'action', and 'data'.
    """
    if not query_text:
        return {
            "text": "I didn't catch that. Could you please repeat?",
            "category": "error",
            "action": None,
            "data": None
        }

    q = query_text.strip().lower()

    # Greeting / Identity
    if any(k in q for k in ['who are you', 'what is your name', 'your identity']):
        return {
            "text": f"I am {BOTNAME}, your Virtual Personal Assistant. I can check the weather, fetch latest news, search Wikipedia, find movies, tell jokes, give advice, open applications, and search the web for you.",
            "category": "info",
            "action": None,
            "data": {"botname": BOTNAME, "username": USERNAME}
        }

    if any(k in q for k in ['hello', 'hey jarvis', 'hi jarvis', 'wake up']):
        return {
            "text": get_greeting(),
            "category": "greeting",
            "action": None,
            "data": None
        }

    # Time & Date
    if any(k in q for k in ['what time is it', 'current time', 'tell me the time', 'what is the time']):
        now = datetime.now().strftime("%I:%M %p")
        return {
            "text": f"The current time is {now}.",
            "category": "time",
            "action": None,
            "data": {"time": now}
        }

    if any(k in q for k in ['today\'s date', 'what is the date', 'current date']):
        today = datetime.now().strftime("%A, %B %d, %Y")
        return {
            "text": f"Today is {today}.",
            "category": "date",
            "action": None,
            "data": {"date": today}
        }

    # System OS Operations
    if 'calculator' in q:
        msg = open_calculator()
        return {
            "text": f"Opening calculator sir.",
            "category": "system",
            "action": "open_calculator",
            "data": {"message": msg}
        }

    if any(k in q for k in ['open camera', 'take a photo', 'photo booth']):
        msg = open_camera()
        return {
            "text": "Opening camera for you sir.",
            "category": "system",
            "action": "open_camera",
            "data": {"message": msg}
        }

    if any(k in q for k in ['open command prompt', 'open cmd', 'open terminal']):
        msg = open_cmd()
        return {
            "text": "Opening terminal / command line interface sir.",
            "category": "system",
            "action": "open_terminal",
            "data": {"message": msg}
        }

    if any(k in q for k in ['notepad', 'text editor', 'textedit']):
        msg = open_notepad()
        return {
            "text": "Opening text editor sir.",
            "category": "system",
            "action": "open_notepad",
            "data": {"message": msg}
        }

    if 'discord' in q:
        msg = open_discord()
        return {
            "text": f"{msg} sir.",
            "category": "system",
            "action": "open_discord",
            "data": {"message": msg}
        }

    # IP Address
    if any(k in q for k in ['ip address', 'my ip', 'what is my ip']):
        ip = find_my_ip()
        return {
            "text": f"Your IP Address is {ip}. I have displayed it on your screen sir.",
            "category": "network",
            "action": None,
            "data": {"ip": ip}
        }

    # Joke
    if 'joke' in q:
        joke = get_random_joke()
        return {
            "text": f"Here is one: {joke}",
            "category": "joke",
            "action": None,
            "data": {"joke": joke}
        }

    # Advice
    if 'advice' in q:
        advice = get_random_advice()
        return {
            "text": f"Here is a piece of advice sir: {advice}",
            "category": "advice",
            "action": None,
            "data": {"advice": advice}
        }

    # Trending Movies
    if any(k in q for k in ['trending movies', 'movie recommendation', 'top movies', 'latest movies']):
        movies = get_trending_movies()
        movie_str = ", ".join(movies[:5])
        return {
            "text": f"Some of the top trending movies right now are: {movie_str}.",
            "category": "movies",
            "action": None,
            "data": {"movies": movies}
        }

    # News
    if any(k in q for k in ['news', 'headlines', 'latest news']):
        news = get_latest_news()
        headline_summary = " Here are the top headlines: " + "; ".join(news[:3])
        return {
            "text": f"I've fetched the latest headlines sir.{headline_summary}",
            "category": "news",
            "action": None,
            "data": {"headlines": news}
        }

    # Weather
    if 'weather' in q:
        city_match = re.search(r'weather (?:in|for|at) ([a-zA-Z\s]+)', q)
        city = city_match.group(1).strip() if city_match else "Delhi"
        weather_desc, temp, feels = get_weather_report(city)
        return {
            "text": f"In {city.title()}, the weather is currently {weather_desc} with a temperature of {temp}, feeling like {feels}.",
            "category": "weather",
            "action": None,
            "data": {
                "city": city.title(),
                "description": weather_desc,
                "temperature": temp,
                "feels_like": feels
            }
        }

    # Wikipedia
    if 'wikipedia' in q:
        search_term = q.replace('search on wikipedia', '').replace('wikipedia', '').replace('search', '').strip()
        if not search_term:
            return {
                "text": "What topic would you like to search on Wikipedia sir?",
                "category": "wikipedia_prompt",
                "action": None,
                "data": None
            }
        result = search_on_wikipedia(search_term)
        return {
            "text": f"According to Wikipedia: {result}",
            "category": "wikipedia",
            "action": "open_wikipedia",
            "data": {"query": search_term, "summary": result}
        }

    # Chrome Application Launch
    if any(k in q for k in ['open chrome', 'launch chrome', 'start chrome', 'open google chrome', 'open browser']):
        msg = open_in_chrome()
        return {
            "text": "Opening Google Chrome sir.",
            "category": "system",
            "action": "open_chrome",
            "data": {"message": msg}
        }

    # Search on Chrome / Google
    if any(k in q for k in [
        'search on chrome', 'search in chrome', 'chrome search',
        'search on google', 'search google', 'google search',
        'search in google', 'search the web for', 'search web for', 'search for'
    ]):
        if 'wikipedia' not in q:
            target, url, status = search_on_chrome(query_text)
            direct_ans, source, _ = fetch_web_google_answer(target)
            return {
                "text": f"Searching for '{target}' on Google Chrome sir.\n\nHere is what I found: {direct_ans}",
                "category": "chrome_search",
                "action": "open_url",
                "data": {
                    "url": url,
                    "query": target,
                    "status": status,
                    "answer": direct_ans,
                    "source": source,
                    "google_url": url
                }
            }

    # Open Any Website (in Chrome / Browser)
    is_open_site_command = False
    for prefix in ['open website', 'open site', 'open page', 'go to website', 'go to', 'launch website', 'launch site']:
        if q.startswith(prefix):
            is_open_site_command = True
            break

    if not is_open_site_command and q.startswith('open '):
        target_name = q[5:].replace('in chrome', '').replace('on chrome', '').strip()
        system_tools = [
            'calculator', 'calc', 'camera', 'photo booth', 'terminal', 'cmd',
            'command prompt', 'notepad', 'textedit', 'discord', 'chrome'
        ]
        if target_name and target_name not in system_tools:
            if target_name in COMMON_WEBSITES or '.' in target_name or ' ' not in target_name or 'chrome' in q:
                is_open_site_command = True

    if is_open_site_command:
        site_name, url = resolve_website_url(query_text)
        if url:
            status = open_in_chrome(url)
            return {
                "text": f"Opening {site_name} on Chrome sir.",
                "category": "chrome_open",
                "action": "open_url",
                "data": {"url": url, "site": site_name, "status": status}
            }

    # YouTube
    if 'youtube' in q:
        video_query = q.replace('play on youtube', '').replace('search on youtube', '').replace('play', '').replace('youtube', '').strip()
        target = video_query if video_query else "Trending music"
        url = play_on_youtube(target)
        return {
            "text": f"Playing {target} on YouTube sir.",
            "category": "youtube",
            "action": "open_url",
            "data": {"url": url, "query": target}
        }

    # WhatsApp Message
    if 'whatsapp' in q:
        return {
            "text": "To send a WhatsApp message, please provide the recipient number and message in the console or web form.",
            "category": "whatsapp",
            "action": "prompt_whatsapp",
            "data": None
        }

    # Email
    if 'email' in q:
        return {
            "text": "To send an email, please verify your EMAIL and PASSWORD credentials are configured in your .env file.",
            "category": "email",
            "action": "prompt_email",
            "data": None
        }

    # Help
    if 'help' in q or 'what can you do' in q:
        return {
            "text": "You can ask me to: check the weather in any city, get the latest news headlines, tell a joke, give advice, show trending movies, search Wikipedia, play videos on YouTube, search Google, show your IP address, or launch system tools like the calculator, camera, terminal, and notepad.",
            "category": "help",
            "action": None,
            "data": None
        }

    # Direct Question Answering (Searches Google & Web Knowledge Base for ANY question)
    answer, source, google_url = fetch_web_google_answer(query_text)
    return {
        "text": answer,
        "category": "answer",
        "action": None,
        "data": {
            "query": query_text,
            "answer": answer,
            "source": source,
            "google_url": google_url
        }
    }
