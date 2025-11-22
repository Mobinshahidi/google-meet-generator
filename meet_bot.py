import os
import logging
from telegram import Update, Bot
from telegram.ext import CommandHandler, InlineQueryHandler, ContextTypes
from telegram import InlineQueryResultArticle, InputTextMessageContent
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import uuid
from flask import Flask, request, abort

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
        update.message.reply_text(f"Error: {str(e)}")

def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    if "meet" in query or not query:
        try:
            client = get_meet_client()
            response = client.spaces().create(body={}).execute()
            link = response['meetingUri']
            results = [InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Instant Open Google Meet",
                description="Anyone can join instantly!",
                input_message_content=InputTextMessageContent(f"Open Meet → {link}")
            )]
            update.inline_query.answer(results)
        except Exception as e:
            pass

app = Flask(__name__)
token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
dispatcher = bot.dispatcher  # For handlers

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("meet", meet))
dispatcher.add_handler(InlineQueryHandler(inline_query))

@app.route(f"/{token}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def health():
    return "Bot alive!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
