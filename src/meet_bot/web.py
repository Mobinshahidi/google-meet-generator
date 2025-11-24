from flask import Flask, request, abort
import os
import telebot
from typing import Optional


def create_app(bot: telebot.TeleBot, token: Optional[str] = None) -> Flask:
    token = token or os.getenv("BOT_TOKEN")
    app = Flask(__name__)

    @app.route(f"/{token}", methods=["POST"])
    def webhook():
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            abort(403)

    @app.route("/")
    def health():
        return "Bot alive!"

    return app

def run(app: Flask, host: str = "0.0.0.0", port: int = 10000):
    app.run(host=host, port=port)
