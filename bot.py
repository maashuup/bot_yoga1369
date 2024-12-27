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
            types.KeyboardButton("🧘‍♂️ О нас"), types.KeyboardButton("📋 Марафон")
        )
        keyboard.add(
            types.KeyboardButton("💙 Отзывы"),
            types.KeyboardButton("🙌 Ответы на вопросы"),
        )
        keyboard.add(types.KeyboardButton("🎥 Видео"))

        # Отправка сообщения
        bot.send_message(
            chat_id,
            f"Привет, {name}!\n\n"
            "Благодарим за интерес к нашему йога-клубу 🙏\n"
            "🖤 Используй кнопки для навигации.",
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


# Хендлер для кнопки "О нас"
@bot.message_handler(func=lambda message: message.text == "🧘‍♂️ О нас")
def about_us(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Привет! Меня зовут Таня, я инструктор FYSM йоги, и йога для меня – это не "
        "только работа, но и образ жизни. Я обожаю помогать людям находить баланс, "
        "чувствовать своё тело и находить гармонию с собой.\n\n"
        "На моих занятиях мы не только делаем асаны, но и учимся расслабляться, "
        "дышать и просто наслаждаться процессом. Я делюсь полезными советами о "
        "йоге, здоровье и самое главное – заботе о себе и своём здоровье.\n\n"
        "Буду рада видеть вас на занятиях – вместе мы сделаем вашу жизнь немного "
        "легче и приятнее! 😊",
    )


# Хендлер для кнопки "Марафон"
@bot.message_handler(func=lambda message: message.text == "📋 Марафон")
def marathon(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Следующий марафон начнётся 1 января. "
        "Подробности и регистрация здесь: https://t.me/yoga_1369",
    )


# Хендлер для кнопки "Отзывы"
@bot.message_handler(func=lambda message: message.text == "💙 Отзывы")
def reviews(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, "Отзывы наших участников можно найти здесь: https://t.me/yoga_1369"
    )


# Хендлер для кнопки "Ответы на вопросы"
@bot.message_handler(func=lambda message: message.text == "🙌 Ответы на вопросы")
def faq(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, "Ответы на часто задаваемые вопросы: https://example.com/faq"
    )


# Хендлер для кнопки "Видео"
@bot.message_handler(func=lambda message: message.text == "🎥 Видео")
def youtube_video(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Посмотрите наше видео на YouTube: "
        "https://www.youtube.com/watch?v=LvdZSKWKnrc",
    )


if __name__ == "__main__":
    logger.info("Бот запущен и готов принимать сообщения")
    # Установка Webhook
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    logger.info("Webhook установлен.")
    
    # Запуск Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
