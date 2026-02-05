import asyncio
import threading
import os
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def home():
    return "OK"
 
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
 
 
async def main():
    import os
 
    from gemini_client import GeminiClient
    from bot import TelegramBot
 
 
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("Token Bot Error")
 
 
    ai_client = GeminiClient()
    bot = TelegramBot(ai_client, BOT_TOKEN)
    await bot.start_polling()
   
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
