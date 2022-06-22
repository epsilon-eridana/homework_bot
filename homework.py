import logging
import os
import sys
import time
from http import HTTPStatus
from logging import Formatter, StreamHandler

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (
    VariablesException,
    EmptyResponseException,
    SendingMessageException
)

load_dotenv()

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

_log_format: str = (
    '%(asctime)s - %(levelname)s - %(funcName)s - %(name)s  - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt=_log_format))
logger.addHandler(handler)


def send_message(bot, message):
    """Функция отправки сообщений ботом."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
    except SendingMessageException:
        logger.error(
            f'Ошибка отправки сообщения пользователю - {TELEGRAM_CHAT_ID}')


def get_api_answer(current_timestamp):
    """Отправка запроса к API-Домашки."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params)
    except SendingMessageException:
        logger.error(f'Сервер {ENDPOINT} не отвечает')
        raise SendingMessageException(
            f'Сервер {ENDPOINT} не отвечает')

    if response.status_code != HTTPStatus.OK:
        raise Exception(f'Неправильный ответ сервера: {response.status_code}')

    return response.json()


def check_response(response):
    """Проверка правильности ответа API-Домашки."""
    if not response:
        raise EmptyResponseException(
            f'В ответе сервера нет данных - {response}')

    if not isinstance(response, dict):
        raise TypeError('Неизвестный тип данных')

    homework = response.get('homeworks')

    if homework is None:
        raise KeyError('В ответе отсуствует ключ "homeworks"')

    if not isinstance(homework, list):
        raise TypeError('Не поддерживаемый тип данных')

    return homework


def parse_status(homework):
    """Парсинг информации о статусе проверки."""
    if isinstance(homework, list):
        homework = homework[0]

    homework_status = homework.get('status')
    if homework_status is None:
        raise KeyError('Отсутствует "status" в словаре "homework"')

    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise KeyError(
            'Отсутствует "homework_name" в словаре "homework"')

    verdict = HOMEWORK_STATUSES.get(homework_status)
    if verdict is None:
        raise KeyError('Пустой статус домашней работы')

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка наличия переменных."""
    if PRACTICUM_TOKEN is None:
        logger.critical(
            'Отсутствует переменная: PRACTICUM_TOKEN')
        return False
    if TELEGRAM_TOKEN is None:
        logger.critical(
            'Отсутствует переменная: TELEGRAM_TOKEN')
        return False
    if TELEGRAM_CHAT_ID is None:
        logger.critical(
            'Отсутствует переменная: TELEGRAM_CHAT_ID')
        return False
    return True


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        raise VariablesException(
            'Нет необходимых переменных, работа бота прекращена'
        )

    new_error: str = ''
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            logger.info(
                f'Отправка запроса к {ENDPOINT}'
            )

            homework = check_response(response)
            logger.info(
                'Проверка ответа'
            )

            answer = parse_status(homework)
            logger.info(
                'Получение статуса проверки'
            )

            current_timestamp = response.get('current_date')

            if not answer:
                time.sleep(RETRY_TIME)
                continue

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(f'Сбой в работе программы: - {error}')

            if new_error != message:
                send_message(bot, message)
                logger.info(
                    f'Отправка ошибки пользователю - {error}'
                )
                new_error = message

            time.sleep(RETRY_TIME)
        else:
            send_message(bot, answer)
            logger.info(
                f'Отправка сообщения пользователю - {TELEGRAM_CHAT_ID}'
            )
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
