import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_URL: str = os.getenv("API_URL", "http://localhost:8000/api/v1/endpoints/")

settings = Settings()
