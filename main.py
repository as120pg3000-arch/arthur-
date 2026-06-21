import os, time, platform, re, json, shutil, asyncio
try:
    from telethon.sync import TelegramClient
except:
    os.system("pip install telethon")
from telethon import Button, events
from telethon.tl import types, functions
from telethon.errors import SessionPasswordNeededError, RPCError

rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'

BOT_TOKEN = '8832480539:AAHZLDVHLp3ubJ0Ngv_agrEcrLw_4dFIU7M'
API_ID = 34418359
API_HASH = 'ffc2e6b7fc449832be0e4c9d2cf7e467'

bot = TelegramClient('report_bot_system', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ===== الكلاسات من الكود الأصلي مع تعديلات بسيطة للتوافق مع asyncio =====
def clr():
    if 'Windows' in platform.uname():
        os.system("cls")
    else:
        os.system("clear")

def pbnr():
    banner = f"""{k}
 ____                             _               
|  _ \   ___  _ __    ___   _ __ | |_   ___  _ __ 
| |_) | / _ \| '_ \  / _ \| '__|| __| / _ \| '__|
|  _ < |  __/| |_) || (_) || |   | |_ |  __/| |    {cn}Channel{k}
|_| \_\ \___|| .__/  \___/ |_|    \__| \___||_|   
             |_|	

    {lrd}[{lgn}+{lrd}] {gn}DxD : {lgn}@	dr4g00nx
"""
    print(banner)

def dndnd(link):
    match_public = re.search(r"(?:https?://)?t(?:telegram)?\.me/([a-zA-Z0-9_]+)/(\d+)", link)
    if match_public:
        return match_public.group(1), int(match_public.group(2)), False
    match_private = re.search(r"(?:https?://)?t(?:telegram)?\.me/c/(-?\d+)/(\d+)", link)
    if match_private:
        chat_id = int(match_private.group(1))
        msg_id = int(match_private.group(2))
        return chat_id, msg_id, True
    return None, None, None

class zzbe:
    def __init__(self):
        self.sessions_dir = "sessions"
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        self.api_id = None
        self.api_hash = None
        self.load_api_credentials()

    def load_api_credentials(self):
        cred_file = os.path.join(self.sessions_dir, "api_creds.json")
        if os.path.exists(cred_file):
            with open(cred_file, 'r') as f:
                data = json.load(f)
                self.api_id = data.get('api_id')
                self.api_hash = data.get('api_hash')
        else:
            self.api_id = input(f"{lrd}[{lgn}+{lrd}] {gn}Enter your Telegram API ID: {g}")
            self.api_hash = input(f"{lrd}[{lgn}+{lrd}] {gn}Enter your Telegram API Hash: {g}")
            with open(cred_file, 'w') as f:
                json.dump({'api_id': self.api_id, 'api_hash': self.api_hash}, f)

    def get_account_name(self, phone):
        session_file = os.path.join(self.sessions_dir, f"{phone}.session")
        if not os.path.exists(session_file):
            return None
        try:
            client = TelegramClient(session_file, int(self.api_id), self.api_hash)
            client.connect()
            if client.is_user_authorized():
                me = client.get_me()
                name = me.first_name or me.username or phone
                client.disconnect()
                return name
            client.disconnect()
            return None
        except:
            return phone

    def add_account_phone(self, phone):
        session_file = os.path.join(self.sessions_dir, f"{phone}.session")
        if os.path.exists(session_file):
            return False, "Account already exists."
        client = TelegramClient(session_file, int(self.api_id), self.api_hash)
        try:
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(phone)
                return True, "code_sent"
            me = client.get_me()
            name = me.first_name or me.username or phone
            client.disconnect()
            return True, f"Account {phone} added successfully. Name: {name}"
        except Exception as e:
            if os.path.exists(session_file):
                os.remove(session_file)
            return False, str(e)

    def complete_add_account(self, phone, code, password=None):
        session_file = os.path.join(self.sessions_dir, f"{phone}.session")
        client = TelegramClient(session_file, int(self.api_id), self.api_hash)
        try:
            client.connect()
            try:
                client.sign_in(phone, code)
            except SessionPasswordNeededError:
                if password is None:
                    return False, "2FA required"
                client.sign_in(password=password)
            me = client.get_me()
            name = me.first_name or me.username or phone
            client.disconnect()
            return True, f"Account {phone} added. Name: {name}"
        except Exception as e:
            if os.path.exists(session_file):
                os.remove(session_file)
            return False, str(e)

    def import_session_file(self, file_path, name):
        if not os.path.isfile(file_path):
            return False, "File not found"
        if not file_path.endswith('.session'):
            return False, "File must have .session extension"
        dest = os.path.join(self.sessions_dir, f"{name}.session")
        if os.path.exists(dest):
            return False, "Session with this name already exists. Delete first."
        try:
            shutil.copy2(file_path, dest)
            return True, f"Session imported as {name}"
        except Exception as e:
            return False, str(e)

    def delete_account(self, phone):
        session_file = os.path.join(self.sessions_dir, f"{phone}.session")
        if os.path.exists(session_file):
            os.remove(session_file)
            return True, f"Account {phone} deleted."
        return False, "Account not found."

    def list_accounts(self):
        sessions = [f for f in os.listdir(self.sessions_dir) if f.endswith('.session') and f != 'api_creds.json']
        if not sessions:
            return []
        accounts = []
        for f in sessions:
            phone = f.replace('.session', '')
            name = self.get_account_name(phone)
            if name:
                accounts.append((phone, name))
            else:
                accounts.append((phone, phone))
        return accounts

    def get_client(self, phone):
        session_file = os.path.join(self.sessions_dir, f"{phone}.session")
        if not os.path.exists(session_file):
            return None
        client = TelegramClient(session_file, int(self.api_id), self.api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.disconnect()
            return None
        return client

class wsi:
    def __init__(self):
        self.comments_file = "comments.json"
        self.comments = []
        self.active_comment = ""
        self.load_comments()

    def load_comments(self):
        if os.path.exists(self.comments_file):
            with open(self.comments_file, 'r') as f:
                data = json.load(f)
                self.comments = data.get('comments', [])
                self.active_comment = data.get('active', '')
        else:
            self.comments = []
            self.active_comment = ""

    def save_comments(self):
        with open(self.comments_file, 'w') as f:
            json.dump({'comments': self.comments, 'active': self.active_comment}, f, indent=4)

    def add_comment(self, text):
        if text.strip() == "":
            return False, "Comment cannot be empty."
        if text in self.comments:
            return False, "Comment already exists."
        self.comments.append(text)
        if not self.active_comment:
            self.active_comment = text
        self.save_comments()
        return True, "Comment added."

    def delete_comment(self, index):
        if 0 <= index < len(self.comments):
            removed = self.comments.pop(index)
            if self.active_comment == removed:
                self.active_comment = self.comments[0] if self.comments else ""
            self.save_comments()
            return True, "Comment deleted."
        return False, "Invalid index."

    def list_comments(self):
        return self.comments.copy(), self.active_comment

    def set_active(self, index):
        if 0 <= index < len(self.comments):
            self.active_comment = self.comments[index]
            self.save_comments()
            return True, f"Active comment set to: {self.active_comment}"
        return False, "Invalid index."

    def get_active(self):
        if not self.active_comment:
            return None
        return self.active_comment

class owdx:
    def __init__(self):
        self.posts_file = "posts.json"
        self.posts = []
        self.selected_posts = []
        self.load_posts()

    def load_posts(self):
        if os.path.exists(self.posts_file):
            with open(self.posts_file, 'r') as f:
                data = json.load(f)
                self.posts = data.get('posts', [])
                self.selected_posts = data.get('selected', [])
        else:
            self.posts = []
            self.selected_posts = []

    def save_posts(self):
        with open(self.posts_file, 'w') as f:
            json.dump({'posts': self.posts, 'selected': self.selected_posts}, f, indent=4)

    def add_post(self, link):
        link = link.strip()
        if not link:
            return False, "Link cannot be empty."
        if link in self.posts:
            return False, "Post already exists."
        self.posts.append(link)
        if not self.selected_posts:
            self.selected_posts.append(link)
        self.save_posts()
        return True, "Post added."

    def delete_post(self, index):
        if 0 <= index < len(self.posts):
            removed = self.posts.pop(index)
            if removed in self.selected_posts:
                self.selected_posts.remove(removed)
            self.save_posts()
            return True, "Post deleted."
        return False, "Invalid index."

    def list_posts(self):
        return self.posts.copy(), self.selected_posts.copy()

    def toggle_select(self, index):
        if 0 <= index < len(self.posts):
            post = self.posts[index]
            if post in self.selected_posts:
                self.selected_posts.remove(post)
            else:
                self.selected_posts.append(post)
            self.save_posts()
            return True, f"Toggled selection for: {post}"
        return False, "Invalid index."

    def get_selected(self):
        return self.selected_posts.copy()

class xw38:
    def __init__(self):
        self.zzbe = zzbe()
        self.wsi = wsi()
        self.owdx = owdx()
        self.selected_accounts = []
        self.reporting_active = False
        self.report_task = None
        self.total_reports = 0
        self.max_reports = 100
        self.report_counter = 0

    def get_accounts_list(self):
        return self.zzbe.list_accounts()

    def get_comments_list(self):
        return self.wsi.list_comments()

    def get_posts_list(self):
        return self.owdx.list_posts()

    def get_selected_accounts(self):
        return self.selected_accounts.copy()

    def toggle_account_selection(self, phone):
        if phone in self.selected_accounts:
            self.selected_accounts.remove(phone)
            return False, f"Removed {phone}"
        else:
            self.selected_accounts.append(phone)
            return True, f"Added {phone}"

    def add_comment(self, text):
        return self.wsi.add_comment(text)

    def delete_comment(self, index):
        return self.wsi.delete_comment(index)

    def set_active_comment(self, index):
        return self.wsi.set_active(index)

    def add_post(self, link):
        return self.owdx.add_post(link)

    def delete_post(self, index):
        return self.owdx.delete_post(index)

    def toggle_post(self, index):
        return self.owdx.toggle_select(index)

    def add_account(self, phone):
        return self.zzbe.add_account_phone(phone)

    def complete_account(self, phone, code, password=None):
        return self.zzbe.complete_add_account(phone, code, password)

    def delete_account(self, phone):
        return self.zzbe.delete_account(phone)

    def import_session(self, file_path, name):
        return self.zzbe.import_session_file(file_path, name)

    def start_reporting(self, chat_id):
        if self.reporting_active:
            return False, "Reporting already active."
        if not self.selected_accounts:
            return False, "No accounts selected."
        active_comment = self.wsi.get_active()
        if not active_comment:
            return False, "No active comment set."
        selected_posts = self.owdx.get_selected()
        if not selected_posts:
            return False, "No posts selected."
        self.reporting_active = True
        self.report_counter = 0
        self.total_reports = len(self.selected_accounts) * len(selected_posts)
        if self.total_reports > 100:
            self.max_reports = 100
        else:
            self.max_reports = self.total_reports
        self.report_task = asyncio.create_task(self.report_loop(chat_id, selected_posts, active_comment))
        return True, f"Started reporting. Total reports: {self.total_reports}"

    def stop_reporting(self):
        if not self.reporting_active:
            return False, "No active reporting."
        self.reporting_active = False
        if self.report_task:
            self.report_task.cancel()
            self.report_task = None
        return True, "Reporting stopped."

    async def report_loop(self, chat_id, selected_posts, active_comment):
        accounts = self.zzbe.list_accounts()
        phone_to_name = {p: name for p, name in accounts}
        reported_count = 0
        reason = types.InputReportReasonChildAbuse()

        for phone in self.selected_accounts:
            if not self.reporting_active:
                break
            name = phone_to_name.get(phone, phone)
            client = self.zzbe.get_client(phone)
            if not client:
                await bot.send_message(chat_id, f"❌ Failed to connect {name} ({phone}). Skipping.")
                continue
            for link in selected_posts:
                if not self.reporting_active:
                    break
                entity_id, msg_id, is_private = dndnd(link)
                if entity_id is None or msg_id is None:
                    await bot.send_message(chat_id, f"❌ Invalid link: {link} - skipped.")
                    continue
                try:
                    if is_private:
                        from telethon.tl.types import PeerChannel
                        entity = client.get_entity(PeerChannel(entity_id))
                    else:
                        entity = client.get_entity(entity_id)
                    client(functions.messages.ReportRequest(
                        peer=entity,
                        id=[msg_id],
                        reason=reason,
                        message=active_comment
                    ))
                    reported_count += 1
                    await bot.send_message(chat_id, f"✅ تم ارسال ابلاغ جديد بنجاح [{reported_count}/{self.max_reports}]")
                    await asyncio.sleep(2)
                except RPCError as e:
                    await bot.send_message(chat_id, f"❌ Error reporting {link}: {str(e)}")
                except Exception as e:
                    await bot.send_message(chat_id, f"❌ Error: {str(e)}")
            client.disconnect()

        self.reporting_active = False
        self.report_task = None
        await bot.send_message(chat_id, f"🏁 انتهى التبليغ. تم ارسال {reported_count} بلاغ.")

# ===== بوت تيليجرام =====
system = xw38()

def main_menu():
    return [
        [Button.text('➕ اضافة حساب')],
        [Button.text('▶️ بدء الابلاغ'), Button.text('⏹ ايقاف الابلاغ')],
        [Button.text('📩 ادارة المنشورات')],
        [Button.text('📝 ادارة التعليقات')],
        [Button.text('👤 اختيار الحسابات'), Button.text('📊 الحالة')],
        [Button.text('🗑 حذف حساب')],
        [Button.text('🔙 الرجوع للقائمة')]
    ]

def accounts_menu(accounts):
    buttons = []
    for phone, name in accounts:
        selected = '✅' if phone in system.selected_accounts else '⬜'
        buttons.append([Button.text(f"{selected} {name} ({phone})")])
    buttons.append([Button.text('🔙 الرجوع للقائمة')])
    return buttons

def posts_menu(posts, selected):
    buttons = []
    for i, post in enumerate(posts):
        sel = '[x]' if post in selected else '[ ]'
        buttons.append([Button.text(f"{sel} {post[:30]}...")])
    buttons.append([Button.text('➕ اضافة منشور')])
    buttons.append([Button.text('🗑 حذف منشور')])
    buttons.append([Button.text('🔙 الرجوع للقائمة')])
    return buttons

def comments_menu(comments, active):
    buttons = []
    for i, c in enumerate(comments):
        act = '✅' if c == active else '⬜'
        buttons.append([Button.text(f"{act} {c[:20]}...")])
    buttons.append([Button.text('➕ اضافة تعليق')])
    buttons.append([Button.text('🗑 حذف تعليق')])
    buttons.append([Button.text('🔙 الرجوع للقائمة')])
    return buttons

@bot.on(events.NewMessage(pattern='(?i)^/start$'))
async def start_handler(event):
    await event.respond('مرحباً، اختر من القائمة:', buttons=main_menu())

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()
    chat_id = event.chat_id

    if data == 'main':
        await event.edit('القائمة الرئيسية:', buttons=main_menu())
        return

    # اضافة حساب
    if data == 'add_account':
        await event.edit('ارسل رقم الهاتف مع مفتاح الدولة:\nمثال: 00966551234567')
        system.user_state = 'awaiting_phone'
        return

    # بدء الابلاغ
    if data == 'start_report':
        result, msg = system.start_reporting(chat_id)
        if result:
            await event.edit(f'✅ {msg}', buttons=main_menu())
        else:
            await event.answer(f'⚠️ {msg}', alert=True)
        return

    # ايقاف الابلاغ
    if data == 'stop_report':
        result, msg = system.stop_reporting()
        if result:
            await event.edit(f'⏹ {msg}', buttons=main_menu())
        else:
            await event.answer(f'⚠️ {msg}', alert=True)
        return

    # ادارة المنشورات
    if data == 'manage_posts':
        posts, selected = system.get_posts_list()
        if not posts:
            await event.edit('لا توجد منشورات. اضف منشوراً:', buttons=[[Button.text('➕ اضافة منشور')], [Button.text('🔙 الرجوع للقائمة')]])
        else:
            await event.edit('المنشورات:', buttons=posts_menu(posts, selected))
        return

    # ادارة التعليقات
    if data == 'manage_comments':
        comments, active = system.get_comments_list()
        if not comments:
            await event.edit('لا توجد تعليقات. اضف تعليقاً:', buttons=[[Button.text('➕ اضافة تعليق')], [Button.text('🔙 الرجوع للقائمة')]])
        else:
            await event.edit('التعليقات:', buttons=comments_menu(comments, active))
        return

    # اختيار الحسابات
    if data == 'select_accounts':
        accounts = system.get_accounts_list()
        if not accounts:
            await event.edit('لا توجد حسابات. اضف حساباً أولاً.', buttons=main_menu())
            return
        await event.edit('اختر الحسابات:', buttons=accounts_menu(accounts))
        return

    # الحالة
    if data == 'status':
        accounts = system.get_accounts_list()
        selected = system.get_selected_accounts()
        comments, active_comment = system.get_comments_list()
        posts, selected_posts = system.get_posts_list()
        status_text = (
            f"📊 **الحالة**\n"
            f"- عدد الحسابات: {len(accounts)}\n"
            f"- حسابات محددة: {len(selected)}\n"
            f"- التعليق النشط: {active_comment or 'لا يوجد'}\n"
            f"- المنشورات: {len(posts)}\n"
            f"- منشورات محددة: {len(selected_posts)}\n"
            f"- التبليغ نشط: {'نعم' if system.reporting_active else 'لا'}"
        )
        await event.edit(status_text, buttons=main_menu())
        return

    # حذف حساب
    if data == 'delete_account':
        accounts = system.get_accounts_list()
        if not accounts:
            await event.edit('لا توجد حسابات لحذفها.', buttons=main_menu())
            return
        buttons = []
        for phone, name in accounts:
            buttons.append([Button.text(f"🗑 {name} ({phone})")])
        buttons.append([Button.text('🔙 الرجوع للقائمة')])
        await event.edit('اختر حساباً لحذفه:', buttons=buttons)
        return

    # معالجة اختيار حساب من قائمة الحسابات
    if data.startswith('toggle_'):
        phone = data.replace('toggle_', '')
        added, msg = system.toggle_account_selection(phone)
        accounts = system.get_accounts_list()
        await event.edit('اختر الحسابات:', buttons=accounts_menu(accounts))
        return

    # معالجة حذف حساب
    if data.startswith('delacc_'):
        phone = data.replace('delacc_', '')
        result, msg = system.delete_account(phone)
        await event.edit(msg if result else f'❌ {msg}', buttons=main_menu())
        return

    # اضافة منشور
    if data == 'add_post':
        system.user_state = 'awaiting_post'
        await event.edit('ارسل رابط المنشور:')
        return

    # حذف منشور
    if data == 'delete_post':
        posts, _ = system.get_posts_list()
        if not posts:
            await event.edit('لا توجد منشورات للحذف.', buttons=main_menu())
            return
        buttons = []
        for i, post in enumerate(posts):
            buttons.append([Button.text(f"🗑 {i+1}: {post[:30]}...")])
        buttons.append([Button.text('🔙 الرجوع للقائمة')])
        system.user_state = 'awaiting_delete_post'
        await event.edit('اختر منشوراً لحذفه:', buttons=buttons)
        return

    # معالجة اختيار منشور للحذف
    if data.startswith('delpost_'):
        idx = int(data.replace('delpost_', ''))
        result, msg = system.delete_post(idx)
        posts, selected = system.get_posts_list()
        if posts:
            await event.edit(msg if result else f'❌ {msg}', buttons=posts_menu(posts, selected))
        else:
            await event.edit(msg if result else f'❌ {msg}', buttons=main_menu())
        return

    # اضافة تعليق
    if data == 'add_comment':
        system.user_state = 'awaiting_comment'
        await event.edit('ارسل نص التعليق:')
        return

    # حذف تعليق
    if data == 'delete_comment':
        comments, _ = system.get_comments_list()
        if not comments:
            await event.edit('لا توجد تعليقات للحذف.', buttons=main_menu())
            return
        buttons = []
        for i, c in enumerate(comments):
            buttons.append([Button.text(f"🗑 {i+1}: {c[:20]}...")])
        buttons.append([Button.text('🔙 الرجوع للقائمة')])
        system.user_state = 'awaiting_delete_comment'
        await event.edit('اختر تعليقاً لحذفه:', buttons=buttons)
        return

    # معالجة اختيار تعليق للحذف
    if data.startswith('delcomment_'):
        idx = int(data.replace('delcomment_', ''))
        result, msg = system.delete_comment(idx)
        comments, active = system.get_comments_list()
        if comments:
            await event.edit(msg if result else f'❌ {msg}', buttons=comments_menu(comments, active))
        else:
            await event.edit(msg if result else f'❌ {msg}', buttons=main_menu())
        return

    # اختيار تعليق نشط
    if data.startswith('setactive_'):
        idx = int(data.replace('setactive_', ''))
        result, msg = system.set_active_comment(idx)
        comments, active = system.get_comments_list()
        if comments:
            await event.edit(msg if result else f'❌ {msg}', buttons=comments_menu(comments, active))
        else:
            await event.edit(msg if result else f'❌ {msg}', buttons=main_menu())
        return

    # اختيار منشور (تبديل التحديد)
    if data.startswith('togglepost_'):
        idx = int(data.replace('togglepost_', ''))
        result, msg = system.toggle_post(idx)
        posts, selected = system.get_posts_list()
        await event.edit(msg if result else f'❌ {msg}', buttons=posts_menu(posts, selected))
        return

    await event.answer('أمر غير معروف', alert=True)

@bot.on(events.NewMessage)
async def text_handler(event):
    if not event.is_private:
        return
    chat_id = event.chat_id
    text = event.text.strip()
    state = getattr(system, 'user_state', '')

    if state == 'awaiting_phone':
        phone = text
        result, msg = system.add_account(phone)
        if result and msg == 'code_sent':
            system.pending_phone = phone
            system.user_state = 'awaiting_code'
            await event.reply('تم ارسال رمز التحقق. ارسل الرمز:')
        elif result:
            system.user_state = ''
            await event.reply(f'✅ {msg}', buttons=main_menu())
        else:
            system.user_state = ''
            await event.reply(f'❌ {msg}', buttons=main_menu())
        return

    if state == 'awaiting_code':
        code = text
        phone = getattr(system, 'pending_phone', '')
        if not phone:
            system.user_state = ''
            await event.reply('❌ حدث خطأ، حاول مجدداً.', buttons=main_menu())
            return
        # نطلب كلمة مرور 2FA إذا كان مطلوباً
        # هنا نبسطها: نحاول مباشرة، إذا فشلت نطلب كلمة المرور
        result, msg = system.complete_account(phone, code)
        if result:
            system.user_state = ''
            await event.reply(f'✅ {msg}', buttons=main_menu())
        elif '2FA' in msg:
            system.pending_phone = phone
            system.pending_code = code
            system.user_state = 'awaiting_2fa'
            await event.reply('⚠️ الحساب محمي بـ 2FA. ارسل كلمة المرور:')
        else:
            system.user_state = ''
            await event.reply(f'❌ {msg}', buttons=main_menu())
        return

    if state == 'awaiting_2fa':
        password = text
        phone = getattr(system, 'pending_phone', '')
        code = getattr(system, 'pending_code', '')
        if not phone or not code:
            system.user_state = ''
            await event.reply('❌ حدث خطأ، حاول مجدداً.', buttons=main_menu())
            return
        result, msg = system.complete_account(phone, code, password)
        system.user_state = ''
        await event.reply(f'✅ {msg}' if result else f'❌ {msg}', buttons=main_menu())
        return

    if state == 'awaiting_post':
        result, msg = system.add_post(text)
        system.user_state = ''
        posts, selected = system.get_posts_list()
        if posts:
            await event.reply(msg if result else f'❌ {msg}', buttons=posts_menu(posts, selected))
        else:
            await event.reply(msg if result else f'❌ {msg}', buttons=main_menu())
        return

    if state == 'awaiting_comment':
        result, msg = system.add_comment(text)
        system.user_state = ''
        comments, active = system.get_comments_list()
        if comments:
            await event.reply(msg if result else f'❌ {msg}', buttons=comments_menu(comments, active))
        else:
            await event.reply(msg if result else f'❌ {msg}', buttons=main_menu())
        return

    # معالجة الضغط على أزرار الحسابات (لأن الكولباك لا يعمل مع الأزرار النصية العادية)
    # هنا نتعامل مع النصوص التي تشبه أزرار الحسابات
    accounts = system.get_accounts_list()
    for phone, name in accounts:
        if text == f"✅ {name} ({phone})" or text == f"⬜ {name} ({phone})":
            added, msg = system.toggle_account_selection(phone)
            await event.reply(msg, buttons=accounts_menu(accounts))
            return

    # معالجة النصوص التي تشبه أزرار المنشورات
    posts, selected = system.get_posts_list()
    for i, post in enumerate(posts):
        if text == f"[x] {post[:30]}..." or text == f"[ ] {post[:30]}...":
            result, msg = system.toggle_post(i)
            posts, selected = system.get_posts_list()
            await event.reply(msg if result else f'❌ {msg}', buttons=posts_menu(posts, selected))
            return

    # معالجة النصوص التي تشبه أزرار التعليقات
    comments, active = system.get_comments_list()
    for i, c in enumerate(comments):
        if text == f"✅ {c[:20]}..." or text == f"⬜ {c[:20]}...":
            result, msg = system.set_active_comment(i)
            comments, active = system.get_comments_list()
            await event.reply(msg if result else f'❌ {msg}', buttons=comments_menu(comments, active))
            return

    await event.reply('استخدم الأزرار أو الأوامر من القائمة.', buttons=main_menu())

print('البوت يعمل بنظام xw38 مع الأزرار والأوامر...')
asyncio.run(bot.run_until_disconnected())
