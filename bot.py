# использовать библиотеку datatime

import re

from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from Menu import *
from DBThing import DBThing
db_thing = DBThing()

from dotenv import dotenv_values
config = dotenv_values(".env")

def change_menu(new_menu: Menu, uid: int) -> None:
    global CURRENT_MENUS
    CURRENT_MENUS[uid] = new_menu

def respond(update: Update, context: CallbackContext, uid: int) -> None:
    print("resond")
    if CURRENT_MENUS[uid].overrideable:
        update.callback_query.message.edit_text(
            CURRENT_MENUS[uid].text,
            ParseMode.HTML,
            reply_markup=CURRENT_MENUS[uid].markup
        )
    else:
        update.callback_query.message.edit_reply_markup()
        context.bot.send_message(
            update.callback_query.from_user.id,
            CURRENT_MENUS[uid].text,
            parse_mode=ParseMode.HTML,
            reply_markup=CURRENT_MENUS[uid].markup
        )

def start(update: Update, context: CallbackContext) -> None:
    global CURRENT_MENUS
    uid: int = update.message.from_user.id
    CURRENT_MENUS[uid] = WELCOME_MENU
    db_thing.add_user(
        uid,
        update.message.from_user.username,
        update.message.from_user.first_name,
        update.message.from_user.last_name
    )
    context.bot.send_message(
        update.message.from_user.id,
        CURRENT_MENUS[uid].text,
        parse_mode=ParseMode.HTML,
        reply_markup=CURRENT_MENUS[uid].markup
    )

def forget_me(update: Update, context: CallbackContext) -> None:
    global CURRENT_MENUS
    uid: int = update.message.from_user.id
    CURRENT_MENUS[uid] = FORGET_ME_MENU
    context.bot.send_message(
        update.message.from_user.id,
        CURRENT_MENUS[uid].text,
        parse_mode=ParseMode.HTML,
        reply_markup=CURRENT_MENUS[uid].markup
    )


def button_tap(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """
    global CURRENT_MENUS
    uid: int = update.callback_query.from_user.id

    data = update.callback_query.data

    if data == WELCOME_MENU.buttons[0]:
        CURRENT_MENUS[uid] = EVENING_TIME_MENU
    elif data == MAIN_MENU.buttons[0]:
        CURRENT_MENUS[uid] = SETTINGS_MENU
    elif data == SETTINGS_MENU.buttons[0]:
        CURRENT_MENUS[uid] = EVENING_TIME_MENU
    elif data == SETTINGS_MENU.buttons[1]:
        CURRENT_MENUS[uid] = MORNING_TIME_MENU

    # Close the query to end the client-side loading animation
    update.callback_query.answer()

    # Update message content with corresponding menu section
    # update.callback_query.message.edit_text(
    #     CURRENT_MENU.text,
    #     ParseMode.HTML,
    #     reply_markup=CURRENT_MENU.markup
    # )
    respond(update, context, uid)
    # if CURRENT_MENUS[uid].overrideable:
    #     update.callback_query.message.edit_text(
    #         CURRENT_MENUS[uid].text,
    #         ParseMode.HTML,
    #         reply_markup=CURRENT_MENUS[uid].markup
    #     )
    # else:
    #     update.callback_query.message.edit_reply_markup()
    #     context.bot.send_message(
    #         update.callback_query.from_user.id,
    #         CURRENT_MENUS[uid].text,
    #         parse_mode=ParseMode.HTML,
    #         reply_markup=CURRENT_MENUS[uid].markup
    #     )


def message_handler(update: Update, context: CallbackContext) -> None:
    global CURRENT_MENUS
    uid: int = update.message.from_user.id
    print("message recieved!", update.message.text)

    if CURRENT_MENUS[uid] == EVENING_TIME_MENU or CURRENT_MENUS[uid] == MORNING_TIME_MENU:
        if re.search("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", update.message.text) == None:
            context.bot.send_message(
                update.message.from_user.id,
                "Неверный формат времени. Попробуй ещё раз: hh:mm"
            )
        else:
            if CURRENT_MENUS[uid] == EVENING_TIME_MENU:
                db_thing.set_user_setting(update.message.from_user.id, evening_time=update.message.text)
                CURRENT_MENUS[uid] = MORNING_TIME_MENU
                context.bot.send_message(
                    update.message.from_user.id,
                    CURRENT_MENUS[uid].text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=CURRENT_MENUS[uid].markup
                )
            elif CURRENT_MENUS[uid] == MORNING_TIME_MENU:
                db_thing.set_user_setting(update.message.from_user.id, morning_time=update.message.text)
                CURRENT_MENUS[uid] = CONFIRMED_TIME_MENU
                context.bot.send_message(
                    update.message.from_user.id,
                    CURRENT_MENUS[uid].text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=CURRENT_MENUS[uid].markup
                )
                CURRENT_MENUS[uid] = MAIN_MENU
                context.bot.send_message(
                    update.message.from_user.id,
                    CURRENT_MENUS[uid].text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=CURRENT_MENUS[uid].markup
                )
            # context.bot.send_message(
            #     update.message.from_user.id,
            #     f"Время установлено на {update.message.text} МСК."
            # )
            # config.evening_time.change(update.message.text)
    
    if CURRENT_MENUS[uid] == FORGET_ME_MENU:
        if update.message.text == 'Да, я хочу удалить данные.':
            context.bot.send_message(
                update.message.from_user.id,
                "Все данные удалены. Если хотите начать заново, отправьте команду /start"
            )
            db_thing.forget_user(update.message.from_user.id)
            CURRENT_MENUS[uid] = None


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
