from enum import Enum

settings = {
    'token': 'OTkwODkxOTE4ODE4OTY3NjIz.GyQ423.b5R3IENyPTyg5W8m8jt588QZwStVOpU6AzXa7A',
    'bot': '♡ |・</aww>・',
    'id': 990891918818967623,
    'prefix': '.',
    'status': '‧͙⁺˚*･༓ котики FM ༓･*˚⁺‧͙',
    'db': 'sqlite:///server.db',

    # нужные штушки
    'chat': 1091657859479113818,
    'server': 1091658183510085662,
    'moder': 1092378054585757706,
    'log': 1096793524877393933,
    'new': 1099396359884378205,
    'color': 0x2e3235,
    'data': '%d.%m.%Y %H:%M:%S',
    'defaultRole': 1097949456030253096,
    'threshold': 50,
    'creator': 503605638484721676
}


class SettingsEnum(Enum):
    TOKEN = 'token'
    THRESHOLD = 'threshold'
    BOT = 'bot'
    ID = 'id'
    PREFIX = 'prefix'
    STATUS = 'status'
    DATABASE_LINK = 'db'
    CHAT = 'chat'
    SERVER = 'server'
    MODER = 'moder'
    LOG = 'log'
    NEW = 'new'
    COLOR = 'color'
    DATA = 'data'
    ROLE = 'defaultRole'
    CREATOR = 'creator'
