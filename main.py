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

# ===== بيانات الاعتماد =====
BOT_TOKEN = '8832480539:AAHZLDVHLp3ubJ0Ngv_agrEcrLw_4dFIU7M'
API_ID = 34418359
API_HASH = 'ffc2e6b7fc449832be0e4c9d2cf7e467'

# ===== تخزين البيانات =====
user_accounts = {}
user_settings = {}

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
        [Button.text('➕ اضافة حساب')],
        [Button.text('▶️ بدء الابلاغ'), Button.text('⏹ ايقاف الابلاغ')],
        [Button.text('📩 تعيين الرسائل')],
        [Button.text('🏷 نوع التبليغ'), Button.text('🔢 عدد الرسائل')],
        [Button.text('⏱ وقت السليب'), Button.text('📝 كليشه التعليق')],
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

# ===== معالج الأزرار =====
@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()
    chat_id = event.chat_id
    settings = user_settings.setdefault(chat_id, {
        'target': '', 'msg_ids': [], 'report_type': None,
        'count': 5, 'sleep': 2, 'active': False,
        'task': None, 'cliche': 'تم الإبلاغ.', 'state': ''
    })

    if data == 'main':
        await event.edit('القائمة الرئيسية:', buttons=main_menu())
        return
    if data == 'back_to_report_types':
        await event.edit('اختر نوع التبليغ:', buttons=report_type_menu())
        return

    if data == 'add_account':
        await event.edit('ارسل: `api_id api_hash phone`\nمثال: 12345 abcdef 00966551234567')
        settings['state'] = 'awaiting_account'
        return

    if data == 'start_report':
        if chat_id not in user_accounts or user_accounts[chat_id].get('client') is None:
            await event.answer('⚠️ أضف حساباً أولاً', alert=True)
            return
        if settings['active']:
            await event.answer('⚠️ البلاغ نشط بالفعل', alert=True)
            return
        if not settings['target']:
            await event.answer('⚠️ أرسل رابط الهدف أولاً', alert=True)
            return
        if not settings['msg_ids']:
            await event.answer('⚠️ عين الرسائل أولاً', alert=True)
            return
        if settings['report_type'] is None:
            await event.answer('⚠️ حدد نوع التبليغ أولاً', alert=True)
            return
        settings['active'] = True
        settings['task'] = asyncio.create_task(report_loop(chat_id))
        await event.edit('✅ بدأ الابلاغ.', buttons=main_menu())
        return

    if data == 'stop_report':
        if settings['active'] and settings['task']:
            settings['active'] = False
            settings['task'].cancel()
            settings['task'] = None
            await event.edit('⏹ تم الايقاف.', buttons=main_menu())
        else:
            await event.answer('⚠️ لا يوجد بلاغ نشط', alert=True)
        return

    if data == 'report_messages':
        await event.edit('ارسل معرفات الرسائل مفصولة بمسافة:\nمثال: `123 456 789`')
        settings['state'] = 'awaiting_msg_ids'
        return

    if data == 'report_type':
        await event.edit('اختر نوع التبليغ:', buttons=report_type_menu())
        return

    for name, reason in REPORT_TYPES.items():
        if data == name:
            settings['report_type'] = reason
            await event.edit(f'✅ تم اختيار: {name}', buttons=main_menu())
            return

    if data == 'count':
        await event.edit('ارسل عدد الرسائل لكل دورة (رقم):')
        settings['state'] = 'awaiting_count'
        return

    if data == 'sleep':
        await event.edit('ارسل وقت السليب بالثواني (رقم):')
        settings['state'] = 'awaiting_sleep'
        return

    if data == 'cliche':
        await event.edit('ارسل نص التعليق الذي تريده:')
        settings['state'] = 'awaiting_cliche'
        return

