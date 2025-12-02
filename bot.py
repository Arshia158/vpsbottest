# file: bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# توکن را یا اینجا مستقیم بذار، یا به صورت متغیر محیطی: TELEGRAM_TOKEN
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "PASTE_YOUR_TOKEN_HERE")

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من یک ربات ساده‌ام.\n"
        "دستورها:\n"
        "• /help راهنما\n"
        "• هر پیام متنی → پاسخ اِکو"
    )

# دستور /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "راهنما:\n"
        "– /start شروع\n"
        "– /help این صفحه\n"
        "– هر پیام متنی را اِکو می‌کنم 😉"
    )

# هندلر پیام‌های متنی (Echo)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("متن خالیه!")
        return
    await update.message.reply_text(f"پیامت: {text}")

# خطایابی ساده
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        raise RuntimeError("توکن رو وارد کن: env TELEGRAM_TOKEN یا داخل کد.")

    app = Application.builder().token(BOT_TOKEN).build()

    # ثبت دستورها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    # هر پیام متنی
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # لاگ خطا
    app.add_error_handler(error_handler)

    # اجرای Polling
    print("Bot is running... Ctrl+C برای توقف")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()