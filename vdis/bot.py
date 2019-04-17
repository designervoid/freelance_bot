# -*- coding: utf-8 -*-

import telebot
import config
import dbworker

bot = telebot.TeleBot(config.token)
user_id = 0
to_user = ''


# Начало диалога
@bot.message_handler(commands=["send_to_user"])
def cmd_start():
    state = dbworker.get_current_state(617194034)
    if state == config.States.S_ENTER_CHAT_ID.value:
        bot.send_message(617194034, "Кажется, кто-то обещал отправить чат айди, но так и не сделал этого :( Жду...")
    elif state == config.States.S_ENTER_MESSAGE.value:
        bot.send_message(617194034, "Кажется, кто-то обещал отправить сообщение, но так и не сделал этого :( Жду...")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(617194034, "Введи чат айди")
        dbworker.set_state(617194034, config.States.S_ENTER_CHAT_ID.value)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset():
    bot.send_message(617194034, "Что ж, начнём по-новой. Введи айди")
    dbworker.set_state(617194034, config.States.S_ENTER_CHAT_ID.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CHAT_ID.value)
def user_entering_id(message):
    # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
    bot.send_message(617194034, "Айди запомнил! Теперь сообщение")
    dbworker.set_state(617194034, config.States.S_ENTER_MESSAGE.value)
    global user_id
    user_id = message.text


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_MESSAGE.value)
def user_entering_message(message):
    bot.send_message(617194034, "Отлично! Повторная отправка командой - /send_to_user.")
    dbworker.set_state(617194034, config.States.S_START.value)
    global to_user
    to_user = message.text
    print(user_id)
    print(to_user)


if __name__ == "__main__":
    bot.polling(none_stop=True)