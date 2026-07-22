import os
import time
import smtplib
import json
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import telebot
from telebot import types

# ========== الاعدادات ==========
TOKEN = "8681754016:AAG2G-e2yBWfJiZZkixgWuqSrR7dox6jFMc"
ADMIN_ID = [67769767, 8506670849, 7923156864]

# ========== الثوابت ==========
USERS_FILE = "allowed_users.json"
DATA_FILE = "user_data_backup.json"

# ========== تهيئة البوت ==========
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ========== دوال مساعدة ==========
def load_json_file(filepath: str, default=None):
    if default is None:
        default = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if data else default
    except (json.JSONDecodeError, IOError) as e:
        print(f"خطأ في تحميل {filepath}: {e}")
    return default

def save_json_file(filepath: str, data) -> bool:
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"خطأ في حفظ {filepath}: {e}")
        return False

# ========== إدارة بيانات الإيميلات (ملف منفصل) ==========
def get_sender_file(user_id) -> str:
    return f"emi_{user_id}.txt"

def load_sender_emails(user_id) -> Dict[str, str]:
    """تحميل الإيميلات مع كلمات المرور من الملف النصي الخاص بالمستخدم"""
    filepath = get_sender_file(user_id)
    emails = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    parts = line.split(':', 1)
                    email = parts[0].strip()
                    pwd = parts[1].strip()
                    if email and pwd:
                        emails[email] = pwd
    return emails

def save_sender_emails(user_id, emails_dict: Dict[str, str]):
    """حفظ جميع الإيميلات في الملف النصي"""
    filepath = get_sender_file(user_id)
    with open(filepath, 'w', encoding='utf-8') as f:
        for email, pwd in emails_dict.items():
            f.write(f"{email}:{pwd}\n")

# ========== إدارة البيانات الأخرى ==========
ALLOWED_USERS = load_json_file(USERS_FILE, [])

def load_user_data() -> dict:
    return load_json_file(DATA_FILE, {})

def save_user_data(data: dict):
    save_json_file(DATA_FILE, data)

user_data = load_user_data()
user_state: Dict[int, Optional[str]] = {}
stop_sending: Dict[int, bool] = {}
pause_sending: Dict[int, bool] = {}

# ========== دوال الإيميل ==========
def send_single_email(sender_email: str, app_password: str, support_emails: List[str],
                      subject: str, body: str, format_type: str = "plain") -> Tuple[bool, str]:
    """إرسال بريد إلكتروني لكل عنوان على حدى بدون تجميعهم في رسالة واحدة"""
    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
            server.starttls()
            server.login(sender_email, app_password)

            for recipient in support_emails:
                recipient = recipient.strip()
                if not recipient:
                    continue

                msg = MIMEMultipart('alternative')
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg['Message-ID'] = f"<{uuid.uuid4()}@gmail.com>"
                msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

                if format_type == "html":
                    msg.attach(MIMEText(body, 'html', 'utf-8'))
                else:
                    msg.attach(MIMEText(body, 'plain', 'utf-8'))

                server.sendmail(sender_email, recipient, msg.as_string())
                del msg

        return True, "تم الإرسال"
    except smtplib.SMTPAuthenticationError:
        return False, "فشل المصادقة"
    except smtplib.SMTPServerDisconnected:
        return False, "انقطع الاتصال"
    except smtplib.SMTPException as e:
        return False, f"خطأ: {str(e)[:100]}"
    except Exception as e:
        return False, f"خطأ غير متوقع: {str(e)[:100]}"

# ========== دوال القائمة ==========
def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("ايميل الدعم", callback_data='set_support')
    btn2 = types.InlineKeyboardButton("اضافة ايميل", callback_data='set_sender')
    btn3 = types.InlineKeyboardButton("عرض الايميلات", callback_data='show_emails')
    btn4 = types.InlineKeyboardButton("الموضوع", callback_data='set_subject')
    btn5 = types.InlineKeyboardButton("الكليشة", callback_data='set_body')
    btn6 = types.InlineKeyboardButton("نوع التنسيق", callback_data='set_format')
    btn7 = types.InlineKeyboardButton("الثواني", callback_data='set_interval')
    btn8 = types.InlineKeyboardButton("عدد الرسايل", callback_data='set_max')
    btn9 = types.InlineKeyboardButton("بدء الارسال", callback_data='start_send')
    btn10 = types.InlineKeyboardButton("المعلومات", callback_data='show_info')
    btn11 = types.InlineKeyboardButton("مسح الكل", callback_data='clear_all')
    btn12 = types.InlineKeyboardButton("قناة البوت", url='https://t.me/Quran_Yotla')
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
    return keyboard

