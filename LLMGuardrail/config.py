# config.py
import os

class AppConfig:
    project_folder = os.path.dirname(os.path.abspath(__file__))
    local_database = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) )+ "/local_database"
    OPENAI_BASE_URL = ""
    OPENAI_API_SECRET_KEY = ""

    
    @classmethod
    def initConfig(cls):
        folders = [
            cls.local_database,
        ]

        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")