import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InputMediaPhoto

CHANNEL_USERNAME = "@Me1Arshia"  # یا آیدی عددی کانال مثل -1001234567890
API_IMAGE_URL = "http://v3.api-free.ir/background"
EDIT_INTERVAL_SECONDS = 20

# توکن جدید شما
BOT_TOKEN = "8324484566:AAFZmP5YgEfRofEGgV87g98KGpJTr3hBzwc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def post_or_get_message_id():
    msg = await bot.send_photo(
        chat_id=CHANNEL_USERNAME,
        photo=API_IMAGE_URL,
        caption="Background auto-refresh (updated every 20s)"
    )
    return msg.message_id

async def background_refresher(message_id: int):
    while True:
        try:
            media = InputMediaPhoto(
                media=API_IMAGE_URL,
                caption="Background auto-refresh (updated every 20s)"
            )
            await bot.edit_message_media(
                chat_id=CHANNEL_USERNAME,
                message_id=message_id,
                media=media
            )
        except Exception as e:
            print(f"Edit failed: {e}")
        await asyncio.sleep(EDIT_INTERVAL_SECONDS)

async def main():
    message_id = await post_or_get_message_id()
    asyncio.create_task(background_refresher(message_id))
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())