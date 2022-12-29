import logging
import os
import time
from http import HTTPStatus
import exceptions
import sys
import json

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('yp_token')
TELEGRAM_TOKEN = os.getenv('tg_token')
TELEGRAM_CHAT_ID = os.getenv('tg_chat_id')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
FROM_DATE = 0


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)


def check_tokens():
    """Проверка доступности переменных окружения."""
    tokens = (
        'PRACTICUM_TOKEN',
        'TELEGRAM_TOKEN',
        'TELEGRAM_CHAT_ID',
    )

    if not PRACTICUM_TOKEN:
        logger.critical('Отсутствует токен: PRACTICUM')
        return False

    if not TELEGRAM_TOKEN:
        logger.critical('Отсутствует токен: TELEGRAM')
        return False

    if not TELEGRAM_CHAT_ID:
        logger.critical('Отсутствует телеграм id')
        return False

    return True


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug('Бот отправил сообщение в чат')
    except telegram.error.TelegramError:
        logger.error('Сбой при отправке сообщения в чат')
        raise exceptions.SendMessageError(
            'Ошибка при отправке сообщения в чат')


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    try:
        logging.debug('Делаем запрос к API')
        api_answer = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp})
        if api_answer.status_code != HTTPStatus.OK:
            raise exceptions.StatusCodeNotOK(
                'Статус запроса к эндпоинту не 200')
        return api_answer.json()
    except json.decoder.JSONDecodeError:
        logging.error('Ответ не преобразован в json')
    except requests.RequestException:
        logging.error('Нет доступа к эндпоинту!')
        raise exceptions.RequestError('Ошибка доступа к эндпоинту!')


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        logger.error('Данные получены не в виде словаря')
        raise TypeError
    if 'homeworks' not in response:
        logger.error('Нет ключа homeworks')
        raise KeyError
    if not isinstance(response['homeworks'], list):
        logger.error('Данные переданы не в виде списка')
        raise TypeError
    if not response.get('homeworks'):
        raise IndexError('Список работ пуст')
    return response.get('homeworks')


def parse_status(homework):
    """Извлекает статус домашней работы."""
    try:
        homework_name = str(homework['homework_name'])
    except KeyError:
        logging.error('Нет названия домашней работы')
        raise KeyError('Нет ключа "homework_name"')
    try:
        homework_status = homework.get('status')
    except KeyError:
        logging.error('Нет статуса домашней работы')
        raise KeyError('Нет ключа "homework_status"')
    if homework_status == 'approved':
        verdict = str(HOMEWORK_VERDICTS[homework_status])
        return str(
            f'Изменился статус проверки работы "{homework_name}". {verdict}'
        )
    elif homework_status == 'reviewing' or homework_status == 'rejected':
        verdict = str(HOMEWORK_VERDICTS[homework_status])
        return str(
            f'Изменился статус проверки работы "{homework_name}". {verdict}'
        )
    else:
        logging.error('Нет статуса домашней робаты')
        raise KeyError


def main():
    """Основная логика работы бота."""
    logging.basicConfig(
        format='%(asctime)s, %(levelname)s, %(message)s',
        handlers=[logging.FileHandler('log.txt')]
    )
    if not check_tokens():
        sys.exit()
    else:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        timestamp = int(time.time() - FROM_DATE)
        first_status = ''
        while True:
            try:
                response = get_api_answer(timestamp)
                check_response(response)
                new_status = parse_status(response['homeworks'][0])
                if new_status != first_status:
                    send_message(bot, new_status)
                first_status = new_status
            except Exception as error:
                message = f'Сбой в работе программы: {error}'
                logging.error(message)
                send_message(bot, message)
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
