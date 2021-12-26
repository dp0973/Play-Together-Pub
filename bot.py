from discord.ext import commands
import os

import cogs
from utils.emojis import CustomEmojis
from utils.room import RoomHandler


token = os.environ["BOT_TOKEN"]
emoji_server = os.environ["EMOJI_SERVER"]
owner_id = os.environ["OWNER_ID"]


class PlayTogether(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or("["), help_command=None
        )

        self.RoomHandler = RoomHandler()
        self.CustomEmojis = CustomEmojis()
        self.emoji_server = emoji_server
        self.owner_id = owner_id

        cogs.load(self)


if __name__ == "__main__":
    bot = PlayTogether()
    bot.run(token)
