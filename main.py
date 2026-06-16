import telebot
import requests

# التوكن الخاص بك
TOKEN = '8635193672:AAE3DJlsOuTPJhviBugWdrJ1vTVO7l_kF6U'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! البوت يعمل الآن. أرسل /gifts لعرض قائمة الهدايا وأسعارها.")

@bot.message_handler(commands=['gifts'])
def get_gifts(message):
    try:
        # جلب الهدايا من API تيليجرام
        url = f"https://api.telegram.org/bot{TOKEN}/getAvailableGifts"
        response = requests.get(url).json()
        
        if response.get("ok"):
            gifts = response["result"]["gifts"]
            if not gifts:
                bot.reply_to(message, "لا توجد هدايا متاحة حالياً.")
                return

            reply = "🎁 **الهدايا المتاحة حالياً:**\n\n"
            for gift in gifts:
                name = gift.get("name", "هدية")
                price = gift.get("star_count", 0)
                reply += f"✨ {name}: **{price}** نجمة\n"
            
            bot.reply_to(message, reply, parse_mode="Markdown")
        else:
            bot.reply_to(message, "حدث خطأ أثناء جلب الهدايا من السيرفر.")
            
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ برمجياً: {str(e)}")

# تشغيل البوت
print("البوت بدأ العمل...")
bot.infinity_polling()

                                
