from telegram.ext import Application
from presentation.router import setup_routes
from config import TELEGRAM_BOT_TOKEN
from application.question_service import QuestionService

def main():
    # Загрузка данных из хранилища
    QuestionService()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    setup_routes(application)
    application.run_polling()

if __name__ == "__main__":
    main()
