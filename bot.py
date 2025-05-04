import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# إعداد التسجيل (Logging) لتتبع الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# استرداد التوكن ومعرف الإداري من المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# التحقق من وجود المتغيرات البيئية
if not BOT_TOKEN:
    raise ValueError("يجب تعيين BOT_TOKEN في المتغيرات البيئية.")
if not ADMIN_CHAT_ID:
    raise ValueError("يجب تعيين ADMIN_CHAT_ID في المتغيرات البيئية.")

# قاعدة بيانات بسيطة لتفسير الأحلام
dream_interpretations = {
    "ماء": "الماء يرمز إلى العواطف أو التغيير.",
    "طيور": "الطيور تشير إلى الحرية.",
    "نار": "النار تدل على الغضب."
}

# نصوص الرقية الشرعية
ruqyah_texts = [
    "أعوذ بالله من الشيطان الرجيم. بسم الله الذي لا يضر مع اسمه شيء.",
    "قُلْ هُوَ ٱللَّهُ أَحَدٌ."
]

# نص الاستشارات النسائية
womens_consultation = "يرجى وصف مشكلتك، سأساعدك أو أرسل رسالتك للإداري."

# دالة الترحيب
async def start(update: Update, context):
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text="مرحبًا! أنا بوت Ehsas. أرسل وصف حلم (مثل 'رأيت ماء')، اطلب رقية (اكتب 'رقية')، أو اطلب استشارة نسائية (اكتب 'استشارة')."
    )

# دالة معالجة الرسائل
async def handle_message(update: Update, context):
    user_message = update.message.text.lower()
    chat_id = update.message.chat_id
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id

    # تفسير الأحلام
    response = "عذرًا، لا أستطيع تفسير هذا الحلم."
    for keyword, interpretation in dream_interpretations.items():
        if keyword in user_message:
            response = interpretation
            break
    if response != "عذرًا، لا أستطيع تفسير هذا الحلم.":
        await context.bot.send_message(chat_id=chat_id, text=response)
        return

    # الرقية الشرعية
    if "رقية" in user_message:
        ruqyah_text = "\n".join(ruqyah_texts)
        await context.bot.send_message(chat_id=chat_id, text=f"الرقية الشرعية:\n{ruqyah_text}")
        return

    # استشارات نسائية
    if "استشارة" in user_message or "نسائية" in user_message:
        await context.bot.send_message(chat_id=chat_id, text=womens_consultation)
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"استشارة نسائية من {user_name} (ID: {user_id}):\n{user_message}"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="تم إرسال استشارتك إلى الإداري، سيعود إليك قريبًا."
        )
        return

    # إرسال الرسالة للإداري إذا لم تكن متعلقة بأي خيار
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"رسالة من {user_name} (ID: {user_id}):\n{user_message}"
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text="تم إرسال رسالتك إلى الإداري، سيعود إليك قريبًا."
    )

# دالة لمعالجة الأخطاء
async def error_handler(update: Update, context):
    logger.error(f"حدث خطأ: {context.error}")
    if update:
        await update.effective_chat.send_message("حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى لاحقًا.")

# دالة التشغيل الرئيسية
async def main():
    try:
        # إنشاء تطبيق البوت
        application = Application.builder().token(BOT_TOKEN).build()

        # إضافة المعالجات
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)

        # بدء التشغيل
        logger.info("بدء تشغيل البوت...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        logger.info("البوت يعمل الآن!")

        # الاستمرار في التشغيل
        await asyncio.Event().wait()

    except Exception as e:
        logger.error(f"فشل تشغيل البوت: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
