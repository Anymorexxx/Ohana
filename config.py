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
    'threshold': 350,
    'creator': 503605638484721676,
    'points_by_word': 0.5,
    'min_word_size': 5,
    'max_word_size': 13,
    'points_by_second': 1 / (120 * 60),
    'reputation_cooldown': 5,
    'max_level': 10,
    'min_level': -2
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
    POINTS_BY_WORD = 'points_by_word'
    MIN_WORD_SIZE = 'min_word_size'
    MAX_WORD_SIZE = 'max_word_size'
    POINTS_BY_SECOND = 'points_by_second'
    REPUTATION_COOLDOWN = 'reputation_cooldown'
    MAX_LEVEL = 'max_level'
    MIN_LEVEL = 'min_level'
