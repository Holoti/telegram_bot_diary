from enum import Enum, auto
from dotenv import dotenv_values
from telegram import ReplyKeyboardMarkup


config = dotenv_values("src/.env")
BOT_TOKEN = config['BOT_TOKEN']


class State(Enum):
    START = auto()
    SELECT_METRIC_TYPE = auto()
    SELECT_METRIC_NAME = auto()
    SELECT_METRIC_TIME = auto()


class Button(Enum):
    ADD_METRIC = 'Создать Метрику'
    LIST_METRIC = 'Список Метрик'
    ADD_ENTRY = 'Добавить запись'
    SETTINGS = 'Настройки'
    ABOUT = 'О проекте'


class MetricType(Enum):
    NON_NUMERIC = auto()
    NUMERIC = auto()


menu_keyboard = [
    [Button.ADD_METRIC.value, Button.LIST_METRIC.value],
    [Button.ADD_ENTRY.value],
    [Button.SETTINGS.value, Button.ABOUT.value]
]


menu_keyboard_markup = ReplyKeyboardMarkup(menu_keyboard, input_field_placeholder='Главное меню', resize_keyboard=True, one_time_keyboard=True)


db_file = 'src/database/db.sqlite'