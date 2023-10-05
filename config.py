from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
