import requests

class OpenAIService:
    """Сервис для работы с OpenAI API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def generate_plan(self, business_type: str, answers: dict) -> str:
        prompt = f"""
        Клиентский бизнес: {business_type.capitalize()}.
        Ответы пользователя:
        {answers}

        Составь подробный план встречи в формате:
        1. Приветствие.
        2. Основные вопросы для обсуждения.
        3. Диагностика бизнеса.
        4. Предложения и рекомендации.
        5. Завершающие комментарии.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-3.5-turbo",  # Проверьте модель
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }

        # Выполнение запроса
        response = requests.post(self.api_url, json=payload, headers=headers)
        
        # Логирование ответа для диагностики
        print(f"Запрос: {payload}")
        print(f"Ответ сервера: {response.status_code}, {response.text}")
        
        # Обработка ошибок
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
