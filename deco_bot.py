import telebot
from telebot import types
from datetime import datetime
from db import Users
import time

TOKEN = '821038681:AAHOZ3Rwx_UwnhAM41d-ZJ9MjssaqLv7KaE'
user_check = None

STATE = 0

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


@bot.message_handler(regexp='input id of user')
def start_id_handler(message):
    global STATE
    STATE = 3
    requests_to_text(message, 'input answer')



@bot.message_handler(content_types='text')
def text_handler(message):
    print(STATE)
    if STATE == 1 and not message.from_user.id == 617194034:
        user_input = message.text
        Users.create(chat_id=message.from_user.id,
                     message_from=message.from_user.username,
                     text=user_input)
        for data in Users.select():
            data_db = f'Chat id: {data.chat_id}\nMessage from: {data.message_from}\n Text: {data.text}'
            bot.send_message(617194034, data_db)

        custom_keyboard = 'input id of user', '222'
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.add(*custom_keyboard)
        bot.send_message(617194034, f'Last message: {message.text}', reply_markup=user_markup)

    elif STATE == 1 and message.from_user.id == 617194034:
        pass

    elif STATE == 2:
        pass

    elif STATE == 3:
        bot.send_message(message.text, 'Get message from consult')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)