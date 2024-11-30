from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.api import APIClient
from database.db_manager import get_user

router = Router()

# Состояния FSM для поиска
class SearchStates(StatesGroup):
    query = State()

# Команда для начала поиска
@router.message(F.text == "/search")
async def search_start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or not user.get("token"):
        await message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        return

    await message.answer("Введите запрос для поиска (например, название встречи или email участника):")
    await state.set_state(SearchStates.query)

# Обработка запроса поиска
@router.message(SearchStates.query)
async def search_query(message: Message, state: FSMContext):
    query = message.text.strip()
    user = await get_user(message.from_user.id)
    if not user or not user.get("token"):
        await message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        return

    try:
        client = APIClient(token=user["token"])
        results = client.search_vks(query)

        if not results:
            await message.answer("Ничего не найдено по вашему запросу.")
        else:
            response = "🔍 **Результаты поиска:**\n\n"
            for meeting in results:
                response += (
                    f"🔹 **{meeting['title']}**\n"
                    f"📆 Дата: {meeting['date']}\n"
                    f"⏰ Время: {meeting['time']}\n"
                    f"👥 Участники: {', '.join(meeting['participants'])}\n"
                    f"ID: {meeting['id']}\n\n"
                )
            await message.answer(response)
    except Exception as e:
        await message.answer(f"Ошибка при выполнении поиска: {str(e)}")
    finally:
        await state.clear()

# Фильтрация ВКС через inline-кнопки
@router.message(F.text == "/filter")
async def filter_start(message: Message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("По дате", callback_data="filter:date"),
        InlineKeyboardButton("По участникам", callback_data="filter:participants"),
        InlineKeyboardButton("По названию", callback_data="filter:title"),
    )
    await message.answer("Выберите критерий фильтрации:", reply_markup=markup)

# Обработка выбора фильтра
@router.callback_query(F.data.startswith("filter:"))
async def filter_select(callback: CallbackQuery):
    criterion = callback.data.split(":")[1]

    if criterion == "date":
        await callback.message.answer("Введите дату в формате YYYY-MM-DD:")
        await callback.answer()

    elif criterion == "participants":
        await callback.message.answer("Введите email или имя участника:")
        await callback.answer()

    elif criterion == "title":
        await callback.message.answer("Введите часть названия встречи:")
        await callback.answer()


