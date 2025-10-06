import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("7670672608:AAHASjUT5IPw_CGbuFXrVejR35ExuJjTDr0")

questions = [
    "1️⃣ Есть ли у вас CRM и фиксируются ли все заявки?",
    "2️⃣ Понимаете ли вы, сколько стоит 1 клиент (CAC)?",
    "3️⃣ Есть ли система повторных продаж и возвратов клиентов?",
    "4️⃣ Используете ли вы более 2 каналов привлечения клиентов?",
    "5️⃣ У команды есть скрипты и сценарии продаж?",
    "6️⃣ Есть ли позиционирование и чёткое УТП?",
    "7️⃣ Реклама даёт предсказуемый поток лидов?",
    "8️⃣ Анализируете ли вы, какие источники приносят прибыль?",
    "9️⃣ Бизнес работает без вас хотя бы 2 недели?",
    "🔟 Клиенты приходят не только по сарафану?"
]

user_answers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_answers[chat_id] = {"q": 0, "score": 0}
    await update.message.reply_text("Привет! 👋 Это тест: «Где твой бизнес теряет клиентов?»\nОтветь честно на 10 вопросов (да/нет). Начнём!")
    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_data = user_answers.get(chat_id)
    q_index = user_data["q"]
    if q_index < len(questions):
        reply_markup = ReplyKeyboardMarkup([["Да", "Нет"]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(questions[q_index], reply_markup=reply_markup)
    else:
        score = user_data["score"]
        result = interpret_score(score)
        await update.message.reply_text(result + "\n\nХочешь индивидуальный разбор — напиши «анализ» @nissan3501")
        del user_answers[chat_id]

def interpret_score(score):
    if score <= 3:
        return "🟥 Уровень системности: низкий. Бизнес держится на хаосе и сарафане."
    elif score <= 7:
        return "🟨 Средний уровень. Есть структура, но много потерь клиентов."
    else:
        return "🟩 Высокий уровень. Отлично! У вас уже есть система, но есть зоны роста."

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.lower()
    if chat_id not in user_answers:
        await update.message.reply_text("Введите /start чтобы начать тест.")
        return
    user_data = user_answers[chat_id]
    if text == "да":
        user_data["score"] += 1
    user_data["q"] += 1
    await ask_question(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
    app.run_polling()

if __name__ == "__main__":
    main()
