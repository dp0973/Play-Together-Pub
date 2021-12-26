from discord.ext import commands

from bot import PlayTogether


class Admin(commands.Cog):
    def __init__(self, bot: PlayTogether):
        self.bot = bot
    
    @commands.command(name="방제거", aliases=["제거", "방삭제", "삭제"])
    async def _remove_room(self, ctx: commands.Context, room_id: int):
        room = self.bot.RoomHandler.get_room(room_id)
        for player in room.players:
            await player.send(":x: 관리자가 현재 있는 방을 강제로 삭제했어요. 스팸방으로 판단하였을 가능성이 높아요.")

        await self.bot.RoomHandler.close_room(room_id)

        await ctx.send(f":white_check_mark: {room_id}번 방을 삭제했어요.")


def setup(bot: PlayTogether):
    bot.add_cog(Admin(bot))
