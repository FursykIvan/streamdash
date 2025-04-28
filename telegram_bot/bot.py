import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.utils import executor
from voice_handler import handle_voice_query

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.VOICE)
async def voice_message_handler(message: types.Message):
    voice = message.voice
    file_info = await bot.get_file(voice.file_id)
    file_path = file_info.file_path

    voice_file = await bot.download_file(file_path)
    voice_data = voice_file.read()

    result = handle_voice_query(voice_data)

    if result["status"] == "success":
        weather = result["data"]
        response_text = (
            f"Погода в {weather['city']}:\n"
            f"Температура: {weather['temperature']}°C\n"
            f"Вологість: {weather['humidity']}%\n"
            f"Час оновлення: {weather['timestamp']}"
        )
    else:
        response_text = f"Помилка: {result['message']}"

    await message.reply(response_text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
