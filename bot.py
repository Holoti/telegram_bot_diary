# использовать библиотеку datatime

import re
import datetime

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from Menu import *
from DBThing import DBThing
db_thing = DBThing()

from dotenv import dotenv_values
config = dotenv_values(".env")


def respond(update: Update, context: CallbackContext, new_menu: Menu, uid: int, change_menu: bool = True) -> None:
    global CURRENT_MENUS
    OLD_MENU: Menu = None
    if CURRENT_MENUS.get(uid) is not None:
        OLD_MENU = CURRENT_MENUS[uid]
    if change_menu:
        CURRENT_MENUS[uid] = new_menu
    if OLD_MENU is not None and OLD_MENU.overrideable and update.callback_query is not None:
        update.callback_query.message.edit_text(
            new_menu.text,
            ParseMode.HTML,
            reply_markup=new_menu.markup
        )
    else:
        if update.callback_query is not None:
            update.callback_query.message.edit_reply_markup()
        context.bot.send_message(
            uid,
            new_menu.text,
            parse_mode=ParseMode.HTML,
            reply_markup=new_menu.markup
        )


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


def set_time(update: Update, context: CallbackContext, time_str: str, uid: int) -> str:
    if re.match("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", update.message.text) is None:
        return "wrong time format"
    
    if CURRENT_MENUS[uid] == EVENING_TIME_MENU:
        if len(time_str) == 4: # h:mm
            time_str = '0' + time_str
        ev_time = datetime.time(int(time_str[:2]), int(time_str[3:5]))
        db_thing.set_user_setting(uid, evening_time=ev_time)
        return "set evening time"
    elif CURRENT_MENUS[uid] == MORNING_TIME_MENU:
        if len(time_str) == 4: # h:mm
            time_str = '0' + time_str
        mo_time = datetime.time(int(time_str[:2]), int(time_str[3:5]))
        db_thing.set_user_setting(uid, morning_time=mo_time)
        return "set morning time"
    return "wrong menu"


def message_handler(update: Update, context: CallbackContext) -> None:
    uid: int = update.message.from_user.id

    if CURRENT_MENUS[uid] == EVENING_TIME_MENU or CURRENT_MENUS[uid] == MORNING_TIME_MENU:
        set_time_result = set_time(update, context, update.message.text, uid)
        if set_time_result == "wrong time format":
            respond(update, context, WRONG_TIME_FORMAT_MENU, uid, False)
        else:
            if CURRENT_MENUS[uid] == EVENING_TIME_MENU and db_thing.get_user_setting(uid)[1] is None:
                respond(update, context, MORNING_TIME_MENU, uid)
            else:
                respond(update, context, CONFIRMED_TIME_MENU, uid)
                respond(update, context, MAIN_MENU, uid)
    
    elif CURRENT_MENUS[uid] == FORGET_ME_MENU:
        if update.message.text == 'Да, я хочу удалить данные.':
            respond(update, context, USER_FORGOTTEN_MENU, uid)
            db_thing.forget_user(update.message.from_user.id)
            del CURRENT_MENUS[uid]


def main() -> None:
    updater = Updater(config["token"])

    # Get the dispatcher to register handlers
    # Then, we register each handler and the conditions the update must meet to trigger it
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("forget_me", forget_me))

    # Register handler for inline buttons
    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    # Process any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, message_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == "__main__":
    main()
