from discord.ext import commands
from utils.config import Config
from cogs import ai_chat, commands

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        await self.add_cog(ai_chat.AICog(self))
        await self.add_cog(commands.CommandCog(self))

async def main():
    bot = Bot()
    await bot.start(Config.DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())