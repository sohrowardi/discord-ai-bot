from discord.ext import commands
from ..utils.ollama_helper import OllamaHandler

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ollama = OllamaHandler()

    @commands.command()
    async def help(self, ctx):
        """Show help message"""
        await ctx.send("Available commands: !help, !reset, !model")

    @commands.command()
    async def reset(self, ctx):
        """Reset conversation history"""
        await self.ollama.save_history([])
        await ctx.send("Conversation history cleared!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def model(self, ctx, model_name: str):
        """Change AI model"""
        self.ollama.model = model_name
        await ctx.send(f"Model changed to {model_name}")