import telebot
from telebot import types
import random

TOKEN = '8635193672:AAE3DJlsOuTPJhviBugWdrJ1vTVO7l_kF6U'
bot = telebot.TeleBot(TOKEN)

def wansa_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # الأزرار الأربعة المطلوبة
    btns = ["اهات", "عدد نيجاتك", "حالتك", "البعصه"]
    markup.add(*[types.KeyboardButton(b) for b in btns])
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "البوت جاهز.. اختار من القائمة:", reply_markup=wansa_menu())

@bot.message_handler(func=lambda message: True)
def handle_wansa(message):
    text = message.text
    chat_id = message.chat.id
    
    if text == "اهات":
        bot.send_message(chat_id, "اه دراكون", reply_markup=wansa_menu())
        
    elif text == "عدد نيجاتك":
        # 10 أرقام عشوائية
        random_nums = [str(random.randint(1, 100)) for _ in range(10)]
        bot.send_message(chat_id, f"أرقامك: {', '.join(random_nums)}", reply_markup=wansa_menu())
        
    elif text == "حالتك":
        status = ["شريف", "مزروف"]
        bot.send_message(chat_id, f"أنت: {random.choice(status)}", reply_markup=wansa_menu())
        
    elif text == "البعصه":
        bot.send_message(chat_id, "بعصتك", reply_markup=wansa_menu())

print("البوت يعمل...")
bot.infinity_polling()
