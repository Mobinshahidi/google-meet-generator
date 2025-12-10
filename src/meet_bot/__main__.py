"""Entry point for the package: python -m meet_bot"""

import os
import logging
from dotenv import load_dotenv

from .bot import create_bot, register_handlers
from .web import create_app, run

logging.basicConfig(level=logging.INFO)


def main():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    bot = create_bot(token)
    register_handlers(bot)

    if os.getenv("RUN_POLLING"):
        logging.info("Starting bot in Polling mode...")
        bot.remove_webhook()
        bot.polling(none_stop=True, interval=0)

    else:
        app = create_app(bot, token=token)
        port = int(os.getenv("PORT", 10000))
        run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
