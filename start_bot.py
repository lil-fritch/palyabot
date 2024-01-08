from aiogram.utils import executor
from create_bot import dp, bot
from handlers import user, admin, other
from database import sqlite 

async def on_startup(_):
    sqlite.start_sql()
    await bot.send_message(1306364171, 'Бот запущено\n/start')
    
user.register_handlers_user(dp)
# admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)