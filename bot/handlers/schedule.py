from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.api import APIClient
from database.db_manager import get_user

router = Router()

# Состояния FSM для создания ВКС
class ScheduleStates(StatesGroup):
    title = State()
    date = State()
    time = State()
    participants = State()

# Команда для просмотра списка ВКС
@router.message(F.text == "/vks")
async def list_vks(message: Message):
    user = await get_user(message.from_user.id)
    if not user or not user.get("token"):
        await message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        return

    try:
        client = APIClient(token=user["token"])
        meetings = client.get_vks()

        if not meetings:
            await message.answer("Нет запланированных встреч.")
            return

        response = "📅 **Запланированные встречи:**\n\n"
        for meeting in meetings:
            response += (
                f"🔹 **{meeting['title']}**\n"
                f"📆 Дата: {meeting['date']}\n"
                f"⏰ Время: {meeting['time']}\n"
                f"👥 Участники: {', '.join(meeting['participants'])}\n"
                f"ID: {meeting['id']}\n\n"
            )
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Ошибка при получении встреч: {str(e)}")

# Команда для начала создания ВКС
@router.message(F.text == "/create_vks")
async def create_vks_start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or not user.get("token"):
        await message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        return

    await message.answer("Введите название встречи:")
    await state.set_state(ScheduleStates.title)

# Ввод названия встречи
@router.message(ScheduleStates.title)
async def set_vks_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await message.answer("Введите дату встречи (в формате YYYY-MM-DD):")
    await state.set_state(ScheduleStates.date)

# Ввод даты встречи
@router.message(ScheduleStates.date)
async def set_vks_date(message: Message, state: FSMContext):
    date = message.text.strip()
    # Можно добавить проверку формата даты
    await state.update_data(date=date)
    await message.answer("Введите время встречи (в формате HH:MM):")
    await state.set_state(ScheduleStates.time)

# Ввод времени встречи
@router.message(ScheduleStates.time)
async def set_vks_time(message: Message, state: FSMContext):
    time = message.text.strip()
    # Можно добавить проверку формата времени
    await state.update_data(time=time)
    await message.answer("Введите участников через запятую (email):")
    await state.set_state(ScheduleStates.participants)

# Ввод участников и завершение создания ВКС
@router.message(ScheduleStates.participants)
async def set_vks_participants(message: Message, state: FSMContext):
    participants = [p.strip() for p in message.text.split(",")]
    data = await state.get_data()

    user = await get_user(message.from_user.id)
    if not user or not user.get("token"):
        await message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        return

    try:
        client = APIClient(token=user["token"])
        client.create_vks(
            title=data["title"],
            date=data["date"],
            time=data["time"],
            participants=participants,
        )
        await message.answer("Встреча успешно создана!")
    except Exception as e:
        await message.answer(f"Ошибка при создании встречи: {str(e)}")
    finally:
        await state.clear()

# Удаление встречи
@router.message(F.text.startswith("/delete_vks "))
async def delete_vks(message: Message):
    user = await get_user(message.from_user.id)
    if not user or not user.get("token"):
        await message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        return

    meeting_id = message.text.split()[1]
    try:
        client = APIClient(token=user["token"])
        client.delete_vks(meeting_id)
        await message.answer("Встреча успешно удалена.")
    except Exception as e:
        await message.answer(f"Ошибка при удалении встречи: {str(e)}")
