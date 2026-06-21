import asyncio
from telethon import TelegramClient, Button, events
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import (
    InputReportReasonSpam,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonChildAbuse,
    InputReportReasonOther,
)
from telethon.errors import RPCError
import time

# ===== بيانات الاعتماد =====
BOT_TOKEN = '8832480539:AAHZLDVHLp3ubJ0Ngv_agrEcrLw_4dFIU7M'
API_ID = 34418359
API_HASH = 'ffc2e6b7fc449832be0e4c9d2cf7e467'

# ===== تخزين البيانات =====
user_accounts = {}
user_settings = {}

# ===== أنواع التبليغ =====
REPORT_TYPES = {
    'اساءة للاطفال': InputReportReasonChildAbuse(),
    'ارهاب': InputReportReasonOther(),
    'اباحي': InputReportReasonPornography(),
    'دموي': InputReportReasonViolence(),
    'سبام': InputReportReasonSpam()
}

bot = TelegramClient('report_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ===== القوائم =====
def main_menu():
    return [
        [Button.text('➕ اضافة حساب', resize=True)],
        [Button.text('▶️ بدء الابلاغ'), Button.text('⏹ ايقاف الابلاغ')],
        [Button.text('📩 التبليغ (رسائل)')],
        [Button.text('🏷 نوع التبليغ'), Button.text('🔢 عدد الرسائل')],
        [Button.text('⏱ عدد السليب (ثانية)'), Button.text('📝 كليشه التعليق')],
        [Button.text('🔙 الرجوع للقائمة')]
    ]

def report_type_menu():
    return [
        [Button.text('👶 اساءة للاطفال')],
        [Button.text('☠️ ارهاب')],
        [Button.text('🔞 اباحي')],
        [Button.text('🩸 دموي')],
        [Button.text('💬 سبام')],
        [Button.text('🔙 الرجوع للقائمة')]
    ]

# ===== معالجة الكولباك =====
@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()
    chat_id = event.chat_id
    user_settings.setdefault(chat_id, {
        'target': '',
        'msg_ids': [],
        'report_type': None,
        'count': 5,
        'sleep': 2,
        'active': False,
        'task': None,
        'cliche': 'تم الإبلاغ عبر البوت.'  # الكليشه الافتراضية
    })

    if data == 'main':
        await event.edit('القائمة الرئيسية:', buttons=main_menu())
        return
    if data == 'back_to_report_types':
        await event.edit('اختر نوع التبليغ:', buttons=report_type_menu())
        return

    # ===== اضافة حساب =====
    if data == 'add_account':
        await event.edit('ارسل: `api_id api_hash phone`\nمثال: 12345 abcdef 00966551234567')
        user_settings[chat_id]['state'] = 'awaiting_account'
        return

    # ===== بدء الابلاغ =====
    if data == 'start_report':
        if chat_id not in user_accounts or user_accounts[chat_id]['client'] is None:
            await event.answer('⚠️ أضف حساباً أولاً', alert=True)
            return
        if user_settings[chat_id]['active']:
            await event.answer('⚠️ يعمل بالفعل', alert=True)
            return
        if not user_settings[chat_id]['target'] or not user_settings[chat_id]['msg_ids']:
            await event.answer('⚠️ حدد الهدف والرسائل', alert=True)
            return
        user_settings[chat_id]['active'] = True
        user_settings[chat_id]['task'] = asyncio.create_task(report_loop(chat_id))
        await event.edit('✅ بدأ الابلاغ.', buttons=main_menu())
        return

    # ===== ايقاف الابلاغ =====
    if data == 'stop_report':
        if user_settings[chat_id]['active'] and user_settings[chat_id]['task']:
            user_settings[chat_id]['active'] = False
            user_settings[chat_id]['task'].cancel()
            user_settings[chat_id]['task'] = None
            await event.edit('⏹ تم الايقاف.', buttons=main_menu())
        else:
            await event.answer('⚠️ لا يوجد بلاغ نشط', alert=True)
        return

    # ===== التبليغ (رسائل) =====
    if data == 'report_messages':
        await event.edit('ارسل معرفات الرسائل مفصولة بمسافة:\nمثال: `123 456 789`')
        user_settings[chat_id]['state'] = 'awaiting_msg_ids'
        return

    # ===== نوع التبليغ =====
    if data == 'report_type':
        await event.edit('اختر نوع التبليغ:', buttons=report_type_menu())
        return

    # ===== اختيار نوع معين =====
    for name, reason in REPORT_TYPES.items():
        if data == name:
            user_settings[chat_id]['report_type'] = reason
            await event.edit(f'✅ تم اختيار: {name}', buttons=main_menu())
            return

    # ===== عدد الرسائل =====
    if data == 'count':
        await event.edit('ارسل عدد الرسائل (رقم صحيح):')
        user_settings[chat_id]['state'] = 'awaiting_count'
        return

    # ===== عدد السليب =====
    if data == 'sleep':
        await event.edit('ارسل وقت السليب بالثواني (رقم):')
        user_settings[chat_id]['state'] = 'awaiting_sleep'
        return

    # ===== كليشه التعليق (جديد) =====
    if data == 'cliche':
        await event.edit('ارسل النص الذي تريد إضافته كتعليق مع كل بلاغ:')
        user_settings[chat_id]['state'] = 'awaiting_cliche'
        return

# ===== حلقة الابلاغ =====
async def report_loop(chat_id):
    settings = user_settings[chat_id]
    acc = user_accounts[chat_id]
    client = acc['client']
    target_entity = await client.get_entity(settings['target'])

    while settings['active']:
        # نأخذ أول settings['count'] رسالة من القائمة (أو جميعها إن كانت أقل)
        msgs_to_report = settings['msg_ids'][:settings['count']]
        for msg_id in msgs_to_report:
            if not settings['active']:
                break
            try:
                await client(ReportRequest(
                    peer=target_entity,
                    id=[msg_id],
                    reason=settings['report_type'],
                    message=settings['cliche']  # هنا يتم استخدام الكليشه المخصصة
                ))
                await bot.send_message(chat_id, f'✅ بلاغ {msg_id} - نص: "{settings["cliche"]}"')
            except RPCError as e:
                await bot.send_message(chat_id, f'❌ فشل {msg_id}: {str(e)}')
            await asyncio.sleep(settings['sleep'])
        if settings['active']:
            await asyncio.sleep(settings['sleep'] * 2)  # راحة بين الدورات

# ===== استقبال الرسائل النصية =====
@bot.on(events.NewMessage(pattern='(?i)^/start$'))
async def start_handler(event):
    await event.respond('مرحباً، القائمة:', buttons=main_menu())

@bot.on(events.NewMessage)
async def text_handler(event):
    if not event.is_private:
        return
    chat_id = event.chat_id
    user_settings.setdefault(chat_id, {
        'target': '',
        'msg_ids': [],
        'report_type': None,
        'count': 5,
        'sleep': 2,
        'active': False,
        'task': None,
        'cliche': 'تم الإبلاغ عبر البوت.',
        'state': ''
    })
    state = user_settings[chat_id].get('state', '')

    # ----- اضافة حساب -----
    if state == 'awaiting_account':
        parts = event.text.split()
        if len(parts) != 3:
            await event.reply('⚠️ احتاج 3 قيم: api_id api_hash phone')
            return
        try:
            api_id = int(parts[0])
            api_hash = parts[1]
            phone = parts[2]
            client = TelegramClient(f'session_{chat_id}', api_id, api_hash)
            await client.start(phone=phone)
            await client.get_dialogs()
            user_accounts[chat_id] = {'api_id': api_id, 'api_hash': api_hash, 'phone': phone, 'client': client}
            user_settings[chat_id]['state'] = ''
            await event.reply('✅ تم اضافة الحساب!', buttons=main_menu())
        except Exception as e:
            await event.reply(f'❌ خطأ: {str(e)}')
            user_settings[chat_id]['state'] = ''
        return

    # ----- رسائل للتبليغ -----
    if state == 'awaiting_msg_ids':
        try:
            msg_ids = list(map(int, event.text.split()))
            if not msg_ids:
                raise ValueError
            user_settings[chat_id]['msg_ids'] = msg_ids
            user_settings[chat_id]['state'] = ''
            await event.reply(f'✅ تم حفظ {len(msg_ids)} رسالة.', buttons=main_menu())
        except:
            await event.reply('⚠️ أدخل أرقاماً صحيحة مفصولة بمسافة.', buttons=main_menu())
        return

    # ----- عدد الرسائل -----
    if state == 'awaiting_count':
        try:
            count = int(event.text)
            if count < 1:
                count = 1
            user_settings[chat_id]['count'] = count
            user_settings[chat_id]['state'] = ''
            await event.reply(f'✅ عدد الرسائل لكل دورة: {count}', buttons=main_menu())
        except:
            await event.reply('⚠️ أدخل رقماً صحيحاً.', buttons=main_menu())
        return

    # ----- عدد السليب -----
    if state == 'awaiting_sleep':
        try:
            sleep_val = float(event.text)
            if sleep_val < 0.5:
                sleep_val = 0.5
            user_settings[chat_id]['sleep'] = sleep_val
            user_settings[chat_id]['state'] = ''
            await event.reply(f'✅ وقت السليب: {sleep_val} ثانية', buttons=main_menu())
        except:
            await event.reply('⚠️ أدخل رقماً (مثل 2 أو 3.5).', buttons=main_menu())
        return

    # ----- كليشه التعليق (جديد) -----
    if state == 'awaiting_cliche':
        cliche_text = event.text.strip()
        if len(cliche_text) < 2:
            await event.reply('⚠️ النص قصير جداً، حاول مجدداً.')
            return
        user_settings[chat_id]['cliche'] = cliche_text
        user_settings[chat_id]['state'] = ''
        await event.reply(f'✅ تم حفظ الكليشه: "{cliche_text}"', buttons=main_menu())
        return

    # ----- التعرف على رابط الهدف تلقائياً -----
    if event.text.startswith('https://t.me/'):
        parts = event.text.split('/')
        username = parts[-1].split('?')[0]
        if username:
            user_settings[chat_id]['target'] = f'@{username}'
            await event.reply(f'✅ الهدف: @{username}', buttons=main_menu())

print('البوت شغال...')
asyncio.run(bot.run_until_disconnected())
