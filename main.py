import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============ توكن البوت ============
BOT_TOKEN = "8635193672:AAE3DJlsOuTPJhviBugWdrJ1vTVO7l_kF6U"

# ============ دالة بدء التشغيل ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📂 القائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌟 *مرحباً بك في البوت المتطور!*\n"
        "اضغط على الزر أدناه لعرض القائمة الرئيسية.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ القائمة الرئيسية (12 قسم) ============
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🎬 أفلام ومسلسلات", callback_data="menu_movies"),
         InlineKeyboardButton("🎵 موسيقى وصوتيات", callback_data="menu_music")],
        [InlineKeyboardButton("📚 كتب ومكتبة", callback_data="menu_books"),
         InlineKeyboardButton("🎮 ألعاب", callback_data="menu_games")],
        [InlineKeyboardButton("🛒 متجر", callback_data="menu_shop"),
         InlineKeyboardButton("💰 خدمات مالية", callback_data="menu_finance")],
        [InlineKeyboardButton("🌐 أدوات ويب", callback_data="menu_web"),
         InlineKeyboardButton("📱 تطبيقات", callback_data="menu_apps")],
        [InlineKeyboardButton("🤖 ذكاء اصطناعي", callback_data="menu_ai"),
         InlineKeyboardButton("🔐 أمان وحماية", callback_data="menu_security")],
        [InlineKeyboardButton("📊 إحصائيات", callback_data="menu_stats"),
         InlineKeyboardButton("⚙️ الإعدادات", callback_data="menu_settings")],
        [InlineKeyboardButton("🏠 الرجوع للبداية", callback_data="back_to_start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📋 *القائمة الرئيسية*\nاختر القسم الذي تريده:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ أزرار الأفلام والمسلسلات ============
async def menu_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🎬 أفلام أكشن", callback_data="movies_action"),
         InlineKeyboardButton("😂 أفلام كوميدية", callback_data="movies_comedy")],
        [InlineKeyboardButton("😱 أفلام رعب", callback_data="movies_horror"),
         InlineKeyboardButton("🔮 أفلام خيال علمي", callback_data="movies_scifi")],
        [InlineKeyboardButton("💕 أفلام رومانسية", callback_data="movies_romance"),
         InlineKeyboardButton("🎭 أفلام دراما", callback_data="movies_drama")],
        [InlineKeyboardButton("📺 مسلسلات تركية", callback_data="series_turkish"),
         InlineKeyboardButton("📺 مسلسلات أجنبية", callback_data="series_foreign")],
        [InlineKeyboardButton("📺 مسلسلات عربية", callback_data="series_arabic"),
         InlineKeyboardButton("🎞 مسلسلات كرتون", callback_data="series_cartoon")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎬 *قسم الأفلام والمسلسلات*\nاختر التصنيف:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ أزرار الموسيقى ============
async def menu_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🎵 موسيقى هادئة", callback_data="music_calm"),
         InlineKeyboardButton("🎸 موسيقى روك", callback_data="music_rock")],
        [InlineKeyboardButton("🎹 موسيقى كلاسيكية", callback_data="music_classic"),
         InlineKeyboardButton("🎤 أغاني عربية", callback_data="music_arabic")],
        [InlineKeyboardButton("🎤 أغاني أجنبية", callback_data="music_foreign"),
         InlineKeyboardButton("🎧 بودكاست", callback_data="music_podcast")],
        [InlineKeyboardButton("🎼 نغمات", callback_data="music_ringtones"),
         InlineKeyboardButton("🥁 إيقاعات", callback_data="music_beats")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎵 *قسم الموسيقى والصوتيات*\nاختر النوع:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ أزرار الكتب ============
async def menu_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📖 روايات", callback_data="books_novels"),
         InlineKeyboardButton("📚 كتب علمية", callback_data="books_science")],
        [InlineKeyboardButton("📚 كتب تاريخ", callback_data="books_history"),
         InlineKeyboardButton("📚 كتب فلسفة", callback_data="books_philosophy")],
        [InlineKeyboardButton("📚 كتب دينية", callback_data="books_religion"),
         InlineKeyboardButton("📚 كتب برمجة", callback_data="books_programming")],
        [InlineKeyboardButton("📚 كتب تطوير ذاتي", callback_data="books_selfdev"),
         InlineKeyboardButton("📚 كتب طبخ", callback_data="books_cooking")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📚 *قسم الكتب والمكتبة*\nاختر النوع:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ أزرار الألعاب ============
async def menu_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🎮 ألعاب كمبيوتر", callback_data="games_pc"),
         InlineKeyboardButton("📱 ألعاب موبايل", callback_data="games_mobile")],
        [InlineKeyboardButton("🕹 ألعاب بلايستيشن", callback_data="games_ps"),
         InlineKeyboardButton("🎲 ألعاب جماعية", callback_data="games_multiplayer")],
        [InlineKeyboardButton("🧩 ألغاز", callback_data="games_puzzles"),
         InlineKeyboardButton("🏆 بطولات", callback_data="games_tournaments")],
        [InlineKeyboardButton("🃏 ألعاب ورق", callback_data="games_cards"),
         InlineKeyboardButton("🎯 ألعاب تصويب", callback_data="games_shooting")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎮 *قسم الألعاب*\nاختر النوع:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ أزرار المتجر ============
async def menu_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("👕 ملابس", callback_data="shop_clothes"),
         InlineKeyboardButton("📱 إلكترونيات", callback_data="shop_electronics")],
        [InlineKeyboardButton("🏠 أدوات منزلية", callback_data="shop_home"),
         InlineKeyboardButton("💄 مستحضرات تجميل", callback_data="shop_cosmetics")],
        [InlineKeyboardButton("🍔 طعام", callback_data="shop_food"),
         InlineKeyboardButton("🎁 هدايا", callback_data="shop_gifts")],
        [InlineKeyboardButton("🛒 سلة المشتريات", callback_data="shop_cart"),
         InlineKeyboardButton("⭐ المفضلة", callback_data="shop_favorites")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🛒 *قسم المتجر*\nاختر القسم:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ باقي الأقسام بنفس النمط ============
async def menu_finance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("💱 صرف عملات", callback_data="finance_exchange"),
         InlineKeyboardButton("📈 أسهم", callback_data="finance_stocks")],
        [InlineKeyboardButton("🏦 بنوك", callback_data="finance_banks"),
         InlineKeyboardButton("💳 بطاقات", callback_data="finance_cards")],
        [InlineKeyboardButton("💰 قروض", callback_data="finance_loans"),
         InlineKeyboardButton("📊 ميزانية", callback_data="finance_budget")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("💰 *قسم الخدمات المالية*", reply_markup=reply_markup, parse_mode="Markdown")

async def menu_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🔍 بحث", callback_data="web_search"),
         InlineKeyboardButton("📥 تحميل", callback_data="web_download")],
        [InlineKeyboardButton("🖼 صور", callback_data="web_images"),
         InlineKeyboardButton("📹 فيديو", callback_data="web_video")],
        [InlineKeyboardButton("🌍 ترجمة", callback_data="web_translate"),
         InlineKeyboardButton("📝 نصوص", callback_data="web_text")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("🌐 *قسم أدوات الويب*", reply_markup=reply_markup, parse_mode="Markdown")

async def menu_apps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📱 أندرويد", callback_data="apps_android"),
         InlineKeyboardButton("🍎 آيفون", callback_data="apps_ios")],
        [InlineKeyboardButton("💻 ويندوز", callback_data="apps_windows"),
         InlineKeyboardButton("🐧 لينكس", callback_data="apps_linux")],
        [InlineKeyboardButton("🔧 أدوات", callback_data="apps_tools"),
         InlineKeyboardButton("🎨 تصميم", callback_data="apps_design")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("📱 *قسم التطبيقات*", reply_markup=reply_markup, parse_mode="Markdown")

async def menu_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("💬 شات", callback_data="ai_chat"),
         InlineKeyboardButton("🖼 توليد صور", callback_data="ai_images")],
        [InlineKeyboardButton("🎵 توليد موسيقى", callback_data="ai_music_gen"),
         InlineKeyboardButton("📝 كتابة نصوص", callback_data="ai_text")],
        [InlineKeyboardButton("🗣 تحويل صوت لنص", callback_data="ai_speech"),
         InlineKeyboardButton("🎥 فيديو", callback_data="ai_video")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("🤖 *قسم الذكاء الاصطناعي*", reply_markup=reply_markup, parse_mode="Markdown")

async def menu_security(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🔑 كلمات سر", callback_data="security_passwords"),
         InlineKeyboardButton("🛡 VPN", callback_data="security_vpn")],
        [InlineKeyboardButton("🔒 تشفير", callback_data="security_encrypt"),
         InlineKeyboardButton("🕵️ فحص روابط", callback_data="security_scan")],
        [InlineKeyboardButton("📧 بريد مؤقت", callback_data="security_temp_mail"),
         InlineKeyboardButton("📱 أرقام وهمية", callback_data="security_fake_number")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("🔐 *قسم الأمان والحماية*", reply_markup=reply_markup, parse_mode="Markdown")

async def menu_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("👥 المستخدمين", callback_data="stats_users"),
         InlineKeyboardButton("📊 النشاط", callback_data="stats_activity")],
        [InlineKeyboardButton("⭐ تقييمات", callback_data="stats_ratings"),
         InlineKeyboardButton("📈 نمو", callback_data="stats_growth")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("📊 *قسم الإحصائيات*", reply_markup=reply_markup, parse_mode="Markdown")

async def menu_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🌍 اللغة", callback_data="settings_language"),
         InlineKeyboardButton("🔔 الإشعارات", callback_data="settings_notifications")],
        [InlineKeyboardButton("🎨 المظهر", callback_data="settings_theme"),
         InlineKeyboardButton("👤 الحساب", callback_data="settings_account")],
        [InlineKeyboardButton("ℹ️ عن البوت", callback_data="settings_about"),
         InlineKeyboardButton("📞 تواصل", callback_data="settings_contact")],
        [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("⚙️ *قسم الإعدادات*", reply_markup=reply_markup, parse_mode="Markdown")

# ============ دوال الأزرار الفردية (تعمل بشكل مستقل) ============
async def movies_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎬 *أفلام الأكشن*\n\n"
        "هنا تجد أفضل أفلام الأكشن:\n"
        "• Fast & Furious\n• John Wick\n• Mission Impossible\n• The Dark Knight\n\n"
        "اختر فيلماً للمزيد من التفاصيل.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")
        ]])
    )

