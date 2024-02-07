from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Создатель бота — @holoti\n'
        'Бот создан на языке <a href="https://www.python.org/">Python 3.12</a> '
        'с использованием библиотеки <a href="https://docs.python-telegram-bot.org/en/v20.7/">python-telegram-bot v.20.7</a>.\n'
        '<a href="https://github.com/Holoti/telegram_bot_diary">Исходный код бота (Github)</a>',
        parse_mode=ParseMode.HTML
    )