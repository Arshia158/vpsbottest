# file: bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توکن رسمی شما
BOT_TOKEN = "8557797762:AAFOD9vHLWB0lBG_hQj5dFbKUCnqPtbB7Mg"

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n"
        "من یک ربات ساده با کتابخونه رسمی python-telegram-bot هستم.\n"
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

# اِکو کردن پیام‌های متنی
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    await update.message.reply_text(f"پیامت: {text}")

def main():
    # ساخت اپلیکیشن با توکن رسمی
    app = Application.builder().token(BOT_TOKEN).build()

    # ثبت دستورها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    # هر پیام متنی
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # اجرای Polling
    print("Bot is running... Ctrl+C برای توقف")
    app.run_polling()

if __name__ == "__main__":
    main()