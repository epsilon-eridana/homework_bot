class CheckResponseAPI(Exception):
    """Исключение для проверки запроса к API на корректность"""
    pass


class APIResponseException(Exception):
    pass


class SendMessageException(Exception):
    pass


class GetAPIException(Exception):
    pass


class ResponseJsonException(Exception):
    """Ошибка сериализации ответа от серверая."""
    pass


class EmptyAPIResponseError(Exception):
    pass


class StatusException(Exception):
    pass


class ResponseDataError(Exception):
    pass


class StatusKeyError(Exception):
    pass


class ParseDataError(Exception):
    pass
