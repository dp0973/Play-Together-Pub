from typing import Union
from discord import Emoji


class CustomEmojis:
    def __init__(self):
        self.custom_emojis = {}
        self.custom_emojis_str = {}

    def load_emojis(self, emojis: tuple[Emoji]):
        for emoji in emojis:
            self.custom_emojis[emoji.name] = emoji
            self.custom_emojis_str[emoji.name] = f"<:{emoji.name}:{emoji.id}>"

    def get_emoji_str(self, name: str) -> str:
        if name in self.custom_emojis_str.keys():
            return self.custom_emojis_str[name]

        return ":black_large_square:"

    def get_emoji(self, name: str) -> Union[Emoji, None]:
        if name in self.custom_emojis.keys():
            return self.custom_emojis[name]

        return None

    
