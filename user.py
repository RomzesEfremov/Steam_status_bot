import datetime


class Steam_user():
    def __init__(self, id_steam: int, online: int,name_game: str, last_status_change: datetime):
        # self.id_tg = id_tg
        # self.user_name_tg = user_name_tg
        self.id_steam = id_steam
        self.name_game = name_game
        self.online = online
        self.last_status_change = last_status_change