async def movies_comedy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "😂 *أفلام كوميدية*\n\n"
        "اضحك مع أفضل الأفلام الكوميدية:\n"
        "• The Hangover\n• Superbad\n• Deadpool\n• Home Alone",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")
        ]])
    )

async def movies_horror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "😱 *أفلام الرعب*\n\n"
        "للعشاق الرعب فقط:\n"
        "• The Conjuring\n• IT\n• A Quiet Place\n• Get Out",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")
        ]])
    )

async def movies_scifi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔮 *أفلام الخيال العلمي*\n\n"
        "استكشف عوالم المستقبل:\n"
        "• Interstellar\n• Inception\n• The Matrix\n• Avatar",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")
        ]])
    )

# ============ دوال إضافية لباقي الأزرار ============
async def movies_romance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("💕 *أفلام رومانسية*\nThe Notebook, Titanic, La La Land...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")]]))

async def movies_drama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎭 *أفلام دراما*\nThe Shawshank Redemption, Forrest Gump...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")]]))

async def series_turkish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📺 *مسلسلات تركية*\nقيامة أرطغرل, نهضة السلاجقة...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")]]))

async def series_foreign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📺 *مسلسلات أجنبية*\nBreaking Bad, Game of Thrones...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")]]))

async def series_arabic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📺 *مسلسلات عربية*\nالهيبة, باب الحارة...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")]]))

