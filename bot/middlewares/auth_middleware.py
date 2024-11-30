from aiogram.types import Update
from aiogram import BaseMiddleware
from aiogram.exceptions import CancelHandler
from aiogram.fsm.context import FSMContext
from typing import Callable, Dict, Any, Awaitable
from database.db_manager import get_user

class AuthMiddleware(BaseMiddleware):
    """
    Middleware для проверки авторизации пользователя.
    """

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем ID пользователя из события
        user_id = event.message.from_user.id if event.message else event.callback_query.from_user.id
        
        # Проверяем наличие пользователя в базе данных
        user = await get_user(user_id)
        if not user or not user.get("token"):
            # Если пользователь не авторизован, отправляем сообщение
            if event.message:
                await event.message.answer("Вы не авторизованы. Используйте команду /start для авторизации.")
            elif event.callback_query:
                await event.callback_query.message.answer("Вы не авторизованы. Используйте команду /start для авторизации.")
                await event.callback_query.answer()
            
            # Прерываем выполнение обработчика
            raise CancelHandler()
        
        # Если пользователь авторизован, передаем управление дальше
        return await handler(event, data)
