from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from utils.api import APIClient
from database.db_manager import get_user

router = Router()

# Функция для создания календаря
def generate_calendar(year, month):
    from calendar import monthrange

    markup = InlineKeyboardMarkup(row_width=7)
    # Заголовок календаря
    markup.add(
        InlineKeyboardButton(f"{year}-{month:02}", callback_data="ignore")
    )

    # Дни недели
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    markup.row(*(InlineKeyboardButton(day, callback_data="ignore") for day in days))

    # Дни месяца
    _, last_day = monthrange(year, month)
    first_day = datetime(year, month, 1).weekday()
    days_buttons = []

    # Добавляем пустые кнопки перед первым днем месяца
    for _ in range(first_day):
        days_buttons.append(InlineKeyboardButton(" ", callback_data="ignore"))

    for day in range(1, last_day + 1):
        days_buttons.append(
            InlineKeyboardButton(
                str(day), callback_data=f"calendar_date:{year}-{month:02}-{day:02}"
            )
        )

    # Добавляем кнопки в календарь
    markup.row(*days_buttons[:7])
    for i in range(7, len(days_buttons), 7):
        markup.row(*days_buttons[i : i + 7])

    # Кнопки навигации
    prev_month = (month - 1) or 12
    next_month = (month % 12) + 1
    prev_year = year if month > 1 else year - 1
    next_year = year if month < 12 else year + 1
    markup.row(
        InlineKeyboardButton("◀️", callback_data=f"calendar_nav:{prev_year}-{prev_month:02}"),
        InlineKeyboardButton("▶️", callback_data=f"calendar_nav:{next_year}-{next_month:02}"),
    )
    return markup

# Команда /calendar
@router.message(F.text == "/calendar")
async def calendar_start(message: Message):
    today = datetime.today()
    calendar = generate_calendar(today.year, today.month)
    await message.answer("Выберите дату:", reply_markup=calendar)

# Обработка навигации календаря
@router.callback_query(F.data.startswith("calendar_nav:"))
async def navigate_calendar(callback: CallbackQuery):
    _, date = callback.data.split(":")
    year, month = map(int, date.split("-"))
    calendar = generate_calendar(year, month)
    await callback.message.edit_text("Выберите дату:", reply_markup=calendar)

# Обработка выбора даты
@router.callback_query(F.data.startswith("calendar_date:"))
async def select_date(callback: CallbackQuery):
    _, date = callback.data.split(":")
    user = await get_user(callback.from_user.id)
    if not user or not user.get("token"):
        await callback.message.answer("Вы не авторизованы. Пожалуйста, войдите в систему через /start.")
        return

    try:
        client = APIClient(token=user["token"])
        meetings = client.get_vks_by_date(date)

        if not meetings:
            await callback.message.answer(f"На {date} встреч не запланировано.")
            return

        response = f"📅 **Встречи на {date}:**\n\n"
        for meeting in meetings:
            response += (
                f"🔹 **{meeting['title']}**\n"
                f"⏰ Время: {meeting['time']}\n"
                f"👥 Участники: {', '.join(meeting['participants'])}\n"
                f"ID: {meeting['id']}\n\n"
            )
        await callback.message.answer(response)
    except Exception as e:
        await callback.message.answer(f"Ошибка при получении встреч: {str(e)}")
