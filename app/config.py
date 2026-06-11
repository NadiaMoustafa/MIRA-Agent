import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    LLM_MODEL: str = "llama-3.3-70b-versatile"  
    
    MAX_TOOL_CALLS: int = 10  
    
    MONITOR_INTERVAL_HOURS: int = 24 

config = Config()