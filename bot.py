import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import sqlite3
import fitz  # PyMuPDF

API_TOKEN = 'token'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для поиска по правовым документам. Введи запрос для поиска.\n"
                        "Если вам потребудется помощь, воспользуйтесь командой /help")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = (
        "Я могу помочь тебе с поиском по правовым документам.\n"
        "\n"
        "Используй команды:\n"
        "/search <текст> - для поиска по документам\n"
        "/template <название шаблона> - для получения шаблона документа"
    )
    await message.reply(help_text)

def extract_text_from_pdf(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

@dp.message_handler(commands=['search'])
async def search_documents(message: types.Message):
    query = message.get_args()
    if not query:
        await message.reply("Пожалуйста, введите запрос для поиска.")
        return

    try:
        conn = sqlite3.connect('law_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM documents")
        results = cursor.fetchall()
        conn.close()

        matching_documents = []
        for title, pdf_data in results:
            text = extract_text_from_pdf(pdf_data)
            if query.lower() in text.lower():
                matching_documents.append((title, text))

        if matching_documents:
            response = "Найденные документы:\n\n"
            for title, content in matching_documents:
                response += f"{title}\n{content[:200]}...\n\n"
        else:
            response = "Ничего не найдено."
    except Exception as e:
        response = f"Произошла ошибка при поиске: {e}"

    await message.reply(response)

@dp.message_handler(commands=['template'])
async def send_template(message: types.Message):
    template_name = message.get_args()
    if not template_name:
        await message.reply("Пожалуйста, введите название шаблона.")
        return

    try:
        conn = sqlite3.connect('law_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM templates WHERE title = ?", (template_name,))
        result = cursor.fetchone()
        conn.close()

        if result:
            await message.reply(result[0])
        else:
            await message.reply("Шаблон не найден.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при получении шаблона: {e}")

@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    info_text = (
        "Право - это система общеобязательных норм, установленных и обеспечиваемых государством, "
        "регулирующих общественные отношения и поведение людей. Эти нормы призваны поддерживать "
        "порядок и справедливость в обществе. Право охватывает различные сферы жизни, включая "
        "семейное, трудовое, гражданское и уголовное право."
    )
    await message.reply(info_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
