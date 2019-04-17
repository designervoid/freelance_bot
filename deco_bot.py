import telebot
from telebot import types
from datetime import datetime
from db import Users
import config
import dbworker
import time

TOKEN = '821038681:AAHOZ3Rwx_UwnhAM41d-ZJ9MjssaqLv7KaE'

STATE = 0
user_id = 0
to_user = ''

bot = telebot.TeleBot(TOKEN)

print(bot.get_me())


def log(message, answer):
    print('\n-------')
    print(datetime.now())
    print('Сообщение от {0} {1}. (id = {2}) '
          '\n Текст - {3}'.format(message.from_user.first_name,
                                  message.from_user.last_name,
                                  str(message.from_user.id),
                                  message.text))
    print(answer)


def custom_keyboard_in_commands(message,
                                custom_keyboard, text='Выберите что вам нужно'):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.add(*custom_keyboard)
    bot.send_message(message.from_user.id, text, reply_markup=user_markup)


def resize_custom_keyboard_in_commands(message, custom_keyboard, text):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*custom_keyboard)
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


def requests_to_text(message, answer='Request to text'):
    log(message, answer)
    bot.send_message(message.chat.id, '{}'.format(answer))


@bot.message_handler(regexp='start')
def start_handler(message):
    words = 'Легкий завтрак', 'Сытный завтрак'
    custom_keyboard_in_commands(message, words, text='Что хочешь поесть?')


@bot.message_handler(regexp='Легкий завтрак')
def start_light_breakfast(message):
    words = 'Задать вопрос', 'Не задавать вопрос'
    custom_keyboard_in_commands(message, words, text='Вы можете задать вопрос')


@bot.message_handler(regexp='Задать вопрос')
def start_question(message):
    global STATE
    STATE = 1
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.add('Завершить')
    bot.send_message(message.from_user.id, 'Задайте ваш вопрос', reply_markup=user_markup)


@bot.message_handler(regexp='Завершить')
def end(message):
    global STATE
    STATE = 2
    requests_to_text(message, answer='Ваш запрос принят')


@bot.message_handler(commands=['stop'])
def stop_handler(message):
    user_hide = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'hide',
                     reply_markup=user_hide)


# Начало диалогa
@bot.message_handler(commands=["send_to_user"])
def cmd_start(message):
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
def cmd_reset(message):
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
    global to_user
    to_user = message.text
    bot.send_message(617194034, "Запомнил данные! Отправил")
    bot.send_message(617194034, "Отлично! Повторная отправка командой - /send_to_user.")
    dbworker.set_state(message.chat.id, config.States.S_SEND_MESSAGE.value)
    bot.send_message(user_id, to_user)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_MESSAGE.value)
def send_msg_to_user(message):
    bot.send_message(user_id, to_user)
    bot.send_message(617194034, "Отлично! Повторная отправка командой - /send_to_user.")
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    print(STATE)
    if not message.from_user.id == 617194034:
        user_input = message.text
        Users.create(chat_id=message.from_user.id,
                     message_from=message.from_user.username,
                     text=user_input)
        for data in Users.select():
            data_db = f'Chat id: {data.chat_id}\nMessage from: {data.message_from}\n Text: {data.text}'
            bot.send_message(617194034, data_db)
        bot.send_message(617194034, f'Last message: {message.text}')

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)