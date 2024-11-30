import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from api_client import APIClient
from keyboards import get_main_menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Инициализация API клиента
api_client = APIClient()

def get_action_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Регистрация", callback_data="register")],
            [InlineKeyboardButton(text="Логин", callback_data="login")]
        ]
    )
    return keyboard

# Клавиатура для стартовой страницы
def get_welcome_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далее", callback_data="next_step")]
        ]
    )
    return keyboard

# Хэндлер для команды /start (Приветственный экран)
async def cmd_start(message: Message):
    text = (
        "👋 Добро пожаловать в нашего бота!\n\n"
        "📅 Здесь вы сможете:\n"
        "- Планировать видеоконференции\n"
        "- Управлять расписанием\n"
        "- Просматривать встречи\n\n"
        "Нажмите **'Далее'**, чтобы начать."
    )
    await message.answer(text, reply_markup=get_welcome_keyboard(), parse_mode="Markdown")

# Хэндлер для кнопки "Далее" (начало диалога)
async def next_step(call: CallbackQuery):
    # Удаляем предыдущее сообщение
    await call.message.delete()

    # Начало диалога
    await call.message.answer(
        "Спасибо, что присоединились! 😊\n\n"
    )
    await call.message.answer("Выберите действие:", reply_markup=get_action_menu_keyboard())



# Хэндлер для команды /start
#async def cmd_start(message: Message):
#ß    await message.answer("Добро пожаловать в систему планирования ВКС! Выберите действие:", reply_markup=get_auth_choice_keyboard())

# Хэндлер для команды /login
async def cmd_login(call: CallbackQuery):
    await call.message.answer("Введите email и пароль через пробел. Пример: `email@example.com password`", parse_mode="Markdown")

# Хэндлер для кнопки "Регистрация"
async def cmd_register(call: CallbackQuery):
    await call.message.answer("Для регистрации введите: `email@example.com password`.", parse_mode="Markdown")

# Хэндлер для обработки логина
async def process_login(message: Message):
    try:
        email, password = message.text.split(" ")
        if api_client.login(email, password):
            await message.answer("Авторизация успешна!", reply_markup=get_main_menu())
        else:
            await message.answer("Не удалось авторизоваться. Проверьте данные.")
    except ValueError:
        await message.answer("Неверный формат. Используйте: `email@example.com password`", parse_mode="Markdown")

# Хэндлер для обработки регистрации
async def process_register(message: Message):
    try:
        email, password = message.text.split(" ")
        # Отправляем запрос на регистрацию
        registration_response = api_client.register(email, password)
        if registration_response.get("id"):
            await message.answer("Регистрация успешна! Теперь вы можете войти в систему.")
        else:
            await message.answer("Ошибка регистрации. Попробуйте снова.")
    except ValueError:
        await message.answer("Неверный формат. Используйте: `email@example.com password`", parse_mode="Markdown")

# Хэндлер для просмотра предстоящих ВКС
async def upcoming_vcs(call: CallbackQuery):
    vcs_list = api_client.get_vcs({"status": "upcoming"})
    if vcs_list:
        response = "\n\n".join([f"{vcs['title']} - {vcs['date']} ({vcs['organizer']})" for vcs in vcs_list])
    else:
        response = "Нет предстоящих ВКС."
    await call.message.answer(response)

# Хэндлер для создания новой ВКС
async def create_vcs(call: CallbackQuery):
    await call.message.answer("Введите данные для новой ВКС в формате:\n`Название, Место, 2023-12-25 15:00, 2 часа, participant1@example.com, participant2@example.com`", parse_mode="Markdown")

# Хэндлер для обработки создания ВКС
async def process_create_vcs(message: Message):
    try:
        data = message.text.split(", ")
        new_vcs = {
            "title": data[0],
            "location": data[1],
            "start_time": data[2],
            "duration": data[3],
            "participants": data[4:]
        }
        response = api_client.create_vcs(new_vcs)
        if response.get("id"):
            await message.answer(f"ВКС успешно создана! Ссылка: {response.get('link')}")
        else:
            await message.answer("Ошибка создания ВКС.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# Хэндлер для команды /help
async def help_command(message: Message):
    await message.answer("Доступные команды:\n/start - Запустить бота\n/login - Авторизация\n/help - Помощь")

# Регистрация хэндлеров
dp.message.register(cmd_start, Command("start"))
dp.callback_query.register(cmd_login, lambda call: call.data == "login")
dp.callback_query.register(cmd_register, lambda call: call.data == "register")
dp.message.register(process_login)
dp.callback_query.register(next_step, lambda call: call.data == "next_step")
dp.message.register(process_register)
dp.callback_query.register(upcoming_vcs, lambda call: call.data == "upcoming")
dp.callback_query.register(create_vcs, lambda call: call.data == "create")
dp.message.register(process_create_vcs, lambda message: "," in message.text)
dp.message.register(help_command, Command("help"))

# Главная функция запуска
async def main():
    try:
        print("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
