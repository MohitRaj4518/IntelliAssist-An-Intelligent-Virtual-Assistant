"""
Fallback decouple module if python-decouple is not installed.
Reads from environment variables and .env file via python-dotenv.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def config(key, default=None, cast=None):
    val = os.environ.get(key)
    if val is None or val == 'None' or val == '':
        val = default
    if val is not None and cast is not None:
        try:
            return cast(val)
        except Exception:
            return val
    return val
