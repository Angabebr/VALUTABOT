from telegram.ext import ApplicationBuilder
from bot_handlers import register_handlers
from dotenv import load_dotenv
import os



load_dotenv()
API_KEY = os.getenv("TELEGRAM_API_KEY")

if not API_KEY:
    raise ValueError("API_KEY не найден! Проверьте .env и имя переменной.")

def main():
    app = ApplicationBuilder().token(API_KEY).build()
    register_handlers(app)
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()