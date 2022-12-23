class StatusCodeNotOK(Exception):
    pass


def status_code_api(status):
    if status != 200:
        raise StatusCodeNotOK('Статус не 200')

status_code_api(200)
