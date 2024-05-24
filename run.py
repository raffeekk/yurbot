import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import PyPDF2
API_TOKEN = '7043328623:AAEgtL4GHG2fYJ8GUii4f8VZUb5BLtBcmX8'

# Включение ведения журнала
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Словарь для хранения соответствия между выбранным пользователем документом и файлом PDF
document_pdf_mapping = {
    'Конституция': r'documents/constitutionrf.pdf',
    'Документ 2': r'documents',
    'Документ 3': r'documents'
}

# Функция извлечения содержимого статьи из PDF-документа
def extract_article_content(pdf_file_path, article_number):
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.numPages

        article_content = ""
        in_article = False
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            page_text = page.extractText()

            if f"Статья {article_number}" in page_text:
                in_article = True
                article_content += page_text[page_text.index(f"Статья {article_number}"):]
            elif in_article:
                if f"Статья {article_number + 1}" in page_text:
                    break
                article_content += page_text

        return article_content

async def select_document(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(title) for title in
                   ['Документ 1', 'Документ 2', 'Документ 3']])  # добавьте свои документы

    await message.answer("Выберите документ:", reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await select_document(message)


@dp.message_handler(lambda message: message.text.startswith('Документ '))
async def handle_document_choice(message: types.Message):
    document_number = message.text.split()[-1]
    await message.answer(f"Вы выбрали: {message.text}. Теперь выберите статью в Документ {document_number}.")


@dp.message_handler(lambda message: message.text.startswith('Статья '))
async def handle_article_choice(message: types.Message):
    await message.answer(f"Вы выбрали статью: {message.text}. Теперь отправьте текст для поиска в статье.")


@dp.message_handler()
async def search_text(message: types.Message):
    query = message.text

    # Получаем путь к файлу PDF для выбранного пользователем документа
    document = message.reply_to_message.text.split()[-1]
    pdf_file_path = document_pdf_mapping.get(document)

    if pdf_file_path:
        # Если файл PDF найден, выполняем поиск текста
        results = []
        for article_number in range(1, 137):
            article_content = extract_article_content(pdf_file_path, f"Статья {article_number}")
            if query in article_content:
                results.append(f"Статья {article_number}: {article_content}")

        if results:
            result_text = "\n".join(results)
        else:
            result_text = "Текст не найден."
    else:
        result_text = "Файл PDF не найден для выбранного документа."

    await message.reply(result_text, parse_mode=ParseMode.HTML)


async def on_startup(dp):
    logging.info("Bot is starting...")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
