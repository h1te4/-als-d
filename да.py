import os
import threading
from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Конфигурация ---
TOKEN = "8157726360:AAEkY_UW7JMATD2G0cuFBs60ZwJRHmAcy54"
WEB_APP_URL = "https://h1te4.github.io/test/index.html"  # Замените на URL вашего веб-приложения
# ---------------------

# --- Веб-сервер Flask ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run_flask():
    # Используйте 0.0.0.0, чтобы сделать сервер доступным извне
    app.run(host='0.0.0.0', port=8080)
# ------------------------


# --- Телеграм-бот ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с кнопкой для запуска веб-приложения."""
    keyboard = [
        [InlineKeyboardButton("Открыть приложение", web_app={"url": WEB_APP_URL})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы запустить приложение:",
        reply_markup=reply_markup
    )

def run_bot():
    """Запускает бота."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()
# --------------------


if __name__ == "__main__":
    # Запускаем Flask и бота в разных потоках
    flask_thread = threading.Thread(target=run_flask)
    bot_thread = threading.Thread(target=run_bot)

    flask_thread.start()
    bot_thread.start()

    flask_thread.join()
    bot_thread.join()
