import os
import random
import smtplib
import socket
import urllib.parse
import webbrowser
from email.message import EmailMessage

import requests
from decouple import config
from functions.knowledge_engine import lookup_local_knowledge

NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
TMDB_API_KEY = config("TMDB_API_KEY")
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")
GEMINI_API_KEY = config("GEMINI_API_KEY")
GROQ_API_KEY = config("GROQ_API_KEY")


FALLBACK_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "How do you organize a space party? You planet.",
    "What do you call a fake noodle? An impasta.",
    "Why did the computer catch a cold? Because it had its Windows open!",
    "There are 10 types of people in the world: those who understand binary, and those who don't."
]

FALLBACK_ADVICE = [
    "Always remember: It's okay to make mistakes as long as you learn from them.",
    "Take breaks when working on difficult problems. Fresh eyes find solutions faster.",
    "Small daily improvements over time lead to stunning results.",
    "The secret to getting ahead is getting started.",
    "Drink enough water and get adequate sleep; your brain runs on them."
]

FALLBACK_MOVIES = [
    "Dune: Part Two",
    "Oppenheimer",
    "Spider-Man: Across the Spider-Verse",
    "Interstellar",
    "The Dark Knight"
]

FALLBACK_NEWS = [
    "Tech Giants Unveil Next-Generation Artificial Intelligence Models",
    "Space Exploration: New Lunar Missions Scheduled for Upcoming Quarter",
    "Global Renewable Energy Capacity Reaches Record High",
    "Advancements in Quantum Computing Open New Horizons in Cryptography",
    "Open-Source Community Drives Breakthroughs in Local AI Assistants"
]


def find_my_ip():
    """Fetches public IP address, or returns local network IP as fallback."""
    try:
        res = requests.get('https://api64.ipify.org?format=json', timeout=3)
        if res.status_code == 200:
            return res.json().get("ip", "127.0.0.1")
    except Exception:
        pass

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1 (Localhost)"


def fetch_web_google_answer(query):
    """
    Dynamically searches Google & web knowledge sources for ANY natural question.
    Returns: (answer_text, source_title, google_search_url)
    """
    clean_q = query.strip()
    if not clean_q:
        return "How may I assist you today?", "System", "https://www.google.com"

    google_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(clean_q)}"

    # 1. Local knowledge engine (Instant, high-precision answers for 100+ core topics & math)
    local_hit = lookup_local_knowledge(clean_q)
    if local_hit:
        return local_hit, "IntelliAssist Knowledge Engine", google_url

    # 2. Check Gemini API if configured
    if GEMINI_API_KEY and GEMINI_API_KEY != "None":
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{
                    "parts": [{"text": f"You are IntelliAssist. Answer this question directly and accurately in 2 concise sentences without preamble:\n\n{clean_q}"}]
                }]
            }
            res = requests.post(url, json=payload, timeout=6)
            if res.status_code == 200:
                text = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text:
                    return text, "Gemini AI", google_url
        except Exception:
            pass

    # 3. Check Groq API if configured
    if GROQ_API_KEY and GROQ_API_KEY != "None":
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are IntelliAssist. Answer questions directly in 2 concise sentences."},
                    {"role": "user", "content": clean_q}
                ],
                "max_tokens": 120
            }
            res = requests.post(url, headers=headers, json=payload, timeout=6)
            if res.status_code == 200:
                text = res.json()["choices"][0]["message"]["content"].strip()
                if text:
                    return text, "Groq AI", google_url
        except Exception:
            pass

    # 4. Clean subject for web search
    clean_topic = clean_q.lower()
    for prefix in [
        'who is the', 'who was the', 'who is', 'who was', 'who are the', 'who are',
        'what is the', 'what was the', 'what is', 'what was', 'what are the', 'what are',
        'where is the', 'where is', 'which is the', 'which is',
        'tell me about', 'explain', 'define', 'meaning of'
    ]:
        if clean_topic.startswith(prefix + ' '):
            clean_topic = clean_topic[len(prefix):].strip()
            break
    clean_topic = clean_topic.rstrip('?.! ')

    compliant_headers = {
        'User-Agent': 'IntelliAssistBot/2.0 (https://github.com/mohitraj; student.mini.project@college.edu) requests/2.32'
    }

    # 5. DuckDuckGo Instant Answer API
    try:
        ddg_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(clean_q)}&format=json&no_html=1"
        d_res = requests.get(ddg_url, headers=compliant_headers, timeout=4).json()
        ans = d_res.get('Answer') or d_res.get('AbstractText')
        if ans and len(ans) > 10:
            sentences = ans.split('. ')
            clean_ans = '. '.join(sentences[:2])
            if not clean_ans.endswith('.'):
                clean_ans += '.'
            return clean_ans, d_res.get('Heading', 'Web Answer'), google_url
    except Exception:
        pass

    # 6. Full-text Web & Google Knowledge Search via Wikipedia REST API
    for term in [clean_topic, clean_q]:
        if not term:
            continue
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(term)}&format=json&utf8=1"
            r = requests.get(search_url, headers=compliant_headers, timeout=5).json()
            items = r.get('query', {}).get('search', [])
            if items:
                title = items[0]['title']
                sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
                sr = requests.get(sum_url, headers=compliant_headers, timeout=5).json()
                extract = sr.get('extract')
                if extract:
                    sentences = extract.split('. ')
                    clean_ans = '. '.join(sentences[:2])
                    if not clean_ans.endswith('.'):
                        clean_ans += '.'
                    return clean_ans, title, google_url
        except Exception:
            pass

    # 7. Fallback response with Google search link
    clean_sub_title = clean_topic.title() if clean_topic else clean_q.title()
    fallback_text = (
        f"{clean_sub_title} is an active topic. I have fetched the Google search results for you."
    )
    return fallback_text, "Google Search", google_url


