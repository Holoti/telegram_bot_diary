from telegram import Update
from telegram.ext import CallbackContext
from bot_features.Menu import (
    FORGET_ME_MENU,
    MAIN_MENU,
    WELCOME_MENU
)
from bot_features.user_communication import respond
from database.DBThing import db_thing


def start(update: Update, context: CallbackContext) -> None:
    uid: int = update.message.from_user.id

    if db_thing.get_user(uid):
        respond(update, context, MAIN_MENU, uid)
        return

    db_thing.add_user(
        uid,
        update.message.from_user.username,
        update.message.from_user.first_name,
        update.message.from_user.last_name
    )
    respond(update, context, WELCOME_MENU, uid)


def forget_me(update: Update, context: CallbackContext) -> None:
    uid: int = update.message.from_user.id
    respond(update, context, FORGET_ME_MENU, uid)

