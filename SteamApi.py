import requests
import json
from user import Steam_user
import datetime
import db


steam_id = "76561198046867429,76561198023956947,76561198081243221,76561198135592820,76561198004765254,76561198045490526,76561198167091486"


def create_users(steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=512A36593F23909C377B98CC74F5F4EB&steamids={steam_id}&"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)  # получаем в ответ json
    all_users = json.loads(response.text)["response"]["players"]
    new_users = []
    for u in all_users:
        new = Steam_user(u["steamid"],u["personastate"], u.get("gameextrainfo", "не играет"), datetime.datetime.now())
        new_users.append(new)

    return new_users


def steam_id_users_db(users_steam_id):
    all_users = ''
    for users in users_steam_id:
        for user in users:
            all_users += f'{user},'
    return all_users

def send_info_user_from_db(all_user):
    for user in all_user:
        game = db.select_game_info(user.id_steam)
        if game is None:
            db.inner_db_steam_bot(user.id_steam, user.name_game, user.online, user.last_status_change)
            return (user.name_game, user.id_steam)

        elif game[0] != user.name_game:
            db.inner_db_steam_bot(user.id_steam, user.name_game, user.online, user.last_status_change)
            return (user.name_game, user.id_steam)




