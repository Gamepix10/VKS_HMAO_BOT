from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.api import APIClient
from database.db_manager import get_user

router = Router()

# Состояния FSM для обработки диалогов
class ReplyStates(StatesGroup):
    custom_input = State()

# Общий обработчик текстовых сообщений
@router.message(F.text)
async def handle_reply(message: Message, state: FSMContext):
    current_state = await state.get_state()

    # Если есть активное состояние FSM
    if current_state:
        if current_state == ReplyStates.custom_input:
            await process_custom_input(message, state)
        return

    # Если нет активного состояния, обработка общего сообщения
    await message.answer(
        "Я вас не понял. Используйте команды или введите запрос. Например:\n"
        "- /search для поиска встреч\n"
        "- /filter для фильтрации встреч\n"
        "- /calendar для работы с календарем"
    )

# Обработка пользовательского ввода в состоянии ReplyStates.custom_input
async def process_custom_input(message: Message, state: FSMContext):
    user_input = message.text.strip()
    user = await get_user(message.from_user.id)
    if not user or not user.get("token"):
        await message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        await state.clear()
        return

    try:
        client = APIClient(token=user["token"])
        # Пример обработки пользовательского ввода
        result = client.process_custom_input(user_input)

        if not result:
            await message.answer("Ничего не найдено по вашему запросу.")
        else:
            response = "🔍 **Результаты обработки:**\n\n"
            for item in result:
                response += f"🔹 {item}\n"
            await message.answer(response)

    except Exception as e:
        await message.answer(f"Ошибка при обработке ввода: {str(e)}")
    finally:
        await state.clear()