async def series_cartoon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎞 *مسلسلات كرتون*\nSpongeBob, Rick and Morty...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_movies")]]))

# دوال الموسيقى
async def music_calm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎵 *موسيقى هادئة للاسترخاء*", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

async def music_rock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎸 *موسيقى الروك*\nQueen, AC/DC, Metallica...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

async def music_classic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎹 *موسيقى كلاسيكية*\nBeethoven, Mozart, Chopin...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

async def music_arabic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎤 *أغاني عربية*\nأم كلثوم, فيروز, كاظم الساهر...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

async def music_foreign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎤 *أغاني أجنبية*\nEd Sheeran, Adele, Taylor Swift...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

async def music_podcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎧 *بودكاست*\nبرامج صوتية ممتعة ومفيدة", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

async def music_ringtones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎼 *نغمات جوال*\nأفضل النغمات لهاتفك", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

async def music_beats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🥁 *إيقاعات*\nللإنتاج الموسيقي", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_music")]]))

# دوال الكتب
async def books_novels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📖 *روايات*\nأجمل الروايات العربية والعالمية", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

async def books_science(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📚 *كتب علمية*\nفيزياء، كيمياء، أحياء...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

async def books_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📚 *كتب تاريخ*\nتاريخ الحضارات والأمم", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

async def books_philosophy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📚 *كتب فلسفة*\nلأعظم الفلاسفة", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

async def books_religion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📚 *كتب دينية*\nتفاسير، فقه، سيرة...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

async def books_programming(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📚 *كتب برمجة*\nPython, JavaScript, AI...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

async def books_selfdev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📚 *تطوير الذات*\nالعادات السبع، فكر تصبح غنياً...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

async def books_cooking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📚 *كتب طبخ*\nأشهى الوصفات العالمية", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_books")]]))

