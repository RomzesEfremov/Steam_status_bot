import psycopg2
import db_config

try:
    connection = psycopg2.connect(
        host=db_config.host,
        user=db_config.user,
        password=db_config.password,
        database=db_config.db_name
    )
    connection.autocommit = True

except Exception as ex:
    print(Exception)
    if connection:
        connection.close()

cursor = connection.cursor()


def check_db(steam_id: str, chat_id: str):
    cursor.execute(
        f"SELECT steam_id FROM steam_bot.tg_steam_bot tsb WHERE steam_id = \'{steam_id}\' and chat_id= \'{chat_id}\'")
    return cursor.fetchone()


def insert_db(tg_user_id: str, chat_id: str, steam_id: str, name_user: str):
    cursor.execute(
        f"INSERT INTO steam_bot.tg_steam_bot (tg_user_id, chat_id, steam_id, name_user) VALUES (\'{tg_user_id}\', \'{chat_id}\',\'{steam_id}\',\'{name_user}\');")


def inner_db_steam_bot(steam_id: str, name_game: str, in_online: int, last_status_change):
    cursor.execute(
        f"INSERT INTO steam_bot.db_steam_bot (steam_id, name_game, in_online, last_status_change) "
        f"VALUES (\'{steam_id}\', \'{name_game}\',\'{in_online}\', \'{last_status_change}\');")


def select_steam_id():
    cursor.execute(f"SELECT DISTINCT steam_id from steam_bot.tg_steam_bot;")
    return cursor.fetchall()


def select_game_info(steam_id):
    cursor.execute(
        f"SELECT name_game  FROM steam_bot.db_steam_bot WHERE steam_id = \'{steam_id}\' "
        f"ORDER BY last_status_change DESC LIMIT 1 ;")
    return cursor.fetchone()


def check_status_user_game(steam_id):
    cursor.execute(
        f"select steam_bot.tg_steam_bot.steam_id, tg_user_id, chat_id, name_game, steam_bot.db_steam_bot.last_status_change "
        f"from steam_bot.tg_steam_bot right join steam_bot.db_steam_bot on steam_bot.db_steam_bot.steam_id = steam_bot.tg_steam_bot.steam_idorder "
        f"by last_status_change DESC LIMIT 1 ;")
    return cursor.fetchone()


def check_status_game(steam_id):
    cursor.execute(
        f"select steam_bot.tg_steam_bot.steam_id, tg_user_id, chat_id, name_game, name_user, steam_bot.db_steam_bot.last_status_change "
        f"from steam_bot.tg_steam_bot "
        f"right join steam_bot.db_steam_bot "
        f"using (steam_id)"
        f"where steam_id  = \'{steam_id}\'"
        f"order by last_status_change desc "
        f"limit 1;")
    return cursor.fetchall()


def select_chat_id(steam_id):
    cursor.execute(f"select chat_id "
                   f"from steam_bot.tg_steam_bot "
                   f"where steam_id = \'{steam_id}\'")
    return cursor.fetchall()
