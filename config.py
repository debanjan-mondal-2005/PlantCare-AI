import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder configurations
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_AUDIO_FOLDER = os.path.join(BASE_DIR, "output_audio")
MODEL_DIR = os.path.join(BASE_DIR, "model")

# File upload restrictions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

# API Keys — loaded from .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
GOOGLE_TTS_API_KEY = os.getenv("GOOGLE_TTS_API_KEY", "")

# Warn on startup if Gemini key is missing
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY is not set in .env file. Explanation features will use mock data.")

# App settings
DEBUG = os.getenv("DEBUG", "True") == "True"
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# Maintenance Mode
MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "False").lower() in ("true", "1", "yes")
MAINTENANCE_TIME = os.getenv("MAINTENANCE_TIME", "some time")

# Model paths
MODEL_PATH = os.path.join(MODEL_DIR, "plant_disease_model.keras")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_AUDIO_FOLDER, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
