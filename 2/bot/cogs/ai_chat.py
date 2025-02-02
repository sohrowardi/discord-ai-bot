import discord
from discord.ext import commands
from ..utils.ollama_helper import OllamaHandler

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ollama = OllamaHandler()
        self.rate_limits = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Check if bot is mentioned
        if self.bot.user.mentioned_in(message):
            async with message.channel.typing():
                prompt = message.clean_content.replace(
                    f"@{self.bot.user.name}", ""
                ).strip()
                
                # Rate limiting
                if await self._check_rate_limit(message.author):
                    response = await self.ollama.generate_response(prompt)
                    await message.reply(response[:2000])

    async def _check_rate_limit(self, user: discord.User) -> bool:
        # Allow 5 requests per minute
        if user.id not in self.rate_limits:
            self.rate_limits[user.id] = []
        
        now = discord.utils.utcnow().timestamp()
        self.rate_limits[user.id] = [
            t for t in self.rate_limits[user.id] if t > now - 60
        ]
        
        if len(self.rate_limits[user.id]) >= 5:
            return False
            
        self.rate_limits[user.id].append(now)
        return True