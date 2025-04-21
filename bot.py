from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

scheduler = AsyncIOScheduler(timezone=pytz.utc)  # или pytz.timezone('Europe/Moscow')
# Вопросы (твои 20)
questions = [
    {
        "question": "Что делает тег <h1> в HTML?",
        "options": ["Создаёт заголовок", "Создаёт таблицу", "Создаёт ссылку"],
        "answer": "Создаёт заголовок"
    },
    {
        "question": "Какой тег используется для создания ссылки?",
        "options": ["<a>", "<img>", "<table>"],
        "answer": "<a>"
    },
    {
        "question": "Какой тег вставляет картинку на страницу?",
        "options": ["<img>", "<link>", "<div>"],
        "answer": "<img>"
    },
    {
        "question": "Какой тег создаёт абзац?",
        "options": ["<p>", "<br>", "<span>"],
        "answer": "<p>"
    },
    {
        "question": "Какой тег создаёт список с точками?",
        "options": ["<ul>", "<ol>", "<li>"],
        "answer": "<ul>"
    },
    {
        "question": "Какой тег делает перенос строки?",
        "options": ["<br>", "<hr>", "<p>"],
        "answer": "<br>"
    },
    {
        "question": "Что делает тег <title>?",
        "options": ["Добавляет заголовок во вкладку", "Создаёт заголовок в тексте", "Добавляет подвал"],
        "answer": "Добавляет заголовок во вкладку"
    },
    {
        "question": "Какой тег используется для жирного текста?",
        "options": ["<b>", "<i>", "<u>"],
        "answer": "<b>"
    },
    {
        "question": "Какой тег используется для подчеркивания?",
        "options": ["<u>", "<i>", "<strong>"],
        "answer": "<u>"
    },
    {
        "question": "Какой тег создаёт таблицу?",
        "options": ["<table>", "<div>", "<span>"],
        "answer": "<table>"
    },
    {
        "question": "Какой тег обозначает ячейку в таблице?",
        "options": ["<td>", "<tr>", "<th>"],
        "answer": "<td>"
    },
    {
        "question": "Какой тег создаёт строку таблицы?",
        "options": ["<tr>", "<td>", "<table>"],
        "answer": "<tr>"
    },
    {
        "question": "Какой тег используется для подключения CSS?",
        "options": ["<link>", "<style>", "<script>"],
        "answer": "<link>"
    },
    {
        "question": "Как задать цвет текста в CSS?",
        "options": ["color", "background", "font-size"],
        "answer": "color"
    },
    {
        "question": "Как изменить размер шрифта?",
        "options": ["font-size", "text-align", "color"],
        "answer": "font-size"
    },
    {
        "question": "Как задать фон элементу?",
        "options": ["background", "color", "border"],
        "answer": "background"
    },
    {
        "question": "Какой CSS-селектор выбирает все элементы <p>?",
        "options": ["p", "#p", ".p"],
        "answer": "p"
    },
    {
        "question": "Как задать отступ внутри элемента?",
        "options": ["padding", "margin", "border"],
        "answer": "padding"
    },
    {
        "question": "Как задать внешний отступ у элемента?",
        "options": ["margin", "padding", "border"],
        "answer": "margin"
    },
    {
        "question": "Как задать границу элементу?",
        "options": ["border", "outline", "padding"],
        "answer": "border"
    }
]

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["score"] = 0
    context.user_data["current"] = 0
    context.user_data["question_list"] = random.sample(questions, 20)  # 20 случайных вопросов
    await update.message.reply_text("Привет! Готов начать тест по HTML и CSS?\n\nНапиши /quiz чтобы начать!")

# Начать викторину
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["score"] = 0
    context.user_data["current"] = 0
    await send_question(update, context)

# Функция для отправки вопроса
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i = context.user_data["current"]
    qlist = context.user_data["question_list"]
    
    # Логирование индекса
    print(f"Текущий индекс вопроса: {i}")

    if i < len(qlist):
        q = qlist[i]
        reply_markup = ReplyKeyboardMarkup([q["options"]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            f"Вопрос {i+1} из {len(qlist)}:\n{q['question']}",
            reply_markup=reply_markup
        )
        context.user_data["answer"] = q["answer"]
    else:
        score = context.user_data["score"]
        await update.message.reply_text(
            f"✅ Тест завершён!\n\nТы набрал: {score} из {len(qlist)} баллов!",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data["score"] = 0  # Сбрасываем счетчик, чтобы можно было начать снова
        context.user_data["current"] = 0  # Сбрасываем текущий индекс вопросов
        context.user_data["question_list"] = []  # Очищаем список вопросов

# Проверка ответа
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    correct_answer = context.user_data.get("answer", "")
    if user_answer == correct_answer:
        context.user_data["score"] += 1
        await update.message.reply_text("✅ Правильно!")
    else:
        await update.message.reply_text(f"❌ Неправильно. Правильный ответ: {correct_answer}")

    context.user_data["current"] += 1
    await send_question(update, context)

# Бот
app = Application.builder().token("7969159324:AAGfgIYicEjUjyP-R-oVOAQpp5SZOpN1oqo").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

app.run_polling()
