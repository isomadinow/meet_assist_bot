import json
import os

class Persistence:
    """Класс для сохранения и загрузки данных."""

    def __init__(self, file_path="data.json"):
        self.file_path = file_path

    def save_data(self, data):
        """
        Сохраняет данные в файл JSON.
        :param data: Данные для сохранения.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def load_data(self):
        """
        Загружает данные из файла JSON.
        :return: Данные, считанные из файла.
        """
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return {}
