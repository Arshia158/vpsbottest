import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# توکن ربات خود را اینجا قرار دهید
TOKEN = "8296047206:AAHpSoqUr2Q-3mTRnZ1bcZ6_dsumMVVKC-k"

# فعال‌سازی لاگ برای دیدن خطاها
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    این تابع پیام‌های دریافتی را پردازش می‌کند.
    """
    # بررسی می‌کنیم که آیا پیام متنی است و با 'امام' شروع می‌شود یا خیر
    if update.message and update.message.text and update.message.text.startswith("امام"):
        
        # استخراج متن بعد از کلمه 'امام'
        # .strip() فاصله‌های اضافی از ابتدا و انتها را حذف می‌کند
        response_text = update.message.text[len("امام"):].strip()
        
        # اگر بعد از 'امام' متنی وجود داشت، آن را ارسال کن
        if response_text:
            # ارسال پاسخ به همان چتی که پیام اصلی از آن آمده است
            await update.message.reply_text(response_text)
            
            # تلاش برای حذف پیام اصلی کاربر
            # این کار فقط در گروه‌ها و سوپرگروه‌ها و اگر ربات ادمین باشد ممکن است
            try:
                await update.message.delete()
                logger.info(f"پیام کاربر {update.effective_user.username} در چت {update.effective_chat.title} حذف شد.")
            except Exception as e:
                # اگر نتوانست پیام را حذف کند (مثلاً در چت خصوصی یا عدم دسترسی)، خطا را لاگ می‌کند
                logger.warning(f"نمی‌توان پیام را حذف کرد: {e}")

def main() -> None:
    """
    نقطه شروع اجرای ربات
    """
    # ایجاد یک شیء Application برای مدیریت ربات
    application = Application.builder().token(TOKEN).build()

    # ایجاد یک هندلر برای پیام‌های متنی
    # این هندلر به تمام پیام‌های متنی گوش می‌دهد و تابع handle_message را فراخوانی می‌کند
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

    # اضافه کردن هندلر به اپلیکیشن
    application.add_handler(message_handler)

    # شروع ربات
    print("ربات با موفقیت شروع به کار کرد...")
    application.run_polling()

if __name__ == "__main__":
    main()