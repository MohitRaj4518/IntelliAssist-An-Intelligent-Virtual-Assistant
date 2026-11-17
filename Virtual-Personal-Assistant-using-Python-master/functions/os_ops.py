import os
import re
import shutil
import subprocess as sp
import sys
import urllib.parse
import webbrowser

paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

COMMON_WEBSITES = {
    'google': 'https://www.google.com',
    'youtube': 'https://www.youtube.com',
    'github': 'https://www.github.com',
    'reddit': 'https://www.reddit.com',
    'twitter': 'https://twitter.com',
    'x': 'https://x.com',
    'instagram': 'https://www.instagram.com',
    'linkedin': 'https://www.linkedin.com',
    'netflix': 'https://www.netflix.com',
    'spotify': 'https://open.spotify.com',
    'amazon': 'https://www.amazon.com',
    'wikipedia': 'https://www.wikipedia.org',
    'stackoverflow': 'https://stackoverflow.com',
    'chatgpt': 'https://chatgpt.com',
    'facebook': 'https://www.facebook.com',
    'leetcode': 'https://leetcode.com',
    'gmail': 'https://mail.google.com',
    'maps': 'https://maps.google.com',
    'flipkart': 'https://www.flipkart.com',
    'whatsapp': 'https://web.whatsapp.com',
    'discord': 'https://discord.com/app',
    'twitch': 'https://www.twitch.tv'
}


def open_in_chrome(url=""):
    """
    Opens Google Chrome (or Chromium-based browser) with an optional URL.
    Works seamlessly across macOS, Windows, and Linux.
    """
    try:
        if sys.platform == 'darwin':
            # Check for Chrome, Brave, Chromium, Opera
            for app_name in ['Google Chrome', 'Brave Browser', 'Chromium', 'Opera']:
                if os.path.exists(f"/Applications/{app_name}.app"):
                    if url:
                        sp.Popen(['open', '-a', app_name, url])
                    else:
                        sp.Popen(['open', '-a', app_name])
                    return f"Opening {app_name}"
            # Fallback to system default browser
            if url:
                sp.Popen(['open', url])
            else:
                sp.Popen(['open', '-a', 'Safari'])
            return "Opening default web browser"

        elif sys.platform == 'win32':
            chrome_paths = [
                os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
            ]
            for p in chrome_paths:
                if os.path.exists(p):
                    sp.Popen([p, url] if url else [p])
                    return "Opening Google Chrome"
            if url:
                webbrowser.open(url)
            else:
                os.system('start chrome')
            return "Opening Chrome"

        else:
            for cmd in ['google-chrome', 'google-chrome-stable', 'chromium-browser', 'brave-browser']:
                if shutil.which(cmd):
                    sp.Popen([cmd, url] if url else [cmd])
                    return "Opening Chrome"
            if url:
                webbrowser.open(url)
            return "Opening web browser"

    except Exception as e:
        if url:
            webbrowser.open(url)
        return f"Opening browser: {e}"


def resolve_website_url(query):
    """
    Resolves any site name, domain, or URL from natural language.
    Returns (site_display_name, full_url).
    """
    q = query.lower().strip()
    for prefix in [
        'open website', 'open site', 'open page', 'open web page',
        'open up', 'open', 'go to website', 'go to', 'launch website', 'launch site', 'launch'
    ]:
        if q.startswith(prefix):
            q = q[len(prefix):].strip()
            break

    # Strip phrases like "in chrome", "on chrome", "using chrome"
    for suffix in ['in chrome', 'on chrome', 'using chrome', 'in browser', 'on browser']:
        if q.endswith(suffix):
            q = q[:-len(suffix)].strip()
            break

    if not q or q == 'chrome':
        return "Chrome", ""

    # Known common site mapping
    if q in COMMON_WEBSITES:
        return q.title(), COMMON_WEBSITES[q]

    # Full HTTP/HTTPS URL
    if q.startswith('http://') or q.startswith('https://'):
        return q, q

    # Has TLD suffix (e.g. reddit.com, news.ycombinator.com, github.io)
    if re.search(r'\.[a-z]{2,}(/.*)?$', q):
        return q, f"https://{q}"

    # Default to .com
    clean_name = re.sub(r'[^a-zA-Z0-9-]', '', q)
    return clean_name.title(), f"https://www.{clean_name}.com"


