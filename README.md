# Instant Meet Generator Bot

A simple Telegram bot that generates instant Google Meet links on demand. Users can type `/meet` in a private chat or `@botusername meet` in any group/channel for a fresh, open Meet room where anyone can join immediately with full access (no host approval needed—the first joiner becomes host).

Built with Python, pyTelegramBotAPI, Flask, and the Google Meet API. Hosted on Render for 24/7 availability.

## Features
- **Instant Meet Links**: Generate a new Google Meet room with `/meet`.
- **Inline Mode**: Use `@botusername meet` in any chat to send a link without adding the bot.
- **Open Rooms**: Rooms are fully open—anyone with the link joins with audio/video/chat/share. No knocking or host wait; first joiner gets admin controls.
- **Unlimited Rooms**: No time limit (rooms last 24+ hours).
- **Free & Private**: Runs on your Google account; links are ephemeral.

## Setup Instructions
To run your own version, follow these steps. (As of November 23, 2025, this works with current APIs.)

### 1. Prerequisites
- A Google account (for Meet API).
- A Telegram account (for BotFather).
- Git and Python installed locally.

### 2. Set Up Google Meet API
1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Create a new project.
3. Enable the **Google Meet API**.
4. Go to Credentials → Create Credentials → OAuth client ID → Desktop app.
5. Download `credentials.json`.
6. Run the bot locally once to generate `token.json` (authorizes your account).

### 3. Create Telegram Bot
1. Talk to [@BotFather](https://t.me/botfather) on Telegram.
2. `/newbot` → Choose name/username → Copy the BOT_TOKEN.
3. `/setinline` → Enable inline mode with placeholder "Creating Meet...".

### 4. Clone & Configure Code
1. Clone the repo: `git clone https://github.com/Mobinsahidi/google-meet-generator.git`.
2. `cd google-meet-generator`.
3. Create `.env` with `BOT_TOKEN=your_token`.
4. Add `credentials.json` and run locally to get `token.json`.

### 5. Dependencies
Install with `pip install -r requirements.txt`:
- pyTelegramBotAPI
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2
- python-dotenv
- flask

### 6. Run locally / project layout

You can run the app directly using Python or inside Docker. The repository has been reorganized into a small package under `src/meet_bot`.

Project layout (short):

```
. 
├─ src/
│  └─ meet_bot/        # package containing the app
│     ├─ __main__.py   # entry point (python -m src.meet_bot)
│     ├─ bot.py        # bot factory and handlers
│     ├─ clients.py    # google meet client helper
│     └─ web.py        # flask app factory
├─ run.py              # convenience script
├─ requirements.txt
├─ Dockerfile
└─ README.md
```

Run locally (from repo root):

```bash
cp .env.example .env
# edit .env to set BOT_TOKEN and place credentials
python run.py
# or
python -m src.meet_bot
```

Or with Docker:

```bash
docker build -t instant-meet-bot .
docker run --env-file .env -p 10000:10000 instant-meet-bot
```

### 7. Hosting on Render (Free 24/7)
1. Sign up at [render.com](https://render.com) with GitHub.
2. New Web Service → Connect your repo.
3. Runtime: Python.
4. Build: `pip install -r requirements.txt`.
5. Start: `python meet_bot.py`.
6. Environment: Add `BOT_TOKEN`.
7. Secret Files: Add `credentials.json` and `token.json` (paste contents).
8. Deploy!

9. Set Webhook (replace <TOKEN>):
   ```
   curl https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-service.onrender.com/<TOKEN>
   ```

### Local Testing
`python meet_bot.py` — test `/meet` in Telegram.

## Usage
- Private chat: `/meet` for a link.
- Any chat: `@botusername meet` to send inline.
- Links are open—share freely!

## Troubleshooting
- Error 400? Check Google Cloud scopes (`meetings.space.created` enabled).
- No response? Reset webhook with `/deleteWebhook` curl.
- Host approval? Rooms are open by default—test with guests.

## License
[MIT License](LICENSE). Feel free to fork and improve!

Built by Mobin Sahidi. Contributions welcome!
