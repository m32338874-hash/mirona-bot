import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

logging.basicConfig(level=logging.INFO)
genai.configure(api_key=GEMINI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text
    user_name = update.message.from_user.first_name or "Неизвестный"
    is_boss = "босс" in user_text.lower()
    if is_boss:
        system = "Ты верный телохранитель Босса Мирона. Говори с ним уважительно, докладывай обстановку."
        prompt = f"Босс Мирон пишет: '{user_text}'. Ответь преданно."
    else:
        system = "Ты агрессивный телохранитель Мирона. Все враги. Допрашивай и угрожай."
        prompt = f"Подозрительный тип {user_name} пишет: '{user_text}'. Допроси жёстко."
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system)
    response = model.generate_content(prompt)
    await update.message.reply_text(response.text)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
