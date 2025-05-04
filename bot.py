import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# استرداد التوكن ومعرف الإداري من المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# التحقق من وجود المتغيرات البيئية
if not BOT_TOKEN:
    raise ValueError("يجب تعيين BOT_TOKEN في المتغيرات البيئية")
if not ADMIN_CHAT_ID:
    raise ValueError("يجب تعيين ADMIN_CHAT_ID في المتغيرات البيئية")

# قاعدة بيانات بسيطة لتفسير الأحلام
dream_interpretations = {
    "ماء": "الماء في الأحلام يرمز عادةً إلى العواطف أو التغيير.",
    "طيور": "الطيور تشير إلى الحرية أو الأمل.",
    "نار": "النار قد تدل على الغضب أو التطهير.",
    "سقوط": "رؤية السقوط في الحلم قد تعني الخوف من الفشل أو فقدان السيطرة.",
    "زواج": "رؤية الزواج في الحلم قد تدل على اتحاد الأفكار أو بداية جديدة."
}

# قاعدة بيانات بسيطة للرقية الشرعية
ruqyah_texts = {
    "1": "أعوذ بالله من الشيطان الرجيم. بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم.",
    "2": "قُلْ هُوَ ٱللَّهُ أَحَدٌ، ٱللَّهُ ٱلصَّمَدُ، لَمْ يَلِدْ وَلَمْ يُولَدْ، وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌ.",
    "3": "وَإِذَا مَرِضْتُ فَهُوَ يَشْفِينِ",
    "4": "اللَّهُمَّ رَبَّ النَّاسِ، أَذْهِبِ البَأسَ، اشْفِ، أَنْتَ الشَّافي، لا شِفَاءَ إِلاَّ شِفَاؤُكَ، شِفَاءً لا يُغَادِرُ سَقَماً"
}

# نص عام للاستشارات النسائية
womens_consultation = """
يرجى وصف مشكلتك أو استفسارك وسأحاول مساعدتك بأفضل طريقة ممكنة. 

ملاحظة: هذه استشارات عامة فقط. للاستشارات الخاصة، يرجى التواصل مع الإداري مباشرة.
يمكنك إرسال رسالتك وسيتم تحويلها للإداري للرد عليك في أقرب وقت.
"""

# دالة الترحيب مع قائمة أزرار
async def start(update: Update, context):
    chat_id = update.effective_chat.id
    
    # إنشاء قائمة الأزرار
    keyboard = [
        [InlineKeyboardButton("تفسير الأحلام", callback_data='interpret_dream')],
        [InlineKeyboardButton("الرقية الشرعية", callback_data='ruqyah')],
        [InlineKeyboardButton("استشارات نسائية", callback_data='womens_consult')],
        [InlineKeyboardButton("تواصل معنا", callback_data='contact_us')],
        [InlineKeyboardButton("معلومات إضافية", callback_data='more_info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = """
مرحبًا بك في بوت إحساس! 🌙
أنا هنا لمساعدتك في:
- تفسير الأحلام العامة
- تقديم الرقية الشرعية
- توجيهك للاستشارات النسائية

اختر من الخيارات أدناه:
"""
    await context.bot.send_message(
        chat_id=chat_id,
        text=welcome_message,
        reply_markup=reply_markup
    )

# دالة لمعالجة النقر على الأزرار
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    
    if query.data == 'interpret_dream':
        response = "أرسل لي وصف حلمك (مثل 'رأيت ماء' أو 'رأيت طيور') وسأحاول تفسيره!\n\nملاحظة: التفسيرات عامة ولا تغني عن استشارة المختصين."
    elif query.data == 'contact_us':
        response = "للتواصل مع الإدارة، يرجى إرسال رسالتك وسيتم تحويلها للإداريين."
    elif query.data == 'more_info':
        response = "معلومات عن البوت:\nهذا البوت يقدم خدمات:\n1. تفسير أحلام عامة\n2. نصوص للرقية الشرعية\n3. توجيه للاستشارات النسائية\n\nالبوت لا يقدم استشارات طبية أو نفسية متخصصة."
    elif query.data == 'ruqyah':
        ruqyah_text = "\n\n".join(ruqyah_texts.values())
        response = f"نصوص الرقية الشرعية:\n\n{ruqyah_text}\n\nيرجى تلاوتها مع الإخلاص واستخارة الله."
    elif query.data == 'womens_consult':
        response = womens_consultation
    else:
        response = "عذرًا، لم أفهم هذا الخيار."
    
    await context.bot.send_message(chat_id=chat_id, text=response)

# دالة لتفسير الأحلام بناءً على الرسالة وإرسالها للإداري إذا لم يتم التفسير
async def handle_message(update: Update, context):
    # تجاهل الرسائل التي تبدأ ب / لأنها أوامر
    if update.message.text.startswith('/'):
        return
    
    user_message = update.message.text.lower()
    chat_id = update.message.chat_id
    
    # محاولة تفسير الحلم
    response = None
    for keyword, interpretation in dream_interpretations.items():
        if keyword in user_message:
            response = f"تفسير الحلم ({keyword}):\n{interpretation}\n\nملاحظة: هذا تفسير عام ولا يعتبر تشخيصًا دقيقًا."
            break
    
    # إذا لم يتم تفسير الحلم
    if not response:
        response = "عذرًا، لا يمكنني تفسير هذا الحلم الآن. يمكنك محاولة وصفه بطريقة أخرى أو التواصل مع الإداري."
        
        # إرسال الرسالة إلى الإداري
        user = update.effective_user
        admin_message = (
            f"رسالة تحتاج تفسير من المستخدم:\n"
            f"الاسم: {user.full_name}\n"
            f"المعرف: @{user.username if user.username else 'غير متوفر'}\n"
            f"ID: {user.id}\n"
            f"الرسالة: {update.message.text}"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
        except Exception as e:
            print(f"فشل في إرسال الرسالة للإداري: {e}")
    
    # إرسال الرد للمستخدم
    await context.bot.send_message(chat_id=chat_id, text=response)

# دالة للرد على الأوامر غير المعروفة
async def unknown(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="عذرًا، لم أفهم هذا الأمر. يرجى استخدام /start لرؤية الخيارات المتاحة."
    )

# إعداد وتشغيل البوت
def main():
    # إعداد البوت
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # بدء البوت
    print("بدء تشغيل البوت...")
    application.run_polling()

if __name__ == "__main__":
    main()
