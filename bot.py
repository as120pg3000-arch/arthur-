import io
import logging
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, CommandHandler, ContextTypes, filters
from transformers import pipeline
import torch

# ================== إعداداتك ==================
TOKEN = "8932758513:AAFL8_-ZrTsMVsPz99rw87i2DJciuamE9yo"
OWNER_ID = 67769767
THRESHOLD = 0.8  # نسبة الثقة (80%)
# =============================================

# قائمة المجموعات النشطة (يحفظها بالذاكرة، عند إعادة التشغيل تحتاج إعادة إضافتها)
active_chats = set()

# تحميل نموذج الذكاء الاصطناعي
print("⏳ جاري تحميل نموذج الكشف...")
device = 0 if torch.cuda.is_available() else -1
nsfw_pipe = pipeline("image-classification", model="Falconsai/nsfw_image_detection", device=device)
print("✅ النموذج جاهز!")

# ========== دالة التحقق من المالك ==========
def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID

# ========== أمر /start للمالك ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.message.reply_text("⛔ هذا البوت للمطور فقط.")
        return

    keyboard = [
        [InlineKeyboardButton("➕ اضف مجموعه", callback_data="add_chat")],
        [InlineKeyboardButton("➖ مسح مجموعه", callback_data="remove_chat")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌟 **مرحبا ببوت الاباحي المطور @mustafa0121**\n\n"
        "اختر الإجراء المناسب:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ========== معالج الأزرار ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if user.id != OWNER_ID:
        await query.edit_message_text("⛔ هذا الأمر للمالك فقط.")
        return

    if query.data == "add_chat":
        context.user_data['state'] = 'waiting_chat_id_add'
        await query.edit_message_text(
            "📥 **أرسل لي الآن معرف المجموعة (chat_id) لتفعيل البوت فيها.**\n"
            "مثال: `-1001234567890`\n"
            "(يمكنك الحصول عليه من بوت @getmyid_bot)"
        )
    elif query.data == "remove_chat":
        context.user_data['state'] = 'waiting_chat_id_remove'
        await query.edit_message_text(
            "📤 **أرسل لي معرف المجموعة لإزالتها من القائمة النشطة.**"
        )

# ========== استقبال المعرف من المالك ==========
async def handle_owner_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    text = update.message.text.strip()
    state = context.user_data.get('state')

    if state == 'waiting_chat_id_add':
        try:
            chat_id = int(text)
            active_chats.add(chat_id)
            await update.message.reply_text(f"✅ تم تفعيل المجموعة `{chat_id}` بنجاح!")
            context.user_data['state'] = None
        except ValueError:
            await update.message.reply_text("❌ خطأ: الرجاء إرسال أرقام فقط (chat_id).")

    elif state == 'waiting_chat_id_remove':
        try:
            chat_id = int(text)
            if chat_id in active_chats:
                active_chats.remove(chat_id)
                await update.message.reply_text(f"✅ تم إلغاء تفعيل المجموعة `{chat_id}`.")
            else:
                await update.message.reply_text(f"⚠️ المجموعة `{chat_id}` غير مفعلة أساساً.")
            context.user_data['state'] = None
        except ValueError:
            await update.message.reply_text("❌ خطأ: الرجاء إرسال أرقام فقط (chat_id).")

# ========== كشف الصور وحذفها ==========
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # هل البوت مفعل في هذه المجموعة؟
    if chat_id not in active_chats:
        return

    message = update.message
    user = update.effective_user

    try:
        # تحميل الصورة
        photo_file = await message.photo[-1].get_file()
        file_bytes = await photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(file_bytes))

        # تحليلها
        results = nsfw_pipe(image)
        is_nsfw = False
        for res in results:
            if res['label'].lower() == 'nsfw' and res['score'] >= THRESHOLD:
                is_nsfw = True
                break

        if is_nsfw:
            await message.delete()  # حذف الصورة

            # تحضير معلومات المرسل
            mention = f"@{user.username}" if user.username else user.first_name
            await message.reply_text(
                f"🚫 **تم العثور على محتوى الاباحي سيتم حذفه**\n"
                f"👤 المرسل: {mention} (ID: `{user.id}`)\n"
                f"✅ تم حذف المحتوى المخالف.",
                parse_mode="Markdown"
            )
    except Exception as e:
        logging.error(f"خطأ أثناء المعالجة: {e}")

# ========== التشغيل الرئيسي ==========
def main():
    app = Application.builder().token(TOKEN).build()

    # الأوامر
    app.add_handler(CommandHandler("start", start))

    # الأزرار
    app.add_handler(CallbackQueryHandler(button_handler))

    # استقبال نصوص المالك (chat_id)
    app.add_handler(MessageHandler(filters.TEXT & filters.USER(OWNER_ID), handle_owner_text))

    # كشف الصور في المجموعات
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 البوت يعمل...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
