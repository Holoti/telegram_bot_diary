from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Menu:
    """
    Menu is a message with text and inline buttons (optional)
    """
    def __init__(self, text: str, overrideable=False, buttons=[]):
        self.text = text
        self.buttons = buttons
        self.overrideable = overrideable
        self.markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(button, callback_data=button) for button in self.buttons]
        ])

    def update_text(self, text):
        self.text = text

WELCOME_MENU = Menu(
    "Добра. Ты можешь использовать этот бот как личный дневник мыслей, сна и общего эмоционального состояния.\n\n"
    "Бот будет отправлять опрос по назначенному тобой расписанию, утром и вечером, так что давай определимся со временем.",
    buttons=["Установить время"]
)
FORGET_ME_MENU = Menu(
    'Ты уверен, что хочешь удалить все данные о себе из базы данных? Все записи удалятся.\n'
    'Если ты уверен, напиши "Да, я хочу удалить данные."'
)
EVENING_TIME_MENU = Menu(
    "Давай установим вечернее время. В это время бот будет напоминать заканчивать дела и готовиться ко сну,"
    "так что я советую поставить время на один час раньше, чем желаемый отход ко сну.\n\n"
    "<b>Напиши желаемое время в формате hh:mm по МСК</b>."
)
MORNING_TIME_MENU = Menu(
    "Отлично. Теперь установим утреннее время. Поставь то время, в которое обычно просыпаешься.\n"
    "<b>Напиши желаемое время в формате hh:mm по МСК</b>."
)
CONFIRMED_TIME_MENU = Menu(
    "Утреннее и вечернее время установлено. Бот почти готов к использованию."
)
MAIN_MENU = Menu(
    "Ты находишься в главном меню.",
    overrideable=True,
    buttons=["Настройки", "Добавить запись", "Обратная связь"]
)
SETTINGS_MENU = Menu(
    "Ты находишься в меню настроек.",
    overrideable=True,
    buttons=["Вечернее время", "Утреннее время"]
)
WRONG_TIME_FORMAT_MENU = Menu(
    "Неверный формат времени. Попробуй ещё раз: hh:mm"
)
USER_FORGOTTEN_MENU = Menu(
    "Все данные удалены. Если хотите начать заново, отправьте команду /start"
)

# this thing stores the last message sent by the bot for each user.
# the key is user's telegram uid; the value is last message sent by the bot.
# this is needed to determine the most appropriate behavior.
# e.g. if a user sends a message containing only time in hh:mm format, bot should ignore it in general.
# but if the bot is currently in a time setting state, it should record this information and do its thing.
# i'm not sure if it's a good method.
CURRENT_MENUS: dict[int, Menu] = {}

