import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile
from aiogram.filters import Command
import threading


class TelegramBot:
    def __init__(self, client, token: str):
        self.client = client
        self.token = token
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.router = Router()
       
        # Реєструємо обробники
        self.setup_handlers()
        self.dp.include_router(self.router)
       
    def setup_handlers(self):
        """Налаштування команд бота"""
       
        @self.router.message(Command("start"))
        async def start_cmd(message: Message):
            await message.answer(
                "🤖 Привіт! Я AI-бот, на основі Gemini.\n"
                f"Поточний режим: {self.client.current_mode}\n\n"
                "Обери режим або напиши повідомлення.",
                reply_markup=self.get_keyboard(),
            )
            print(f"Користувач {message.from_user.id} запустив бота") # логування
           
     
        @self.router.message(lambda m: m.text in ["👨‍💻 Програміст", "🧠 Асистент", "ℹ️ Режими"])
        async def handle_buttons(message: Message):
            if message.text == "👨‍💻 Програміст":
                self.client.set_mode("teach")
                await message.answer("✅ Режим 👨‍💻 Програміст активовано")
               
            elif message.text == "🧠 Асистент":
                self.client.set_mode("assistant")
                await message.answer("✅ Режим 🧠 Асистент активовано")
               
            elif message.text == "ℹ️ Режими":
                modes = self.client.get_available_modes()
                await message.answer(
                    "📌 **Доступні режими:**\n" + "\n".join(f"• {m}" for m in modes),
                    parse_mode="Markdown"
                )
       
        @self.router.message()
        async def ai_chat(message: Message):
            if message.text.startswith('/'):
                return
               
           
            print(f"Отримано {message.text[:50]}")
           
            await message.answer("⏳ Думаю...")
           
           
            response = self.client.ask(message.text)
           
           
            max_len = 4000
            for i in range(0, len(response), max_len):
                await message.answer(response[i:i+max_len])
   
    def get_keyboard(self):
        """Створити клавіатуру"""
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👨‍💻 Програміст"), KeyboardButton(text="🧠 Асистент")],
                [KeyboardButton(text="ℹ️ Режими")]
            ],
            resize_keyboard=True
        )
   
    def run_bot(self):
        """Запустити бота (викликається в потоці)"""
    
    async def start_polling(self):
        print("Телеграм бот запущено!")
        await self.dp.start_polling(self.bot)


