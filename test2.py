from aiogram.utils import executor
from create_bot import dp, bot
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, filters
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot('6271486620:AAFSMvMTChthiBP6vr5f5-tRX00MgiiZVZ0')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    await bot.send_message(1306364171, 'Бот запущено\n/start')

inkb = InlineKeyboardMarkup(row_width=1)
inbutt = InlineKeyboardButton(text='Стерти', callback_data='clean')
inkb.add(inbutt)

class FSMTest(StatesGroup):
    test = State()

    
async def test(message: types.Message, state: FSMContext):
    await FSMTest.test.set()
    await message.answer(message.text, reply_markup=inkb)
    
# @dp.callback_query_handler(text='clean', state='*')
async def clean(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.delete()
    
def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(test)
    dp.register_callback_query_handler(clean, filters.Text(equals='clean'), state='*' )
    
register_handlers_user(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)