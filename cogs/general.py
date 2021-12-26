from discord.ext import commands

from bot import PlayTogether
from utils.embeds import Embeds
from utils.interactions import PaginatorView


class General(commands.Cog):
    def __init__(self, bot: PlayTogether):
        self.bot = bot
        self.embeds = Embeds(self.bot.CustomEmojis)
    
    @commands.command(name="도움말", aliases=["help"])
    async def _help(self, ctx: commands.Context):
        await ctx.send(embed=self.embeds.helpEmbed)

    @commands.command(name="명령어", aliases=["commands"])
    async def _commands(self, ctx: commands.Context):
        embeds = [self.embeds.commandsEmbed, self.embeds.commandsEmbed2]
        await ctx.send(embed=embeds[0], view=PaginatorView(embeds))

    @commands.command(name="초대", aliases=["invite"])
    async def _invite(self, ctx: commands.Context):
        await ctx.send(embed=self.embeds.inviteEmbed)


def setup(bot: PlayTogether):
    bot.add_cog(General(bot))
