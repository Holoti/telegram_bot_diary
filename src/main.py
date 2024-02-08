from telegram import Bot, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    Application,
    ConversationHandler
)
from dotenv import dotenv_values
from constants import (
    Button,
    State,
    BOT_TOKEN
)
from bot_features.add_entry import add_entry, add_entry_cancel
from bot_features.add_metric import (
    start,
    add_metric,
    select_metric_type,
    select_metric_name,
    select_metric_time,
    skip_metric_time,
    add_metric_cancel
)
from bot_features.about import about
import logging
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning


filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    config = dotenv_values("src/.env")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .arbitrary_callback_data(True)
        .concurrent_updates(False)
        .build()
    )

    add_metric_conversation = ConversationHandler(
        block=False,
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex(f'^{Button.ADD_METRIC.value}$'), add_metric)
        ],
        states={
            State.SELECT_METRIC_TYPE: [CallbackQueryHandler(select_metric_type)],
            State.SELECT_METRIC_NAME: [MessageHandler(~filters.COMMAND, select_metric_name)],
            State.SELECT_METRIC_TIME: [
                CommandHandler('skip', skip_metric_time),
                MessageHandler(~filters.Regex('^/skip$') & ~filters.COMMAND, callback=select_metric_time)
            ]
        },
        fallbacks=[CommandHandler('cancel', add_metric_cancel)]
    )
    application.add_handler(add_metric_conversation)

    add_entry_conversation = ConversationHandler(
        block=False,
        entry_points=[
            MessageHandler(filters.Regex(f'^{Button.ADD_ENTRY.value}$'), add_entry)
        ],
        states={},
        fallbacks=[CommandHandler('cancel', add_entry_cancel)]
    )
    application.add_handler(add_entry_conversation)

    application.add_handler(MessageHandler(filters.Regex(Button.ABOUT.value), about))

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()