def search_on_chrome(query):
    """Searches Google on Chrome."""
    clean_q = query.strip()
    # Strip trigger words
    for prefix in [
        'search on chrome for', 'search in chrome for', 'search chrome for',
        'search on chrome', 'search in chrome', 'chrome search for', 'chrome search',
        'search on google for', 'search on google', 'search google for', 'search google',
        'google search for', 'google search', 'search for', 'search web for', 'search web', 'search'
    ]:
        if clean_q.lower().startswith(prefix):
            clean_q = clean_q[len(prefix):].strip()
            break

    for suffix in ['in chrome', 'on chrome', 'on google', 'in google']:
        if clean_q.lower().endswith(suffix):
            clean_q = clean_q[:-len(suffix)].strip()
            break

    if not clean_q:
        clean_q = "Google"

    encoded = urllib.parse.quote(clean_q)
    url = f"https://www.google.com/search?q={encoded}"
    msg = open_in_chrome(url)
    return clean_q, url, msg


def open_notepad():
    """Opens text editor / notepad according to platform."""
    try:
        if sys.platform == 'darwin':
            sp.Popen(['open', '-a', 'TextEdit'])
            return "Opening TextEdit"
        elif sys.platform == 'win32':
            if os.path.exists(paths['notepad']):
                os.startfile(paths['notepad'])
            else:
                sp.Popen('notepad.exe')
            return "Opening Notepad"
        else:
            sp.Popen(['xdg-open', 'temp.txt'])
            return "Opening default text editor"
    except Exception as e:
        return f"Could not open notepad: {e}"


def open_discord():
    """Opens Discord app or web version."""
    try:
        if sys.platform == 'darwin':
            if os.path.exists('/Applications/Discord.app'):
                sp.Popen(['open', '-a', 'Discord'])
                return "Opening Discord"
            else:
                open_in_chrome('https://discord.com/app')
                return "Opening Discord in Chrome"
        elif sys.platform == 'win32':
            if os.path.exists(paths['discord']):
                os.startfile(paths['discord'])
            else:
                open_in_chrome('https://discord.com/app')
            return "Opening Discord"
        else:
            open_in_chrome('https://discord.com/app')
            return "Opening Discord in browser"
    except Exception as e:
        open_in_chrome('https://discord.com/app')
        return f"Opening Discord: {e}"


def open_cmd():
    """Opens terminal / command prompt."""
    try:
        if sys.platform == 'darwin':
            sp.Popen(['open', '-a', 'Terminal'])
            return "Opening Terminal"
        elif sys.platform == 'win32':
            os.system('start cmd')
            return "Opening Command Prompt"
        else:
            sp.Popen(['x-terminal-emulator'])
            return "Opening Terminal"
    except Exception as e:
        return f"Could not open terminal: {e}"


def open_camera():
    """Opens camera / photo booth."""
    try:
        if sys.platform == 'darwin':
            sp.Popen(['open', '-a', 'Photo Booth'])
            return "Opening Camera (Photo Booth)"
        elif sys.platform == 'win32':
            sp.run('start microsoft.windows.camera:', shell=True)
            return "Opening Camera"
        else:
            sp.Popen(['cheese'])
            return "Opening Camera"
    except Exception as e:
        return f"Could not open camera: {e}"


def open_calculator():
    """Opens system calculator."""
    try:
        if sys.platform == 'darwin':
            sp.Popen(['open', '-a', 'Calculator'])
            return "Opening Calculator"
        elif sys.platform == 'win32':
            if os.path.exists(paths['calculator']):
                sp.Popen(paths['calculator'])
            else:
                sp.Popen('calc.exe')
            return "Opening Calculator"
        else:
            sp.Popen(['gnome-calculator'])
            return "Opening Calculator"
    except Exception as e:
        return f"Could not open calculator: {e}"
