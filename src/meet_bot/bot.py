import os
import logging
import uuid
from typing import Optional

import telebot
from telebot import types

from .clients import get_meet_client

logging.basicConfig(level=logging.INFO)


def create_bot(token: Optional[str] = None):
    token = token or os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")
    return telebot.TeleBot(token)


def register_handlers(bot: telebot.TeleBot, allowed_users: Optional[list] = None):
    def is_allowed(user_id):
        if not allowed_users:
            return True
        return user_id in allowed_users

    @bot.message_handler(commands=["start"])
    def start(message):
        if not is_allowed(message.from_user.id):
            return
        bot.reply_to(
            message, "Instant Meet Bot\nUse /meet or @yourbot meet in any chat!"
        )

    @bot.message_handler(commands=["meet"])
    def meet(message):
        if not is_allowed(message.from_user.id):
            bot.reply_to(
                message,
                "⚠️ Authorization Required: You are not allowed to use this bot.",
            )
            return

        try:
            client = get_meet_client()
            response = (
                client.spaces()
                .create(
                    body={"config": {"accessType": "OPEN", "entryPointAccess": "ALL"}}
                )
                .execute()
            )
            link = response["meetingUri"]
            bot.reply_to(
                message,
                f"Instant Meet (full access for all—first joiner is host!)\nJoin → {link}",
            )
        except Exception as e:
            logging.exception("Failed to create meet")
            bot.reply_to(message, f"Error: {str(e)}")

    @bot.inline_handler(lambda query: "meet" in query.query.lower() or not query.query)
    def inline_query(query):
        if not is_allowed(query.from_user.id):
            # Optionally return an unauthorized result or just nothing
            r = types.InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Unauthorized",
                description="You are not allowed to use this bot.",
                input_message_content=types.InputTextMessageContent(
                    "⚠️ Unauthorized usage request."
                ),
            )
            bot.answer_inline_query(query.id, [r], cache_time=60)
            return

        try:
            client = get_meet_client()
            response = (
                client.spaces()
                .create(
                    body={"config": {"accessType": "OPEN", "entryPointAccess": "ALL"}}
                )
                .execute()
            )
            link = response["meetingUri"]
            r = types.InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Instant Open Google Meet",
                description="Full access for all—first joiner is host!",
                input_message_content=types.InputTextMessageContent(
                    f"Open Meet → {link}"
                ),
            )
            bot.answer_inline_query(query.id, [r], cache_time=0)
        except Exception:
            logging.exception("inline handler failed")

    return bot
