import telebot
from telebot import types
import random
from datetime import datetime

# التوكن الخاص بك
TOKEN = '8635193672:AAE3DJlsOuTPJhviBugWdrJ1vTVO7l_kF6U'
bot = telebot.TeleBot(TOKEN)

# التخزين
storage = []
user_state = {}

# القائمة الرئيسية
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [
        "🌦 الطقس", "⏰ الوقت", "💾 التخزين", "😂 النكت", 
        "🗓 السنة الهجرية", "👑 الملك", "🍑 الطيز", "❤️ يحبج ام جلال", 
        "🐈 قطيتك", "🚫 فارغ"
    ]
    markup.add(*[types.KeyboardButton(b) for b in btns])
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بك في بوت ارثر الشامل! اختر من القائمة:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text
    chat_id = message.chat.id

    if text == "🌦 الطقس":
        bot.send_message(chat_id, "الطقس في جسر ديالى الآن مشمس ودرجة الحرارة مناسبة للصيف.", reply_markup=main_menu())

    elif text == "⏰ الوقت":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add("العراق", "أمريكا", "إنجلترا", "طوكيو", "الصين", "⬅️ رجوع")
        bot.send_message(chat_id, "اختر الدولة لمعرفة الوقت:", reply_markup=markup)

    elif text in ["العراق", "أمريكا", "إنجلترا", "طوكيو", "الصين"]:
        bot.send_message(chat_id, f"الوقت الآن في {text} هو: {datetime.now().strftime('%H:%M')}", reply_markup=main_menu())

    elif text == "💾 التخزين":
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add("📂 المخزن", "📥 تخزين", "⬅️ رجوع")
        bot.send_message(chat_id, "ماذا تريد أن تفعل؟", reply_markup=markup)

    elif text == "📂 المخزن":
        msg = "\n".join(storage) if storage else "المخزن فارغ حالياً."
        bot.send_message(chat_id, msg, reply_markup=main_menu())

    elif text == "📥 تخزين":
        user_state[chat_id] = "waiting_for_text"
        bot.send_message(chat_id, "أرسل الكلام الذي تريد تخزينه:")

    elif text == "😂 النكت":
        jokes = [f"نكتة {i}: هذا دراكون سأل نفسه سؤال وما عرف يجاوب!" for i in range(1, 51)]
        bot.send_message(chat_id, random.choice(jokes), reply_markup=main_menu())

    elif text == "🗓 السنة الهجرية":
        bot.send_message(chat_id, "السنة الهجرية: 1448 هـ - شهر محرم.", reply_markup=main_menu())

    elif text == "👑 الملك":
        bot.send_message(chat_id, "ارثر هو الملك الأسطوري الذي لا يقهر! 👑", reply_markup=main_menu())

    elif text == "🍑 الطيز":
        bully = ["دراكون يا تيس...", "دراكون غبي...", "دراكون أنت فاشل..."]
        bot.send_message(chat_id, f"تنمر على دراكون: {random.choice(bully)}", reply_markup=main_menu())

    elif text == "❤️ يحبج ام جلال":
        names = ["ارثر", "دراكون", "علي", "سيف", "عمر"] + ["شخص عشوائي"] * 45
        bot.send_message(chat_id, f"{random.choice(names)} يحبج ام جلال", reply_markup=main_menu())

    elif text == "🐈 قطيتك":
        bot.send_message(chat_id, "قطيتك رسمي يا بعد روحي! 🐈", reply_markup=main_menu())

    elif text == "🚫 فارغ":
        bot.send_message(chat_id, "معوزين وهمي.. لا يوجد شيء هنا!", reply_markup=main_menu())

    elif text == "⬅️ رجوع":
        bot.send_message(chat_id, "القائمة الرئيسية:", reply_markup=main_menu())

    elif user_state.get(chat_id) == "waiting_for_text":
        storage.append(text)
        user_state[chat_id] = None
        bot.send_message(chat_id, "تم التخزين بنجاح!", reply_markup=main_menu())

bot.infinity_polling()
