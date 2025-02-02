import tomli
import os
from dotenv import load_dotenv

load_dotenv()

with open("config.toml", "rb") as f:
    config = tomli.load(f)

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    PREFIX = config["discord"]["prefix"]
    
    OLLAMA_MODEL = config["ollama"]["model"]
    OLLAMA_URL = config["ollama"]["api_url"]
    MAX_HISTORY = config["ollama"]["max_history"]
    
    DATABASE_URL = config["database"]["url"]