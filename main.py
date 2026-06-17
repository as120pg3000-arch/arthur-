import sqlite3
import os
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup

# --- البيانات ---
TOKEN = "8988959320:AAHvWLscdTU2r7c1DjUOe1DycgHQ4ZDjz_0"
API_ID = os.environ.get("34418359")
API_HASH = os.environ.get("ffc2e6b7fc449832be0e4c9d2cf7e467")

# تهيئة بوت التحكم (للأزرار)
bot = Client("ControlBot", bot_token=TOKEN)

# تهيئة حساب المستخدم (للإبلاغ) - سيبحث عن ملف الجلسة
user = Client("MyUserAccount", api_id=int(API_ID) if API_ID else None, api_hash=API_HASH)

# تهيئة قاعدة البيانات
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS links (link TEXT)")
conn.commit()

# قائمة الأزرار
@bot.on_message(filters.command("start"))
async def start(client, message):
    menu = ReplyKeyboardMarkup([
        ["⚙️ السليب", "🔢 عدد الرسائل"],
        ["🔗 إضافة رابط", "▶️ بدء الإرسال"],
        ["ℹ️ المعلومات"]
    ], resize_keyboard=True)
    await message.reply("مرحباً بك، استخدم الأزرار للتحكم:", reply_markup=menu)

# تشغيل البوت وحساب المستخدم معاً
if __name__ == "__main__":
    # هذا السطر يشغل الاثنين معاً في نفس الوقت
    from pyrogram import idle
    bot.start()
    user.start()
    print("البوت وحساب المستخدم يعملان الآن...")
    idle()
    bot.stop()
    user.stop()
