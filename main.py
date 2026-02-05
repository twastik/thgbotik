import asyncio

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
    asyncio.run(main())