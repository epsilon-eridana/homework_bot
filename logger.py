import logging
from sys import stdout


def logger_conf():
    """Set up settings"""
    logging.basicConfig(
                level=logging.INFO,
            format='%(asctime)s - [%(levelname)s] - %(message)s',
            handlers=[
                logging.FileHandler('main.log', mode='w', encoding='UTF-8'),
                logging.StreamHandler(stdout)

            ]
    )
