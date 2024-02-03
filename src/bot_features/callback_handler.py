from telegram import Update
from telegram.ext import CallbackContext
from bot_features.Menu import (
    WELCOME_MENU,
    EVENING_TIME_MENU,
    MORNING_TIME_MENU,
    SETTINGS_MENU,
    MAIN_MENU
)
from bot_features.user_communication import respond


def button_tap(update: Update, context: CallbackContext) -> None:
    uid: int = update.callback_query.from_user.id
    data = update.callback_query.data

    if data == WELCOME_MENU.buttons[0]:
        respond(update, context, EVENING_TIME_MENU, uid)
    elif data == MAIN_MENU.buttons[0]:
        respond(update, context, SETTINGS_MENU, uid)
    elif data == SETTINGS_MENU.buttons[0]:
        respond(update, context, EVENING_TIME_MENU, uid)
    elif data == SETTINGS_MENU.buttons[1]:
        respond(update, context, MORNING_TIME_MENU, uid)

    # Close the query to end the client-side loading animation
    update.callback_query.answer()

