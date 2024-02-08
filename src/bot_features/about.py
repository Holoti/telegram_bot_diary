from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Создатель бота — @holoti\n'
        '<a href="https://github.com/Holoti/telegram_bot_diary">Исходный код (Github)</a>',
        parse_mode=ParseMode.HTML
    )