### Телеграм-бот для API сервиса Практикум.Домашка
Telegram-бота, который обращается к API сервиса Практикум.Домашка и узнает статус домашней работы: взята ли домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку. При обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram. Логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

### Используемые технологии
- python-telegram-bot 13.7
- python-dotenv 0.19.0
- requests 2.26.0

### Как запустить проект

- Клонировать репозиторий и перейти в него в командной строке:

```git clone https://git@github.com:DmitryOstrovskiy/homework_dot.git```

```cd homework_dot```

- Cоздать и активировать виртуальное окружение:

```python3 -m venv env```

Windows: ```source venv\scripts\activate```; Linux/Mac: ```sorce venv/bin/activate```

- Установить зависимости из файла requirements.txt:

```python -m pip install --upgrade pip```

```pip install -r requirements.txt```


