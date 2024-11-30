from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from utils.api import APIClient
from database.db_manager import get_user
from uuid import uuid4

router = Router()

# Обработка inline-запросов
@router.inline_query()
async def inline_search(inline_query: InlineQuery):
    user_id = inline_query.from_user.id
    query = inline_query.query.strip()

    if not query:
        await inline_query.answer(
            results=[],
            cache_time=1,
            is_personal=True,
            switch_pm_text="Введите текст для поиска",
            switch_pm_parameter="start",
        )
        return

    user = await get_user(user_id)
    if not user or not user.get("token"):
        await inline_query.answer(
            results=[],
            cache_time=1,
            is_personal=True,
            switch_pm_text="Авторизуйтесь, чтобы использовать поиск",
            switch_pm_parameter="start",
        )
        return

    try:
        client = APIClient(token=user["token"])
        results = client.search_vks(query)

        if not results:
            await inline_query.answer(
                results=[],
                cache_time=1,
                is_personal=True,
                switch_pm_text="Ничего не найдено",
                switch_pm_parameter="start",
            )
            return

        inline_results = []
        for meeting in results:
            text_content = (
                f"📅 **Встреча:** {meeting['title']}\n"
                f"📆 Дата: {meeting['date']}\n"
                f"⏰ Время: {meeting['time']}\n"
                f"👥 Участники: {', '.join(meeting['participants'])}\n"
                f"ID: {meeting['id']}"
            )
            inline_results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=meeting['title'],
                    description=f"Дата: {meeting['date']}, Время: {meeting['time']}",
                    input_message_content=InputTextMessageContent(
                        message_text=text_content
                    ),
                )
            )

        await inline_query.answer(
            results=inline_results,
            cache_time=1,
            is_personal=True,
        )
    except Exception as e:
        await inline_query.answer(
            results=[],
            cache_time=1,
            is_personal=True,
            switch_pm_text=f"Ошибка: {str(e)}",
            switch_pm_parameter="start",
        )
