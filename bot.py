import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Замени токен на свой из @BotFather
TOKEN = "8942200173:AAG7Z_JEC0zpO0IW64QZDoAzIxLQQ_FOrWo"
# Ссылка на твой индекс-файл (пока тестируешь локально, можно использовать GitHub Pages или Ngrok)
WEBAPP_URL = "https://snuvik3-cloud.github.io/mlbb-counter-bot/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создаем кнопку, которая откроет наше Web App прямо внутри ТГ
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Открыть Помощник Драфта ⚔️",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ])
    
    await message.answer(
        "Привет! Я помогу тебе затащить драфт в MLBB.\n"
        "Нажми на кнопку ниже, чтобы открыть ассистента контрпиков.",
        reply_markup=markup
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())