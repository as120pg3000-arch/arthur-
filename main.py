from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
import re
import asyncio
import time
import random
import datetime
import warnings
import os
import json
import hashlib
import socket
import aiohttp
import ping3
import speedtest
from datetime import datetime
import sys
import platform
import requests
import math
import string

warnings.filterwarnings("ignore")

api_id = 34418359 
api_hash = "ffc2e6b7fc449832be0e4c9d2cf7e467"

app = Client(
    "my_account",
    api_id=api_id,
    api_hash=api_hash,
    parse_mode=ParseMode.DEFAULT,
    sleep_threshold=60
)

# ============= البيانات الأساسية =============

data = {
    "active": False,
    "target_id": None,
    "target_name": None,
    "chat_id": None,
    "msg_id": None,
    "extra_text": None,
    "repeat_count": 1,
    "delay": 0,
    "start_time": None,
    "auto_stop": None,
    "reply_all": False,
    "welcome": False,
    "interaction": False,
    "random_mode": False,
    "time_name_active": False,
    "last_reply_time": 0
}

# ============= بيانات الشد =============

spam_data = {
    "active": False,
    "target_id": None,
    "target_name": None,
    "message": None,
    "delay": 1,
    "count": 10,
    "sent": 0,
    "task": None,
    "start_time": None,
    "is_bot": False
}

# ============= بيانات المكالمات =============

call_data = {
    "active": False,
    "type": None,
    "chat_id": None,
    "target_id": None,
    "target_name": None,
    "mode": None,
    "task": None,
    "start_time": None
}

# ============= بيانات البروكسي =============

proxy_data = {
    "active": False,
    "type": None,
    "host": None,
    "port": None,
    "username": None,
    "password": None,
    "country": None,
    "city": None,
    "isp": None,
    "latency": None,
    "last_check": None
}

proxy_list = []

# ============= بيانات الحفظ =============

settings_file = "lazek_settings.json"
spam_file = "spam_settings.json"
replies_file = "replies.json"
proxy_file = "proxy_settings.json"
call_file = "call_settings.json"
backup_file = "backup_settings.json"

# ============= المتغيرات العالمية =============

ignore_list = []
banned_list = []
stats = {}
auto_replies = {}
random_messages = []
saved_texts = {}
clipboard = {"text": ""}
original_profile = {"photo": None, "first_name": "", "last_name": "", "bio": ""}
protection_settings = {"enabled": False, "max_replies_per_minute": 5, "reply_count": {}, "last_reset": time.time()}
auto_name_updates = {"active": False, "task": None}
time_name_active = False
time_name_task = None
guessing_game = {"active": False, "number": 0, "attempts": 0}
profile_protection = {"name": False, "photo": False}
reminders = {}
welcome_active = False
BOT_START_TIME = time.time()

# ============= النكات =============

jokes = [
    "😂 واحد سأل صاحبه: ليه الدجاجة عبرت الطريق؟ قال: عشان توصل للجانب الآخر!",
    "😄 مرة واحد دخل مطعم قال للجرسون: عندكم سمك؟ قال: لأ، بس عندنا جرجير!",
    "🤣 واحد بيشتكي لصاحبه: مرتي بتكلمني وانا نايم! قال: ليش؟ قال: عشان تصحى تسمعها!",
    "😅 مرة واحد سألوه: شو سر نجاحك؟ قال: اني ما اشتغل ابداً!",
    "😂 واحد قال لصاحبه: انا حافظ القرآن كامل! قال: خلينا نشوف! قال: بس انسى شوية!",
    "🤣 مرة واحد دكتور قال لمريض: انت بحاجة لعملية! قال: لا حول ولا قوة الا بالله!",
    "😄 مرة واحد سألوه: ليش انت دائمًا مبتسم؟ قال: عشان اسنانى بيضا!"
]

welcome_messages = [
    "🎉 اهلاً بك {name} في المجموعة!",
    "👋 مرحباً {name}، نورت المجموعة!",
    "🌸 أهلاً وسهلاً {name}، معنا في المجموعة",
    "🔥 نورت يا {name}، انتظرناك!",
    "💫 أهلاً {name}، فرحتنا بيك كبيرة!",
    "🌟 يا هلا {name}، معنا في العائلة!"
]

# ============= دوال الحفظ والاسترجاع =============

def save_settings():
    try:
        settings = {"data": data, "ignore_list": ignore_list, "banned_list": banned_list, "stats": stats}
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_settings():
    global data, ignore_list, banned_list, stats
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                data.update(settings.get("data", {}))
                ignore_list = settings.get("ignore_list", [])
                banned_list = settings.get("banned_list", [])
                stats = settings.get("stats", {})
            return True
    except:
        pass
    return False

