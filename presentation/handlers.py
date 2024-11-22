from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes
from presentation.keyboards import business_type_keyboard, manage_questions_keyboard, question_delete_keyboard
from application.question_service import QuestionService
from application.plan_service import PlanService
from infrastructure.openai_service import OpenAIService
from config import OPENAI_API_KEY

# Инициализация сервисов
question_service = QuestionService()
plan_service = PlanService(OpenAIService(api_key=OPENAI_API_KEY))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Начало диалога: отображение доступных бизнесов."""
    business_types = question_service.get_all_business_types()
    if business_types:
        await update.message.reply_text(
            "Выберите тип бизнеса:",
            reply_markup=business_type_keyboard(business_types)
        )
    else:
        await update.message.reply_text(
            "На данный момент нет сохранённых бизнесов. Напишите новый тип бизнеса."
        )
    return "CHOOSE_BUSINESS"


async def choose_business(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Обработчик выбора типа бизнеса."""
    business_type = update.message.text.lower()
    context.user_data["business_type"] = business_type
    questions = question_service.get_questions(business_type)

    if questions:
        await update.message.reply_text(
            f"Вопросы для бизнеса '{business_type}':\n" +
            "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions)),
            reply_markup=manage_questions_keyboard()
        )
    else:
        await update.message.reply_text(
            f"Бизнес '{business_type}' не найден. Добавьте вопросы для этого бизнеса.",
            reply_markup=manage_questions_keyboard()
        )
    return "MANAGE_QUESTIONS"


async def view_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Отображение текущих вопросов для выбранного бизнеса."""
    business_type = context.user_data["business_type"]
    questions = question_service.get_questions(business_type)

    if questions:
        await update.message.reply_text(
            f"Текущие вопросы для бизнеса '{business_type}':\n" +
            "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions)),
            reply_markup=manage_questions_keyboard()
        )
    else:
        await update.message.reply_text(
            f"Для бизнеса '{business_type}' пока нет вопросов.",
            reply_markup=manage_questions_keyboard()
        )
    return "MANAGE_QUESTIONS"


async def add_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Начало добавления нового вопроса."""
    await update.message.reply_text("Введите новый вопрос:")
    return "SAVE_QUESTION"


async def save_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Сохранение нового вопроса для выбранного бизнеса."""
    business_type = context.user_data["business_type"]
    question = update.message.text
    question_service.add_question(business_type, question)

    await update.message.reply_text(
        f"Вопрос добавлен: {question}",
        reply_markup=manage_questions_keyboard()
    )
    return "MANAGE_QUESTIONS"


async def delete_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Отображение списка вопросов для удаления."""
    business_type = context.user_data["business_type"]
    questions = question_service.get_questions(business_type)

    if not questions:
        await update.message.reply_text(
            f"Для бизнеса '{business_type}' нет вопросов для удаления.",
            reply_markup=manage_questions_keyboard()
        )
        return "MANAGE_QUESTIONS"

    await update.message.reply_text(
        "Выберите номер вопроса для удаления:\n" +
        "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions)),
        reply_markup=question_delete_keyboard(questions)
    )
    return "CONFIRM_DELETE_QUESTION"


async def confirm_delete_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Подтверждение удаления вопроса."""
    business_type = context.user_data["business_type"]
    questions = question_service.get_questions(business_type)

    try:
        index = int(update.message.text) - 1
        deleted_question = question_service.delete_question(business_type, index)
        if deleted_question:
            await update.message.reply_text(
                f"Вопрос удалён: {deleted_question}",
                reply_markup=manage_questions_keyboard()
            )
        else:
            await update.message.reply_text("Неверный номер вопроса.", reply_markup=manage_questions_keyboard())
    except ValueError:
        await update.message.reply_text("Введите корректный номер.", reply_markup=manage_questions_keyboard())
    return "MANAGE_QUESTIONS"


async def create_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Создание плана встречи через OpenAI."""
    business_type = context.user_data["business_type"]
    questions = question_service.get_questions(business_type)

    if not questions:
        await update.message.reply_text(
            f"Для бизнеса '{business_type}' нет сохранённых вопросов. Добавьте вопросы, чтобы создать план.",
            reply_markup=manage_questions_keyboard()
        )
        return "MANAGE_QUESTIONS"

    answers = {f"Вопрос {i+1}": f"Ответ пользователя на {q}" for i, q in enumerate(questions)}  # Заглушка
    plan = plan_service.generate_plan(business_type, answers)

    await update.message.reply_text(
        f"План встречи:\n\n{plan}",
        reply_markup=ReplyKeyboardRemove()
    )
    return "END_DIALOG"
