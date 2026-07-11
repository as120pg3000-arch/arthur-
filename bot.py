from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8932758513:AAFL8_-ZrTsMVsPz99rw87i2DJciuamE9yo"
OWNER_ID = 67769767

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال 100% أرسل لي صورة")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    
    # احذف الصورة فوراً
    await message.delete()
    
    # رد بالرسالة المطلوبة
    mention = f"@{user.username}" if user.username else user.first_name
    await message.reply_text(
        f"🚫 **تم العثور على محتوى الاباحي سيتم حذفه**\n"
        f"👤 المرسل: {mention} (ID: `{user.id}`)",
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🤖 بوت الاختبار شغال...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
