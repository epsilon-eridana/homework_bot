import os
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PKTOKEN')
TELEGRAM_TOKEN = os.getenv('TGTOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT')
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
