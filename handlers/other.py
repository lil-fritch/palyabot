from create_bot import bot, dp
from aiogram import types, Dispatcher
from database.sqlite import *
from handlers.user import start

async def unknown_message(message: types.Message):
    if message.chat.type == 'private':
        if await user_exists(message.from_user.id):   
            await message.answer('☹️ Невідома команда. Я не знаю, що відповісти 🤷‍♂️')
        else:
            await message.answer('Щоб продовжити роботу з ботом, тобі необхідно прив\'язати свій ігровий аккаунт Clash of Clans до Telegram')
            await start(message)
            
def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(unknown_message)
