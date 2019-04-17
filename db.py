from peewee import *
from datetime import date
from datetime import time


user_data = SqliteDatabase('user_data.db')


class Users(Model):
    chat_id = IntegerField()
    message_from = CharField()
    text = CharField()

    class Meta:
        database = user_data


if __name__ == '__main__':
    Users.create_table()