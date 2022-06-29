from http import HTTPStatus
import logging
import sys
import requests
import time

import telegram
from dotenv import load_dotenv

from exceptions import (
    SendMessageException,
    GetAPIException,
    ResponseJsonException,
    HomeworkStatusError,
)
from logger import logger_conf
from constants import (
    RETRY_TIME,
    ENDPOINT,
    HOMEWORK_STATUSES,
)
from variables import (
    HEADERS,
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
)

load_dotenv()

logger = logging.getLogger(__name__)


def send_message(bot, message):
    """Sending message in telegram."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logger.info(f'The message was sended into chat {TELEGRAM_CHAT_ID}')
    except SendMessageException:
        logger.error(
            f'Error sending message to user - {TELEGRAM_CHAT_ID}'
        )


def get_api_answer(current_timestamp):
    """Sending request to API."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT,
                                headers=HEADERS, params=params)
    except Exception:
        error = 'API is not accesible'
        logger.error(error)
        raise GetAPIException(error)
    if response.status_code != HTTPStatus.OK:
        response.raise_for_status()
        error = 'Error, wrong HTTP status code'
        logger.error(error)
        raise GetAPIException(error)
    try:
        response = response.json()
    except ResponseJsonException:
        logger.error(
            f'Error transformation of response into json format'
            f' - {type(response)}'
        )
        raise ResponseJsonException(
            f'Error transformation of response into json format'
            f' - {type(response)}'
        )
    logger.info('Request to API is sended.')
    return response


def check_response(response: dict) -> list:
    """Checking API response."""
    if not isinstance(response, dict):
        raise TypeError('APIs answer is not a dictionary.')
    homeworks = response.get('homeworks')
    if homeworks is None:
        raise KeyError(
            'APIs answer does not contains data about homework.'
            'APIs response: ', response
        )
    current_date = response.get('current_date')
    if current_date is None:
        raise KeyError('There is no current date in the APIs answer.')
    if not isinstance(homeworks, list):
        raise TypeError(
            "Answer with a 'homeworks' key is not a list."
        )
    if not isinstance(current_date, int):
        raise TypeError(
            "Answer with a 'current_date' key in not an integer."
        )
    logging.info('Checking APIs answer passed.')
    return homeworks


def parse_status(homework: dict):
    """Parsing API's response, for homework status."""
    if homework != []:
        if "homework_name" not in homework.keys():
            logger.error('No key: "homework_name"')
            raise KeyError('No key: "homework_name"')
        elif "status" not in homework.keys():
            logger.error('No key: "status"')
            raise KeyError('No key: "status"')
        homework_name = homework.get("homework_name")
        homework_status = homework.get("status")
        if homework_status in HOMEWORK_STATUSES.keys():
            verdict = HOMEWORK_STATUSES.get(homework_status)
            logger.error(
                f'Status of the homework is changed: {verdict}')
            return (
                f'Изменился статус проверки работы "{homework_name}".'
                f'{verdict}'
            )
        elif homework_status not in HOMEWORK_STATUSES.keys():
            logger.error(
                f'Unknown status of the homework: {homework_status}'
            )
            raise HomeworkStatusError(
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
    PREVIOUS_ERROR = ''
    current_timestamp = int(0)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks_list = check_response(response)
            if len(homeworks_list) > 0:
                for homework in homeworks_list:
                    status_msg = parse_status(homework)
                    send_message(bot, status_msg)
            else:
                logger.debug(
                    'Новых записей о статусах домашних работ не найдено'
                )
            current_timestamp = response.get(
                'current_date',
                int(time.time())
            )
        except Exception as error:
            message = f'Ошибка в работе: {error}'
            logger.error(message)
            if error != PREVIOUS_ERROR:
                PREVIOUS_ERROR = error
                send_message(bot, message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logger_conf()
    main()
