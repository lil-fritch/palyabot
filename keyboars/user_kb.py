from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

button_verification_me = KeyboardButton('Прив\'яжи мене!')

kb_beginning = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_beginning.add(button_verification_me)


button_back = KeyboardButton('Відміна')

kb_back = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_back.add(button_back)


button_settings = KeyboardButton('Налаштунки')

button_feedback = KeyboardButton('Зворотній зв\'язок')

button_сlan_interaction = KeyboardButton('Взаємодія з кланом')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_start.add(button_сlan_interaction).add(button_feedback).insert(button_settings)


button_default_clan_tag = KeyboardButton('Клан тег за замовчуванням')
button_add_new_acc = KeyboardButton('Прив\'язати ще 1 аккаунт')
button_delete_acc = KeyboardButton('Відв\'язати аккаунт')
button_about = KeyboardButton('Про бота')

kb_settings = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_settings.add(button_default_clan_tag).add(button_add_new_acc).add(button_delete_acc).add(button_about)

button_back_2 =  InlineKeyboardButton(text='Назад', callback_data='back')

kbi_back = InlineKeyboardMarkup(row_width=1)
kbi_back.add(button_back_2)
