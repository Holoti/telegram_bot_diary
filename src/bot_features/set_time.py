import re
import datetime
from telegram import Update
from telegram.ext import CallbackContext
from bot_features.Menu import (
    CURRENT_MENUS,
    EVENING_TIME_MENU,
    MORNING_TIME_MENU
)
from database.DBThing import db_thing


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
