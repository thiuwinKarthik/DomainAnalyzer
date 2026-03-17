import os

# Base Directories
# Get the backend directory (parent of app directory)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(APP_DIR)  # This is the backend directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# Input/Output Paths
OFFLINE_SITES_DIR = os.path.join(DATA_DIR, "offline_sites")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# LLM Config
LLM_MODEL = "phi3"
LLM_TIMEOUT = 300

# Ensure directories exist
os.makedirs(OFFLINE_SITES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)