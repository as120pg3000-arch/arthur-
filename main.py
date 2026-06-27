# ============================================================
# بوت تحميل يوتيوب مع البحث والاختيار التفاعلي
# ============================================================
# التثبيت:
# pip install python-telegram-bot yt-dlp
# ============================================================

import os
import re
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import asyncio
import logging

# ========== الإعدادات الأساسية ==========
TOKEN = "8913342850:AAGZZvYz3Gfo-cCWQG1z1AFlGkSRe52GAQE"
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# تفعيل التسجيل للأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== دوال مساعدة ==========
def sanitize_filename(title):
    """إزالة الأحرف غير المسموح بها من اسم الملف"""
    return re.sub(r'[<>:"/\\|?*]', '_', title)

def search_youtube(query, max_results=5):
    """
    البحث عن مقاطع في يوتيوب وإرجاع قائمة بالنتائج
    كل نتيجة تحتوي على: عنوان، رابط، مدة، قناة
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # لا نحتاج تفاصيل كاملة
        'force_generic_extractor': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخدام البحث المدمج
            search_query = f"ytsearch{max_results}:{query}"
            info = ydl.extract_info(search_query, download=False)
            entries = info.get('entries', [])
            results = []
            for entry in entries:
                results.append({
                    'title': entry.get('title', 'بدون عنوان'),
                    'url': f"https://youtube.com/watch?v={entry.get('id', '')}",
                    'duration': entry.get('duration', 0),
                    'uploader': entry.get('uploader', 'غير معروف'),
                })
            return results
    except Exception as e:
        logger.error(f"خطأ في البحث: {e}")
        return []

def get_video_formats(url):
    """
    الحصول على قائمة الصيغ المتاحة (جودة الفيديو والصوت)
    نرجع قائمة تحتوي على: (الوصف, format_id, نوع)
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            # استخراج الصيغ المفيدة (فيديو+صوت مدمج، أو فيديو فقط، أو صوت فقط)
            # سنبني قائمة فريدة من الجودات
            quality_set = set()
            video_formats = []
            audio_formats = []

            # تجميع أفضل الصيغ لكل جودة
            for f in formats:
                # تخطي الصيغ الغريبة
                if not f.get('vcodec') and not f.get('acodec'):
                    continue
                resolution = f.get('resolution', '')
                height = f.get('height', 0)
                if height and height > 0:
                    # فيديو
                    if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                        # صيغة مدمجة (فيديو+صوت)
                        if height not in quality_set:
                            quality_set.add(height)
                            video_formats.append({
                                'description': f"{height}p (فيديو+صوت)",
                                'format_id': f['format_id'],
                                'type': 'video_audio'
                            })
                    elif f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                        # فيديو فقط (بحاجة لدمج مع صوت)
                        if height not in quality_set:
                            quality_set.add(height)
                            video_formats.append({
                                'description': f"{height}p (فيديو فقط، يحتاج دمج مع صوت)",
                                'format_id': f['format_id'],
                                'type': 'video_only'
                            })
                elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    # صوت فقط
                    audio_formats.append({
                        'description': f"صوت {f.get('abr', '')}kbps",
                        'format_id': f['format_id'],
                        'type': 'audio'
                    })

            # ترتيب الفيديو تنازلياً حسب الجودة
            video_formats.sort(key=lambda x: int(re.search(r'(\d+)p', x['description']).group(1)) if re.search(r'(\d+)p', x['description']) else 0, reverse=True)
            # اختيار أفضل صوت (أعلى معدل بت)
            audio_formats.sort(key=lambda x: int(re.search(r'(\d+)kbps', x['description']).group(1)) if re.search(r'(\d+)kbps', x['description']) else 0, reverse=True)

            # إذا لم نجد صيغ مناسبة، نضيف صيغة "best" كخيار
            if not video_formats and not audio_formats:
                return [{'description': 'أفضل جودة (افتراضي)', 'format_id': 'best', 'type': 'best'}]

            # نعيد قائمة الخيارات (فيديو ثم صوت)
            options = []
            # إضافة فيديو (أفضل 3 جودات)
            for f in video_formats[:3]:
                options.append(f)
            # إضافة أفضل صوت (واحد)
            if audio_formats:
                options.append(audio_formats[0])
            # إذا لم نجد فيديو، نضيف خيار الصوت فقط
            if not video_formats and audio_formats:
                options.append(audio_formats[0])

            return options
    except Exception as e:
        logger.error(f"خطأ في جلب الصيغ: {e}")
        return []

