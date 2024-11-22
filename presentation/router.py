from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters
from presentation.handlers import (
    start, choose_business, view_questions, add_question, save_question,
    delete_question, confirm_delete_question, create_plan
)

def setup_routes(application):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            "CHOOSE_BUSINESS": [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_business)
            ],
            "MANAGE_QUESTIONS": [
                MessageHandler(filters.Regex("Просмотреть вопросы"), view_questions),
                MessageHandler(filters.Regex("Добавить вопрос"), add_question),
                MessageHandler(filters.Regex("Удалить вопрос"), delete_question),
                MessageHandler(filters.Regex("Создать план"), create_plan),
            ],
            "SAVE_QUESTION": [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_question)
            ],
            "CONFIRM_DELETE_QUESTION": [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete_question)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", lambda update, context: update.message.reply_text("Диалог завершён."))
        ],
    )
    application.add_handler(conv_handler)
