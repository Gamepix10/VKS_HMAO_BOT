from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Функция для создания клавиатуры с кнопками "Регистрация" и "Логин"
def start_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[  # Матрица кнопок
            [InlineKeyboardButton(text="Регистрация", callback_data="register")],
            [InlineKeyboardButton(text="Логин", callback_data="login")]
        ]
    )
    return keyboard