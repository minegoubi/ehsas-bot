import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

# استرداد التوكن ومعرف الإداري من المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# إعداد البوت
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# قاعدة بيانات بسيطة لتفسير الأحلام (يمكن توسيعها)
dream_interpretations = {
    "ماء": "الماء في الأحلام يرمز عادةً إلى العواطف أو التغيير.",
    "طيور": "الطيور تشير إلى الحرية أو الأمل.",
    "نار": "النار قد تدل على الغضب أو التطهير."
}

# دالة الترحيب مع قائمة أزرار
def start(update, context):
    chat_id = update.effective_chat.id
    
    # إنشاء قائمة الأزرار
    keyboard = [
        [InlineKeyboardButton("تفسير الأحلام", callback_data='interpret_dream')],
        [InlineKeyboardButton("تواصل معنا", callback_data='contact_us')],
        [InlineKeyboardButton("معلومات إضافية", callback_data='more_info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الرسالة مع الأزرار
    context.bot.send_message(
        chat_id=chat_id,
        text="مرحبًا! أنا بوت Ehsas. كيف يمكنني مساعدتك؟ اختر من الخيارات أدناه:",
        reply_markup=reply_markup
    )

# دالة لمعالجة النقر على الأزرار
def button(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    
    if query.data == 'interpret_dream':
        context.bot.send_message(chat_id=chat_id, text="أرسل لي وصف حلمك (مثل 'رأيت ماء' أو 'رأيت طيور') وسأحاول تفسيره!")
    elif query.data == 'contact_us':
        context.bot.send_message(chat_id=chat_id, text="يمكنك التواصل معنا عبر هذا الرابط: [رابط الدعم]")
    elif query.data == 'more_info':
        context.bot.send_message(chat_id=chat_id, text="معلومات إضافية: هذا البوت مخصص لتفسير الأحلام ومساعدتك!")

# دالة لتفسير الأحلام بناءً على الرسالة
def interpret_dream(update, context):
    user_message = update.message.text.lower()
    chat_id = update.message.chat_id
    
    # البحث عن كلمة في قاعدة البيانات
    response = "عذرًا، لا يمكنني تفسير هذا الحلم الآن. حاول وصفًا آخر!"
    for keyword, interpretation in dream_interpretations.items():
        if keyword in user_message:
            response = interpretation
            break
    
    context.bot.send_message(chat_id=chat_id, text=response)

# دالة لإرسال الرسائل إلى الإداري
def forward_to_admin(update, context):
    user_message = update.message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_username = update.effective_user.username or "لا يوجد اسم مستخدم
