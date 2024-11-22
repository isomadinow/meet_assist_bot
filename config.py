from decouple import config

# Загружаем токены из переменных окружения
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = config("OPENAI_API_KEY")
