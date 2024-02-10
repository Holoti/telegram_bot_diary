from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode

import datetime
import re

from constants import State, menu_keyboard_markup
from metric import Metric
from constants import MetricType
from database.queries import db_add_metric

#TODO Сохранять метрики
#TODO Изучить SQL инъекции

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Добра. Этот бот представляет собой инструмент для сбора неких "Метрик".\n'
        'В назначенное тобой время для каждой Метрики бот будет собирать с тебя данные.\n'
        'Метрики бывают двух типов: числовые и нет.\n'
        'Данные числовых метрик бот будет визуализировать в виде графика.\n'
        'Обычные же, в свою очередь, выступают как своего рода дневник.\n'
        'Выбери тип Метрики, нажав на соответствующую кнопку.\n'
        '<b>Важно: тип нельзя изменить после создания.</b>',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text='Числовая', callback_data=MetricType.NUMERIC),
            InlineKeyboardButton(text='Обычная', callback_data=MetricType.NON_NUMERIC)
        ]])
    )
    return State.SELECT_METRIC_TYPE


async def add_metric(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Чтобы создать Метрику, сперва выбери тип метрики.\n'
        'Тип "Числовая" позволит визуализировать данные в виде графика.\n'
        'Ты можешь написать /cancel, чтобы отменить создание Метрики.',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text='Числовая', callback_data=MetricType.NUMERIC),
            InlineKeyboardButton(text='Обычная', callback_data=MetricType.NON_NUMERIC)
        ]])
    )
    return State.SELECT_METRIC_TYPE


async def select_metric_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid: int = update.effective_user.id
    metric = Metric(uid)
    metric.set_type(update.callback_query.data)
    context.user_data[uid] = metric
    await update.callback_query.answer()
    await update.callback_query.edit_message_reply_markup()
    await context.bot.send_message(
        update.effective_user.id,
        'Отлично, тип выбран. Теперь придумай название.\n'
        'Лучше выбрать лаконичное название, дающее понять смысл Метрики.'
    )
    return State.SELECT_METRIC_NAME


async def select_metric_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid: int = update.effective_user.id
    context.user_data[uid].set_name(update.message.text)
    await update.message.reply_text(
        'Записал. Теперь нужно выбрать время сбора данных.\n'
        'Время должно быть указано в формате hh:mm в часовом поясе МСК.\n' #TODO Сделать выбор часового пояса
        'Ты можешь написать /skip, если не хочешь, чтобы чтобы данные собирались регулярно.\n'
        'Тогда ты сможешь сам добавить запись в любой момент.'
    )
    return State.SELECT_METRIC_TIME


async def select_metric_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid: int = update.effective_user.id
    message_text = update.message.text
    pattern = re.compile('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$') # hh:mm | h:mm
    if pattern.match(message_text) is None:
        await update.message.reply_text(
            'Неверный формат времени! (hh:mm - требуемый формат)\n'
            'Попробуй ещё раз.'
        )
        return State.SELECT_METRIC_TIME
    h, m = map(int, update.message.text.split(':'))
    time = datetime.time(h, m)
    context.user_data[uid].set_time(time)
    await update.message.reply_text(
        f'Время установлено на {message_text} (МСК).'
    )
    await finish(update, context)
    return ConversationHandler.END


async def skip_metric_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Время не установлено.'
    )
    await finish(update, context)
    return ConversationHandler.END


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid: int = update.effective_user.id
    await db_add_metric(context.user_data[uid])
    # print(context.user_data[uid])
    await update.message.reply_text(
        'Поздравляю! Метрика создана и настроена.\n'
        'Направляю тебя в меню.',
        reply_markup=menu_keyboard_markup
    )
    return ConversationHandler.END


async def add_metric_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid: int = update.effective_user.id
    await context.user_data.pop(uid)
    await update.message.reply_text(
        'Создание Метрики отменено.',
        reply_markup=menu_keyboard_markup
    )
    return ConversationHandler.END

