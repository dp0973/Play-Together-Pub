import discord

from utils.emojis import CustomEmojis
from utils.room import MatchingRoom


class Embeds:
    def __init__(self, emojis: CustomEmojis):
        self.emojis = emojis

        self.helpEmbed = discord.Embed(
            title=":book: 도움말",
            description="**PlTo**의 사용 방법에 대한 도움말입니다!",
            color=discord.Color.random()
        )
        self.helpEmbed.add_field(
            name="1. 게시물(방) 생성하기",
            value="모든 유저는 봇의 dm에서 `[게시물생성` 명령어를 입력하여 게임 파트너를 모집하는 게시물을 생성할 수 있어요.\n",
            inline=False
        )
        self.helpEmbed.add_field(
            name="2. 다른 유저들의 방을 탐색하고 참가하기",
            value="만약 다른 사람들이 생성한 게시물(방)에 참가하고 싶다면 `[게시물목록`을 사용해 방의 목록을 확인하고, 버튼을 통해 참가하거나 신고할 수 있어요.\n",
            inline=False
        )
        self.helpEmbed.add_field(
            name="3. 게시물 마감하기",
            value="방에 충분한 인원이 모였다고 판단하면 방의 호스트는 `[게시물마감` 명령어를 사용해 마감할 수 있어요. 방의 마감은 자신이 관리자 권한을 가진 서버에서 진행해야 하고, 마감하는 즉시 방의 모든 참가자에게 그 서버의 초대 주소를 보내요.\n",
            inline=False    
        )
        self.helpEmbed.add_field(
            name="명령어 목록 불러오기",
            value="`[명령어`를 사용하여 명령어 목록을 불러올 수 있어요.\n",
            inline=False
        )

        self.commandsEmbed = discord.Embed(
            title=":book: 명령어 목록 (1/2)",
            description="**PlTo**의 명령어 목록입니다!",
            color=discord.Color.blue()
        )
        self.commandsEmbed.add_field(
            name="[게시물생성 (최대 참가자 수) (게시물 제목)",
            value="**방을 생성하는 명령어입니다.** 봇과의 dm에서만 사용 가능합니다. 최대 참가자 수는 2~12명, 제목은 30자 이하여야 합니다. (aka. 방생성, 생성, 게시물등록...)\n",
            inline=False
        )
        self.commandsEmbed.add_field(
            name="[게시물목록",
            value="**게시물 목록을 불러오는 명령어입니다.** 봇과의 dm에서만 사용 가능합니다. 해당 목록에서 방을 탐색해 참가할 수 있습니다. (aka. 방목록, 목록...)\n",
            inline=False
        )
        self.commandsEmbed.add_field(
            name="[게시물마감",
            value="**게시물을 마감하는 명령어입니다.** 본인이 관리자인 서버에서만 사용 가능합니다. 사용 즉시 해당 방 참가자 모두에게 그 서버의 초대 주소를 전송합니다. 호스트만 사용할 수 있습니다. (aka. 마감, 방마감, 종료...)\n",
            inline=False
        )
        self.commandsEmbed.add_field(
            name="[내방",
            value="**내가 참여 중인 방의 정보를 불러오는 명령어입니다.** 봇과의 dm에서만 사용 가능합니다. 이 명령어를 통해 방에서 나갈 수 있습니다. (aka. 방보기, 방...)\n",
            inline=False
        )
        self.commandsEmbed.add_field(
            name="[게시물삭제",
            value="**게시물을 삭제하는 명령어입니다.** 봇과의 dm에서만 사용 가능합니다. 해당 방의 호스트만 사용할 수 있습니다. (aka. 삭제, 방삭제...)\n",
            inline=False
        )

        self.commandsEmbed2 = discord.Embed(
            title=":book: 명령어 목록 (2/2)",
            description="**PlTo**의 명령어 목록입니다!",
            color=discord.Color.blue()
        )
        self.commandsEmbed2.add_field(
            name="[초대",
            value="봇의 초대 링크를 전송합니다.\n",
            inline=False
        )
        self.commandsEmbed2.add_field(
            name="[도움말",
            value="봇의 사용 방법을 불러옵니다.\n",
            inline=False
        )
        self.commandsEmbed2.add_field(
            name="[명령어",
            value="봇의 명령어 목록을 불러옵니다.\n",
        )

        self.inviteEmbed = discord.Embed(
            title=":link: 초대",
            description="**PlTo**의 초대 주소입니다! [여기](https://discord.com/oauth2/authorize?client_id=807225018156449812&scope=bot&permissions=347137)를 클릭하여 초대해주세요!",
            color=discord.Color.random()
        )

        self.roomlistEmbed = discord.Embed(
            title=":book: 게임 선택하기",
            description="검색할 게임을 선택하세요!",
            color=discord.Color.blue()
        )

    def room_info(self, room: MatchingRoom):
        embed = discord.Embed(
            title=f":tools: {room.title}",
            description=f"**호스트:** {room.host.name}",
            color=discord.Color.blue(),
        )

        embed.set_footer(text=f"방 ID: {room.id}")
        embed.add_field(
            name="**게임 :video_game:**", value=f"{self.emojis.get_emoji_str(room.game)} {room.game}" if room.game else "-"
        )
        embed.add_field(name="**참가자 수 :pencil:**", value=f"{len(room.players)}/{room.max_players}")
        embed.add_field(name="**정보 :speech_balloon:**", value=room.description if room.description else "-", inline=False)
        return embed

    def room_page_info(self, room: MatchingRoom, page: int, page_count: int):
        embed = discord.Embed(
            title=f":green_book: {room.title} ({page}/{page_count})",
            description=f"**호스트:** {room.host.name}",
            color=discord.Color.blue(),
        )

        embed.set_footer(text=f"방 ID: {room.id}")
        embed.add_field(
            name="**게임 :video_game:**", value=f"{self.emojis.get_emoji_str(room.game)} {room.game}" if room.game else "-"
        )
        embed.add_field(name="**참가자 수 :pencil:**", value=f"{len(room.players)}/{room.max_players}")
        embed.add_field(name="**정보 :speech_balloon:**", value=room.description if room.description else "-", inline=False)
        return embed
