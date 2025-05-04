import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# استرداد التوكن ومعرف الإداري من المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# قاعدة بيانات بسيطة لتفسير الأحلام
dream_interpretations = {
    "ماء": "الماء في الأحلام يرمز عادةً إلى العواطف أو التغيير.",
    "طيور": "الطيور تشير إلى الحرية أو الأمل.",
    "نار": "النار قد تدل على الغضب أو التطهير."
}

# دالة الترحيب مع قائمة أزرار
async def start(update: Update, context):
    chat_id = update.effective_chat.id
    
    # إنشاء قائمة الأزرار
    keyboard = [
        [InlineKeyboardButton("تفسير الأحلام", callback_data='interpret_dream')],
        [InlineKeyboardButton("تواصل معنا", callback_data='contact_us')],
        [InlineKeyboardButton("معلومات إضافية", callback_data='more_info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الرسالة مع الأزرار
    await context.bot.send_message(
        chat_id=chat_id,
        text="مرحبًا! أنا بوت Ehsas. كيف يمكنني مساعدتك؟ اختر من الخيارات أدناه:",
        reply_markup=reply_markup
    )

# دالة لمعالجة النقر على الأزرار
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    
    if query.data == 'interpret_dream':
        await context.bot.send_message(chat_id=chat_id, text="أرسل لي وصف حلمك (مثل 'رأيت ماء' أو 'رأيت طيور') وسأحاول تفسيره!")
    elif query.data == 'contact_us':
        await context.bot.send_message(chat_id=chat_id, text="يمكنك التواصل معنا عبر هذا الرابط: [رابط الدعم]")
    elif query.data == 'more_info':
        await context.bot.send_message(chat_id=chat_id, text="معلومات إضافية: هذا البوت مخصص لتفسير الأحلام ومساعدتك!")

# دالة لتفسير الأحلام بناءً على الرسالة
async def interpret_dream(update: Update, context):
    user_message = update.message.text.lower()
    chat_id = update.message.chat_id
    
    # البحث عن كلمة في قاعدة البيانات
    response = "عذرًا، لا يمكنني تفسير هذا الحلم الآن. حاول وصفًا آخر!"
    for keyword, interpretation in dream_interpretations.items():
        if keyword in user_message:
            response = interpretation
            break
    
    await context.bot.send_message(chat_id=chat_id, text=response)

# دالة لإرسال الرسائل إلى الإداري
async def forward_to_admin(update: Update, context):
    user_message = update.message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_username = update.effective_user.username or "لا يوجد اسم مستخدم"
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"رسالة جديدة من {user_name} (@{user_username}, ID: {user_id}):\n{user_message}"
    )

# دالة للرد على الأوامر غير المعروفة
async def unknown(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="عذرًا، لم أفهم هذا الأمر.")

# إعداد البوت
application = Application.builder().token(BOT_TOKEN).build()

# إضافة المعالجات
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interpret_dream))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
application.add_handler(MessageHandler(filters.COMMAND, unknown))

# بدء البوت
application.run_polling()
