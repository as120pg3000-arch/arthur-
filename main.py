import telebot
from telebot import types
import random

TOKEN = '8635193672:AAE3DJlsOuTPJhviBugWdrJ1vTVO7l_kF6U'
bot = telebot.TeleBot(TOKEN)

# قاموس لتخزين اليوزرات (Username -> ChatID)
users_db = {}
# التخزين العام
storage = []
user_state = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = ["🌦 الطقس", "⏰ الوقت", "💾 التخزين", "😂 النكت", "🗓 السنة الهجرية", 
            "👑 الملك", "🍑 الطيز", "❤️ يحبج ام جلال", "🐈 قطيتك", "💬 دردشة"]
    markup.add(*[types.KeyboardButton(b) for b in btns])
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    # تسجيل المستخدم في القاعدة عند الضغط على ستارت
    if message.from_user.username:
        users_db[message.from_user.username.lower()] = message.chat.id
    bot.send_message(message.chat.id, "أهلاً بك! تم تسجيلك في نظام البوت.", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id
    
    if text == "💬 دردشة":
        user_state[chat_id] = "waiting_for_user"
        bot.send_message(chat_id, "أرسل لي 'يوزر' الشخص (بدون @) لطلب الدردشة معه:")
    
    elif user_state.get(chat_id) == "waiting_for_user":
        target_username = text.lower().replace("@", "")
        if target_username in users_db:
            target_id = users_db[target_username]
            user_state[chat_id] = f"chatting_with_{target_id}"
            bot.send_message(target_id, f"المستخدم @{message.from_user.username} يريد الدردشة معك! أرسل 'موافق' للبدء.")
            bot.send_message(chat_id, "تم إرسال طلب الدردشة، انتظر الموافقة.")
        else:
            bot.send_message(chat_id, "هذا الشخص غير موجود في البوت (يجب أن يضغط /start أولاً).")
        user_state[chat_id] = None

    elif text.lower() == "موافق":
        # منطق بسيط للموافقة (يمكن تطويره)
        bot.send_message(chat_id, "تم فتح الدردشة! أرسل رسالتك الآن.")
        
    elif text == "⬅️ رجوع":
        bot.send_message(chat_id, "القائمة الرئيسية:", reply_markup=main_menu())
    
    else:
        # الأزرار الأخرى كما كانت...
        bot.send_message(chat_id, "أمر غير معروف، جرب الضغط على الأزرار.", reply_markup=main_menu())

print("البوت يعمل الآن يا أرثر...")
bot.infinity_polling()
