import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# توکن ربات خود را اینجا قرار دهید
TOKEN = "8296047206:AAHpSoqUr2Q-3mTRnZ1bcZ6_dsumMVVKC-k"

# فعال‌سازی لاگ برای دیدن خطاها (فقط خطاها و هشدارها نمایش داده می‌شوند)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)

# آیدی کاربر شما برای دریافت خطاها (اختیاری ولی پیشنهادی)
# می‌توانید با ربات userinfobot در تلگرام آیدی خود را پیدا کنید
DEVELOPER_CHAT_ID = 123456789 # <-- آیدی عددی خود را اینجا وارد کنید

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    به دستور /start در پیوی پاسخ می‌دهد.
    """
    # ایجاد دکمه شیشه‌ای برای افزودن به گروه
    keyboard = [
        [InlineKeyboardButton("➕ افزودن ربات به گروه", url=f"https://t.me/{context.bot.username}?startgroup=true")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # متن پیام خوشامدگوی کامل
    welcome_text = (
        "سلام! به ربات من خوش آمدید.\n\n"
        "کار من اینه که پیام‌هایی که با کلمه‌ی «امام» شروع می‌شن رو براتون بازنویسی کنم.\n\n"
        "🔹 **نحوه استفاده در گروه:**\n"
        "فقط کافیه قبل از پیامتون کلمه‌ی «امام» رو بنویسید. من خودم پیام اصلی شما رو پاک می‌کنم و فقط پیام اصلی رو می‌فرستم.\n\n"
        "مثال:\n"
        "شما می‌نویسید: `امام سلام به همه`\n"
        "من می‌فرستم: `سلام به همه`\n\n"
        "برای شروع، من را به گروه مورد نظرتون اضافه کنید و حتماً دسترسی حذف پیام رو بهم بدید."
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    پیام‌های دریافتی را پردازش می‌کند و پیام‌های شروع شده با 'امام' را مدیریت می‌کند.
    """
    # این تابع فقط در گروه‌ها و سوپرگروه‌ها روی پیام‌هایی که دستور نیستند کار می‌کند
    if update.message and update.message.text and update.message.text.startswith("امام"):
        
        # استخراج متن بعد از کلمه 'امام'
        response_text = update.message.text[len("امام"):].strip()
        
        # اگر بعد از 'امام' متنی وجود داشت، آن را ارسال کن
        if response_text:
            # ارسال پاسخ به همان چتی که پیام اصلی از آن آمده است
            await update.message.reply_text(response_text)
            
            # تلاش برای حذف پیام اصلی کاربر
            try:
                await update.message.delete()
                # logger.info(f"پیام کاربر {update.effective_user.username} در چت {update.effective_chat.title} حذف شد.")
            except Exception as e:
                # اگر نتوانست پیام را حذف کند (مثلاً عدم دسترسی)، خطا را لاگ می‌کند
                logger.warning(f"نمی‌توان پیام را حذف کرد در چت {update.effective_chat.title}: {e}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    برای مدیریت کلیک روی دکمه‌های شیشه‌ای (در این مثال لازم نیست ولی برای ساختار خوب است)
    """
    query = update.callback_query
    await query.answer() # به کاربر نشان می‌دهد که کلیک ثبت شد

def main() -> None:
    """
    نقطه شروع اجرای ربات
    """
    # ایجاد یک شیء Application برای مدیریت ربات
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلر برای دستور /start فقط در چت‌های خصوصی
    application.add_handler(CommandHandler("start", start_command, filters=filters.ChatType.PRIVATE))
    
    # اضافه کردن هندلر برای کلیک روی دکمه‌های شیشه‌ای
    application.add_handler(CallbackQueryHandler(button_callback))

    # ایجاد یک هندلر برای پیام‌های متنی در گروه‌ها و سوپرگروه‌ها
    # این هندلر به تمام پیام‌های متنی گوش می‌دهد و تابع handle_message را فراخوانی می‌کند
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS, handle_message)
    application.add_handler(message_handler)

    # ارسال خطاها به توسعه‌دهنده (اختیاری ولی بسیار مفید)
    # اگر DEVELOPER_CHAT_ID را پر کرده باشید، تمام خطاهای ربات برای شما ارسال می‌شود
    if DEVELOPER_CHAT_ID != 123456789:
        application.add_error_handler(lambda update, context: context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=f"Error: {context.error}"))

    # شروع ربات
    print("ربات با موفقیت شروع به کار کرد...")
    application.run_polling()

if __name__ == "__main__":
    main()