from enum import Enum

token = '821038681:AAHOZ3Rwx_UwnhAM41d-ZJ9MjssaqLv7KaE'
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_CHAT_ID = "1"
    S_ENTER_MESSAGE = "2"
    S_SEND_MESSAGE = "3"