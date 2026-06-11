import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FINNHUB_API_KEY: str = os.getenv("FINNHUB_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")

config = Config()
