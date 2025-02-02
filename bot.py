"""Телеграм-бот для йога-клуба"""

import os
import logging
from telebot import TeleBot, types
from telebot.types import Update
from dotenv import load_dotenv
from flask import Flask, request

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Лог-файл
        logging.StreamHandler(),  # Вывод в консоль
    ],
)
logger = logging.getLogger(__name__)

# Загрузка токена из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = f"https://bot-yoga1369.onrender.com/webhook"

bot = TeleBot(TELEGRAM_TOKEN)

# Хендлер команды /start
@bot.message_handler(commands=["start"])
def start_message(message):
    chat_id = message.chat.id
    name = message.from_user.first_name

    logger.info(f"Пользователь {name} ({chat_id}) запустил команду /start")

    try:
        # Создание клавиатуры
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton("✨ обо мне"),
            types.KeyboardButton("🧘🏼‍♀️ пробная практика")
        )
        keyboard.add(types.KeyboardButton("🎟 13·YOGA·69"))
        keyboard.add(
            types.KeyboardButton("👯‍♀️ мероприятия"),
            types.KeyboardButton("🫂 поддержка"))

        # Отправка сообщения
        bot.send_message(
            chat_id,
            f"Приветствую, {name}!\n\n"
            "Здесь вы можете попробовать 2 практики со мной,\n"
            "после чего оформить подписку на закрытый телеграмм канал\n"
            "🎟️ 13• YOGA •69 и начать практиковать вместе со мной.",
            reply_markup=keyboard,
        )
        logger.info(f"Сообщение успешно отправлено пользователю {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения пользователю {chat_id}: {e}")


# Flask-приложение для обработки запросов Telegram
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json()
        if json_data:
            bot.process_new_updates([Update.de_json(json_data)])
    except Exception as e:
        logger.error(f"Ошибка обработки Webhook: {e}")
    return 'OK', 200


# Хендлер для кнопки "обо мне"
@bot.message_handler(func=lambda message: message.text == "✨ обо мне")
def about_us(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Привет, я Таня, тренер по йоге в стиле fysm."
        "Физическая активность в моей жизни отсутствовала до 30 лет."
        "Я пришла в йогу с больными ногами и спиной, постоянными мигренями."
        "Первые результаты я ощутила спустя месяц занятий. Все, что вы могли "
        "видеть на фото в инстаграм у меня получилось за 2 года регулярных занятий."
        "Я практикую и преподаю безопасную йогу по методологии fysm. "
        "Если вы так же хотите за короткий срок избавиться от:"
        "-болей в спине, ногах"
        "-головных болей"
        "-нормализовать эмоциональное состояние"
        "-обрести силу, гибкость, выносливость,"
        "буду рада видеть вас в моём закрытом телеграмм канале 13• YOGA •69",
    )


# Хендлер для кнопки "пробная практика"
@bot.message_handler(func=lambda message: message.text == "🧘🏼‍♀️ пробная практика")
def marathon(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "https://t.me/yoga13_69",
    )


# Хендлер для кнопки "покупка подписки"
@bot.message_handler(func=lambda message: message.text == "🎟 13·YOGA·69")
def reviews(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, "???????"
    )


# Хендлер для кнопки "Ответы на вопросы"
@bot.message_handler(func=lambda message: message.text == "👯‍♀️ мероприятия")
def faq(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, "Ближайшие мероприятия очно в Петербурге или онлайн: ???"
    )


# Хендлер для кнопки "Видео"
@bot.message_handler(func=lambda message: message.text == "🫂 поддержка")
def youtube_video(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "если у вас возникли вопросы/предложения, напишите @Tania1369",
    )


if __name__ == "__main__":
    logger.info("Бот запущен и готов принимать сообщения")
    # Установка Webhook
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    logger.info("Webhook установлен.")
    
    # Запуск Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
