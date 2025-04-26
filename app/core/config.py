from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME")
    API_URL: str  = os.getenv("API_URL")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
