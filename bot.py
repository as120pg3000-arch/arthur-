import io
import logging
from PIL import Image
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import torch
from transformers import pipeline

TOKEN = "8932758513:AAFL8_-ZrTsMVsPz99rw87i2DJciuamE9yo"
OWNER_ID = 67769767

print("⏳ جاري تحميل النموذج... (انتظر)")
device = 0 if torch.cuda.is_available() else -1
nsfw_pipe = pipeline("image-classification", model="Falconsai/nsfw_image_detection", device=device)
print("✅ النموذج جاهز")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت شغال ✅ ارسل لي صوره لأختبرها")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    message = update.message
    
    # 🔥 طباعة معلومات التشخيص في سيرفرك (شوفها بلogs)
    print(f"📩 استلمت صورة من {user.id} في دردشة {chat_id}")

    try:
        photo_file = await message.photo[-1].get_file()
        file_bytes = await photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(file_bytes))
        results = nsfw_pipe(image)
        
        is_nsfw = False
        for res in results:
            if res['label'].lower() == 'nsfw' and res['score'] >= 0.8:
                is_nsfw = True
                break
        
        if is_nsfw:
            await message.delete()
            mention = f"@{user.username}" if user.username else user.first_name
            await message.reply_text(
                f"🚫 تم العثور على محتوى الاباحي سيتم حذفه\n"
                f"👤 المرسل: {mention} (ID: `{user.id}`)",
                parse_mode="Markdown"
            )
            print("✅ تم الحذف")
        else:
            await message.reply_text("✅ الصورة آمنة")
            print("✅ آمنة")
    except Exception as e:
        print(f"❌ خطأ: {e}")
        await message.reply_text("حدث خطأ تقني")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🤖 البوت شغال... ارسل له صور بالخاص أو بالمجموعة")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
