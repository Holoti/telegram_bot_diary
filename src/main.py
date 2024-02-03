from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    Application
)
from dotenv import dotenv_values
from bot_features.command_handlers import (
    start,
    forget_me
)
from bot_features.callback_handler import button_tap
from bot_features.message_handler import message_handler

# TODO: анализ данных юзера (построение графиков и пр.)
# TODO: настроить venv
# TODO:


def main() -> None:
    config = dotenv_values("src/.env")

    application = (
        Application.builder()
        .token(config["token"])
        .arbitrary_callback_data(True)
        .concurrent_updates(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("forget_me", forget_me))

    application.add_handler(CallbackQueryHandler(button_tap))

    application.add_handler(MessageHandler(~filters.COMMAND, message_handler))

    application.run_polling()

    # dispatcher = updater.dispatcher

    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("forget_me", forget_me))

    # dispatcher.add_handler(CallbackQueryHandler(button_tap))

    # dispatcher.add_handler(MessageHandler(~Filters.command, message_handler))

    # updater.start_polling()

    # updater.idle()


if __name__ == "__main__":
    main()

