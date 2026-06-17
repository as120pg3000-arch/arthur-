import sqlite3
import os
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, CallbackQuery

TOKEN = "8988959320:AAHvWLscdTU2r7c1DjUOe1DycgHQ4ZDjz_0"
API_ID = os.environ.get("34418359")
API_HASH = os.environ.get("ffc2e6b7fc449832be0e4c9d2cf7e467")

app = Client("ControlBot", bot_token=TOKEN, api_id=int(API_ID) if API_ID else None, api_hash=API_HASH)

# تهيئة قاعدة البيانات
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (session_name TEXT)")
conn.commit()

# قائمة الأزرار (أضفت فيها زر إضافة حساب)
def main_menu():
    return ReplyKeyboardMarkup([
        ["⚙️ السليب", "🔢 عدد الرسائل"],
        ["➕ إضافة حساب", "📱 الحسابات المضافة"],
        ["🔗 إضافة رابط", "▶️ بدء الإرسال"],
        ["ℹ️ المعلومات"]
    ], resize_keyboard=True)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("أهلاً بك، اختر من القائمة:", reply_markup=main_menu())

# دالة زر إضافة حساب
@app.on_message(filters.regex("➕ إضافة حساب"))
async def add_account(client, message):
    await message.reply("لإضافة حساب، يرجى إرسال رقم الهاتف مع رمز الدولة (مثال: +9647xxxxxxxxx)")

# هنا ستحتاج لإضافة دالة تستقبل الرقم وتسجل الدخول (هذا الجزء متقدم قليلاً)

print("البوت يعمل الآن...")
app.run()
