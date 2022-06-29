class SendMessageException(Exception):
    pass


class GetAPIException(Exception):
    """Error of access to API."""
    pass


class ResponseJsonException(Exception):
    """Error of parsing APIs answer into json."""
    pass


class HomeworkStatusError(Exception):
    """Error of collecting unknown status of the homework, that not in STATUSES constant."""
    pass
