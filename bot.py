from rubka import Bot

# توکن ربات روبیکا
TOKEN = "DBBAB0VAVOAWFLDIEJEFYOVLBXOYPYDEAEINKNCYHOMVVYRAMUQEPBUMMINZGMIL"

# ساخت شیء بات
bot = Bot(TOKEN)

def main():
    print("ربات روبیکا با rubka شروع شد...")

    while True:
        try:
            updates = bot.get_updates()
            for update in updates:
                chat_id = update['object_guid']
                message_id = update['message_id']
                text = update.get('text', '')

                # دستور start (نمایش راهنما)
                if text == "/start":
                    welcome_text = (
                        "سلام! به ربات من خوش آمدید.\n\n"
                        "کار من اینه که پیام‌هایی که با کلمه‌ی «امام» شروع می‌شن رو براتون بازنویسی کنم.\n\n"
                        "🔹 **نحوه استفاده در گروه:**\n"
                        "فقط کافیه قبل از پیامتون کلمه‌ی «امام» رو بنویسید. من خودم پیام اصلی شما رو پاک می‌کنم و فقط متن اصلی رو می‌فرستم.\n\n "مثال:\n"
                        "شما می‌نویسید: امام سلام به همه\n"
                        "من می‌فرستم: سلام به همه\n\n"
                        "برای شروع، من را به گروه مورد نظرتون اضافه کنید و حتماً دسترسی حذف پیام رو بهم بدید."
                    )
                    bot.send_message(chat_id, welcome_text)

                # بررسی پیام‌هایی که با "امام" شروع می‌شوند
                elif text.startswith("امام"):
                    response_text = text[len("امام"):].strip()
                    if response_text:
                        bot.send_message(chat_id, response_text)
                        # حذف پیام اصلی
                        bot.delete_messages(chat_id, [message_id])

        except Exception as e:
            print("خطا:", e)

if __name__ == "__main__":
    main()