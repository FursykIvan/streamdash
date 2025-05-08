import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from voice_handler import handle_voice_query
from dotenv import load_dotenv

# Logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initializing the Telegram bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def download_voice_message(message: Message) -> bytes:
    """
    Downloads a voice message from Telegram.

    Args:
        message (Message): The Telegram message containing the voice file

    Returns:
        bytes: The binary data of the voice message

    Raises:
        Exception: If there's an error downloading the voice message
    """
    try:
        file = await bot.download(message.voice.file_id)
        return file.read() if hasattr(file, 'read') else file
    except Exception as e:
        logger.error(f"Voice download error: {e}")
        raise

@dp.message(F.content_type == ContentType.VOICE)
async def voice_message_handler(message: Message):
    """
    Handles voice messages received by the Telegram bot.

    This handler:
    1. Downloads the voice message
    2. Processes it using the voice handler to extract weather information
    3. Sends the weather information back to the user

    Args:
        message (Message): The Telegram message containing the voice file
    """
    try:
        logger.info(f"Отримано голосове повідомлення від {message.from_user.id}")

        voice_data = await download_voice_message(message)
        logger.debug("Отримано голосове повідомлення, починаю обробку.")

        result = await handle_voice_query(voice_data)
        logger.info(f"Результат обробки: {result}")

        if result.get("status") == "success":
            # We use ready-made formatted text from voice_handler
            await message.answer(result["speech_response"])
        else:
            error_msg = result.get("message", "Невідома помилка")
            logger.error(f"Помилка обробки: {error_msg}")
            await message.answer(f"❌ {error_msg}")

    except asyncio.TimeoutError:
        error_msg = "Час очікування вичерпано"
        logger.error(error_msg)
        await message.answer("⌛ Перевищено час обробки запиту. Спробуйте ще раз.")
    except Exception as e:
        logger.exception("Критична помилка при обробці повідомлення")
        await message.answer("⚠️ Сталася несподівана помилка. Спробуйте пізніше.")

@dp.message(F.text == "/start")
async def start_command(message: Message):
    """
    Handles the /start command with a reply keyboard and intro message.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ℹ️ Як дізнатись погоду?")]
        ],
        resize_keyboard=True,
    )

    await message.answer(
        "👋 Вітаю! Для того щоб дізнатись погоду у вашому місті, "
        "відправте голосове повідомлення з назвою вашого міста чи села. Наприклад: *Київ* 🎤",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def main():
    """
    Starts the Telegram bot and begins polling for messages.

    This is the main entry point for the bot application.
    The function runs until interrupted or an error occurs.
    """
    logger.info("Запуск бота...")
    await dp.start_polling(bot)
    logger.info("Бот зупинено")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинено користувачем")
