import os
import asyncio
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

# قاعدة بيانات بسيطة للرقية الشرعية
ruqyah_texts = {
    "1": "أعوذ بالله من الشيطان الرجيم. بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم.",
    "2": "قُلْ هُوَ ٱللَّهُ أَحَدٌ، ٱللَّهُ ٱلصَّمَدُ، لَمْ يَلِدْ وَلَمْ يُولَدْ، وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌ."
}

# نص عام للاستشارات النسائية
womens_consultation = "يرجى وصف مشكلتك أو استفسارك وسأحاول مساعدتك بأفضل طريقة ممكنة. يمكنك التواصل مع الإداري للحصول على استشارة خاصة."

# دالة الترحيب مع قائمة أزرار
async def start(update: Update, context):
    chat_id = update.effective_chat.id
    
    # إنشاء قائمة الأزرار
    keyboard = [
        [InlineKeyboardButton("تفسير الأحلام", callback_data='interpret_dream')],
        [InlineKeyboardButton("تواصل معنا", callback_data='contact_us')],
        [InlineKeyboardButton("معلومات إضافية", callback_data='more_info')],
        [InlineKeyboardButton("الرقية الشرعية", callback_data='ruqyah')],
        [InlineKeyboardButton("استشارات نسائية", callback_data='womens_consult')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
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
    elif query.data == 'ruqyah':
        ruqyah_text = "\n".join(ruqyah_texts.values())
        await context.bot.send_message(chat_id=chat_id, text=f"الرقية الشرعية:\n{ruqyah_text}\nيرجى تلاوتها مع الإخلاص واستخارة الله.")
    elif query.data == 'womens_consult':
        await context.bot.send_message(chat_id=chat_id, text=womens_consultation)

# دالة لتفسير الأحلام بناءً على الرسالة وإرسالها للإداري إذا لم يتم التفسير
async def handle_message(update: Update, context):
    user_message = update.message.text.lower()
    chat_id = update.message.chat_id
    
    # محاولة تفسير الحلم
    response = "عذرًا، لا يمكنني تفسير هذا الحلم الآن. حاول وصفًا آخر!"
    dream_interpreted = False
    for keyword, interpretation in dream_interpretations.items():
        if keyword in user_message:
            response = interpretation
            dream_interpreted = True
            break
    
    # إرسال الرد للمستخدم
    await context.bot.send_message(chat_id=chat_id, text=response)
    
    # إذا لم يتم تفسير الحلم، أرسل الرسالة إلى الإداري
    if not dream_interpreted:
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

# إعداد وتشغيل البوت
async def main():
    # التحقق من وجود التوكن
    if not BOT_TOKEN:
        print("خطأ: يجب تعيين BOT_TOKEN في المتغيرات البيئية.")
        return
    
    if not ADMIN_CHAT_ID:
        print("خطأ: يجب تعيين ADMIN_CHAT_ID في المتغيرات البيئية.")
        return
    
    # إعداد البوت
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # بدء البوت
    print("بدء تشغيل البوت...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("البوت يعمل الآن!")

    # الاستمرار في التشغيل حتى يتم إيقاف البوت
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
