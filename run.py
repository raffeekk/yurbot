# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import ParseMode
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.utils import executor
# import PyPDF2
#
# API_TOKEN = 'token'
#
# # Включение ведения журнала
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
# dp.middleware.setup(LoggingMiddleware())
#
# # Словарь для хранения соответствия между выбранным пользователем документом и файлом PDF
# document_pdf_mapping = {
#     'Конституция РФ': r'documents/Конституция РФ/constitutionrf.pdf',
#     'Гражданский кодекс РФ (часть 1)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(1).pdf',
#     'Гражданский кодекс РФ (часть 2)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(2).pdf',
#     'Гражданский кодекс РФ (часть 3)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(3).pdf',
#     'Гражданский кодекс РФ (часть 4)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(4).pdf',
#     'Налоговый кодекс РФ (часть 1)': r'documents/Кодексы Российской Федерации/Налоговый кодекс РФ(1).pdf',
#     'Налоговый кодекс РФ (часть 2)': r'documents/Кодексы Российской Федерации/Налоговый кодекс РФ(2).pdf'
# }
#
# # Функция извлечения содержимого статьи из PDF-документа
# def extract_article_content(pdf_file_path, article_number):
#     with open(pdf_file_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfFileReader(file)
#         num_pages = pdf_reader.numPages
#
#         article_content = ""
#         in_article = False
#         for page_num in range(num_pages):
#             page = pdf_reader.getPage(page_num)
#             page_text = page.extractText()
#
#             if f"Статья {article_number}" in page_text:
#                 in_article = True
#                 article_content += page_text[page_text.index(f"Статья {article_number}"):]
#             elif in_article:
#                 if f"Статья {article_number + 1}" in page_text:
#                     break
#                 article_content += page_text
#
#         return article_content
#
# async def select_document(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*[types.KeyboardButton(title) for title in
#                    ['Конституция РФ', 'Гражданский кодекс РФ', 'Налоговый кодекс РФ']])
#
#     await message.answer("Выберите документ:", reply_markup=keyboard)
#
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     await select_document(message)
#
# @dp.message_handler(lambda message: message.text in ['Конституция РФ', 'Гражданский кодекс РФ', 'Налоговый кодекс РФ'])
# async def handle_document_choice(message: types.Message):
#     document = message.text
#     if document == 'Конституция РФ':
#         await message.answer("Вы выбрали Конституцию РФ. Укажите номер статьи(В следующем формате: Статья <Нормер статьи>):", reply_markup=back_button_keyboard())
#     elif document == 'Гражданский кодекс РФ':
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(*[types.KeyboardButton(title) for title in
#                        ['Гражданский кодекс РФ (часть 1)', 'Гражданский кодекс РФ (часть 2)',
#                         'Гражданский кодекс РФ (часть 3)', 'Гражданский кодекс РФ (часть 4)']])
#         keyboard.add(types.KeyboardButton('Назад'))
#         await message.answer("Вы выбрали Гражданский кодекс РФ. Выберите часть:", reply_markup=keyboard)
#     elif document == 'Налоговый кодекс РФ':
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(*[types.KeyboardButton(title) for title in
#                        ['Налоговый кодекс РФ (часть 1)', 'Налоговый кодекс РФ (часть 2)']])
#         keyboard.add(types.KeyboardButton('Назад'))
#         await message.answer("Вы выбрали Налоговый кодекс РФ. Выберите часть:", reply_markup=keyboard)
#
# @dp.message_handler(lambda message: message.text.startswith('Гражданский кодекс РФ') or message.text.startswith('Налоговый кодекс РФ'))
# async def handle_code_part_choice(message: types.Message):
#     document_part = message.text
#     await message.answer(f"Вы выбрали: {document_part}. Укажите номер статьи(В следующем формате: Статья <Нормер статьи>):", reply_markup=back_button_keyboard())
#
# @dp.message_handler(lambda message: message.text.startswith('Статья '))
# async def handle_article_choice(message: types.Message):
#     await message.answer(f"Вы выбрали статью: {message.text}. Теперь отправьте текст для поиска в статье(В следующем формате: <Формат поиска по тексту>).", reply_markup=back_button_keyboard())
#
# @dp.message_handler(lambda message: message.text == 'Назад')
# async def handle_back(message: types.Message):
#     await select_document(message)
#
# @dp.message_handler()
# async def search_text(message: types.Message):
#     query = message.text
#
#     # Получаем путь к файлу PDF для выбранного пользователем документа
#     document_message = await message.get_reply_message()
#     if document_message:
#         document = document_message.text.split()[-1]
#         pdf_file_path = document_pdf_mapping.get(document)
#
#         if pdf_file_path:
#             # Если файл PDF найден, выполняем поиск текста
#             results = []
#             for article_number in range(1, 137):
#                 article_content = extract_article_content(pdf_file_path, article_number)
#                 if query in article_content:
#                     results.append(f"Статья {article_number}: {article_content}")
#
#             if results:
#                 result_text = "\n".join(results)
#             else:
#                 result_text = "Текст не найден."
#         else:
#             result_text = "Файл PDF не найден для выбранного документа."
#
#         await message.reply(result_text, parse_mode=ParseMode.HTML)
#     else:
#         await message.reply("Пожалуйста, сначала выберите документ и укажите статью.")
#
# def back_button_keyboard():
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton('Назад'))
#     return keyboard
#
# async def on_startup(dp):
#     logging.info("Bot is starting...")
#
# if __name__ == '__main__':
#     executor.start_polling(dp, on_startup=on_startup)

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from PyPDF2 import PdfReader

API_TOKEN = 'token'

# Включение ведения журнала
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота, диспетчера и хранилища состояний
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Словарь для хранения соответствия между выбранным пользователем документом и файлом PDF
document_pdf_mapping = {
    'Конституция РФ': r'documents/Конституция РФ/constitutionrf.pdf',
    'Гражданский кодекс РФ (часть 1)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(1).pdf',
    'Гражданский кодекс РФ (часть 2)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(2).pdf',
    'Гражданский кодекс РФ (часть 3)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(3).pdf',
    'Гражданский кодекс РФ (часть 4)': r'documents/Кодексы Российской Федерации/Гражданский кодекс РФ(4).pdf',
    'Налоговый кодекс РФ (часть 1)': r'documents/Кодексы Российской Федерации/Налоговый кодекс РФ(1).pdf',
    'Налоговый кодекс РФ (часть 2)': r'documents/Кодексы Российской Федерации/Налоговый кодекс РФ(2).pdf'
}

# Определение состояний
class Form(StatesGroup):
    document = State()  # Состояние для выбора документа
    article = State()   # Состояние для ввода номера статьи

# Функция извлечения содержимого статьи из PDF-документа
def extract_article_content(pdf_file_path, article_number):
    logging.info(f"Extracting content from {pdf_file_path} for article {article_number}")
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        logging.info(f"Number of pages in PDF: {num_pages}")

        article_content = ""
        in_article = False
        next_article_str = f"Статья {article_number + 1}"
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            logging.debug(f"Extracted text from page {page_num}: {page_text[:100]}...")  # Log only the first 100 characters for brevity

            if f"Статья {article_number}" in page_text:
                in_article = True
                start_index = page_text.index(f"Статья {article_number}")
                article_content += page_text[start_index:]
            elif in_article:
                if next_article_str in page_text:
                    end_index = page_text.index(next_article_str)
                    article_content += page_text[:end_index]
                    break
                article_content += page_text

        logging.info(f"Extracted article content: {article_content[:500]}...")  # Log only the first 500 characters for brevity
        return article_content.strip()

async def select_document(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(title) for title in
                   ['Конституция РФ', 'Гражданский кодекс РФ', 'Налоговый кодекс РФ']])

    await message.answer("Выберите документ:", reply_markup=keyboard)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await select_document(message)

@dp.message_handler(lambda message: message.text in ['Конституция РФ', 'Гражданский кодекс РФ', 'Налоговый кодекс РФ'], state='*')
async def handle_document_choice(message: types.Message, state: FSMContext):
    document = message.text
    await state.update_data(document=document)  # Сохраняем выбранный документ в состоянии пользователя

    if document == 'Конституция РФ':
        await message.answer("Вы выбрали Конституцию РФ. Укажите номер статьи (в следующем формате: Статья <Номер статьи>):", reply_markup=back_button_keyboard())
        await Form.article.set()
    elif document == 'Гражданский кодекс РФ':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(title) for title in
                       ['Гражданский кодекс РФ (часть 1)', 'Гражданский кодекс РФ (часть 2)',
                        'Гражданский кодекс РФ (часть 3)', 'Гражданский кодекс РФ (часть 4)']])
        keyboard.add(types.KeyboardButton('Назад'))
        await message.answer("Вы выбрали Гражданский кодекс РФ. Выберите часть:", reply_markup=keyboard)
    elif document == 'Налоговый кодекс РФ':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(title) for title in
                       ['Налоговый кодекс РФ (часть 1)', 'Налоговый кодекс РФ (часть 2)']])
        keyboard.add(types.KeyboardButton('Назад'))
        await message.answer("Вы выбрали Налоговый кодекс РФ. Выберите часть:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text.startswith('Гражданский кодекс РФ') or message.text.startswith('Налоговый кодекс РФ'), state='*')
async def handle_code_part_choice(message: types.Message, state: FSMContext):
    document_part = message.text
    await state.update_data(document=document_part)  # Обновляем документ в состоянии пользователя
    await message.answer(f"Вы выбрали: {document_part}. Укажите номер статьи (в следующем формате: Статья <Номер статьи>):", reply_markup=back_button_keyboard())
    await Form.article.set()

@dp.message_handler(lambda message: message.text.startswith('Статья '), state=Form.article)
async def handle_article_choice(message: types.Message, state: FSMContext):
    # Получаем номер статьи из текста сообщения
    try:
        article_number = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Пожалуйста, укажите номер статьи в правильном формате: Статья <Номер статьи>")
        return

    # Получаем выбранный документ из состояния пользователя
    user_data = await state.get_data()
    document = user_data.get('document')
    pdf_file_path = document_pdf_mapping.get(document)

    logging.info(f"Handling article choice: document={document}, article_number={article_number}, pdf_file_path={pdf_file_path}")

    if pdf_file_path:
        # Извлекаем содержание статьи
        article_content = extract_article_content(pdf_file_path, article_number)
        if article_content:
            # Отправляем текст статьи пользователю
            for chunk in [article_content[i:i + 4096] for i in range(0, len(article_content), 4096)]:
                await message.reply(f"{chunk}", parse_mode=ParseMode.HTML, reply_markup=back_button_keyboard())
        else:
            await message.reply(f"Статья {article_number} не найдена.", reply_markup=back_button_keyboard())
    else:
        await message.reply("Файл PDF не найден для выбранного документа.", reply_markup=back_button_keyboard())

@dp.message_handler(lambda message: message.text == 'Назад', state='*')
async def handle_back(message: types.Message, state: FSMContext):
    await select_document(message)
    await state.finish()  # Сбрасываем состояние

@dp.message_handler(state='*')
async def handle_unrecognized_message(message: types.Message, state: FSMContext):
    await message.reply("Пожалуйста, выберите документ и укажите статью.", reply_markup=back_button_keyboard())

def back_button_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Назад'))
    return keyboard

async def on_startup(dp):
    logging.info("Bot is starting...")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

