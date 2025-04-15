import os

# ==================================================== Env Vars ====================================================
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "host.docker.internal")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VALID_USERS = os.getenv("VALID_USERS").split(',')

# ==================================================== App Specific Config ====================================================
PREFIX = 'hey '
TIMEOUT = 120.0  # seconds
MAX_RESP_SIZE = 2000 # characters
