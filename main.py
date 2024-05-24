import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
API_TOKEN = ''

# Создание объектов бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот. Как дела?")

# Обработчик для кнопки "Старт"
@dp.callback_query_handler(lambda c: c.data == 'start')
async def process_callback_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вы нажали кнопку "Старт".')

# Обработчик для всех входящих сообщений
@dp.message_handler()
async def send_start_button(message: types.Message):
    # Создаем кнопку "Старт"
    start_button = InlineKeyboardButton("Старт", callback_data='start')
    keyboard = InlineKeyboardMarkup().add(start_button)

    # Отправляем сообщение с кнопкой
    await message.answer("Нажмите кнопку 'Старт'", reply_markup=keyboard)

# Главная функция для запуска бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
