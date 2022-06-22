class VariablesException(Exception):
    """Ошибка проверки переменных"""

    pass


class EmptyResponseException(Exception):
    """Пустой ответ сервера"""

    pass


class SendingMessageException(Exception):
    """Ошибка при отправке сообщения"""

    pass
