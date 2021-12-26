from discord import User
from typing import Union


class MatchingRoom:
    def __init__(
        self,
        id: int,
        title: str,
        host: User,
        max_players: int,
        timestamp: int,
    ):
        self.id = id
        self.title = title
        self.host = host
        self.players = [host]
        self.max_players = max_players
        self.timestamp = timestamp
        self.description = None
        self.game = None

    def set_desc(self, description: str):
        self.description = description

    def set_game(self, game: str):
        self.game = game
    
    def set_max_players(self, max_players: int):
        self.max_players = max_players

    def add_user(self, user: User):
        self.players.append(user)

    def del_user(self, user: User):
        self.players.remove(user)


class RoomHandler:
    def __init__(self):
        self.rooms: dict[int, MatchingRoom] = {}  # room_id: room
        self.users: dict[User, int] = {}  # user: room_id

    def is_room_exist(self, room_id: int) -> bool:
        return room_id in self.rooms

    def is_room_full(self, room_id: int) -> bool:
        return len(self.rooms[room_id].players) >= self.rooms[room_id].max_players

    def is_user_in_room(self, user: User) -> bool:
        return user in self.users

    def register_room(self, room: MatchingRoom):
        self.rooms[room.id] = room
        self.users[room.host] = room.id

    def close_room(self, room_id: int):
        for user in self.rooms[room_id].players:
            del self.users[user]

        del self.rooms[room_id]

    def join_room(self, room_id: int, user: User):
        self.rooms[room_id].add_user(user)
        self.users[user] = room_id

    def leave_room(self, user: User):
        room_id = self.users[user]
        self.rooms[room_id].del_user(user)
        del self.users[user]

    def get_room(self, room_id: int) -> Union[MatchingRoom, None]:
        if room_id in self.rooms:
            return self.rooms[room_id]
        
        return None

    def get_room_by_user(self, user: User) -> Union[MatchingRoom, None]:
        if self.is_user_in_room(user):
            return self.get_room(self.users[user])
        
        return None
