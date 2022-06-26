import logging
import sys
import os

import time
from http import HTTPStatus
from dotenv import load_dotenv

import requests
import telegram

import exceptions
from logcfg import logger_setup
import constants

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PKTOKEN')
TELEGRAM_TOKEN = os.getenv('TGTOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT')
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

logger = logger_setup(__name__)


def send_message(bot, message):
    """Sending message in telegram."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
    except exceptions.SendMessageException:
        logger.error(
            f'Error sending message to user - {TELEGRAM_CHAT_ID}')


def get_api_answer(current_timestamp):
    """Sending request to API."""
    timestamp = current_timestamp or int(0)
    params = {'from_date': timestamp}
    try:
        response = requests.get(constants.ENDPOINT,
                                headers=HEADERS, params=params)
    except Exception:
        error = 'API is not accesible'
        logger.error(error)
        raise exceptions.GetAPIException(error)
    if response.status_code != HTTPStatus.OK:
        response.raise_for_status()
        error = 'Error, wrong HTTP status code'
        logger.error(error)
        raise exceptions.GetAPIException(error)
    try:
        return response.json()
    except exceptions.ResponseJsonException:
        logger.error(
            f'Error transformation of response into json format'
            f' - {type(response)}'
        )
        raise exceptions.ResponseJsonException(
            f'Error transformation of response into json format'
            f' - {type(response)}'
        )


def check_response(response: dict) -> list:
    """Checking API response."""
    if not isinstance(response, dict):
        raise TypeError
    if 'homeworks' in response:
        if isinstance(response['homeworks'], list):
            if not response['homeworks']:
                logger.error('В ответе нет новых статусов.')
            return response['homeworks']
    raise exceptions.ResponseDataError(
        'Отсутствуют ожидаемые ключи в ответе API.')


def parse_status(homework: dict):
    """Parsing API's response, for homework status."""
    if homework != []:
        if "homework_name" not in homework.keys():
            logger.error('No key: "homework_name"')
            raise KeyError('No key: "homework_name"')
        elif "status" not in homework.keys():
            logger('No key: "status"')
            raise KeyError('No key: "status"')
        homework_name = homework.get("homework_name")
        homework_status = homework.get("status")
        if homework_status in constants.HOMEWORK_STATUSES.keys():
            verdict = constants.HOMEWORK_STATUSES.get(homework_status)
            logger.error(
                f'Изменился статус проверки работы: {verdict}')
            return (
                f'Изменился статус проверки работы "{homework_name}".{verdict}'
            )
        elif homework_status not in constants.HOMEWORK_STATUSES.keys():
            logger.error(
                f'Unknown status of the homework: {homework_status}'
            )
            raise exceptions.ParseDataError(
                f'Unknown status of the homework: {homework_status}'
            )
    elif homework == []:
        logger.info(
            'Request successfull. Homework status does not changed')
        return (
            'Request successfull. Homework status does not changed')
    else:
        logger.error(
            f'Unknown request format {homework}.'
        )


def check_tokens():
    """Checking constants."""
    return all(
        [PRACTICUM_TOKEN,
         TELEGRAM_TOKEN,
         TELEGRAM_CHAT_ID]
        )


def main():
    """Main function of the Bot."""
    if not check_tokens():
        message = 'Missing required environment variable'
        logger.critical(message)
        sys.exit(message)
    current_timestamp = int(0)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    while True:
        try:
            """Request for API"""
            response = get_api_answer(current_timestamp)
            """Checking answer"""
            check_response(response)
            """Getting homework status"""
            message = parse_status(response.get('homeworks')[0])
            send_message(bot, message)
            if not check_tokens():
                logger.critical('Missing required environment variable!')
                raise SystemExit()
            current_timestamp = int(time.time())
            time.sleep(constants.RETRY_TIME)

        except Exception as error:
            message = f'Program crash: {error}'
            time.sleep(constants.RETRY_TIME)


if __name__ == '__main__':
    main()
