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
from bot_features.add_metric import (
    start,
    create_metric,
    select_metric_type,
    select_metric_name,
    select_metric_time,
    skip_metric_time,
    cancel
)
from bot_features.about import about
import logging


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

    start_conv_handler = ConversationHandler(
        block=False,
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex(f'^{Button.CREATE_METRIC.value}$'), create_metric)
        ],
        states={
            State.SELECT_METRIC_TYPE: [CallbackQueryHandler(select_metric_type)],
            State.SELECT_METRIC_NAME: [MessageHandler(~filters.COMMAND, select_metric_name)],
            State.SELECT_METRIC_TIME: [
                CommandHandler('skip', skip_metric_time),
                MessageHandler(~filters.Regex('^/skip$') & ~filters.COMMAND, callback=select_metric_time)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(start_conv_handler)

    application.add_handler(MessageHandler(filters.Regex(Button.ABOUT.value), about))

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()

