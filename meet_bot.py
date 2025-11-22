import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import uuid
from flask import Flask, request, abort
import asyncio

logging.basicConfig(level=logging.INFO)

SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']
TOKEN_FILE = 'token.json'

def get_meet_client():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return build('meet', 'v2', credentials=creds,
                 discoveryServiceUrl='https://meet.googleapis.com/$discovery/rest?version=v2')

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text("Instant Meet Bot\nUse /meet or @yourbot meet in any chat!")

def meet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        client = get_meet_client()
        response = client.spaces().create(body={}).execute()
        link = response['meetingUri']
        update.message.reply_text(f"Instant Meet (open to all!)\nJoin → {link}")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    if "meet" in query or query == "" or "link" in query or "room" in query:
        try:
            client = get_meet_client()
            response = client.spaces().create(body={}).execute()
            link = response['meetingUri']

            results = [
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Instant Open Google Meet",
                    description="Anyone can join instantly — no waiting!",
                    input_message_content=InputTextMessageContent(
                        f"Open Meet — anyone can join!\nJoin → {link}"
                    )
                )
            ]
            update.inline_query.answer(results, cache_time=1)
        except Exception as e:
            pass

def create_app():
    flask_app = Flask(__name__)
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    # Sync handlers (Flask-friendly)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("meet", meet))
    application.add_handler(InlineQueryHandler(inline_query))

    @flask_app.route(f"/{token}", methods=["POST"])
    def webhook():
        json_string = request.get_json()
        update = Update.de_json(json_string, application.bot)
        if update:
            asyncio.run(application.process_update(update))
        return "OK"

    @flask_app.route("/")
    def health():
        return "Bot is alive!"

    return flask_app

def main():
    if not os.getenv("BOT_TOKEN"):
        raise ValueError("BOT_TOKEN not set")

    flask_app = create_app()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()
