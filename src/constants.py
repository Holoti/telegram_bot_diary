from enum import Enum, auto
from dotenv import dotenv_values


class State(Enum):
    START = auto()
    SELECT_METRIC_NAME = auto()
    SELECT_METRIC_TIME = auto()
    SETUP_FINISHED = auto()


config = dotenv_values("src/.env")
BOT_TOKEN = config['BOT_TOKEN']