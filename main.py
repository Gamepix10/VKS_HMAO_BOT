import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import BotCommand
import logging
from bot.keyboards.keyboards import start_inline_keyboard

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    filename="../hantaton/logs/bot.log",  # Имя файла для записи логов
    filemode="a",        # Режим записи (a - дописывать, w - перезаписывать файл)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат логов
    datefmt="%Y-%m-%d %H:%M:%S",  # Формат времени
)
logger = logging.getLogger(__name__)

async def set_bot_commands(bot: Bot):
    """
    Установить команды для меню бота.
    """
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/search", description="Поиск ВКС"),
        BotCommand(command="/calendar", description="Календарь встреч"),
        BotCommand(command="/schedule", description="Запланировать ВКС"),
    ]
    await bot.set_my_commands(commands)


API_TOKEN = '7297102701:AAE_1tlhZ3WPiUu1b8i_wNXc32LfInY5npg'

async def start_command(message: Message):
    """Обработчик команды /start."""
    keyboard = start_inline_keyboard()
    await message.answer(
        "Привет! Я бот, работающий через asyncio. Как я могу помочь?", 
        reply_markup=keyboard
    )

async def echo_message(message: Message):
    """Эхо-ответ на любое сообщение."""
    await message.answer(message.text)

async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "register":
        await callback_query.message.answer("Вы выбрали регистрацию.")
    elif callback_query.data == "login":
        await callback_query.message.answer("Вы выбрали логин.")

async def main():
    # Создаем экземпляр бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Регистрируем хендлеры
    dp.message.register(start_command, Command(commands=["start"]))
    dp.message.register(echo_message)
    dp.callback_query.register(process_callback)

    # Запускаем polling
    try:
        print("Бот запущен!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    # Запускаем event loop
    asyncio.run(main())