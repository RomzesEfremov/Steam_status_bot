import telebot
from telebot import types
import schedule
import SteamApi
from threading import Thread
import db
import Start_server

bot = telebot.TeleBot("6475426074:AAFL7ShmU59fQIWDG8p0lqctN-N62V7GJ04")


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.username}  если хочешь чтобы твои друзья были вкурсе что ты играешь во что-то \nТо просто ответь на это сообщение свойи стим айди')


@bot.message_handler(commands=['start_server'])
def send_start_server(message):
    Start_server.start_server()


@bot.message_handler(
    func=lambda message: message.reply_to_message is not None and message.reply_to_message.from_user.id == 6475426074)
def handle_text_doc(message):
    if message.text.isdigit() is True:
        bot.send_message(message.chat.id, "Хорошо, сейчас посмотрим новенький ли ты")
        """Если все прошло то в этом моменте необходимо провести проверку на наличие данного айди в бд"""
        if db.check_db(message.text, message.chat.id) is None:
            db.insert_db(message.from_user.id, message.chat.id, message.text, message.from_user.username)
            bot.send_message(message.chat.id, "Я тебя добавил в свой список")
        else:
            bot.send_message(message.chat.id, "Так за этим айди уже следят")
    else:
        bot.send_message(message.chat.id,
                         "Стим айди должен состоять только из цифр\nЦитируй любое моё сообщение и попробуй еще раз")


def check_steam_status():
    users_steam_id = db.select_steam_id()
    all_id_users = SteamApi.steam_id_users_db(users_steam_id)
    all_users = SteamApi.create_users(all_id_users)
    check_game_id = SteamApi.send_info_user_from_db(all_users)
    if check_game_id is None:
        pass
    elif check_game_id == 'не играет':
        pass
    else:
        info_for_user = db.check_status_game(check_game_id[1])
        chat_id = db.select_chat_id(info_for_user[0][0])
        for chat in chat_id:
            if info_for_user[0][3] == 'не играет':
                pass
            else:
                bot.send_message(chat[0], f'{info_for_user[0][4]} сейчас в {info_for_user[0][3]}')


def main():
    schedule.every(10).seconds.do(check_steam_status)
    while True:
        schedule.run_pending()


th = Thread(target=main)

if __name__ == '__main__':
    th.start()
    bot.infinity_polling()
