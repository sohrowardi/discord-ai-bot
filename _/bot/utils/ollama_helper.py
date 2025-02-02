from typing import List, Dict
import aiohttp
import json
import os
from .config import Config

class OllamaHandler:
    def __init__(self):
        self.history_file = "history.json"
        self.max_history = Config.MAX_HISTORY
        self.session = aiohttp.ClientSession()

    async def _truncate_history(self, history: List[Dict]) -> List[Dict]:
        return history[-self.max_history*2:]

    async def load_history(self) -> List[Dict]:
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    async def save_history(self, history: List[Dict]):
        with open(self.history_file, "w") as f:
            json.dump(history, f)

    async def generate_response(self, prompt: str) -> str:
        history = await self.load_history()
        history.append({"role": "user", "content": prompt})
        
        try:
            async with self.session.post(
                Config.OLLAMA_URL,
                json={
                    "model": Config.OLLAMA_MODEL,
                    "messages": history,
                    "stream": False
                },
                timeout=30
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                history.append(data["message"])
                history = await self._truncate_history(history)
                await self.save_history(history)
                
                return data["message"]["content"]
                
        except Exception as e:
            return f"Error: {str(e)}"