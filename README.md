# Yoga Bot

Телеграм-бот для йога-клуба с функциями навигации и информирования пользователей.

## Установка

1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать виртуальное окружение:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Создать файл `.env` и добавить токен бота:
   ```
   TELEGRAM_TOKEN=ваш_токен_бота
   ```
6. Запустить бота: `python bot.py`