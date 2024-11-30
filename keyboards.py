from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Просмотреть предстоящие ВКС", callback_data="upcoming"))
    keyboard.add(InlineKeyboardButton("Создать новую ВКС", callback_data="create"))
    keyboard.add(InlineKeyboardButton("Мои ВКС", callback_data="my_vcs"))
    keyboard.add(InlineKeyboardButton("ВКС моей организации", callback_data="org_vcs"))
    return keyboard