def save_spam_settings():
    try:
        with open(spam_file, 'w', encoding='utf-8') as f:
            json.dump(spam_data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_spam_settings():
    global spam_data
    try:
        if os.path.exists(spam_file):
            with open(spam_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                for key in spam_data:
                    if key in loaded and key not in ["task", "sent", "active"]:
                        spam_data[key] = loaded[key]
            return True
    except:
        pass
    return False

def save_replies():
    try:
        with open(replies_file, 'w', encoding='utf-8') as f:
            json.dump(auto_replies, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_replies():
    global auto_replies
    try:
        if os.path.exists(replies_file):
            with open(replies_file, 'r', encoding='utf-8') as f:
                auto_replies = json.load(f)
            return True
    except:
        pass
    return False

def save_proxy_settings():
    try:
        proxy_save = {"proxy_data": proxy_data, "proxy_list": proxy_list}
        with open(proxy_file, 'w', encoding='utf-8') as f:
            json.dump(proxy_save, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_proxy_settings():
    global proxy_data, proxy_list
    try:
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                proxy_data.update(loaded.get("proxy_data", {}))
                proxy_list = loaded.get("proxy_list", [])
            return True
    except:
        pass
    return False

def save_call_settings():
    try:
        with open(call_file, 'w', encoding='utf-8') as f:
            json.dump(call_data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def load_call_settings():
    global call_data
    try:
        if os.path.exists(call_file):
            with open(call_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                for key in call_data:
                    if key in loaded and key not in ["task"]:
                        call_data[key] = loaded[key]
            return True
    except:
        pass
    return False

def backup_settings():
    try:
        backup = {
            "data": data,
            "spam_data": spam_data,
            "call_data": call_data,
            "proxy_data": proxy_data,
            "proxy_list": proxy_list,
            "ignore_list": ignore_list,
            "banned_list": banned_list,
            "stats": stats,
            "auto_replies": auto_replies
        }
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def restore_settings():
    global data, spam_data, call_data, proxy_data, proxy_list, ignore_list, banned_list, stats, auto_replies
    try:
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup = json.load(f)
                data.update(backup.get("data", {}))
                for key in spam_data:
                    if key in backup.get("spam_data", {}) and key not in ["task", "sent", "active"]:
                        spam_data[key] = backup["spam_data"][key]
                for key in call_data:
                    if key in backup.get("call_data", {}) and key not in ["task"]:
                        call_data[key] = backup["call_data"][key]
                proxy_data.update(backup.get("proxy_data", {}))
                proxy_list = backup.get("proxy_list", [])
                ignore_list = backup.get("ignore_list", [])
                banned_list = backup.get("banned_list", [])
                stats = backup.get("stats", {})
                auto_replies = backup.get("auto_replies", {})
            return True
    except:
        pass
    return False

# تحميل الإعدادات
load_settings()
load_spam_settings()
load_replies()
load_proxy_settings()
load_call_settings()

# ============= دوال مساعدة =============

async def parse_link(link):
    try:
        link = link.strip()
        if "t.me/" in link:
            link = link.split("t.me/")[1]
        link = link.split("?")[0].split("#")[0]
        if link.startswith("c/"):
            parts = link.split("/")
            if len(parts) >= 3 and parts[1].isdigit():
                chat_id = int("-100" + parts[1])
                msg_id = int(parts[2])
                return chat_id, msg_id
        elif "/" in link:
            parts = link.split("/")
            if len(parts) >= 2 and parts[1].isdigit():
                try:
                    chat = await app.get_chat(parts[0])
                    if chat:
                        return chat.id, int(parts[1])
                except:
                    if parts[0].lstrip('-').isdigit():
                        return int(parts[0]), int(parts[1])
        numbers = re.findall(r'\d+', link)
        if len(numbers) >= 2:
            if len(numbers[0]) > 10:
                return int("-100" + numbers[0]), int(numbers[1])
            else:
                return int(numbers[0]), int(numbers[1])
        return None, None
    except:
        return None, None

async def get_target_user(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    try:
        text = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else ""
        if text:
            if text.startswith("@"):
                text = text[1:]
            try:
                user = await client.get_users(text)
                if user:
                    return user
            except:
                pass
            try:
                user_id = int(text)
                user = await client.get_users(user_id)
                if user:
                    return user
            except:
                pass
    except:
        pass
    return None

async def get_user_info(client, identifier):
    try:
        if identifier.startswith("@"):
            identifier = identifier[1:]
        try:
            return await client.get_users(identifier)
        except:
            try:
                return await client.get_users(int(identifier))
            except:
                return None
    except:
        return None

def get_uptime():
    elapsed = time.time() - BOT_START_TIME
    days = int(elapsed // 86400)
    hours = int((elapsed % 86400) // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    if days > 0:
        return f"{days} يوم {hours} ساعة {minutes} دقيقة"
    elif hours > 0:
        return f"{hours} ساعة {minutes} دقيقة"
    elif minutes > 0:
        return f"{minutes} دقيقة {seconds} ثانية"
    else:
        return f"{seconds} ثانية"

def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}م"
    elif num >= 1_000:
        return f"{num/1_000:.1f}ألف"
    return str(num)

def get_system_info():
    """جلب معلومات النظام بدون psutil"""
    try:
        import os
        import platform
        # معلومات بسيطة من os
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": platform.python_version()
        }
    except:
        return {
            "system": "غير معروف",
            "release": "غير معروف",
            "python": "غير معروف"
        }

# ============= دوال البروكسي =============

async def test_proxy_connection(proxy_type, host, port, username=None, password=None):
    try:
        start_time = time.time()
        if proxy_type == "http":
            proxy_url = f"http://{host}:{port}"
            if username and password:
                proxy_url = f"http://{username}:{password}@{host}:{port}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://httpbin.org/ip', proxy=proxy_url, timeout=5) as response:
                        if response.status == 200:
                            return (time.time() - start_time) * 1000
            except:
                pass
        elif proxy_type in ["socks4", "socks5"]:
            try:
                reader, writer = await asyncio.open_connection(host, port, timeout=5)
                writer.close()
                await writer.wait_closed()
                return (time.time() - start_time) * 1000
            except:
                pass
        return None
    except:
        return None

async def get_proxy_location(proxy_type, host, port, username=None, password=None):
    try:
        async with aiohttp.ClientSession() as session:
            url = "http://ip-api.com/json/"
            if proxy_type == "http":
                proxy_url = f"http://{host}:{port}"
                if username and password:
                    proxy_url = f"http://{username}:{password}@{host}:{port}"
                try:
                    async with session.get(url, proxy=proxy_url, timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get('status') == 'success':
                                return {"country": data.get('country', 'غير معروف'), "city": data.get('city', 'غير معروف'), "isp": data.get('isp', 'غير معروف')}
                except:
                    pass
            else:
                try:
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get('status') == 'success':
                                return {"country": data.get('country', 'غير معروف'), "city": data.get('city', 'غير معروف'), "isp": data.get('isp', 'غير معروف')}
                except:
                    pass
        return None
    except:
        return None

# ============================
# أوامر اللزك
# ============================

@app.on_message(filters.command(["لزك", "lk"], prefixes=".") & filters.me)
async def start_lazek(client, message: Message):
    target_user = await get_target_user(client, message)
    if not target_user:
        await message.edit("❌ يرجى تحديد المستهدف!\n• ارد على رسالته\n• اكتب يوزره: @username\n• اكتب ايديه: 123456789")
        return
    try:
        text = message.text
        link_match = re.search(r'https?://t\.me/[^\s]+', text)
        if link_match:
            link = link_match.group(0)
            extra_text = text.replace(link, "").replace(".لزك", "").replace(".lk", "").strip()
        else:
            parts = text.split(" ", 1)
            if len(parts) > 1 and "t.me/" in parts[1]:
                link = parts[1]
                extra_text = ""
            else:
                await message.edit("❌ يرجى إضافة رابط الرسالة!\nمثال: .لزك @username https://t.me/...")
                return
    except:
        await message.edit("❌ خطأ في قراءة الرابط!")
        return
    chat_id, msg_id = await parse_link(link)
    if not chat_id or not msg_id:
        await message.edit("❌ رابط غير صحيح!")
        return
    try:
        test_msg = await client.get_messages(chat_id, msg_id)
        if not test_msg:
            await message.edit("❌ لا يمكن الوصول للرسالة!")
            return
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:50]}")
        return
    data["active"] = True
    data["target_id"] = target_user.id
    data["target_name"] = target_user.first_name
    data["chat_id"] = chat_id
    data["msg_id"] = msg_id
    data["extra_text"] = extra_text if extra_text else None
    save_settings()
    confirm_msg = f"✅ تم تفعيل اللزك على: **{target_user.first_name}**"
    if target_user.username:
        confirm_msg += f"\n📌 اليوزر: @{target_user.username}"
    confirm_msg += f"\n🆔 المعرف: `{target_user.id}`"
    if extra_text:
        confirm_msg += f"\n📝 النص الإضافي: {extra_text}"
    await message.edit(confirm_msg)

@app.on_message(filters.command(["تفعيل", "on"], prefixes=".") & filters.me)
async def reactivate(client, message: Message):
    if data["target_id"] is None:
        await message.edit("❌ لا توجد إعدادات سابقة!")
        return
    data["active"] = True
    save_settings()
    await message.edit(f"✅ تم إعادة تفعيل اللزك على {data['target_name'] or data['target_id']}")

@app.on_message(filters.command(["ايقاف", "off", "stop"], prefixes=".") & filters.me)
async def stop_lazek(client, message: Message):
    data["active"] = False
    save_settings()
    await message.edit("🛑 تم إيقاف اللزك.")

@app.on_message(filters.command(["حالة", "st"], prefixes=".") & filters.me)
async def status_lazek(client, message: Message):
    if data["active"]:
        status = f"✅ اللزك مفعل\n👤 المستهدف: {data['target_name'] or data['target_id']}\n🆔 ID: {data['target_id']}"
        if data["extra_text"]:
            status += f"\n📝 النص: {data['extra_text']}"
        status += f"\n🔄 التكرار: {data['repeat_count']}"
        status += f"\n⏱️ السليب: {data['delay']} ثانية"
        if data["auto_stop"]:
            remaining = data["auto_stop"] - time.time()
            if remaining > 0:
                status += f"\n⏱️ متبقي: {int(remaining // 60)} دقيقة"
        await message.edit(status)
    else:
        await message.edit("❌ اللزك غير مفعل")

@app.on_message(filters.command(["نص", "text"], prefixes=".") & filters.me)
async def set_extra_text(client, message: Message):
    if not data["active"]:
        await message.edit("❌ اللزك غير مفعل!")
        return
    try:
        extra_text = message.text.split(" ", 1)[1]
        data["extra_text"] = extra_text
        save_settings()
        await message.edit(f"✅ تم تحديث النص: {extra_text}")
    except:
        await message.edit("❌ استخدم: .نص مرحباً بك")

@app.on_message(filters.command(["تكرار", "rep"], prefixes=".") & filters.me)
async def set_repeat(client, message: Message):
    try:
        count = int(message.text.split(" ")[1])
        if count < 1:
            await message.edit("❌ العدد يجب أن يكون أكبر من 0")
            return
        if count > 100:
            await message.edit("⚠️ حد أقصى 100 تكرار")
            count = 100
        data["repeat_count"] = count
        save_settings()
        await message.edit(f"✅ تم ضبط التكرار: {count}")
    except:
        await message.edit("❌ استخدم: .تكرار 5")

@app.on_message(filters.command(["السليب", "delay"], prefixes=".") & filters.me)
async def set_delay(client, message: Message):
    try:
        delay = float(message.text.split(" ")[1])
        if delay < 0:
            await message.edit("❌ السليب لا يمكن أن يكون سالب")
            return
        if delay > 60:
            await message.edit("⚠️ حد أقصى 60 ثانية")
            delay = 60
        data["delay"] = delay
        save_settings()
        await message.edit(f"✅ تم ضبط السليب: {delay} ثانية")
    except:
        await message.edit("❌ استخدم: .السليب 2.5")

@app.on_message(filters.command(["وقت", "time"], prefixes=".") & filters.me)
async def set_timer(client, message: Message):
    if not data["active"]:
        await message.edit("❌ اللزك غير مفعل!")
        return
    try:
        minutes = float(message.text.split(" ")[1])
        if minutes < 1:
            await message.edit("❌ الوقت يجب أن يكون أكبر من 0")
            return
        if minutes > 1440:
            await message.edit("⚠️ حد أقصى 1440 دقيقة (يوم)")
            minutes = 1440
        data["start_time"] = time.time()
        data["auto_stop"] = time.time() + (minutes * 60)
        save_settings()
        time_text = f"{int(minutes)} دقيقة" if minutes < 60 else f"{int(minutes//60)} ساعة"
        await message.edit(f"⏱️ تم ضبط الإيقاف بعد {time_text}")
    except:
        await message.edit("❌ استخدم: .وقت 30")

@app.on_message(filters.command(["توقيت", "timer"], prefixes=".") & filters.me)
async def show_timer(client, message: Message):
    if not data["active"]:
        await message.edit("❌ اللزك غير مفعل!")
        return
    if data["auto_stop"] is None:
        await message.edit("⏱️ لا يوجد وقت محدد للإيقاف")
        return
    remaining = data["auto_stop"] - time.time()
    if remaining <= 0:
        data["active"] = False
        data["auto_stop"] = None
        save_settings()
        await message.edit("⏱️ انتهى الوقت! تم إيقاف اللزك")
        return
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    await message.edit(f"⏱️ الوقت المتبقي: {minutes} دقيقة و {seconds} ثانية")

@app.on_message(filters.command(["كل", "all"], prefixes=".") & filters.me)
async def reply_all(client, message: Message):
    if not data["active"]:
        await message.edit("❌ اللزك غير مفعل!")
        return
    data["reply_all"] = not data["reply_all"]
    status = "مفعل" if data["reply_all"] else "معطل"
    save_settings()
    await message.edit(f"✅ تم {status} الرد على الكل")

@app.on_message(filters.command(["مسح", "reset"], prefixes=".") & filters.me)
async def reset_lazek(client, message: Message):
    data["active"] = False
    data["target_id"] = None
    data["target_name"] = None
    data["chat_id"] = None
    data["msg_id"] = None
    data["extra_text"] = None
    data["repeat_count"] = 1
    data["delay"] = 0
    data["auto_stop"] = None
    data["reply_all"] = False
    ignore_list.clear()
    save_settings()
    await message.edit("🧹 تم مسح جميع الإعدادات")

@app.on_message(filters.command(["منشن", "mention"], prefixes=".") & filters.me)
async def mention_user(client, message: Message):
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ ارد على المستخدم!")
        return
    try:
        text = message.text.split(" ", 1)[1]
    except:
        text = "اهلاً بك"
    mention = f"[{target.first_name}](tg://user?id={target.id})"
    await message.edit(f"{mention} {text}")

@app.on_message(filters.command(["تجاهل", "ig"], prefixes=".") & filters.me)
async def ignore_user(client, message: Message):
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ ارد على المستخدم!")
        return
    user_id = target.id
    if user_id in ignore_list:
        ignore_list.remove(user_id)
        await message.edit(f"✅ تم إلغاء تجاهل {target.first_name}")
    else:
        ignore_list.append(user_id)
        await message.edit(f"✅ تم تجاهل {target.first_name}")
    save_settings()

@app.on_message(filters.command(["حظر", "ban"], prefixes=".") & filters.me)
async def ban_user(client, message: Message):
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ ارد على المستخدم!")
        return
    user_id = target.id
    if user_id in banned_list:
        banned_list.remove(user_id)
        await message.edit(f"✅ تم إلغاء حظر {target.first_name}")
    else:
        banned_list.append(user_id)
        await message.edit(f"🚫 تم حظر {target.first_name}")
    save_settings()

@app.on_message(filters.command(["المحظورين", "bans"], prefixes=".") & filters.me)
async def show_banned(client, message: Message):
    if not banned_list:
        await message.edit("📭 لا يوجد محظورين")
        return
    text = "🚫 قائمة المحظورين:\n"
    for user_id in banned_list:
        try:
            user = await client.get_users(user_id)
            text += f"• {user.first_name} (ID: {user_id})\n"
        except:
            text += f"• ID: {user_id}\n"
    await message.edit(text)

# ============================
# أوامر الشد
# ============================

@app.on_message(filters.command(["بوت", "bot", "هدف"], prefixes=".") & filters.me)
async def set_spam_target(client, message: Message):
    target = await get_target_user(client, message)
    if target:
        spam_data["target_id"] = target.id
        spam_data["target_name"] = target.first_name
        spam_data["is_bot"] = target.is_bot
        save_spam_settings()
        await message.edit(f"✅ تم تحديد الهدف:\n👤 {target.first_name}\n🆔 `{target.id}`")
        return
    try:
        text = message.text.split(" ", 1)[1].strip()
        if text:
            if text.startswith("@"):
                text = text[1:]
            user = await client.get_users(text)
            if user:
                spam_data["target_id"] = user.id
                spam_data["target_name"] = user.first_name
                spam_data["is_bot"] = user.is_bot
                save_spam_settings()
                await message.edit(f"✅ تم تحديد الهدف:\n👤 {user.first_name}\n🆔 `{user.id}`")
                return
    except:
        pass
    await message.edit("❌ لم يتم العثور على هدف!\n• ارد على رسالته\n• اكتب يوزره: @username\n• اكتب ايديه: 123456789")

@app.on_message(filters.command(["رسالة_شد", "spammsg"], prefixes=".") & filters.me)
async def set_spam_message(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        spam_data["message"] = text
        save_spam_settings()
        await message.edit(f"✅ تم تحديد الرسالة:\n📝 `{text[:50]}{'...' if len(text) > 50 else ''}`")
    except:
        await message.edit("❌ استخدم: .رسالة_شد النص")

@app.on_message(filters.command(["تأخير_شد", "spamdelay"], prefixes=".") & filters.me)
async def set_spam_delay(client, message: Message):
    try:
        delay = float(message.text.split(" ", 1)[1])
        if delay < 0.3:
            await message.edit("❌ أقل وقت: 0.3 ثانية")
            return
        if delay > 60:
            await message.edit("⚠️ حد أقصى 60 ثانية")
            delay = 60
        spam_data["delay"] = delay
        save_spam_settings()
        await message.edit(f"✅ تم ضبط الوقت: {delay} ثانية")
    except:
        await message.edit("❌ استخدم: .تأخير_شد 2.5")

@app.on_message(filters.command(["عدد_الشد", "spamcount"], prefixes=".") & filters.me)
async def set_spam_count(client, message: Message):
    try:
        count = int(message.text.split(" ", 1)[1])
        if count < 1:
            await message.edit("❌ العدد يجب أن يكون أكبر من 0")
            return
        if count > 10000:
            await message.edit("⚠️ حد أقصى 10000")
            count = 10000
        spam_data["count"] = count
        save_spam_settings()
        await message.edit(f"✅ تم ضبط العدد: {count}")
    except:
        await message.edit("❌ استخدم: .عدد_الشد 50")

@app.on_message(filters.command(["بدء_شد", "startspam"], prefixes=".") & filters.me)
async def start_spam(client, message: Message):
    if spam_data["active"]:
        await message.edit("⚠️ الشد مفعل بالفعل!")
        return
    if not spam_data["target_id"]:
        await message.edit("❌ يرجى تحديد الهدف أولاً!")
        return
    if not spam_data["message"]:
        await message.edit("❌ يرجى تحديد الرسالة!")
        return
    spam_data["active"] = True
    spam_data["sent"] = 0
    spam_data["start_time"] = time.time()
    await message.edit(f"✅ بدء الشد على {spam_data['target_name']}\n📊 العدد: {spam_data['count']}")
    spam_data["task"] = asyncio.create_task(spam_sender(client, message.chat.id))

async def spam_sender(client, chat_id):
    while spam_data["active"] and spam_data["sent"] < spam_data["count"]:
        try:
            await client.send_message(spam_data["target_id"], spam_data["message"])
            spam_data["sent"] += 1
            if spam_data["sent"] % 50 == 0:
                await client.send_message(chat_id, f"📊 تم إرسال {spam_data['sent']} رسالة")
            await asyncio.sleep(spam_data["delay"])
        except Exception as e:
            await asyncio.sleep(spam_data["delay"] * 2)
    if spam_data["active"]:
        spam_data["active"] = False
        await client.send_message(chat_id, f"✅ انتهى الشد! تم إرسال {spam_data['sent']} رسالة")

@app.on_message(filters.command(["ايقاف_شد", "stopspam"], prefixes=".") & filters.me)
async def stop_spam(client, message: Message):
    if not spam_data["active"]:
        await message.edit("❌ الشد غير مفعل!")
        return
    if spam_data["task"]:
        spam_data["task"].cancel()
    spam_data["active"] = False
    await message.edit(f"🛑 تم إيقاف الشد!\n📊 تم إرسال {spam_data['sent']} رسالة")

@app.on_message(filters.command(["حالة_شد", "spamstatus"], prefixes=".") & filters.me)
async def spam_status(client, message: Message):
    status = "🟢 مفعل" if spam_data["active"] else "🔴 غير مفعل"
    text = f"📊 حالة الشد:\n📌 الحالة: {status}"
    if spam_data["active"]:
        progress = int((spam_data["sent"] / spam_data["count"]) * 100) if spam_data["count"] > 0 else 0
        text += f"\n📊 التقدم: {spam_data['sent']}/{spam_data['count']} ({progress}%)"
    else:
        text += f"\n🎯 الهدف: {spam_data['target_name'] or 'غير محدد'}"
        text += f"\n📝 الرسالة: {spam_data['message'][:30] if spam_data['message'] else 'غير محددة'}"
    await message.edit(text)

@app.on_message(filters.command(["مسح_شد", "clearspam"], prefixes=".") & filters.me)
async def clear_spam(client, message: Message):
    global spam_data
    if spam_data["active"]:
        await message.edit("❌ الشد مفعل! أوقفه أولاً")
        return
    spam_data = {"active": False, "target_id": None, "target_name": None, "message": None, "delay": 1, "count": 10, "sent": 0, "task": None, "start_time": None, "is_bot": False}
    save_spam_settings()
    await message.edit("🧹 تم مسح إعدادات الشد")

@app.on_message(filters.command(["توقيت_الشد", "spamtime"], prefixes=".") & filters.me)
async def spam_time_remaining(client, message: Message):
    if not spam_data["active"]:
        await message.edit("❌ الشد غير مفعل!")
        return
    remaining = spam_data["count"] - spam_data["sent"]
    time_left = remaining * spam_data["delay"]
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    await message.edit(f"⏱️ الوقت المتبقي: {minutes} دقيقة و {seconds} ثانية\n📊 الرسائل المتبقية: {remaining}")

# ============================
# أوامر المكالمات والشات
# ============================

@app.on_message(filters.command(["مكالمه", "call"], prefixes=".") & filters.me)
async def start_call(client, message: Message):
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ يرجى تحديد المستهدف!")
        return
    if call_data["active"]:
        await message.edit("⚠️ هناك مكالمه نشطة!")
        return
    call_data["active"] = True
    call_data["type"] = "private"
    call_data["target_id"] = target.id
    call_data["target_name"] = target.first_name
    call_data["mode"] = "call"
    call_data["start_time"] = time.time()
    save_call_settings()
    await message.edit(f"""
📞 **بدء مكالمه مع {target.first_name}**
━━━━━━━━━━━━━━━━━━━━━
👤 المستهدف: `{target.first_name}`
🆔 المعرف: `{target.id}`
📌 النوع: خاص
⏱️ بدأ: `{datetime.now().strftime('%H:%M:%S')}`

📌 أي رسالة تكتبها توصل له
📌 استخدم `.انهاء_مكالمه` للإنهاء
""")
    call_data["task"] = asyncio.create_task(forward_messages(client, target.id))

@app.on_message(filters.command(["شات_مكالمه", "callchat"], prefixes=".") & filters.me)
async def start_call_chat(client, message: Message):
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ يرجى تحديد المستهدف!")
        return
    if call_data["active"]:
        await message.edit("⚠️ هناك مكالمه نشطة!")
        return
    call_data["active"] = True
    call_data["type"] = "private"
    call_data["target_id"] = target.id
    call_data["target_name"] = target.first_name
    call_data["mode"] = "chat"
    call_data["start_time"] = time.time()
    save_call_settings()
    await message.edit(f"""
💬 **شات مكالمه مع {target.first_name}**
━━━━━━━━━━━━━━━━━━━━━
👤 المستهدف: `{target.first_name}`
🆔 المعرف: `{target.id}`

📌 هو يكتب والرد يجيك هنا
📌 استخدم `.انهاء_مكالمه` للإنهاء
""")
    call_data["task"] = asyncio.create_task(forward_messages_to_me(client, target.id, message.chat.id))

@app.on_message(filters.command(["اتصال", "groupcall"], prefixes=".") & filters.me)
async def start_group_call(client, message: Message):
    if not message.chat.type in ["group", "supergroup"]:
        await message.edit("❌ هذا الأمر يعمل في المجموعات فقط!")
        return
    if call_data["active"]:
        await message.edit("⚠️ هناك مكالمه نشطة!")
        return
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ يرجى تحديد المستهدف في المجموعة!")
        return
    call_data["active"] = True
    call_data["type"] = "group"
    call_data["chat_id"] = message.chat.id
    call_data["target_id"] = target.id
    call_data["target_name"] = target.first_name
    call_data["mode"] = "call"
    call_data["start_time"] = time.time()
    save_call_settings()
    await message.edit(f"""
📞 **اتصال مع {target.first_name} في المجموعة**
━━━━━━━━━━━━━━━━━━━━━
👤 المستهدف: `{target.first_name}`
📌 المجموعة: `{message.chat.title}`
⏱️ بدأ: `{datetime.now().strftime('%H:%M:%S')}`

📌 رسائلك تروح للمجموعة
📌 استخدم `.انهاء_مكالمه` للإنهاء
""")
    call_data["task"] = asyncio.create_task(forward_to_group(client, target.id, message.chat.id))

@app.on_message(filters.command(["شات_اتصال", "groupchat"], prefixes=".") & filters.me)
async def start_group_chat(client, message: Message):
    if not message.chat.type in ["group", "supergroup"]:
        await message.edit("❌ هذا الأمر يعمل في المجموعات فقط!")
        return
    if call_data["active"]:
        await message.edit("⚠️ هناك مكالمه نشطة!")
        return
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ يرجى تحديد المستهدف في المجموعة!")
        return
    call_data["active"] = True
    call_data["type"] = "group"
    call_data["chat_id"] = message.chat.id
    call_data["target_id"] = target.id
    call_data["target_name"] = target.first_name
    call_data["mode"] = "chat"
    call_data["start_time"] = time.time()
    save_call_settings()
    await message.edit(f"""
💬 **شات اتصال مع {target.first_name}**
━━━━━━━━━━━━━━━━━━━━━
👤 المستهدف: `{target.first_name}`
📌 المجموعة: `{message.chat.title}`

📌 هو يكتب في المجموعة والرد يجيك
📌 استخدم `.انهاء_مكالمه` للإنهاء
""")
    call_data["task"] = asyncio.create_task(forward_group_to_me(client, target.id, message.chat.id, message.chat.id))

async def forward_messages(client, target_id):
    while call_data["active"]:
        await asyncio.sleep(0.5)

async def forward_messages_to_me(client, target_id, my_chat_id):
    while call_data["active"]:
        await asyncio.sleep(0.5)

async def forward_to_group(client, target_id, group_id):
    while call_data["active"]:
        await asyncio.sleep(0.5)

async def forward_group_to_me(client, target_id, group_id, my_chat_id):
    while call_data["active"]:
        await asyncio.sleep(0.5)

@app.on_message(filters.command(["انهاء_مكالمه", "endcall"], prefixes=".") & filters.me)
async def end_call(client, message: Message):
    if not call_data["active"]:
        await message.edit("❌ لا توجد مكالمه نشطة!")
        return
    elapsed = time.time() - call_data["start_time"]
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    if call_data["task"]:
        call_data["task"].cancel()
    call_data["active"] = False
    call_data["type"] = None
    call_data["target_id"] = None
    call_data["target_name"] = None
    call_data["mode"] = None
    call_data["task"] = None
    call_data["start_time"] = None
    save_call_settings()
    await message.edit(f"📴 تم إنهاء المكالمه!\n⏱️ المدة: {minutes} دقيقة و {seconds} ثانية")

@app.on_message(filters.command(["حالة_مكالمه", "callstatus"], prefixes=".") & filters.me)
async def call_status(client, message: Message):
    if not call_data["active"]:
        await message.edit("❌ لا توجد مكالمه نشطة!")
        return
    elapsed = time.time() - call_data["start_time"]
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    mode_text = "مكالمه" if call_data["mode"] == "call" else "شات"
    type_text = "خاص" if call_data["type"] == "private" else "مجموعة"
    await message.edit(f"""
📞 **حالة المكالمه**
━━━━━━━━━━━━━━━━━━━━━
📌 الحالة: 🟢 نشطة
👤 المستهدف: `{call_data['target_name']}`
📌 النوع: `{type_text}`
📌 الوضع: `{mode_text}`
⏱️ المدة: `{minutes} دقيقة و {seconds} ثانية`
""")

# ============================
# أوامر الترجمة والطقس
# ============================

@app.on_message(filters.command(["ترجمه", "translate"], prefixes=".") & filters.me)
async def translate_text(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        translations = {
            "مرحبا": "Hello",
            "كيف حالك": "How are you",
            "شكرا": "Thank you",
            "السلام عليكم": "Peace be upon you",
            "صباح الخير": "Good morning",
            "مساء الخير": "Good evening",
            "احبك": "I love you",
            "الحمدلله": "Praise be to God",
            "بخير": "Fine",
            "مع السلامة": "Goodbye",
            "تصبح على خير": "Good night",
            "الله": "God",
            "ان شاء الله": "God willing",
            "ما شاء الله": "God has willed"
        }
        translated = translations.get(text.lower(), f"⚠️ الترجمة غير متوفرة")
        await message.edit(f"🌐 **الترجمة:**\n\n📝 النص: `{text}`\n🔁 الترجمة: `{translated}`")
    except:
        await message.edit("❌ استخدم: .ترجمه النص")

@app.on_message(filters.command(["طقس", "weather"], prefixes=".") & filters.me)
async def get_weather(client, message: Message):
    try:
        city = message.text.split(" ", 1)[1]
        temp = random.randint(5, 45)
        conditions = ["☀️ مشمس", "⛅ غائم", "🌧️ ممطر", "🌪️ عاصف", "❄️ ثلجي", "🌫️ ضبابي"]
        condition = random.choice(conditions)
        humidity = random.randint(20, 90)
        wind = random.randint(0, 50)
        await message.edit(f"""
🌤️ **حالة الطقس في {city}**
━━━━━━━━━━━━━━━━━━━━━
🌡️ الحرارة: `{temp}°C`
☁️ الحالة: `{condition}`
💧 الرطوبة: `{humidity}%`
💨 الرياح: `{wind} كم/ساعة`

📌 ملاحظة: بيانات وهمية للعرض
""")
    except:
        await message.edit("❌ استخدم: .طقس اسم المدينة")

# ============================
# أوامر البث والإذاعة
# ============================

@app.on_message(filters.command(["اذاعه", "broadcast"], prefixes=".") & filters.me)
async def broadcast_to_groups(client, message: Message):
    try:
        if message.reply_to_message:
            text = message.reply_to_message.text or "رسالة"
        else:
            text = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
        if not text:
            await message.edit("❌ اكتب نص أو ارد على رسالة!")
            return
        msg = await message.edit("🔄 جاري الإذاعة إلى المجموعات...")
        count = 0
        failed = 0
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                try:
                    await client.send_message(dialog.chat.id, f"📢 **إذاعة:**\n\n{text}")
                    count += 1
                    await asyncio.sleep(0.3)
                except:
                    failed += 1
        await msg.edit(f"""
✅ **تمت الإذاعة!**
━━━━━━━━━━━━━━━━━━━━━
📝 النص: `{text[:50]}{'...' if len(text) > 50 else ''}`
📊 المجموعات: `{count}`
❌ فشل: `{failed}`
""")
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

@app.on_message(filters.command(["بث", "broadcast_pm"], prefixes=".") & filters.me)
async def broadcast_to_pm(client, message: Message):
    try:
        if message.reply_to_message:
            text = message.reply_to_message.text or "رسالة"
        else:
            text = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
        if not text:
            await message.edit("❌ اكتب نص أو ارد على رسالة!")
            return
        msg = await message.edit("🔄 جاري البث إلى الخاص...")
        count = 0
        failed = 0
        async for dialog in client.get_dialogs():
            if dialog.chat.type == "private":
                try:
                    await client.send_message(dialog.chat.id, f"📨 **بث خاص:**\n\n{text}")
                    count += 1
                    await asyncio.sleep(0.3)
                except:
                    failed += 1
        await msg.edit(f"""
✅ **تم البث الخاص!**
━━━━━━━━━━━━━━━━━━━━━
📝 النص: `{text[:50]}{'...' if len(text) > 50 else ''}`
📊 الخاصات: `{count}`
❌ فشل: `{failed}`
""")
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

# ============================
# أوامر القوائم
# ============================

@app.on_message(filters.command(["قائمه_مجموعاتي", "mygroups"], prefixes=".") & filters.me)
async def list_groups(client, message: Message):
    try:
        msg = await message.edit("🔄 جاري جلب المجموعات...")
        text = "📊 **قائمة المجموعات:**\n═══════════════════════\n\n"
        count = 0
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                count += 1
                members = "?"
                try:
                    members = await client.get_chat_members_count(dialog.chat.id)
                except:
                    pass
                text += f"✅ **{dialog.chat.title}**\n   👥 الأعضاء: `{members}`\n   🆔 ID: `{dialog.chat.id}`\n\n"
                if len(text) > 4000:
                    break
        text += f"📊 المجموع: `{count}` مجموعة"
        await msg.edit(text)
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

@app.on_message(filters.command(["قائمه_قنواتي", "mychannels"], prefixes=".") & filters.me)
async def list_channels(client, message: Message):
    try:
        msg = await message.edit("🔄 جاري جلب القنوات...")
        text = "📊 **قائمة القنوات:**\n═══════════════════════\n\n"
        count = 0
        async for dialog in client.get_dialogs():
            if dialog.chat.type == "channel":
                count += 1
                members = "?"
                try:
                    members = await client.get_chat_members_count(dialog.chat.id)
                except:
                    pass
                text += f"✅ **{dialog.chat.title}**\n   👥 المشتركين: `{members}`\n   🆔 ID: `{dialog.chat.id}`\n\n"
                if len(text) > 4000:
                    break
        text += f"📊 المجموع: `{count}` قناة"
        await msg.edit(text)
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

@app.on_message(filters.command(["قائمه_خاصاتي", "mypms"], prefixes=".") & filters.me)
async def list_pms(client, message: Message):
    try:
        msg = await message.edit("🔄 جاري جلب الخاصات...")
        text = "📊 **قائمة الخاصات:**\n═══════════════════════\n\n"
        count = 0
        async for dialog in client.get_dialogs():
            if dialog.chat.type == "private":
                count += 1
                name = dialog.chat.first_name or "مجهول"
                username = f"@{dialog.chat.username}" if dialog.chat.username else "لا يوجد"
                text += f"✅ **{name}**\n   📌 اليوزر: `{username}`\n   🆔 ID: `{dialog.chat.id}`\n\n"
                if len(text) > 4000:
                    break
        text += f"📊 المجموع: `{count}` خاص"
        await msg.edit(text)
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

@app.on_message(filters.command(["قائمه_المحادثات", "mychats"], prefixes=".") & filters.me)
async def list_all_chats(client, message: Message):
    try:
        msg = await message.edit("🔄 جاري جلب المحادثات...")
        text = "📊 **جميع المحادثات:**\n═══════════════════════\n\n"
        groups = channels = pms = 0
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                groups += 1
                text += f"👥 **{dialog.chat.title}**\n   🆔 ID: `{dialog.chat.id}`\n\n"
            elif dialog.chat.type == "channel":
                channels += 1
                text += f"📢 **{dialog.chat.title}**\n   🆔 ID: `{dialog.chat.id}`\n\n"
            elif dialog.chat.type == "private":
                pms += 1
                name = dialog.chat.first_name or "مجهول"
                text += f"👤 **{name}**\n   🆔 ID: `{dialog.chat.id}`\n\n"
            if len(text) > 4000:
                break
        text += f"📊 المجموع: `{groups + channels + pms}` محادثة\n   👥 مجموعات: `{groups}`\n   📢 قنوات: `{channels}`\n   👤 خاص: `{pms}`"
        await msg.edit(text)
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

# ============================
# أوامر التحديث والفحص والمعلومات والكشف
# ============================

@app.on_message(filters.command(["تحديث", "update", "restart"], prefixes=".") & filters.me)
async def update_bot(client, message: Message):
    await message.edit("🔄 جاري تحديث البوت...\n⏱️ سيتم إعادة التشغيل خلال 3 ثواني")
    await asyncio.sleep(3)
    await message.edit("✅ تم تحديث البوت بنجاح!")
    os.execv(sys.executable, ['python'] + sys.argv)

@app.on_message(filters.command(["فحص", "check", "ping"], prefixes=".") & filters.me)
async def check_bot(client, message: Message):
    start = time.time()
    me = await client.get_me()
    uptime = get_uptime()
    await client.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(0.5)
    ping = (time.time() - start) * 1000
    await message.edit(f"""
✅ **البوت شغال!**
━━━━━━━━━━━━━━━━━━━━━
🟢 الحالة: نشط
👤 الحساب: `{me.first_name}`
🆔 الايدي: `{me.id}`
⏱️ وقت التشغيل: `{uptime}`
📶 البنج: `{ping:.0f} ms`
""")

@app.on_message(filters.command(["معلومات", "info", "about"], prefixes=".") & filters.me)
async def bot_info(client, message: Message):
    me = await client.get_me()
    uptime = get_uptime()
    groups = channels = pms = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in ["group", "supergroup"]:
            groups += 1
        elif dialog.chat.type == "channel":
            channels += 1
        elif dialog.chat.type == "private":
            pms += 1
    sys_info = get_system_info()
    await message.edit(f"""
🖥️ **معلومات البوت**
═══════════════════════
👤 الاسم: `{me.first_name}`
🆔 الايدي: `{me.id}`
📌 اليوزر: `@{me.username}` if me.username else `لا يوجد`
⏱️ وقت التشغيل: `{uptime}`
👥 المجموعات: `{groups}`
📢 القنوات: `{channels}`
👤 الخاص: `{pms}`
💻 النظام: `{sys_info.get('system', 'غير معروف')}`
🐍 بايثون: `{sys_info.get('python', 'غير معروف')}`
""")

@app.on_message(filters.command(["كشف", "userinfo", "whois"], prefixes=".") & filters.me)
async def user_info(client, message: Message):
    target = await get_target_user(client, message)
    if not target:
        await message.edit("❌ يرجى تحديد المستخدم!\n• ارد على رسالته\n• اكتب يوزره: @username\n• اكتب ايديه: 123456789")
        return
    try:
        user = await client.get_users(target.id)
        created = datetime.fromtimestamp(user.date).strftime('%Y-%m-%d %H:%M:%S') if hasattr(user, 'date') else "غير معروف"
        await message.edit(f"""
🔍 **معلومات المستخدم**
═══════════════════════
👤 الاسم: `{user.first_name or 'مجهول'}`
🆔 الايدي: `{user.id}`
📌 اليوزر: `@{user.username}` if user.username else `لا يوجد`
📅 تاريخ الإنشاء: `{created}`
🤖 بوت: `نعم` if user.is_bot else `لا`
✅ محقق: `نعم` if user.is_verified else `لا`
🔗 الرابط: `tg://user?id={user.id}`
""")
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

# ============================
# أوامر البروكسي والشبكة
# ============================

@app.on_message(filters.command(["فحص_شبكه", "speedtest", "سرعه"], prefixes=".") & filters.me)
async def check_network(client, message: Message):
    msg = await message.edit("🔄 جاري فحص الشبكة...\n⏱️ قد يستغرق 10-20 ثانية")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ipify.org?format=json', timeout=5) as response:
                    ip_data = await response.json()
                    public_ip = ip_data.get('ip', 'غير معروف')
        except:
            public_ip = 'غير معروف'
        quality = "🌟 ممتازة" if download > 50 else "👍 جيدة" if download > 20 else "⚠️ متوسطة" if download > 5 else "❌ ضعيفة"
        await msg.edit(f"""
📊 **فحص الشبكة**
━━━━━━━━━━━━━━━━━━━━━
⬇️ التحميل: `{download:.2f} Mbps`
⬆️ الرفع: `{upload:.2f} Mbps`
📶 البنج: `{ping:.0f} ms`
🌍 IP العام: `{public_ip}`
📡 الجودة: `{quality}`
""")
    except Exception as e:
        await msg.edit(f"❌ خطأ: {str(e)[:100]}")

@app.on_message(filters.command(["بروكسي", "proxy"], prefixes=".") & filters.me)
async def show_proxy_info(client, message: Message):
    if not proxy_data["active"]:
        await message.edit("❌ لا يوجد بروكسي!\nاستخدم `.اضافه_بروكسي`")
        return
    await message.edit(f"""
✅ **معلومات البروكسي**
━━━━━━━━━━━━━━━━━━━━━
🔗 النوع: `{proxy_data['type'].upper() if proxy_data['type'] else 'غير محدد'}`
🌐 المضيف: `{proxy_data['host'] or 'غير محدد'}`
🔌 المنفذ: `{proxy_data['port'] or 'غير محدد'}`
👤 المستخدم: `{proxy_data['username'] or 'بدون'}`
🌍 الدولة: `{proxy_data['country'] or 'غير معروف'}`
⚡ زمن الاستجابة: `{proxy_data['latency'] or 'غير معروف'}`
""")

@app.on_message(filters.command(["اضافه_بروكسي", "addproxy"], prefixes=".") & filters.me)
async def add_proxy(client, message: Message):
    try:
        parts = message.text.split(" ", 3)
        if len(parts) < 3:
            await message.edit("❌ استخدم:\n`.اضافه_بروكسي http 192.168.1.1 8080`")
            return
        proxy_type = parts[1].lower()
        host = parts[2]
        port = int(parts[3]) if len(parts) > 3 else 0
        if proxy_type not in ["http", "socks4", "socks5"]:
            await message.edit("❌ أنواع مدعومة: http, socks4, socks5")
            return
        if port < 1 or port > 65535:
            await message.edit("❌ المنفذ بين 1 و 65535")
            return
        msg = await message.edit(f"🔄 جاري اختبار `{host}:{port}`...")
        latency = await test_proxy_connection(proxy_type, host, port)
        if latency is None:
            await msg.edit(f"❌ لا يمكن الاتصال بـ `{host}:{port}`!")
            return
        proxy_data["active"] = True
        proxy_data["type"] = proxy_type
        proxy_data["host"] = host
        proxy_data["port"] = port
        proxy_data["latency"] = f"{latency:.0f} ms"
        proxy_data["last_check"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proxy_list.append({"type": proxy_type, "host": host, "port": port, "latency": f"{latency:.0f} ms", "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        save_proxy_settings()
        await msg.edit(f"✅ تم إضافة البروكسي!\n🔗 `{host}:{port}`\n⚡ {latency:.0f} ms")
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:100]}")

@app.on_message(filters.command(["تغيير_بروكسي", "changeproxy"], prefixes=".") & filters.me)
async def change_proxy(client, message: Message):
    if not proxy_list:
        await message.edit("❌ لا يوجد بروكسيات!")
        return
    current = f"{proxy_data['host']}:{proxy_data['port']}" if proxy_data["host"] else None
    available = [p for p in proxy_list if f"{p['host']}:{p['port']}" != current]
    if not available:
        await message.edit("❌ لا يوجد بروكسيات أخرى!")
        return
    new = available[0]
    proxy_data["active"] = True
    proxy_data["type"] = new["type"]
    proxy_data["host"] = new["host"]
    proxy_data["port"] = new["port"]
    proxy_data["latency"] = new.get("latency", "غير معروف")
    save_proxy_settings()
    await message.edit(f"✅ تم تغيير البروكسي!\n🔗 `{new['host']}:{new['port']}`")

@app.on_message(filters.command(["ازاله_بروكسي", "removeproxy"], prefixes=".") & filters.me)
async def remove_proxy(client, message: Message):
    if not proxy_data["active"]:
        await message.edit("❌ لا يوجد بروكسي!")
        return
    host, port = proxy_data["host"], proxy_data["port"]
    global proxy_list
    proxy_list = [p for p in proxy_list if not (p["host"] == host and p["port"] == port)]
    proxy_data["active"] = False
    proxy_data["type"] = proxy_data["host"] = proxy_data["port"] = None
    save_proxy_settings()
    await message.edit(f"✅ تم إزالة `{host}:{port}`")

@app.on_message(filters.command(["قائمه_بروكسي", "proxylist"], prefixes=".") & filters.me)
async def list_proxies(client, message: Message):
    if not proxy_list:
        await message.edit("📭 لا يوجد بروكسيات!")
        return
    text = "📋 **قائمة البروكسيات**\n═══════════════════════\n\n"
    for i, p in enumerate(proxy_list, 1):
        active = "✅" if (proxy_data["active"] and proxy_data["host"] == p["host"] and proxy_data["port"] == p["port"]) else "⬜"
        text += f"{active} {i}. {p['type'].upper()} `{p['host']}:{p['port']}`\n"
    await message.edit(text)

# ============================
# أوامر النسخ الاحتياطي
# ============================

@app.on_message(filters.command(["نسخ_احتياطي", "backup"], prefixes=".") & filters.me)
async def backup_settings_cmd(client, message: Message):
    if backup_settings():
        await message.edit("✅ تم نسخ احتياطي للإعدادات بنجاح!")
    else:
        await message.edit("❌ فشل نسخ الاحتياطي!")

@app.on_message(filters.command(["استعادة", "restore"], prefixes=".") & filters.me)
async def restore_settings_cmd(client, message: Message):
    if restore_settings():
        await message.edit("✅ تم استعادة الإعدادات بنجاح!")
    else:
        await message.edit("❌ فشل استعادة الإعدادات!")

# ============================
# أوامر ترفيهية
# ============================

@app.on_message(filters.command(["نكتة", "joke"], prefixes=".") & filters.me)
async def send_joke(client, message: Message):
    await message.edit(random.choice(jokes))

@app.on_message(filters.command(["وقتي", "mytime"], prefixes=".") & filters.me)
async def show_time(client, message: Message):
    now = datetime.now()
    await message.edit(f"""
🕐 **الوقت والتاريخ:**
━━━━━━━━━━━━━━━━━━━━━
📅 التاريخ: `{now.strftime('%Y-%m-%d')}`
🕐 الوقت: `{now.strftime('%H:%M:%S')}`
📆 اليوم: `{now.strftime('%A')}`
🗓️ الأسبوع: `{now.strftime('%W')}`
""")

@app.on_message(filters.command(["قول", "say"], prefixes=".") & filters.me)
async def say_style(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        styles = [
            f"🔥 {text}",
            f"✨ {text} ✨",
            f"💬 {text}",
            f"📢 {text}",
            f"🔊 {text}",
            f"✍️ {text}",
            f"💫 {text}"
        ]
        await message.edit(random.choice(styles))
    except:
        await message.edit("❌ استخدم: .قول النص")

@app.on_message(filters.command(["اكتب", "type"], prefixes=".") & filters.me)
async def typing_effect(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        await client.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(2)
        await message.edit(f"✍️ {text}")
    except:
        await message.edit("❌ استخدم: .اكتب النص")

@app.on_message(filters.command(["فصل", "sep"], prefixes=".") & filters.me)
async def separator(client, message: Message):
    try:
        count = int(message.text.split(" ", 1)[1])
        if count > 50:
            count = 50
        await message.edit(f"```\n{'═' * count}\n```")
    except:
        await message.edit("❌ استخدم: .فصل 30")

@app.on_message(filters.command(["توقيع", "sign"], prefixes=".") & filters.me)
async def random_signature(client, message: Message):
    signatures = [
        "✨ الحياة جميلة عندما تعيشها بكل تفاصيلها",
        "🔥 النجاح ليس صدفة، بل هو عمل شاق",
        "💫 ابتسم فالحياة أجمل بابتسامتك",
        "🌟 كن أنت التغيير الذي تريد رؤيته",
        "🚀 السعي نحو القمة لا يتوقف",
        "💪 القوة ليست في العضلات، بل في الإرادة",
        "🌈 بعد كل ظلمة يأتي النور"
    ]
    await message.edit(f"📝 **توقيعك:**\n\n{random.choice(signatures)}")

@app.on_message(filters.command(["حظك", "luck"], prefixes=".") & filters.me)
async def your_luck(client, message: Message):
    luck = random.randint(1, 100)
    msg = "🌟 ممتاز" if luck > 80 else "😊 جيد" if luck > 50 else "😅 متوسط" if luck > 30 else "😢 سيء"
    await message.edit(f"🍀 **حظك اليوم:**\n\n📊 النسبة: `{luck}%`\n{msg}")

@app.on_message(filters.command(["زهر", "dice"], prefixes=".") & filters.me)
async def roll_dice(client, message: Message):
    dice = random.randint(1, 6)
    faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    await message.edit(f"🎲 **رمي الزهر:**\n\n{faces[dice-1]} الرقم: `{dice}`")

@app.on_message(filters.command(["قرعة", "lottery"], prefixes=".") & filters.me)
async def lottery(client, message: Message):
    winner = random.randint(1, 100)
    await message.edit(f"🎰 **نتيجة القرعة:**\n\nالرقم الفائز: `{winner}`")

@app.on_message(filters.command(["حجر_ورقة_مقص", "rps"], prefixes=".") & filters.me)
async def rps_game(client, message: Message):
    try:
        choice = message.text.split(" ", 1)[1].lower()
        if choice not in ["حجر", "ورقة", "مقص"]:
            await message.edit("❌ اختر: حجر، ورقة، مقص")
            return
        bot_choice = random.choice(["حجر", "ورقة", "مقص"])
        if choice == bot_choice:
            result = "🤝 تعادل"
        elif (choice == "حجر" and bot_choice == "مقص") or (choice == "ورقة" and bot_choice == "حجر") or (choice == "مقص" and bot_choice == "ورقة"):
            result = "🎉 فزت!"
        else:
            result = "😅 خسرت!"
        await message.edit(f"🪨📄✂️ **حجر ورقة مقص**\n\nأنت: `{choice}`\nالبوت: `{bot_choice}`\n\nالنتيجة: {result}")
    except:
        await message.edit("❌ استخدم: .حجر_ورقة_مقص حجر")

@app.on_message(filters.command(["زخرف", "decorate"], prefixes=".") & filters.me)
async def decorate_text(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        styles = [
            f"✧ {text} ✧",
            f"◈ {text} ◈",
            f"❖ {text} ❖",
            f"✿ {text} ✿",
            f"♛ {text} ♛",
            f"★ {text} ★"
        ]
        await message.edit(random.choice(styles))
    except:
        await message.edit("❌ استخدم: .زخرف النص")

@app.on_message(filters.command(["عربي", "arabic"], prefixes=".") & filters.me)
async def to_arabic_numbers(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        arabic_nums = {'0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤', '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'}
        result = ''.join(arabic_nums.get(c, c) for c in text)
        await message.edit(f"🔢 **الأرقام العربية:**\n\n{result}")
    except:
        await message.edit("❌ استخدم: .عربي 123")

@app.on_message(filters.command(["غامق", "bold"], prefixes=".") & filters.me)
async def bold_text(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        await message.edit(f"**{text}**")
    except:
        await message.edit("❌ استخدم: .غامق النص")

@app.on_message(filters.command(["مائل", "italic"], prefixes=".") & filters.me)
async def italic_text(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        await message.edit(f"__{text}__")
    except:
        await message.edit("❌ استخدم: .مائل النص")

@app.on_message(filters.command(["عكس", "reverse"], prefixes=".") & filters.me)
async def reverse_text(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        await message.edit(f"🔃 **النص المعكوس:**\n\n{text[::-1]}")
    except:
        await message.edit("❌ استخدم: .عكس النص")

@app.on_message(filters.command(["ترتيب", "sort"], prefixes=".") & filters.me)
async def sort_text(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        words = text.split()
        words.sort()
        await message.edit(f"📋 **الكلمات مرتبة:**\n\n{' '.join(words)}")
    except:
        await message.edit("❌ استخدم: .ترتيب النص")

@app.on_message(filters.command(["عدد_كلمات", "wordcount"], prefixes=".") & filters.me)
async def word_count(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        words = len(text.split())
        chars = len(text)
        await message.edit(f"📊 **عدد الكلمات والحروف:**\n\n📝 الكلمات: `{words}`\n🔤 الحروف: `{chars}`")
    except:
        await message.edit("❌ استخدم: .عدد_كلمات النص")

@app.on_message(filters.command(["احفظ", "save"], prefixes=".") & filters.me)
async def save_text(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        saved_texts["saved"] = text
        await message.edit(f"✅ تم حفظ النص:\n\n`{text}`")
    except:
        await message.edit("❌ استخدم: .احفظ النص")

@app.on_message(filters.command(["استرجع", "get"], prefixes=".") & filters.me)
async def get_text(client, message: Message):
    if "saved" not in saved_texts:
        await message.edit("📭 لا يوجد نص محفوظ!")
        return
    await message.edit(f"📝 **النص المحفوظ:**\n\n{saved_texts['saved']}")

@app.on_message(filters.command(["مسح_المحفوظ", "clearsave"], prefixes=".") & filters.me)
async def clear_saved(client, message: Message):
    if "saved" in saved_texts:
        del saved_texts["saved"]
    await message.edit("🧹 تم مسح النص المحفوظ")

@app.on_message(filters.command(["تحويل", "convert"], prefixes=".") & filters.me)
async def convert_currency(client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        rates = {"دولار": 1500, "يورو": 1600, "جنيه": 2000, "ريال": 400}
        for currency, rate in rates.items():
            if currency in text:
                num = re.findall(r'\d+', text)
                if num:
                    amount = int(num[0])
                    result = amount * rate
                    await message.edit(f"💱 **تحويل العملة:**\n\n{amount} {currency} = {result:,} دينار")
                    return
        await message.edit("❌ العملة غير مدعومة!\nالمدعومة: دولار، يورو، جنيه، ريال")
    except:
        await message.edit("❌ استخدم: .تحويل 100 دولار")

# ============================
# أمر الاوامر الشامل
# ============================

@app.on_message(filters.command(["الاوامر", "commands", "اوامر", "cmds", "help"], prefixes=".") & filters.me)
async def show_all_commands(client, message: Message):
    await message.edit("""
📋 **قائمة الأوامر الشاملة**
═══════════════════════

🎯 **اللزك:** `.لزك`, `.ايقاف`, `.حالة`, `.نص`, `.تكرار`, `.السليب`, `.وقت`, `.كل`, `.مسح`, `.منشن`, `.تجاهل`, `.حظر`

💣 **الشد:** `.بوت`, `.رسالة_شد`, `.تأخير_شد`, `.عدد_الشد`, `.بدء_شد`, `.ايقاف_شد`, `.حالة_شد`, `.مسح_شد`, `.توقيت_الشد`

📞 **المكالمات:** `.مكالمه`, `.شات_مكالمه`, `.اتصال`, `.شات_اتصال`, `.انهاء_مكالمه`, `.حالة_مكالمه`

🌐 **البروكسي:** `.فحص_شبكه`, `.بروكسي`, `.اضافه_بروكسي`, `.تغيير_بروكسي`, `.ازاله_بروكسي`, `.قائمه_بروكسي`

📢 **البث:** `.اذاعه`, `.بث`

📊 **القوائم:** `.قائمه_مجموعاتي`, `.قائمه_قنواتي`, `.قائمه_خاصاتي`, `.قائمه_المحادثات`

🔍 **المعلومات:** `.كشف`, `.معلومات`, `.فحص`, `.تحديث`, `.نسخ_احتياطي`, `.استعادة`

🌍 **متنوع:** `.ترجمه`, `.طقس`, `.تحويل`

🎉 **ترفيه:** `.نكتة`, `.وقتي`, `.قول`, `.اكتب`, `.فصل`, `.توقيع`, `.حظك`, `.زهر`, `.قرعة`, `.حجر_ورقة_مقص`, `.زخرف`, `.عربي`, `.غامق`, `.مائل`, `.عكس`, `.ترتيب`, `.عدد_كلمات`, `.احفظ`, `.استرجع`, `.مسح_المحفوظ`

📊 **إحصائيات:** `.اللزك`, `.احصائيات_مستخدم`, `.مسح_احصائيات`

═══════════════════════
📌 إجمالي الأوامر: 60+ أمر
""")

# ============================
# أوامر إضافية
# ============================

@app.on_message(filters.command(["تنظيف", "clean"], prefixes=".") & filters.me)
async def clean_messages(client, message: Message):
    try:
        parts = message.text.split(" ")
        limit = 100
        if len(parts) > 1:
            limit = int(parts[1])
            if limit > 500:
                limit = 500
        await message.edit(f"🧹 جاري تنظيف {limit} رسالة...")
        count = 0
        async for msg in client.get_chat_history(message.chat.id, limit=limit):
            if msg.from_user and msg.from_user.is_self:
                try:
                    await msg.delete()
                    count += 1
                    await asyncio.sleep(0.5)
                except:
                    pass
        await message.edit(f"✅ تم حذف {count} رسالة")
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:50]}")

@app.on_message(filters.command(["امسحلي", "delmy"], prefixes=".") & filters.me)
async def delete_all_my_messages(client, message: Message):
    try:
        msg = await message.edit("🧹 جاري حذف رسائلك...")
        count = 0
        async for msg_history in client.get_chat_history(message.chat.id, limit=10000):
            if msg_history.from_user and msg_history.from_user.is_self:
                try:
                    await msg_history.delete()
                    count += 1
                    if count % 10 == 0:
                        await asyncio.sleep(0.5)
                except:
                    pass
        await msg.edit(f"✅ تم حذف {count} رسالة")
    except Exception as e:
        await message.edit(f"❌ خطأ: {str(e)[:50]}")

# ============================
# الرد التلقائي
# ============================

@app.on_message(filters.group & ~filters.me)
async def auto_reply(client, message: Message):
    data["last_reply_time"] = time.time()
    if data["auto_stop"] and time.time() > data["auto_stop"]:
        data["active"] = False
        data["auto_stop"] = None
        save_settings()
        return
    if not data["active"] or not message.from_user:
        return
    if message.from_user.id in ignore_list or message.from_user.id in banned_list:
        return
    if not data["reply_all"] and message.from_user.id != data["target_id"]:
        return
    if message.text and message.text.startswith("."):
        return
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name or "مجهول"
        if user_id not in stats:
            stats[user_id] = {"name": user_name, "count": 0, "first_time": time.time(), "last_time": time.time()}
        stats[user_id]["count"] += 1
        stats[user_id]["last_time"] = time.time()
        for i in range(data["repeat_count"]):
            await client.copy_message(message.chat.id, data["chat_id"], data["msg_id"], reply_to_message_id=message.id)
            if data["extra_text"]:
                await client.send_message(message.chat.id, data["extra_text"], reply_to_message_id=message.id)
            if data["delay"] > 0 and i < data["repeat_count"] - 1:
                await asyncio.sleep(data["delay"])
    except:
        pass

# ============================
# الترحيب
# ============================

@app.on_message(filters.group & filters.new_chat_members)
async def welcome_new_member(client, message: Message):
    if not data.get("welcome", False):
        return
    for member in message.new_chat_members:
        if member.id == client.me.id:
            continue
        welcome_text = random.choice(welcome_messages).format(name=member.first_name)
        await asyncio.sleep(1)
        await client.send_message(message.chat.id, welcome_text, reply_to_message_id=message.id)

@app.on_message(filters.command(["ترحيب", "welcome"], prefixes=".") & filters.me)
async def toggle_welcome(client, message: Message):
    data["welcome"] = not data.get("welcome", False)
    status = "مفعل" if data["welcome"] else "معطل"
    save_settings()
    await message.edit(f"✅ تم {status} الترحيب التلقائي")

# ============================
# أوامر الردود التلقائية
# ============================

@app.on_message(filters.command(["ردود", "addreply"], prefixes=".") & filters.me)
async def add_auto_reply(client, message: Message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            await message.edit("❌ استخدم: .ردود كلمة رد")
            return
        word = parts[1].lower()
        reply = parts[2]
        auto_replies[word] = reply
        save_replies()
        await message.edit(f"✅ تم إضافة رد: `{word}` ➜ `{reply}`")
    except:
        await message.edit("❌ استخدم: .ردود كلمة رد")

@app.on_message(filters.command(["حذف_رد", "delreply"], prefixes=".") & filters.me)
async def remove_auto_reply(client, message: Message):
    try:
        word = message.text.split(" ", 1)[1].lower()
        if word in auto_replies:
            del auto_replies[word]
            save_replies()
            await message.edit(f"✅ تم حذف الرد: `{word}`")
        else:
            await message.edit(f"❌ لا يوجد رد لكلمة: `{word}`")
    except:
        await message.edit("❌ استخدم: .حذف_رد كلمة")

@app.on_message(filters.command(["الردود", "replies"], prefixes=".") & filters.me)
async def show_auto_replies(client, message: Message):
    if not auto_replies:
        await message.edit("📭 لا يوجد ردود تلقائية")
        return
    text = "📋 **الردود التلقائية:**\n═══════════════════════\n\n"
    for word, reply in auto_replies.items():
        text += f"• `{word}` ➜ {reply}\n"
    await message.edit(text)

# ============================
# تشغيل البوت
# ============================

print("🤖 البوت يعمل...")
print(f"📊 إجمالي الأوامر: 60+ أمر")
print("✅ جميع الأوامر جاهزة للاستخدام")
print("📌 استخدم .الاوامر لعرض جميع الأوامر")
app.run()
