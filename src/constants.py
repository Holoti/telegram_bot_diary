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
    CREATE_METRIC = 'Создать Метрику'
    LIST_METRIC = 'Список Метрик'
    ADD_ENTRY = 'Добавить запись'
    SETTINGS = 'Настройки'
    ABOUT = 'О проекте'

menu_keyboard = [
    [Button.CREATE_METRIC.value, Button.LIST_METRIC.value],
    [Button.ADD_ENTRY.value],
    [Button.SETTINGS.value, Button.ABOUT.value]
]

menu_keyboard_markup = ReplyKeyboardMarkup(menu_keyboard, input_field_placeholder='Главное меню', resize_keyboard=True, one_time_keyboard=True)