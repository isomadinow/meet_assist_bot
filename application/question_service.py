from shared.state import business_questions
from infrastructure.persistence import Persistence

persistence = Persistence()

class QuestionService:
    """Управление вопросами для бизнеса."""

    def __init__(self):
        self.data = persistence.load_data()
        global business_questions
        business_questions = self.data if self.data else business_questions

    def get_all_business_types(self):
        """
        Возвращает список всех типов бизнеса.
        """
        return list(business_questions.keys())

    def get_questions(self, business_type: str):
        """
        Возвращает список вопросов для указанного типа бизнеса.
        """
        return business_questions.get(business_type, [])

    def add_question(self, business_type: str, question: str):
        """
        Добавляет новый вопрос для указанного типа бизнеса.
        """
        if business_type not in business_questions:
            business_questions[business_type] = []
        business_questions[business_type].append(question)
        persistence.save_data(business_questions)

    def delete_question(self, business_type: str, index: int):
        """
        Удаляет вопрос по индексу из списка вопросов указанного типа бизнеса.
        """
        if business_type in business_questions:
            try:
                deleted_question = business_questions[business_type].pop(index)
                persistence.save_data(business_questions)
                return deleted_question
            except IndexError:
                return None