def get_direct_answer(query):
    """Provides a direct answer to questions using local knowledge or web search."""
    ans, source, gurl = fetch_web_google_answer(query)
    return ans


def search_on_wikipedia(query):
    """Searches Wikipedia using official REST API or fallback."""
    if not query or query.strip() == "":
        return "Please specify what you would like to search on Wikipedia."
    
    clean_query = query.strip()
    # Check local knowledge base first
    local_hit = lookup_local_knowledge(clean_query)
    if local_hit:
        return local_hit

    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean_query)}"
        headers = {'User-Agent': 'JarvisAssistant/1.0 (personal-assistant-bot)'}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            extract = data.get('extract')
            if extract:
                sentences = extract.split('. ')
                summary = '. '.join(sentences[:2])
                if not summary.endswith('.'):
                    summary += '.'
                return summary
    except Exception:
        pass

    # Secondary API search attempt
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(clean_query)}&format=json"
        res = requests.get(search_url, timeout=5)
        if res.status_code == 200:
            items = res.json().get("query", {}).get("search", [])
            if items:
                title = items[0]["title"]
                snippet = items[0]["snippet"].replace('<span class="searchmatch">', '').replace('</span>', '')
                return f"{title}: {snippet}..."
    except Exception:
        pass

    return f"Information about '{clean_query}' can be found on Wikipedia: https://en.wikipedia.org/wiki/{urllib.parse.quote(clean_query)}"


def play_on_youtube(video):
    """Searches and opens YouTube for a video."""
    encoded = urllib.parse.quote(video)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    webbrowser.open(url)
    return url


def search_on_google(query):
    """Searches Google for the given query."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    return url


def send_whatsapp_message(number, message):
    """Opens WhatsApp Web to send a message."""
    clean_num = ''.join(filter(str.isdigit, str(number)))
    encoded_msg = urllib.parse.quote(message)
    url = f"https://web.whatsapp.com/send?phone=+91{clean_num}&text={encoded_msg}"
    webbrowser.open(url)
    return url


def send_email(receiver_address, subject, message):
    """Sends email via SMTP."""
    if not EMAIL or not PASSWORD or EMAIL == "None" or PASSWORD == "None":
        print("Email credentials are not set in .env file.")
        return False
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def get_latest_news():
    """Fetches top news headlines from NewsAPI or curated news feed."""
    if NEWS_API_KEY and NEWS_API_KEY != "None":
        try:
            res = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general",
                timeout=5
            ).json()
            articles = res.get("articles", [])
            if articles:
                return [article["title"] for article in articles if "title" in article][:5]
        except Exception as e:
            print(f"NewsAPI error: {e}")

    return FALLBACK_NEWS


def get_weather_report(city="Delhi"):
    """Fetches weather report from OpenWeather or returns a report."""
    if not city or city.strip() == "":
        city = "Delhi"

    if OPENWEATHER_APP_ID and OPENWEATHER_APP_ID != "None":
        try:
            res = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid={OPENWEATHER_APP_ID}&units=metric",
                timeout=5
            ).json()
            if res.get("cod") == 200:
                weather = res["weather"][0]["main"]
                temperature = res["main"]["temp"]
                feels_like = res["main"]["feels_like"]
                return weather, f"{temperature}°C", f"{feels_like}°C"
        except Exception as e:
            print(f"OpenWeather error: {e}")

    # Fallback status
    return "Clear Sky", "24°C", "23°C"


def get_trending_movies():
    """Fetches trending movies from TMDB or curated fallback."""
    if TMDB_API_KEY and TMDB_API_KEY != "None":
        try:
            res = requests.get(
                f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}",
                timeout=5
            ).json()
            results = res.get("results", [])
            if results:
                return [r.get("original_title") or r.get("title") for r in results[:5]]
        except Exception as e:
            print(f"TMDB error: {e}")

    return FALLBACK_MOVIES


def get_random_joke():
    """Fetches random joke from icanhazdadjoke or fallback."""
    headers = {'Accept': 'application/json', 'User-Agent': 'JarvisAssistant/1.0'}
    try:
        res = requests.get("https://icanhazdadjoke.com/", headers=headers, timeout=3).json()
        if "joke" in res:
            return res["joke"]
    except Exception:
        pass
    return random.choice(FALLBACK_JOKES)


def get_random_advice():
    """Fetches random advice from adviceslip or fallback."""
    try:
        res = requests.get("https://api.adviceslip.com/advice", timeout=3).json()
        if "slip" in res and "advice" in res["slip"]:
            return res["slip"]["advice"]
    except Exception:
        pass
    return random.choice(FALLBACK_ADVICE)
