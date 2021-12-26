from discord.ext import commands
import time

from bot import PlayTogether
from utils.embeds import Embeds
from utils.interactions import RoomSetView, RoomListGameView, RoomInfoView
from utils.room import MatchingRoom


class Room(commands.Cog):
    def __init__(self, bot: PlayTogether):
        self.bot = bot
        self.embeds = Embeds(self.bot.CustomEmojis)

    @commands.dm_only()
    @commands.command(name="게시물생성", aliases=["생성", "글생성", "방생성", "등록", "게시물등록"])
    async def _create_room(self, ctx: commands.Context, max_players: int, *, title: str):
        """
        방을 만듭니다.
        """
        if max_players < 2 or max_players > 12:
            return await ctx.send(":x: 2명 이상 12명 이하로 입력해주세요.", delete_after=5)

        if len(title) > 30:
            return await ctx.send(":x: 제목은 30자 이하로 입력해주세요.", delete_after=5)

        id = int(time.time()/2)

        room = MatchingRoom(id=id, title=title, host=ctx.author, max_players=max_players, timestamp=id)

        embed = self.embeds.room_info(room=room)
        view = RoomSetView(bot=self.bot, room=room)
        await ctx.send(view=view, embed=embed)

    @commands.dm_only()
    @commands.command(name="게시물목록", aliases=["글리스트", "목록", "글목록", "방목록"])
    async def _room_list(self, ctx: commands.Context):
        """
        방 목록을 보여줍니다.
        """
        await ctx.send(embed=self.embeds.roomlistEmbed, view=RoomListGameView(bot=self.bot, embeds=self.embeds))

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(create_instant_invite=True)
    @commands.command(name="게시물마감", aliases=["게시물종료", "방마감", "종료", "마감"])
    async def _close_room(self, ctx: commands.Context):
        """
        게시물 작성자일 경우 방을 마감합니다.
        """
        room = self.bot.RoomHandler.get_room_by_user(ctx.author)
        if not room:
            return await ctx.send(":x: 현재 방에 있지 않아요.", delete_after=5)

        if not room.host == ctx.author:
            return await ctx.send(":x: 게시물을 생성한 사람만 방을 종료할 수 있어요.", delete_after=5)
        
        link = await ctx.channel.create_invite(max_uses=room.max_players)
        for player in room.players:
            if player == ctx.author:
                continue

            await player.send(f":exclamation: {room.id}번 방이 마감되었어요! 방장의 서버 링크는 {link} 이에요.")

        await ctx.send(f":white_check_mark: {room.id}번 방을 성공적으로 마감했어요! 모든 참가자에게 해당 서버의 초대 링크를 전송할게요.", delete_after=5)

        self.bot.RoomHandler.close_room(room.id)

    @commands.dm_only()
    @commands.command(name="게시물삭제", aliases=["삭제", "글삭제", "방삭제"])
    async def _delete_room(self, ctx: commands.Context):
        """
            게시물 작성자일 경우 방을 삭제합니다.
        """
        room = self.bot.RoomHandler.get_room_by_user(ctx.author)
        if not room:
            return await ctx.send(":x: 현재 방에 있지 않아요.", delete_after=5)

        if not room.host == ctx.author:
            return await ctx.send(":x: 게시물을 생성한 사람만 방을 종료할 수 있어요.", delete_after=5)

        await ctx.send(f":white_check_mark: {room.id}번 방이 삭제되었어요.")

        for player in room.players:
            if player == ctx.author:
                continue

            await player.send(f":exclamation: {room.id}번 방이 인원 모집에 실패했어요. 다른 방에 참가해주세요.")

        self.bot.RoomHandler.close_room(room.id)

    @commands.dm_only()
    @commands.command(name="내방", aliases=["방", "방보기"])
    async def _my_room(self, ctx: commands.Context):
        """
        내가 있는 방을 보여줍니다.
        """
        room = self.bot.RoomHandler.get_room_by_user(ctx.author)
        if not room:
            return await ctx.send(":x: 현재 방에 있지 않아요.", delete_after=5)

        embed = self.embeds.room_info(room=room)
        await ctx.send(view=RoomInfoView(self.bot), embed=embed)


def setup(bot: PlayTogether):
    bot.add_cog(Room(bot))
