# sourcery skip: raise-specific-error
import asyncio
import Config
import logging
from pyromod import listen
from pyrogram import Client, idle
from ChannelBot.database import Database
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid


logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if Config.REPLIT:
    from threading import Thread

    from flask import Flask, jsonify
    
    web_app = Flask('')
    
    @web_app.route('/')
    def main():
        res = {
            "status":"running",
            "hosted":"replit.com",
        }
        
        return jsonify(res)

    def run():
      web_app.run(host="0.0.0.0", port=8000)
    
    async def keep_alive():
      server = Thread(target=run)
      server.start()

app = Client(
    ":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="ChannelBot"),
)
app.db = Database(Config.DATABASE_URL, 'ChannelAuto')

# Run Bot
if __name__ == "__main__":
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood) as e:
        raise Exception("Your API_ID/API_HASH is not valid.") from e
    except AccessTokenInvalid as e:
        raise Exception("Your BOT_TOKEN is not valid.") from e
    uname = app.get_me().username

    if Config.REPLIT:
        asyncio.run(keep_alive())

    print(f"@{uname} Started Successfully!")
    idle()
    app.stop()
    print("Bot stopped. Alvida!")
