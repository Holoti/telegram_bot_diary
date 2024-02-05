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
    State,
    BOT_TOKEN
)
from bot_features.start_conversation import (
    start,
    select_metric_name,
    select_metric_time
)
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
        #// .concurrent_updates(False)
        .build()
    )

    print(application.bot.token)

    start_conv_handler = ConversationHandler(
        block=False,
        entry_points=[CommandHandler("start", start)],
        states={
            State.SELECT_METRIC_NAME: [MessageHandler(None, select_metric_name)],
            State.SELECT_METRIC_TIME: [MessageHandler(None, select_metric_time)],
        },
        fallbacks=[]
    )
    application.add_handler(start_conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()

