import rubpy

# توکن ربات روبیکا
TOKEN = "DBBAB0VAVOAWFLDIEJEFYOVLBXOYPYDEAEINKNCYHOMVVYRAMUQEPBUMMINZGMIL"

# ساخت کلاینت
client = rubpy.Client(TOKEN)

@client.on_message
def handle_message(message):
    if message.text == "/start":
        message.reply("سلام 👋")

# اجرای ربات
client.run()
