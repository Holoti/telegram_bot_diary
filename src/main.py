from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)
from dotenv import dotenv_values
from bot_features.command_handlers import (
    start,
    forget_me
)
from bot_features.callback_handler import button_tap
from bot_features.message_handler import message_handler


def main() -> None:
    config = dotenv_values(".env")
    updater = Updater(config["token"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("forget_me", forget_me))

    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    dispatcher.add_handler(MessageHandler(~Filters.command, message_handler))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()

