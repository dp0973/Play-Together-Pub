import discord
from discord import Embed
from bot import PlayTogether

from utils.embeds import Embeds
from utils.emojis import CustomEmojis
from utils.room import MatchingRoom


class PaginatorView(discord.ui.View):
    def __init__(self, embeds: list[Embed]):
        super().__init__()
        self.embeds = embeds
        self.index = 0
        self.total = len(embeds)

    @discord.ui.button(label="뒤로", emoji="◀️", style=discord.ButtonStyle.primary)
    async def backward(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index -= 1
        if self.index < 0:
            self.index = self.total - 1

        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(label="앞으로", emoji="▶️", style=discord.ButtonStyle.primary)
    async def forward(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index += 1
        if self.index >= self.total:
            self.index = 0

        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)


class RoomPaginatorView(discord.ui.View):
    def __init__(self, bot: PlayTogether, room_ids: list[int], embeds: list[Embed]):
        super().__init__()
        self.bot = bot
        self.embeds = embeds
        self.index = 0
        self.room_ids = room_ids
        self.current_room_id = room_ids[0]
        self.total = len(embeds)

    @discord.ui.button(label="뒤로", emoji="◀️", style=discord.ButtonStyle.primary)
    async def backward(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index -= 1
        if self.index < 0:
            self.index = self.total - 1

        self.current_room_id = self.room_ids[self.index]
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(label="앞으로", emoji="▶️", style=discord.ButtonStyle.primary)
    async def forward(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index += 1
        if self.index >= self.total:
            self.index = 0

        self.current_room_id = self.room_ids[self.index]
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(label="들어가기", emoji="📥", style=discord.ButtonStyle.green)
    async def enter(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.bot.RoomHandler.is_user_in_room(interaction.user):
            return await interaction.response.send_message(":x: 이미 방에 있어요. 현재 있는 방을 나가서 다시 시도해주세요.", ephemeral=True, delete_after=5)

        if self.bot.RoomHandler.is_room_full(self.current_room_id):
            return await interaction.response.send_message(":x: 방이 이미 꽉 찼어요. 나중에 다시 시도해주세요.", ephemeral=True, delete_after=5)

        self.bot.RoomHandler.join_room(self.current_room_id, interaction.user)
        room = self.bot.RoomHandler.rooms[self.current_room_id]

        await room.host.send(f":loudspeaker: {interaction.user.name} 님이 {room.id}번 방에 입장했어요. ({len(room.players)}/{room.max_players})")
        if len(room.players) == room.max_players:
            await room.host.send(f":white_check_mark: {room.id}번 방이 채워졌어요! 본인이 관리자인 서버에서 `[방마감`을 입력하면 참가자 모두에게 서버 초대 링크를 전송해요.")

        await interaction.response.send_message(f":white_check_mark: {room.id}번 방에 입장했어요.", ephemeral=True)

    @discord.ui.button(label="신고", emoji="🚫", style=discord.ButtonStyle.red)
    async def report(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("신고 사유를 적어주세요. (시간 제한 - 1분)", ephemeral=True, delete_after=5)
        msg = await self.bot.wait_for(
            "message", check=lambda m: m.author == interaction.user, timeout=60
        )
        
        await interaction.channel.send(f":exclamation: 성공적으로 {self.current_room_id}번 게시물을 신고했어요! 신고 사유: {msg.content}")
        await self.bot.owner.send(f":exclamation: {interaction.user.name} 님이 {self.current_room_id}번 게시물의 신고를 요청했어요. 신고 사유: {msg.content}")


class RoomListGameSelect(discord.ui.Select):
    def __init__(self, emojis: CustomEmojis):
        options = [
            discord.SelectOption(
                label="모두", description="All", value="All", emoji="⬛"
            ),
            discord.SelectOption(
                label="리그 오브 레전드", description="League of Legends", value="LoL", emoji=emojis.get_emoji("LoL")
            ),
            discord.SelectOption(
                label="배틀그라운드",
                description="Playerunknown's Battlegrounds", emoji=emojis.get_emoji("PUBG"),
                value="PUBG",
            ),
            discord.SelectOption(
                label="오버워치", description="Overwatch", value="Overwatch", emoji=emojis.get_emoji("Overwatch")
            ),
            discord.SelectOption(
                label="메이플스토리", description="Maplestory", value="Maplestory", emoji=emojis.get_emoji("Maplestory")
            ),
            discord.SelectOption(label="서든어택", description="Sudden Attack", value="SA", emoji=emojis.get_emoji("SA")),
            discord.SelectOption(
                label="피파 온라인 4", description="Fifa Online 4", value="FO4", emoji=emojis.get_emoji("FO4")
            )
        ]

        super().__init__(
            placeholder="게임을 선택해주세요",
            min_values=1,
            max_values=1,
            options=options,
            row=2,
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoomListGameView = self.view
        room_ids = []

        if self.values[0] == "All":
            room_ids = list(view.bot.RoomHandler.rooms.keys())

        else:
            for room_id, room in view.bot.RoomHandler.rooms.items():
                if room.game == self.values[0]:
                    room_ids.append(room_id)

        if not room_ids:
            return await interaction.response.send_message(":x: 해당 게임의 방이 없어요. 다른 게임을 선택해주세요.", ephemeral=True, delete_after=5)
        
        embeds = []
        for i, room_id in enumerate(room_ids):
            embeds.append(view.embeds.room_page_info(room=view.bot.RoomHandler.get_room(room_id), page=i+1, page_count=len(room_ids)))

        new_view = RoomPaginatorView(bot=view.bot, room_ids=room_ids, embeds=embeds)

        return await interaction.response.edit_message(embed=embeds[0], view=new_view)


class RoomListGameView(discord.ui.View):
    def __init__(self, bot: PlayTogether, embeds: Embeds):
        super().__init__()
        self.bot = bot
        self.embeds = embeds
        self.add_item(RoomListGameSelect(self.bot.CustomEmojis))


class RoomInfoView(discord.ui.View):
    def __init__(self, bot: PlayTogether):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="나가기", emoji="🚪", style=discord.ButtonStyle.primary)
    async def leave(self, button: discord.ui.Button, interaction: discord.Interaction):
        room = self.bot.RoomHandler.get_room_by_user(interaction.user)
        if interaction.user == room.host:
            return await interaction.response.send_message(":x: 방장은 방을 나갈 수 없어요. `[게시물삭제`를 통해 방을 삭제해주세요.", ephemeral=True, delete_after=5)

        self.bot.RoomHandler.leave_room(interaction.user)

        await interaction.response.send_message(f":white_check_mark: {room.id}번 방을 나갔어요.", ephemeral=True)
        await room.host.send(f":door: {interaction.user.name} 님이 방을 나갔어요.")


class RoomGameSelect(discord.ui.Select):
    def __init__(self, emojis: CustomEmojis):
        options = [
            discord.SelectOption(
                label="리그 오브 레전드", description="League of Legends", value="LoL", emoji=emojis.get_emoji("LoL")
            ),
            discord.SelectOption(
                label="배틀그라운드",
                description="Playerunknown's Battlegrounds", emoji=emojis.get_emoji("PUBG"),
                value="PUBG",
            ),
            discord.SelectOption(
                label="오버워치", description="Overwatch", value="Overwatch", emoji=emojis.get_emoji("Overwatch")
            ),
            discord.SelectOption(
                label="메이플스토리", description="Maplestory", value="Maplestory", emoji=emojis.get_emoji("Maplestory")
            ),
            discord.SelectOption(label="서든어택", description="Sudden Attack", value="SA", emoji=emojis.get_emoji("SA")),
            discord.SelectOption(
                label="피파 온라인 4", description="Fifa Online 4", value="FO4", emoji=emojis.get_emoji("FO4")
            ),
            discord.SelectOption(
                label="기타", description="Others", value="Others", emoji="⬛"
            )
        ]

        super().__init__(
            placeholder="게임을 선택해주세요",
            min_values=1,
            max_values=1,
            options=options,
            row=2,
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoomSetView = self.view

        game = self.values[0]
        if game == "Others":
            await interaction.response.send_message("게임 제목을 입력해주세요. ex - 로스트 아크 (시간 제한 - 1분)", ephemeral=True, delete_after=5)
            msg = await view.bot.wait_for(
            "message", check=lambda m: m.author == interaction.user, timeout=60
            )
            game = msg.content

        view.room.set_game(game)
        view.remove_item(self)
        
        view.game_set = True
        if view.game_set and view.desc_set:
            view.children[3].disabled = False

        await interaction.message.edit(view=view, embed=view.embeds.room_info(view.room))


class MaxPlayersSetButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="인원 수정",
            emoji="📝",
            style=discord.ButtonStyle.primary,
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoomSetView = self.view

        await interaction.response.send_message(":exclamation: 최대 인원을 입력해주세요. (시간 제한 - 30초)", ephemeral=True, delete_after=5)
        title: discord.Message = await view.bot.wait_for(
            "message", check=lambda m: m.author == interaction.user, timeout=30
        )
        
        try:
            max_players = int(title.content)
            if max_players < 2 or max_players > 12:
                raise ValueError
        except ValueError:
            return await interaction.channel.send(":x: 2명 이상 12명 이하로 입력해주세요.", delete_after=5)

        view.room.set_max_players(int(title.content))

        await interaction.message.edit(
            content=":white_check_mark: 최대 인원 수를 수정했어요!", embed=view.embeds.room_info(view.room), view=view
        )


class GameSetButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="게임 설정",
            emoji="🎮",
            style=discord.ButtonStyle.primary,
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoomSetView = self.view

        view.add_item(RoomGameSelect(view.bot.CustomEmojis))

        await interaction.response.edit_message(view=view, embed=interaction.message.embeds[0])


class DescSetButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="방 설명 설정",
            emoji="💬",
            style=discord.ButtonStyle.primary,
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoomSetView = self.view

        await interaction.response.send_message("설명을 입력해주세요. 최대 100자 (시간 제한 - 3분)", ephemeral=True, delete_after=5)
        desc: discord.Message = await view.bot.wait_for(
            "message", check=lambda m: m.author == interaction.user, timeout=180
        )
        if len(desc.content) > 100:
            return await interaction.channel.send(":x: 최대 100자를 초과했어요. 버튼을 다시 눌러 시도해주세요.", delete_after=5)

        view.room.set_desc(desc.content)

        view.desc_set = True
        if view.game_set and view.desc_set:
            view.children[3].disabled = False

        await interaction.message.edit(
            content=":white_check_mark: 게시물 설명이 설정되었어요.", embed=view.embeds.room_info(view.room), view=view
        )


class RoomRegisterButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="방 등록",
            emoji="✏️",
            style=discord.ButtonStyle.green,
        )

    async def callback(self, interaction: discord.Interaction):
        view: RoomSetView = self.view
        view.bot.RoomHandler.register_room(view.room)

        for child in view.children:
            child.disabled = True

        view.stop()

        await interaction.response.edit_message(
            content=":white_check_mark: 방이 성공적으로 등록되었어요. `[게시물마감`을 통해 방을 마감할 수 있어요.", view=view
        )


class RoomSetView(discord.ui.View):
    def __init__(self, bot: PlayTogether, room: MatchingRoom):
        super().__init__()

        self.add_item(GameSetButton())
        self.add_item(DescSetButton())
        self.add_item(MaxPlayersSetButton())
        self.add_item(RoomRegisterButton())
        self.children[3].disabled = True

        self.bot = bot
        self.embeds = Embeds(self.bot.CustomEmojis)
        self.room = room

        self.desc_set = False
        self.game_set = False
        