# دوال الألعاب
async def games_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎮 *ألعاب الكمبيوتر*\nأفضل ألعاب PC", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

async def games_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📱 *ألعاب الموبايل*\nPUBG, Free Fire, Clash...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

async def games_ps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🕹 *ألعاب بلايستيشن*\nGod of War, Spider-Man...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

async def games_multiplayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎲 *ألعاب جماعية*\nالعب مع أصدقائك", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

async def games_puzzles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🧩 *ألغاز*\nاختبر ذكاءك", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

async def games_tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🏆 *بطولات*\nشارك في البطولات", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

async def games_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🃏 *ألعاب الورق*\nبوكر، طرنيب، بلوت...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

async def games_shooting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🎯 *ألعاب التصويب*\nCall of Duty, Valorant...", parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="menu_games")]]))

# ============ الرجوع للبداية ============
async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📂 القائمة الرئيسية", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🌟 *مرحباً بك في البوت المتطور!*\nاضغط على الزر أدناه لعرض القائمة الرئيسية.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============ الدالة الرئيسية ============
def main():
    # إنشاء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    
    # معالجات القوائم الرئيسية
    app.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(menu_movies, pattern="^menu_movies$"))
    app.add_handler(CallbackQueryHandler(menu_music, pattern="^menu_music$"))
    app.add_handler(CallbackQueryHandler(menu_books, pattern="^menu_books$"))
    app.add_handler(CallbackQueryHandler(menu_games, pattern="^menu_games$"))
    app.add_handler(CallbackQueryHandler(menu_shop, pattern="^menu_shop$"))
    app.add_handler(CallbackQueryHandler(menu_finance, pattern="^menu_finance$"))
    app.add_handler(CallbackQueryHandler(menu_web, pattern="^menu_web$"))
    app.add_handler(CallbackQueryHandler(menu_apps, pattern="^menu_apps$"))
    app.add_handler(CallbackQueryHandler(menu_ai, pattern="^menu_ai$"))
    app.add_handler(CallbackQueryHandler(menu_security, pattern="^menu_security$"))
    app.add_handler(CallbackQueryHandler(menu_stats, pattern="^menu_stats$"))
    app.add_handler(CallbackQueryHandler(menu_settings, pattern="^menu_settings$"))
    
    # معالجات الأزرار الفردية - أفلام
    app.add_handler(CallbackQueryHandler(movies_action, pattern="^movies_action$"))
    app.add_handler(CallbackQueryHandler(movies_comedy, pattern="^movies_comedy$"))
    app.add_handler(CallbackQueryHandler(movies_horror, pattern="^movies_horror$"))
    app.add_handler(CallbackQueryHandler(movies_scifi, pattern="^movies_scifi$"))
    app.add_handler(CallbackQueryHandler(movies_romance, pattern="^movies_romance$"))
    app.add_handler(CallbackQueryHandler(movies_drama, pattern="^movies_drama$"))
    app.add_handler(CallbackQueryHandler(series_turkish, pattern="^series_turkish$"))
    app.add_handler(CallbackQueryHandler(series_foreign, pattern="^series_foreign$"))
    app.add_handler(CallbackQueryHandler(series_arabic, pattern="^series_arabic$"))
    app.add_handler(CallbackQueryHandler(series_cartoon, pattern="^series_cartoon$"))
    
    # معالجات الأزرار الفردية - موسيقى
    app.add_handler(CallbackQueryHandler(music_calm, pattern="^music_calm$"))
    app.add_handler(CallbackQueryHandler(music_rock, pattern="^music_rock$"))
    app.add_handler(CallbackQueryHandler(music_classic, pattern="^music_classic$"))
    app.add_handler(CallbackQueryHandler(music_arabic, pattern="^music_arabic$"))
    app.add_handler(CallbackQueryHandler(music_foreign, pattern="^music_foreign$"))
    app.add_handler(CallbackQueryHandler(music_podcast, pattern="^music_podcast$"))
    app.add_handler(CallbackQueryHandler(music_ringtones, pattern="^music_ringtones$"))
    app.add_handler(CallbackQueryHandler(music_beats, pattern="^music_beats$"))
    
    # معالجات
