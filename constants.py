import os

from dotenv import load_dotenv

load_dotenv()

'''Прописываем необходимые секретные токены'''
PRACTICUM_TOKEN = os.getenv('PKTOKEN')
TELEGRAM_TOKEN = os.getenv('TGTOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT')
RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
HOMEWORK_STATUSES = { 

    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',

    'reviewing': 'Работа взята на проверку ревьюером.',

    'rejected': 'Работа проверена: у ревьюера есть замечания.'

}
