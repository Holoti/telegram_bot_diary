from telegram import Update
from telegram.constants import (
    ParseMode
)
from telegram.ext import CallbackContext
from bot_features.Menu import (
    Menu,
    CURRENT_MENUS
)

async def respond(update: Update, context: CallbackContext, new_menu: Menu, uid: int, change_menu: bool = True) -> None:
    global CURRENT_MENUS
    OLD_MENU: Menu = None
    if CURRENT_MENUS.get(uid) is not None:
        OLD_MENU = CURRENT_MENUS[uid]
    if change_menu:
        CURRENT_MENUS[uid] = new_menu
    if OLD_MENU is not None and OLD_MENU.overrideable and update.callback_query is not None:
        await update.callback_query.message.edit_text(
            new_menu.text,
            ParseMode.HTML,
            reply_markup=new_menu.markup
        )
    else:
        if update.callback_query is not None:
            await update.callback_query.message.edit_reply_markup()
        await context.bot.send_message(
            uid,
            new_menu.text,
            parse_mode=ParseMode.HTML,
            reply_markup=new_menu.markup
        )

