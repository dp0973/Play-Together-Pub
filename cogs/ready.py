import discord
from discord import emoji
from discord.ext import commands

from bot import PlayTogether


class Ready(commands.Cog):
    def __init__(self, bot: PlayTogether):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game("[도움말"))

        emoji_server = await self.bot.fetch_guild(self.bot.emoji_server)
        self.bot.CustomEmojis.load_emojis(emoji_server.emojis)

        self.bot.owner = await self.bot.fetch_user(self.bot.owner_id)

        print(f"{self.bot.user} is ready!")


def setup(bot: PlayTogether):
    bot.add_cog(Ready(bot))