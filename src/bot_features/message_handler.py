from telegram import Update
from telegram.ext import CallbackContext
from bot_features.Menu import (
    CURRENT_MENUS,
    EVENING_TIME_MENU,
    MORNING_TIME_MENU,
    WRONG_TIME_FORMAT_MENU,
    CONFIRMED_TIME_MENU,
    MAIN_MENU,
    FORGET_ME_MENU,
    USER_FORGOTTEN_MENU
)
from bot_features.user_communication import respond
from bot_features.set_time import set_time
from database.DBThing import db_thing


async def message_handler(update: Update, context: CallbackContext) -> None:
    uid: int = update.message.from_user.id

    if CURRENT_MENUS[uid] == EVENING_TIME_MENU or CURRENT_MENUS[uid] == MORNING_TIME_MENU:
        set_time_result = await set_time(update, context, update.message.text, uid)
        if set_time_result == "wrong time format":
            await respond(update, context, WRONG_TIME_FORMAT_MENU, uid, False)
        else:
            if CURRENT_MENUS[uid] == EVENING_TIME_MENU and (await db_thing.get_user_setting(uid))[1] is None:
                await respond(update, context, MORNING_TIME_MENU, uid)
            else:
                await respond(update, context, CONFIRMED_TIME_MENU, uid)
                await respond(update, context, MAIN_MENU, uid)
    
    elif CURRENT_MENUS[uid] == FORGET_ME_MENU:
        if update.message.text == 'Да, я хочу удалить данные.':
            await respond(update, context, USER_FORGOTTEN_MENU, uid)
            await db_thing.forget_user(update.message.from_user.id)
            del CURRENT_MENUS[uid]

