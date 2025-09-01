import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent


load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MODEL_PATH = os.path.join(BASE_DIR, os.getenv('MODEL_PATH'))
DATABASE_PATH = os.path.join(BASE_DIR, os.getenv('DATABASE_PATH'))
MODEL_API_PORT= int(os.getenv('MODEL_API_PORT'))
TELEGRAM_BOT_PORT= os.getenv('MODEL_API_PORT')
DOMAIN=os.getenv('DOMAIN')

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

if not os.path.exists(DATABASE_PATH):
    raise FileNotFoundError(f"Model file not found: {DATABASE_PATH}")