import sqlite3
import os
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

# التوكن الخاص بالبوت
TOKEN = "8988959320:AAHvWLscdTU2r7c1DjUOe1DycgHQ4ZDjz_0"

# --- التعديل الجوهري هنا ---
# جلب المتغيرات، وإذا لم توجد، نضع قيمة افتراضية فارغة لتجنب الانهيار
api_id_env = os.environ.get("API_ID")
api_hash_env = os.environ.get("API_HASH")

# التحقق من وجود المتغيرات وتحويلها للنوع الصحيح
if api_id_env and api_hash_env:
    # استخدام المتغيرات إذا وجدت
    app = Client("ControlBot", bot_token=TOKEN, api_id=int(api_id_env), api_hash=api_hash_env)
else:
    # تشغيل البوت بدونهم إذا لم يتم ضبط المتغيرات (سيعمل كبوت فقط)
    app = Client("ControlBot", bot_token=TOKEN)
# ----------------------------

# تهيئة قاعدة البيانات
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (session_name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS links (link TEXT)")
conn.commit()

def get_config(key, default):
    cursor.execute("SELECT value FROM config WHERE key=?", (key,))
    res = cursor.fetchone()
    return res[0] if res else default

# الأزرار الرئيسية
def main_menu():
    return ReplyKeyboardMarkup([
        ["⚙️ السليب", "🔢 عدد الرسائل"],
        ["➕ إضافة حساب", "📱 الحسابات المضافة"],
        ["🔗 إضافة رابط", "▶️ بدء الإرسال"],
        ["⏹ إيقاف", "ℹ️ المعلومات"]
    ], resize_keyboard=True)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("أهلاً بك في بوت البلاغات الذكي، اختر من القائمة:", reply_markup=main_menu())

@app.on_message(filters.regex("ℹ️ المعلومات"))
async def info(client, message):
    sleep = get_config("sleep", "2")
    count = get_config("count", "1")
    cursor.execute("SELECT link FROM links")
    links = [r[0] for r in cursor.fetchall()]
    await message.reply(f"📊 الإعدادات:\n- السليب: {sleep} ثانية\n- عدد الرسائل: {count}\n- الروابط: {len(links)} رابط")

print("البوت يعمل الآن...")
app.run()
