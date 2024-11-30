from aiogram import Router

from bot.handlers.auth import router as auth_router
from bot.handlers.schedule import router as schedule_router
from bot.handlers.calendar import router as calendar_router
from bot.handlers.search import router as search_router


def setup_handlers() -> Router:
    """
    Функция для настройки и регистрации всех обработчиков.

    :return: Основной роутер с подключёнными обработчиками.
    """
    router = Router()

    # Регистрация обработчиков
    router.include_router(auth_router)
    router.include_router(schedule_router)
    router.include_router(calendar_router)
    router.include_router(search_router)


    return router
