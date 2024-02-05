from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode

import datetime
import re

from constants import State

class Metric():
    def __init__(self):
        self.name: str
        self.time: datetime.time()
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def set_time(self, time: str) -> bool:
        pattern = re.compile('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$') # hh:mm
        if pattern.match(time) is None:
            return False
        h, m = map(int, time.split(':'))
        self.time = datetime.time(h, m)
        return True

metric = Metric()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Добра. Этот бот представляет собой инструмент для добавления неких "Метрик".\n'
        'В назначенное тобой время для каждой Метрики бот будет собирать с тебя данные (текст или число), чтобы потом анализировать их.\n'
        'Давай начнём с обучения: ты создашь первую Метрику, дав ей название и время.\n'
        'Сперва придумай название для Метрики.'
    )
    return State.SELECT_METRIC_NAME


async def select_metric_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #TODO: изучить SQL инъекции (здесь потенциальная уязвимость)
    metric.set_name(update.message.text)
    await update.message.reply_text(
        f'Отлично. Создана Метрика под названием {metric.name}.\n'
        'Теперь напиши время, когда эта Метрика будет собираться, в формате hh:mm в часовом поясе МСК\n' #TODO сделать выбор часового пояса
        'Ты также можешь отправить сообщение "None" (без кавычек), если не хочешь, чтобы Метрика собиралась регулярно.\n'
        'Тогда ты сам сможешь добавлять записи Метрики в любое время.\n'
        '<b>Обрати внимание, что ты не сможешь удалить время или установить его, если изначально не задал.</b>',
        parse_mode=ParseMode.HTML
    )
    return State.SELECT_METRIC_TIME


async def select_metric_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    if message_text == "None":
        await update.message.reply_text(
            f'Время метрики не установлено.'
        )
    else:
        if not metric.set_time(message_text):
            await update.message.reply_text(
                'Неверный формат времени! (hh:mm - требуемый формат)\n'
                'Попробуй ещё раз.'
            )
            return State.SELECT_METRIC_TIME
        await update.message.reply_text(
            f'Время установлено на {str(metric.time)[:5]} (МСК).'
        )
    #TODO передавать Метрику в бэкенд
    await update.message.reply_text(
        'Поздравляю! Ты только что настроил Метрику.\n'
        'Направляю тебя в меню.'
    )
    return ConversationHandler.END
