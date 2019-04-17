import telebot
from telebot import types
from datetime import datetime
from db import Users
import config
import dbworker


STATE = 0

TOKEN = '821038681:AAHOZ3Rwx_UwnhAM41d-ZJ9MjssaqLv7KaE'

bot = telebot.TeleBot(TOKEN)


def log(message):
    print('\n-------')
    print(datetime.now())
    print('Сообщение от {0} {1}. (id = {2}) '
          '\n Текст - {4} \n {3}'.format(message.from_user.first_name,
                                  message.from_user.last_name,
                                  message.chat.id,
                                  str(message.from_user.id),
                                  message.text))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет Что хочешь поесть?", reply_markup=markup_menu)



markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_zavtrak = types.KeyboardButton(
    'Хочу позавтракать')  # здесь в дальнейшем будут еще варианты, в зависимости от кнопки информация должна пересылаться разным людям (id чата заранее известны  )
markup_menu.add(btn_zavtrak)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    log(message)
    if message.text == "Хочу позавтракать":
        bot.reply_to(message, 'Варианты завтраков', reply_markup=markup_zavtrak)
    #  bot.send_message(chat_id="841260346", text="Хочу позавтракать").  #попытка сделать пересыл информации при нажатии на опресненную кнопку определенному человеку   (такой вариант не сработал )

    if message.text == "Легкий":
        bot.reply_to(message, 'Выбран легкий, есть вопросы?', reply_markup=markup_otvet)
    # bot.send_message(chat_id="841260346", text="Легкий").    #id чата заменяем на свой

    if message.text == "Вопросов нет":
        bot.reply_to(message, 'Ваш запрос принят, обработка займет не более 5 мин')
    # bot.send_message(chat_id="841260346", text="вопросов нет")
    if message.text == "Есть вопрос":
        global STATE
        STATE = 1
        bot.reply_to(message, 'Задайте ваш вопрос и нажмите завершить', reply_markup=markup_ok)
    if message.text == "Завершить":

        bot.reply_to(message, 'Ваш запрос принят, обработка займет не более 5 мин')

    if STATE == 1:
        custom_keyboard = 'input id of user', '222'
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.add(*custom_keyboard)
        bot.send_message('617194034', message.text, reply_markup=user_markup)
        msg = "Пользователь {} написал \"{}\".".format(message.from_user.username, message.text)
        log(message)
        bot.send_message(617194034, msg)
        bot.send_message(message.from_user.id, msg)
        Users.create(chat_id=message.from_user.id,
                     message_from=message.from_user.username,
                     text=message.text)
        for data in Users.select():
            data_db = f'Chat id: {data.chat_id}\nMessage from: {data.message_from}\nText: {data.text}'
            bot.send_message('617194034', data_db)
        # if message.text == TAKE WITH LOOP ALL ID FROM DATABASE
        if message.text == 'input id of user':
            bot.send_message(515090561, 'GET MESSAGE FROM CONSULTANT 2')

        if message.from_user.id == '617194034':
            bot.send_message(515090561, 'GET MESSAGE FROM CONSULTANT 1')







# в итоге все свел в else но при таком раскладе получается что вся информация независимо от кнопок будет прилетать одному человеку


markup_zavtrak = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
btn_legkii_zavtrak = types.KeyboardButton('Легкий')
markup_zavtrak.add(btn_legkii_zavtrak)

markup_otvet = types.ReplyKeyboardMarkup()
btn_noq = types.KeyboardButton('Вопросов нет')
btn_q = types.KeyboardButton('Есть вопрос')
markup_otvet.add(btn_q, btn_noq)

markup_ok = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_ok = types.KeyboardButton('Завершить')
markup_ok.add(btn_ok)

bot.polling()