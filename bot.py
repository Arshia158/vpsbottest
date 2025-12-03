import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

channel_id: str | None = None
task: asyncio.Task | None = None

SLEEP_INTERVAL = 0
BACKGROUND_URL = "http://v3.api-free.ir/background/"
CAPTION = "✨ لحظه‌ای برای خودت، لحظه‌ای برای آرامش ✨\n\nID : @rubka_library"


async def send_backgrounds(app):
    global channel_id
    while channel_id:
        try:
            await app.bot.send_photo(chat_id=channel_id, photo=BACKGROUND_URL, caption=CAPTION)
            print("Background sent")
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(SLEEP_INTERVAL)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global channel_id, task

    channel_id = update.effective_chat.id
    await context.bot.send_message(chat_id=channel_id, text="✅ ربات در کانال فعال شد و شروع به ارسال بک‌گراند می‌کند")

    if not task or task.done():
        task = asyncio.create_task(send_backgrounds(context.application))


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()