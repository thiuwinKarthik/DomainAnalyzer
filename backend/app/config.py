import os

# Base Directories
# Get the backend directory (parent of app directory)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(APP_DIR)  # This is the backend directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# Input/Output Paths
OFFLINE_SITES_DIR = os.path.join(DATA_DIR, "offline_sites")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# API / Network Config (localhost first)
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

# LLM Config (optimized default for low-mid range PCs)
# Ollama model can be changed without code edits using env vars.
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:1.5b")
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "180"))
LLM_NUM_CTX = int(os.getenv("LLM_NUM_CTX", "2048"))

# Ensure directories exist
os.makedirs(OFFLINE_SITES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)