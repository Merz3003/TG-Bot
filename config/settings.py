from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str
    DEFAULT_CURRENCY: str = "RUB"

settings = Settings()
