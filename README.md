# Fundraising-BOT
# Telegram Scout Bot

A Telegram bot that scouts information from Twitter, Telegram, and OpenAI.

## Setup

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in your API keys
3. Install dependencies:
   - Python: `pip install -r requirements.txt`
4. Run the bot:
   - Python: `python bot.py`

## Deployment

This bot can be deployed on:
- Heroku
- Railway  
- Any VPS with Python support

## Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `TELEGRAM_API_ID`: Your Telegram API ID from my.telegram.org
- `TELEGRAM_API_HASH`: Your Telegram API hash from my.telegram.org  
- `OPENAI_API_KEY`: Your OpenAI API key
- `TWITTER_BEARER_TOKEN`: Twitter API bearer token (for read-only access)
- `TELETHON_SESSION`: Session name for Telethon client (e.g., "bot_session")
