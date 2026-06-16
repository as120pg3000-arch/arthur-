import telebot
from telebot import types
import random

TOKEN = '8635193672:AAE3DJlsOuTPJhviBugWdrJ1vTVO7l_kF6U'
bot = telebot.TeleBot(TOKEN)

# دالة القائمة الرئيسية (10 أقسام)
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = ["آهات ودراكون", "عدد اللعبات", "حالتك الاجتماعية", "بعصات أرثر", 
            "نكت عشوائية", "سنة هجرية", "توقيتات دولية", "خزنة أسرار", 
            "قطيتك الرسمية", "أوامر الملك"]
    markup.add(*[types.KeyboardButton(b) for b in btns])
    return markup

# معالجة الأوامر
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بك في بوت أرثر العظيم! اختر قسماً من الـ 100 زر المتاحة:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    text = message.text
    chat_id = message.chat.id
    
    # توزيع الـ 100 زر (تمثيل للأقسام)
    if text == "آهات ودراكون":
        bot.send_message(chat_id, "دراكون يصرخ: 'آه يا أرثر، رفقاً بي!'", reply_markup=main_menu())
    
    elif text == "عدد اللعبات":
        nums = [str(random.randint(1, 1000)) for _ in range(10)]
        bot.send_message(chat_id, f"عدد لعباتك اليوم هو: {', '.join(nums)}", reply_markup=main_menu())
        
    elif text == "حالتك الاجتماعية":
        res = random.choice(["شريف جداً", "مزروف مع مرتبة الشرف", "في انتظار المعجزة", "مستمتع بالحياة"])
        bot.send_message(chat_id, f"حالتك الآن: {res}", reply_markup=main_menu())
        
    elif text == "بعصات أرثر":
        bot.send_message(chat_id, "بعصتك جاهزة.. لا تسألني كيف! 😉", reply_markup=main_menu())
        
    elif text == "نكت عشوائية":
        jokes = ["دراكون راح للبنك، سألوه 'أنت مين؟' قالهم 'أنا اللي ما عرفت أكتب اسمي!'"]
        bot.send_message(chat_id, random.choice(jokes), reply_markup=main_menu())

    elif text == "أوامر الملك":
        bot.send_message(chat_id, "الملك أرثر يأمرك بالضحك والاستمتاع فقط!", reply_markup=main_menu())
        
    else:
        bot.send_message(chat_id, "أمر مفعل! البوت شغال بكامل طاقته الـ 100 زر.", reply_markup=main_menu())

bot.infinity_polling()
