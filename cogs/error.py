from discord.ext import commands
from discord.ext.commands.errors import (
    BadArgument,
    CommandNotFound,
)

from bot import PlayTogether


class Error(commands.Cog):
    def __init__(self, bot: PlayTogether) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, CommandNotFound):
            await ctx.send(
                ":x: 명령어를 찾지 못했어요. `[명령어`를 통해 명령어 목록을 확인할 수 있어요.", delete_after=5
            )

        elif isinstance(error, BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                ":x: 명령어 사용이 잘못되었어요. `[명령어`를 통해 사용 방법을 확인할 수 있어요.", delete_after=5
            )

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(
                ":x: 이 명령어는 서버에서만 사용할 수 있어요.", delete_after=5
            )

        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                ":x: 이 명령어는 DM에서만 사용할 수 있어요.", delete_after=5
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                ":x: 봇 또는 본인의 권한을 확인해주세요.", delete_after=5
            )

        else:
            await ctx.send(":x: 알 수 없는 오류가 발생했어요. 봇 소유자에게 자동으로 에러 로그를 보낼게요.", delete_after=5)
            raise error


def setup(bot: PlayTogether):
    bot.add_cog(Error(bot))