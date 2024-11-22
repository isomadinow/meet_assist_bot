from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

def business_type_keyboard(business_types):
    """Клавиатура для выбора типа бизнеса."""
    keyboard = [[business] for business in business_types] + [["Добавить новый тип бизнеса"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def manage_questions_keyboard():
    """Клавиатура для управления вопросами."""
    keyboard = [
        ["Просмотреть вопросы", "Добавить вопрос"],
        ["Удалить вопрос", "Создать план"],
        ["Завершить управление"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def question_delete_keyboard(questions):
    """Клавиатура для выбора вопроса для удаления."""
    keyboard = [[str(i + 1)] for i in range(len(questions))]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
