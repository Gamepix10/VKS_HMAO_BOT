import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://test.vcc.uriit.ru/api")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")