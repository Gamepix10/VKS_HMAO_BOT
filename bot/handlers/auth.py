from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.api import APIClient
from database.db_manager import get_user, save_user

router = Router()

# Состояния FSM для авторизации
class AuthStates(StatesGroup):
    email = State()
    password = State()

# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer("Вы уже авторизованы. Для выхода используйте команду /logout.")
    else:
        await message.answer("Добро пожаловать! Пожалуйста, введите ваш email.")
        await state.set_state(AuthStates.email)

# Ввод email
@router.message(AuthStates.email)
async def email_handler(message: Message, state: FSMContext):
    email = message.text.strip()
    await state.update_data(email=email)
    await message.answer("Введите ваш пароль:")
    await state.set_state(AuthStates.password)

# Ввод пароля и аутентификация
@router.message(AuthStates.password)
async def password_handler(message: Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()
    email = data.get("email")

    try:
        # Аутентификация через API
        client = APIClient()
        token = client.authenticate(email, password)

        # Сохранение пользователя в локальной базе
        user_data = {"user_id": message.from_user.id, "email": email, "token": token}
        await save_user(user_data)

        await message.answer("Авторизация успешна! Теперь вы можете использовать бота.")
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка авторизации: {str(e)}. Попробуйте снова.")
        await state.set_state(AuthStates.email)

# Обработчик команды /logout
@router.message(Command("logout"))
async def logout_handler(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await save_user({"user_id": message.from_user.id, "email": None, "token": None})
        await message.answer("Вы успешно вышли из системы.")
    else:
        await message.answer("Вы не авторизованы. Используйте команду /start для входа.")