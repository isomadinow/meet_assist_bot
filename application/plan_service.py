from infrastructure.openai_service import OpenAIService

class PlanService:
    """Генерация планов через OpenAI."""

    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service

    def generate_plan(self, business_type: str, answers: dict) -> str:
        return self.openai_service.generate_plan(business_type, answers)