def show_main_menu(chat_id, message_id=None, text="القائمة الرئيسية\nاختر العملية المطلوبة:"):
    keyboard = get_main_keyboard()
    if message_id:
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text=text, reply_markup=keyboard)
        except Exception:
            bot.send_message(chat_id, text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, text, reply_markup=keyboard)

# ========== أوامر البوت ==========
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USERS:
        ALLOWED_USERS.append(user_id)
        save_json_file(USERS_FILE, ALLOWED_USERS)

    show_main_menu(message.chat.id, None, "بوت الشد الخارجي\nاضبط الاعدادات من الأزرار:")

# ========== معالج الأزرار ==========
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_id = call.from_user.id
    data = call.data

    user_state.pop(user_id, None)

    if data == 'set_support':
        msg = bot.edit_message_text(
            "📧 أدخل ايميل الدعم:\n\n"
            "اذا ايميل واحد:\n"
            "stopCA@telegram.org\n\n"
            "اذا عدة ايميلات:\n"
            "abuse@telegram.org\n"
            "support@telegram.org",
            chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(msg, process_support)

    elif data == 'set_sender':
        msg = bot.edit_message_text(
            "➕ أدخل ايميلات الشد مع كلمة مرور التطبيقات:\n\n"
            "example@gmail.com:xxxx xxxx xxxx xxxx\n\n"
            "يمكنك اضافة أكثر من ايميل بوضع كل ايميل في سطر.\n"
            "سيتم اضافة الجديد والاحتفاظ بالقديم، تحديث كلمة المرور لو تكرر الايميل.",
            chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(msg, process_sender)

    elif data == 'show_emails':
        sender_emails = load_sender_emails(user_id)
        if sender_emails:
            display = '\n'.join([f"📨 {email}" for email in sender_emails.keys()])
        else:
            display = "لا يوجد ايميلات مضافة"
        bot.edit_message_text(f"📋 الايميلات المسجلة:\n{display}",
                              chat_id=chat_id, message_id=message_id)
        time.sleep(2)
        show_main_menu(chat_id, message_id)

    elif data == 'show_info':
        data_dict = user_data.get(str(user_id), {})
        support_emails = '\n'.join(data_dict.get('support', [])) if data_dict.get('support') else "لم يتم الإدخال"
        sender_dict = load_sender_emails(user_id)
        sender_count = len(sender_dict)
        sender_display = f"{sender_count} ايميل" if sender_count else "لم يتم الإدخال"
        subject = data_dict.get('subject', 'لم يتم الإدخال')
        body = data_dict.get('body', 'لم يتم الإدخال')
        if body != 'لم يتم الإدخال':
            body = body[:100] + "..." if len(body) > 100 else body
        interval = data_dict.get('interval', '5 (افتراضي)')
        max_msg = data_dict.get('max_msg', '50 (افتراضي)')
        format_type = data_dict.get('format', 'plain')

        info_text = f"""
ℹ️ المعلومات المدخلة:

📧 ايميل الدعم:
{support_emails}

➕ ايميلات الشد:
{sender_display}

📝 الموضوع:
{subject}

💬 الكليشة:
{body}

📄 نوع التنسيق: {format_type}
⏱️ الفاصل الزمني: {interval}
🔢 عدد الرسايل: {max_msg}
"""
        bot.edit_message_text(info_text, chat_id=chat_id, message_id=message_id)
        time.sleep(3)
        show_main_menu(chat_id, message_id)

    elif data == 'set_subject':
        msg = bot.edit_message_text("📝 أدخل موضوع الرسالة:",
                                    chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(msg, process_subject)

    elif data == 'set_body':
        msg = bot.edit_message_text(
            "💬 أدخل الكليشة أو محتوى الرسالة:\n\n"
            "يمكنك استخدام تنسيق HTML:\n"
            "<b>نص عريض</b>\n"
            "<i>نص مائل</i>\n"
            "<u>نص مسطر</u>\n"
            "<a href='https://example.com'>رابط</a>",
            chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(msg, process_body)

    elif data == 'set_format':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("📄 نص عادي", callback_data='format_plain'),
            types.InlineKeyboardButton("🌐 HTML", callback_data='format_html')
        )
        bot.edit_message_text("📄 اختر نوع تنسيق الرسالة:",
                              chat_id=chat_id, message_id=message_id,
                              reply_markup=keyboard)

    elif data in ['format_plain', 'format_html']:
        format_type = 'plain' if data == 'format_plain' else 'html'
        if str(user_id) not in user_data:
            user_data[str(user_id)] = {}
        user_data[str(user_id)]['format'] = format_type
        save_user_data(user_data)
        bot.edit_message_text(f"✅ تم تحديد نوع التنسيق: {format_type}",
                              chat_id=chat_id, message_id=message_id)
        time.sleep(1)
        show_main_menu(chat_id, message_id)

    elif data == 'set_interval':
        msg = bot.edit_message_text("⏱️ أدخل عدد الثواني بين كل رسالة (1-60):",
                                    chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(msg, process_interval)

    elif data == 'set_max':
        msg = bot.edit_message_text("🔢 أدخل عدد الرسائل لكل ايميل (1-1000):",
                                    chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(msg, process_max)

    elif data == 'clear_all':
        if str(user_id) in user_data:
            del user_data[str(user_id)]
            save_user_data(user_data)
        filepath = get_sender_file(user_id)
        if os.path.exists(filepath):
            os.remove(filepath)
        bot.edit_message_text("🗑️ تم مسح كل المعلومات بما فيها الإيميلات.",
                              chat_id=chat_id, message_id=message_id)
        time.sleep(1)
        show_main_menu(chat_id, message_id)

    elif data == 'start_send':
        start_sending_process(call)

    elif data == 'stop_sending':
        user_id = call.from_user.id
        stop_sending[user_id] = True
        bot.edit_message_text("⏹️ جاري ايقاف عملية الارسال...",
                              chat_id=chat_id, message_id=message_id)

    elif data == 'pause_sending':
        user_id = call.from_user.id
        pause_sending[user_id] = True
        bot.edit_message_text("⏸️ تم الايقاف المؤقت. اضغط على استكمال للمتابعة.",
                              chat_id=chat_id, message_id=message_id)

    elif data == 'resume_sending':
        user_id = call.from_user.id
        pause_sending[user_id] = False
        bot.edit_message_text("▶️ جاري استكمال عملية الارسال...",
                              chat_id=chat_id, message_id=message_id)

    else:
        show_main_menu(chat_id, message_id)

# ========== دوال معالجة الإدخالات ==========
def process_support(message):
    user_id = message.from_user.id
    text = message.text.strip()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {}
    user_data[str(user_id)]['support'] = [e.strip() for e in text.split('\n') if e.strip()]
    save_user_data(user_data)
    count = len(user_data[str(user_id)]['support'])
    bot.send_message(message.chat.id, f"✅ تم تسجيل {count} ايميل دعم.")
    time.sleep(1)
    show_main_menu(message.chat.id)

def process_sender(message):
    user_id = message.from_user.id
    text = message.text.strip()
    current_emails = load_sender_emails(user_id)

    added = 0
    updated = 0
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if ':' in line:
            parts = line.split(':', 1)
            email = parts[0].strip()
            pwd = parts[1].strip()
            if email and pwd:
                if email in current_emails:
                    updated += 1
                else:
                    added += 1
                current_emails[email] = pwd

    save_sender_emails(user_id, current_emails)

    msg = f"✅ تمت معالجة الإيميلات:\n"
    if added:
        msg += f"➕ تم اضافة {added} ايميل جديد.\n"
    if updated:
        msg += f"🔄 تم تحديث كلمة مرور {updated} ايميل موجود.\n"
    if not added and not updated:
        msg += "❌ لم يتم العثور على إيميلات صالحة (تأكد من الصيغة)."

    bot.send_message(message.chat.id, msg)
    time.sleep(1)
    show_main_menu(message.chat.id)

def process_subject(message):
    user_id = message.from_user.id
    text = message.text.strip()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {}
    user_data[str(user_id)]['subject'] = text
    save_user_data(user_data)
    bot.send_message(message.chat.id, "✅ تم حفظ الموضوع.")
    time.sleep(1)
    show_main_menu(message.chat.id)

def process_body(message):
    user_id = message.from_user.id
    text = message.text.strip()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {}
    user_data[str(user_id)]['body'] = text
    save_user_data(user_data)
    bot.send_message(message.chat.id, f"✅ تم حفظ الكليشة ({len(text)} حرف).")
    time.sleep(1)
    show_main_menu(message.chat.id)

def process_interval(message):
    user_id = message.from_user.id
    text = message.text.strip()
    if text.isdigit() and 1 <= int(text) <= 60:
        if str(user_id) not in user_data:
            user_data[str(user_id)] = {}
        user_data[str(user_id)]['interval'] = text
        save_user_data(user_data)
        bot.send_message(message.chat.id, f"✅ تم ضبط الفاصل: {text} ثانية.")
        time.sleep(1)
        show_main_menu(message.chat.id)
    else:
        msg = bot.send_message(message.chat.id, "❌ أدخل رقم صحيح بين 1 و 60.")
        bot.register_next_step_handler(msg, process_interval)

def process_max(message):
    user_id = message.from_user.id
    text = message.text.strip()
    if text.isdigit() and 1 <= int(text) <= 1000:
        if str(user_id) not in user_data:
            user_data[str(user_id)] = {}
        user_data[str(user_id)]['max_msg'] = text
        save_user_data(user_data)
        bot.send_message(message.chat.id, f"✅ تم تحديد {text} رسالة لكل ايميل.")
        time.sleep(1)
        show_main_menu(message.chat.id)
    else:
        msg = bot.send_message(message.chat.id, "❌ أدخل رقم صحيح بين 1 و 1000.")
        bot.register_next_step_handler(msg, process_max)

# ========== عملية الارسال ==========
def start_sending_process(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_id = call.from_user.id

    data = user_data.get(str(user_id), {})

    support_list = data.get('support', [])
    subject = data.get('subject', '')
    body = data.get('body', '')
    interval = int(data.get('interval', 5))
    max_per_sender = int(data.get('max_msg', 50))
    format_type = data.get('format', 'plain')

    sender_dict = load_sender_emails(user_id)

    if not all([support_list, sender_dict, subject, body]):
        missing = []
        if not support_list: missing.append("ايميل الدعم")
        if not sender_dict: missing.append("ايميلات الشد")
        if not subject: missing.append("الموضوع")
        if not body: missing.append("الكليشة")

        bot.edit_message_text(
            "❌ بيانات ناقصة:\n" +
            "\n".join([f"• {item}" for item in missing]) +
            "\n\n⚠️ أكمل جميع الحقول أولاً.",
            chat_id=chat_id, message_id=message_id)
        time.sleep(2)
        show_main_menu(chat_id, message_id)
        return

    senders = [(email, pwd) for email, pwd in sender_dict.items()]

    if not senders:
        bot.edit_message_text("❌ لا توجد ايميلات صالحة للإرسال.",
                              chat_id=chat_id, message_id=message_id)
        time.sleep(2)
        return

    stop_sending[user_id] = False
    pause_sending[user_id] = False

    bot.edit_message_text("🚀 بدء تنفيذ عملية الشد...",
                          chat_id=chat_id, message_id=message_id)

    total_stats = {
        'total_sent': 0,
        'total_failed': 0,
        'auth_failed': 0,
        'blocked': 0,
        'completed_senders': 0,
        'sender_details': {}
    }

    start_time = datetime.now()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("ايقاف الارسال", callback_data='stop_sending'),
        types.InlineKeyboardButton("ايقاف مؤقت", callback_data='pause_sending'),
        types.InlineKeyboardButton("استكمال", callback_data='resume_sending')
    )
    status_msg = bot.send_message(chat_id, "⏰ جاري تجهيز الارسال...",
                                  reply_markup=keyboard)

    for idx, (s_email, s_pass) in enumerate(senders, 1):
        if stop_sending.get(user_id, False):
            break

        while pause_sending.get(user_id, False):
            time.sleep(1)
            if stop_sending.get(user_id, False):
                break

        if stop_sending.get(user_id, False):
            break

        sender_stat = {'sent': 0, 'failed': 0, 'status': 'نشط', 'blocked': False}
        total_stats['sender_details'][s_email] = sender_stat

        for i in range(max_per_sender):
            if stop_sending.get(user_id, False):
                break

            while pause_sending.get(user_id, False):
                time.sleep(1)
                if stop_sending.get(user_id, False):
                    break

            if stop_sending.get(user_id, False):
                break

            elapsed = str(datetime.now() - start_time).split('.')[0]
            progress = ((i + 1) / max_per_sender) * 100

            pause_status = "متوقف مؤقتاً" if pause_sending.get(user_id, False) else "جاري الارسال"

            live_text = f"""
📊 عملية الارسال جارية...

الحالة: {pause_status}
⏰ الوقت المنقضي: {elapsed}
📨 الايميل الحالي: {s_email} ({i+1}/{max_per_sender})
✅ التقدم: {progress:.1f}%

📈 احصائيات:
✅ اجمالي مرسل: {total_stats['total_sent']}
❌ اجمالي فشل: {total_stats['total_failed']}
🔑 فشل مصادقة: {total_stats['auth_failed']}
"""
            try:
                bot.edit_message_text(live_text, chat_id=chat_id,
                                      message_id=status_msg.message_id,
                                      reply_markup=keyboard)
            except Exception:
                pass

            unique_subject = subject + ('\u200b' * (i + 1))
            success, reason = send_single_email(
                s_email, s_pass, support_list, unique_subject, body, format_type
            )

            if success:
                total_stats['total_sent'] += 1
                sender_stat['sent'] += 1
            else:
                total_stats['total_failed'] += 1
                sender_stat['failed'] += 1
                if "مصادقة" in reason:
                    total_stats['auth_failed'] += 1
                    sender_stat['status'] = 'محظور'
                    sender_stat['blocked'] = True
                    break
                elif "انقطع" in reason:
                    sender_stat['status'] = 'محظور'
                    sender_stat['blocked'] = True
                    break

            time.sleep(interval)

        if stop_sending.get(user_id, False):
            break

        if sender_stat['blocked']:
            total_stats['blocked'] += 1
        else:
            total_stats['completed_senders'] += 1

    stop_sending.pop(user_id, None)
    pause_sending.pop(user_id, None)

    end_time = datetime.now()
    total_time = str(end_time - start_time).split('.')[0]
    total_senders = len(senders)

    details_text = ""
    for em, st in total_stats['sender_details'].items():
        status = "مكتمل" if not st['blocked'] else "محظور"
        details_text += f"• {em}: {status} ({st['sent']}/{max_per_sender})\n"

    final_report = f"""
✅ انتهت عملية الارسال

📊 النتائج النهائية (الوقت: {total_time}):
✅ اجمالي المرسل: {total_stats['total_sent']}
❌ اجمالي الفشل: {total_stats['total_failed']}
🔑 منها فشل مصادقة: {total_stats['auth_failed']}
📨 ايميلات مكتملة: {total_stats['completed_senders']}/{total_senders}
🚫 ايميلات محظورة: {total_stats['blocked']}/{total_senders}

تفاصيل الحالة:
{details_text}
"""
    bot.send_message(chat_id, final_report)
    try:
        bot.delete_message(chat_id, status_msg.message_id)
    except Exception:
        pass
    show_main_menu(chat_id, None, "✅ تمت العملية.\nالقائمة الرئيسية:")

# ========== تشغيل البوت ==========
print("=" * 50)
print("✅ البوت يعمل بنجاح...")
print(f"👑 الأدمن: {ADMIN_ID}")
print("=" * 50)

if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"خطأ: {e}")
            time.sleep(10)