def download_video(url, format_id, quality_type):
    """
    تحميل الفيديو بالصيغة المحددة
    نعيد مسار الملف المحمل
    """
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'format': format_id,
        'merge_output_format': 'mp4',  # إذا كان دمج مطلوب
        'postprocessors': []
    }

    # إذا كان الصوت فقط، نضبط postprocessors
    if quality_type == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        # تغيير الامتداد النهائي
        ydl_opts['outtmpl'] = os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s')
        # نضمن أن الصيغة هي bestaudio
        if format_id == 'best' or not format_id:
            ydl_opts['format'] = 'bestaudio/best'
    else:
        # إذا كانت صيغة فيديو فقط أو مدمجة
        if quality_type == 'video_only':
            # نحتاج إلى دمج مع الصوت، نستخدم format مع +bestaudio
            ydl_opts['format'] = f"{format_id}+bestaudio/best"
            ydl_opts['merge_output_format'] = 'mp4'
        elif quality_type == 'video_audio':
            ydl_opts['format'] = format_id
        else:  # best
            ydl_opts['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # قد يكون الملف بامتداد مختلف إذا تم التحويل
            if quality_type == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            # التأكد من وجود الملف
            if not os.path.exists(filename):
                # ربما الاسم مختلف بسبب الدمج
                # نبحث عن ملف يحمل نفس العنوان
                base = os.path.join(DOWNLOAD_PATH, sanitize_filename(info.get('title', 'video')))
                for ext in ['.mp4', '.mkv', '.webm', '.mp3']:
                    test = base + ext
                    if os.path.exists(test):
                        filename = test
                        break
            if os.path.exists(filename):
                return filename
            else:
                # قد يكون الملف محفوظاً باسم آخر، نحاول العثور عليه
                files = os.listdir(DOWNLOAD_PATH)
                for f in files:
                    if info.get('title', '') in f:
                        return os.path.join(DOWNLOAD_PATH, f)
                return None
    except Exception as e:
        logger.error(f"فشل التحميل: {e}")
        return None

# ========== دوال البوت ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة ترحيب"""
    await update.message.reply_text(
        "👋 مرحباً! أرسل لي رابط فيديو يوتيوب لتحميله، أو اكتب اسم فيديو للبحث عنه.\n"
        "مثال: 'أغنية حب' أو رابط مثل https://youtube.com/watch?v=...\n"
        "سأعرض لك 5 نتائج للاختيار منها، ثم خيارات الجودة."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية"""
    text = update.message.text.strip()
    if not text:
        return

    # التحقق إذا كان الرابط
    if re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/', text):
        # رابط مباشر، نعرض خيارات التحميل فوراً
        await show_format_options(update, context, text)
        return

    # بحث
    await search_and_show(update, context, text)

async def search_and_show(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str):
    """البحث وعرض 5 نتائج كأزرار"""
    await update.message.reply_text(f"🔍 جاري البحث عن: {query} ...")
    results = search_youtube(query, max_results=5)
    if not results:
        await update.message.reply_text("❌ لم أجد نتائج لهذا البحث.")
        return

    # بناء الأزرار
    keyboard = []
    for idx, item in enumerate(results):
        title = item['title'][:50] + "..." if len(item['title']) > 50 else item['title']
        # نضيف رقم تسلسلي أو رمز
        button_text = f"{idx+1}. {title}"
        callback_data = f"vid_{idx}"  # سنخزن النتائج في context.user_data
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

    # زر إلغاء
    keyboard.append([InlineKeyboardButton("❌ إلغاء", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    # حفظ النتائج في user_data
    context.user_data['search_results'] = results
    await update.message.reply_text("📋 اختر المقطع المطلوب:", reply_markup=reply_markup)

async def show_format_options(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str, edit=True):
    """عرض خيارات الصيغ للمقطع المحدد"""
    # جلب الصيغ
    formats = get_video_formats(url)
    if not formats:
        if edit:
            await update.callback_query.edit_message_text("❌ لا يمكن الحصول على خيارات التحميل.")
        else:
            await update.message.reply_text("❌ لا يمكن الحصول على خيارات التحميل.")
        return

    # تخزين الرابط في user_data
    context.user_data['current_url'] = url

    # بناء الأزرار
    keyboard = []
    for f in formats:
        desc = f['description']
        callback_data = f"dl_{f['format_id']}_{f['type']}"
        keyboard.append([InlineKeyboardButton(desc, callback_data=callback_data)])

    keyboard.append([InlineKeyboardButton("❌ إلغاء", callback_data="cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if edit:
        await update.callback_query.edit_message_text(
            "🎯 اختر الجودة المطلوبة:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "🎯 اختر الجودة المطلوبة:",
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة ضغط الأزرار"""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "cancel":
        await query.edit_message_text("❌ تم الإلغاء.")
        return

    # معالجة اختيار نتيجة بحث
    if data.startswith("vid_"):
        index = int(data.split("_")[1])
        results = context.user_data.get('search_results', [])
        if not results or index >= len(results):
            await query.edit_message_text("❌ حدث خطأ، حاول مجدداً.")
            return
        selected = results[index]
        url = selected['url']
        # عرض خيارات التحميل لهذا المقطع
        await show_format_options(update, context, url, edit=True)
        return

    # معالجة اختيار جودة التحميل
    if data.startswith("dl_"):
        parts = data.split("_")
        if len(parts) < 3:
            await query.edit_message_text("❌ بيانات غير صحيحة.")
            return
        format_id = parts[1]
        quality_type = parts[2]
        url = context.user_data.get('current_url')
        if not url:
            await query.edit_message_text("❌ لا يوجد رابط للتحميل.")
            return

        # إعلام المستخدم بالبدء
        await query.edit_message_text("⏳ جاري التحميل... قد يستغرق بعض الوقت.")

        # تحميل الملف (في الخلفية)
        try:
            # نرسل رسالة مؤقتة
            msg = await query.message.reply_text("⏳ جاري التحميل...")

            # تحميل الملف (متزامن، لكن نستخدم run_in_executor لتجنب حظر)
            loop = asyncio.get_event_loop()
            filename = await loop.run_in_executor(None, download_video, url, format_id, quality_type)

            if filename and os.path.exists(filename):
                # إرسال الملف
                with open(filename, 'rb') as f:
                    await query.message.reply_document(document=f, caption="✅ تم التحميل بنجاح!")
                # حذف الملف بعد الإرسال (اختياري)
                os.remove(filename)
                await msg.delete()
                await query.edit_message_text("✅ اكتمل التحميل.")
            else:
                await query.edit_message_text("❌ فشل التحميل. حاول مرة أخرى أو اختر جودة أخرى.")
        except Exception as e:
            logger.error(f"خطأ في التحميل: {e}")
            await query.edit_message_text(f"❌ حدث خطأ: {e}")

# ========== التشغيل ==========
def main():
    """تشغيل البوت"""
    application = Application.builder().token(TOKEN).build()

    # أوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))

    # بدء البوت
    print("✅ البوت يعمل...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
