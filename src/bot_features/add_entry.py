from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler


async def add_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button1 = InlineKeyboardButton(text='Длинное название', callback_data='Длинное название')
    await update.message.reply_text(
        'Выбери метрику, в которую хочешь добавить запись.',
        reply_markup=InlineKeyboardMarkup([ #TODO Собирать Метрики юзера и отображать списком из страниц по 6 кнопок
            [button1, button1],
            [button1, button1],
            [button1, button1],
            [InlineKeyboardButton(text='<-  Назад', callback_data='<-  Назад'), InlineKeyboardButton(text='Вперёд  ->', callback_data='Вперёд  ->')]
        ])
    )


async def add_entry_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END