# ===== حلقة الابلاغ =====
async def report_loop(chat_id):
    settings = user_settings[chat_id]
    acc = user_accounts[chat_id]
    client = acc['client']
    target_entity = await client.get_entity(settings['target'])

    while settings['active']:
        msgs = settings['msg_ids'][:settings['count']]
        for msg_id in msgs:
            if not settings['active']:
                break
            try:
                await client(ReportRequest(
                    peer=target_entity,
                    id=[msg_id],
                    reason=settings['report_type'],
                    message=settings['cliche']
                ))
                await bot.send_message(chat_id, f'✅ بلاغ {msg_id} - نجح')
            except RPCError as e:
                await bot.send_message(chat_id, f'❌ فشل {msg_id}: {str(e)}')
            await asyncio.sleep(settings['sleep'])
        if settings['active']:
            await asyncio.sleep(settings['sleep'] * 2)

# ===== معالج الرسائل النصية (الأوامر + دعم الأزرار) =====
@bot.on(events.NewMessage)
async def text_handler(event):
    if not event.is_private:
        return

    chat_id = event.chat_id
    text = event.text.strip()

    # تهيئة الإعدادات
    if chat_id not in user_settings:
        user_settings[chat_id] = {
            'target': '', 'msg_ids': [], 'report_type': None,
            'count': 5, 'sleep': 2, 'active': False,
            'task': None, 'cliche': 'تم الإبلاغ.', 'state': ''
        }
    settings = user_settings[chat_id]

    # ===== أمر /start يعرض القائمة بالأزرار =====
    if text == '/start':
        await event.reply('مرحباً، اختر من القائمة:', buttons=main_menu())
        return

    # ===== معالجة الأوامر النصية كبديل للأزرار =====
    command_map = {
        '➕ اضافة حساب': 'add_account',
        '▶️ بدء الابلاغ': 'start_report',
        '⏹ ايقاف الابلاغ': 'stop_report',
        '📩 تعيين الرسائل': 'report_messages',
        '🏷 نوع التبليغ': 'report_type',
        '🔢 عدد الرسائل': 'count',
        '⏱ وقت السليب': 'sleep',
        '📝 كليشه التعليق': 'cliche',
        '🔙 الرجوع للقائمة': 'main'
    }

    if text in command_map:
        # محاكاة حدث ضغط الزر
        fake_data = command_map[text].encode()
        fake_event = events.CallbackQuery(event, data=fake_data)
        await callback_handler(fake_event)
        return

    # ===== معالجة أوامر نصية إضافية (اختصارات) =====
    if text.startswith('اضف حساب'):
        parts = text.split()
        if len(parts) != 4:
            await event.reply('⚠️ استخدم: اضف حساب api_id api_hash phone')
            return
        try:
            api_id = int(parts[2])
            api_hash = parts[3]
            phone = parts[4]
            client = TelegramClient(f'session_{chat_id}', api_id, api_hash)
            await client.start(phone=phone)
            await client.get_dialogs()
            user_accounts[chat_id] = {'client': client, 'phone': phone}
            await event.reply('✅ تم اضافة الحساب.', buttons=main_menu())
        except Exception as e:
            await event.reply(f'❌ خطأ: {str(e)}')
        return

    if text.startswith('هدف'):
        parts = text.split()
        if len(parts) < 2:
            await event.reply('⚠️ استخدم: هدف @username')
            return
        target = parts[1]
        if not target.startswith('@'):
            target = '@' + target
        settings['target'] = target
        await event.reply(f'✅ تم حفظ الهدف: {target}', buttons=main_menu())
        return

    if text.startswith('رسائل'):
        parts = text.split()[1:]
        if not parts:
            await event.reply('⚠️ استخدم: رسائل 123 456 789')
            return
        try:
            msg_ids = [int(x) for x in parts]
            settings['msg_ids'] = msg_ids
            await event.reply(f'✅ تم حفظ {len(msg_ids)} رسالة.', buttons=main_menu())
        except:
            await event.reply('⚠️ أدخل أرقاماً صحيحة.')
        return

    if text.startswith('نوع'):
        parts = text.split()
        if len(parts) != 2:
            await event.reply('⚠️ استخدم: نوع اساءة|ارهاب|اباحي|دموي|سبام')
            return
        type_name = parts[1]
        type_map = {
            'اساءة': 'اساءة للاطفال',
            'ارهاب': 'ارهاب',
            'اباحي': 'اباحي',
            'دموي': 'دموي',
            'سبام': 'سبام'
        }
        if type_name in type_map:
            full_name = type_map[type_name]
            settings['report_type'] = REPORT_TYPES[full_name]
            await event.reply(f'✅ تم اختيار نوع: {full_name}', buttons=main_menu())
        else:
            await event.reply('⚠️ الأنواع: اساءة، ارهاب، اباحي، دموي، سبام')
        return

    if text.startswith('عدد'):
        parts = text.split()
        if len(parts) != 2:
            await event.reply('⚠️ استخدم: عدد 5')
            return
        try:
            count = int(parts[1])
            if count < 1:
                count = 1
            settings['count'] = count
            await event.reply(f'✅ عدد الرسائل: {count}', buttons=main_menu())
        except:
            await event.reply('⚠️ أدخل رقماً صحيحاً.')
        return

    if text.startswith('سليب'):
        parts = text.split()
        if len(parts) != 2:
            await event.reply('⚠️ استخدم: سليب 2')
            return
        try:
            sleep_val = float(parts[1])
            if sleep_val < 0.5:
                sleep_val = 0.5
            settings['sleep'] = sleep_val
            await event.reply(f'✅ وقت السليب: {sleep_val} ثانية', buttons=main_menu())
        except:
            await event.reply('⚠️ أدخل رقماً (مثل 2 أو 3.5).')
        return

    if text.startswith('كليشه'):
        cliche_text = text[7:].strip()
        if len(cliche_text) < 2:
            await event.reply('⚠️ النص قصير جداً.')
            return
        settings['cliche'] = cliche_text
        await event.reply(f'✅ تم حفظ الكليشه: "{cliche_text}"', buttons=main_menu())
        return

    if text == 'بدء':
        # محاكاة زر بدء الابلاغ
        await callback_handler(events.CallbackQuery(event, data=b'start_report'))
        return

    if text == 'ايقاف':
        await callback_handler(events.CallbackQuery(event, data=b'stop_report'))
        return

    if text == 'حالة':
        status = 'نشط' if settings['active'] else 'متوقف'
        await event.reply(
            f'الحالة:\n- الهدف: {settings["target"] or "غير محدد"}\n'
            f'- عدد الرسائل: {len(settings["msg_ids"])}\n'
            f'- عدد لكل دورة: {settings["count"]}\n'
            f'- السليب: {settings["sleep"]} ثانية\n'
            f'- الحالة: {status}',
            buttons=main_menu()
        )
        return

    if text == 'مساعدة' or text == 'اوامر':
        await event.reply(
            'الأوامر النصية:\n'
            'اضف حساب api_id api_hash phone\n'
            'هدف @username\n'
            'رسائل 123 456 789\n'
            'نوع اساءة|ارهاب|اباحي|دموي|سبام\n'
            'عدد 5\n'
            'سليب 2\n'
            'كليشه النص\n'
            'بدء\n'
            'ايقاف\n'
            'حالة\n'
            'مساعدة\n\n'
            'أو استخدم الأزرار.',
            buttons=main_menu()
        )
        return

    # ===== إذا كان النص رابطاً، يعتبره هدفاً =====
    if text.startswith('https://t.me/'):
        parts = text.split('/')
        username = parts[-1].split('?')[0]
        if username:
            settings['target'] = f'@{username}'
            await event.reply(f'✅ تم حفظ الهدف: @{username}', buttons=main_menu())
        return

    # ===== أي أمر غير معروف =====
    await event.reply('أمر غير معروف. استخدم الأزرار أو اكتب "مساعدة".', buttons=main_menu())

print('البوت يعمل بالأزرار والأوامر النصية معاً...')
asyncio.run(bot.run_until_disconnected())
