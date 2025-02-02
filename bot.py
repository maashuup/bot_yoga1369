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
        "Привет, я Таня, тренер по йоге в стиле fysm. Физическая активность в моей жизни отсутствовала до 30 лет.\n"
        "Я пришла в йогу с больными ногами и спиной, постоянными мигренями. Первые результаты я ощутила спустя месяц занятий.\n"
        "Все, что вы могли видеть на фото в Instagram у меня получилось за 2 года регулярных занятий.\n\n"
        "Я практикую и преподаю безопасную йогу по методологии fysm. Если вы также хотите за короткий срок избавиться от:\n"
        "- болей в спине, ногах\n"
        "- головных болей\n"
        "- нормализовать эмоциональное состояние\n"
        "- обрести силу, гибкость, выносливость,\n"
        "буду рада видеть вас в моём закрытом Telegram-канале!\n\n"
        "буду рада видеть вас в моём закрытом телеграмм канале 13• YOGA •69",
    )

    # Отправка фото из папки media/
    photo_path = "media/about_me.png"
    try:
        with open(photo_path, "rb") as photo:
            bot.send_photo(chat_id, photo)
    except FileNotFoundError:
        bot.send_message(chat_id, "Ошибка: фото не найдено.")


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
        chat_id,
        "На канале безопасные практики, которые помогут вам за короткое время приобрести мышечный корсет, "
        "избавят от болей в теле, сделают его сильным, гибким и выносливым.\n\n"
        "Практики проходят 2 раза в неделю:\n"
        "- в среду выходит запись практики\n"
        "- в пятницу 10:00 zoom, где ты можешь подключиться и получить корректировку положений.\n"
        "Если у вас не получается подключиться онлайн – все практики остаются в записи.\n\n"
        "Практики подходят всем, вне зависимости от опыта в йоге.\n\n"
        "Противопоказания:\n"
        "• беременность\n"
        "• злокачественные новообразования\n"
        "• болезни в острой фазе\n\n"
        "Что можно получить:\n"
        "- убрать боли в спине/теле\n"
        "- улучшить мобильность и выносливость тела\n"
        "- исправить осанку\n"
        "- стабилизировать психо-эмоциональное состояние\n"
        "- убрать зажимы в теле\n"
        "- научиться ровно и правильно дышать\n"
        "- наладить режим дня, сон\n"
        "- научиться отслеживать и контролировать свои неосознанные паттерны поведения\n\n"
        "ССЫЛКА НА ОПЛАТУ"
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
