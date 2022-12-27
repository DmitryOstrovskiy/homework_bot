class StatusCodeNotOK(Exception):
    '''Ошибка статуса API-сервиса'''
    pass


class SendMessageError(ValueError):
    '''Ошибка при отправке сообщения в чат'''
    pass

class RequestError(Exception):
    '''Ошибка доступа к эндпоинту'''
    pass
