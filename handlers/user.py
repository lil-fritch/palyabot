from aiogram import types, Dispatcher, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, dp, API_KEY
from database.sqlite import *
from keyboars.user_kb import *

import requests

headers = {
    'Authorization': f'Bearer {API_KEY}'
}
"""=========ІНШІ ФУНКЦІЇ========="""

    
async def start_process(message: types.Message):
    if message.chat.type == 'private':
        if await user_exists(message.from_user.id):
            global user_tag, action
            user_tag = await get_user_tag(message.from_user.id)
            action = message.text
            await message.answer('Введи тег свого клану\nВін виглядає приблизно так: #2Q8C2Y9GG')
            await FSMClanTag.clan_tag.set()  

        else:
            await message.answer('Щоб продовжити роботу з ботом, тобі необхідно прив\'язати свій ігровий аккаунт Clash of Clans до Telegram')
            
class FSMClanTag(StatesGroup):
    clan_tag = State()
    
async def clan_tag(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        global clan_tag_cr, members_cr
        if message.text[0] != '#': clan_tag_cr = message.text
        else: clan_tag_cr = message.text.removeprefix('#')
        req = requests.get(f'https://api.clashofclans.com/v1/clans/%23{clan_tag_cr}/members', headers=headers)
        print(req.status_code)
        if req.status_code == 200:
            members_cr = req.json()['items']
            for member in members_cr:
                if user_tag == member['tag']:
                    if member['role'] == 'leader' or member['role'] == 'coLeader':
                        await message.answer('Доступ дозволено')
                        if action == 'Столиця клану': await FSMCapitalRaidNotification.capital_raid_notification.set()
                        elif action == 'Кланова війна': await FSMClanWar.clan_war_notification.set()
                    else: 
                        await message.answer('Щоб виконати цю команду, ви повинні бути головою клану або керівником :(')
                        await state.finish()
                        break
                else:
                    await message.answer('Доступ заборонено. Ти не є учасником цього клану.')
                    await state.finish()
                    break
        elif req.status_code == 404:
            await message.answer('Клана з таким тегом не існує, або ти в ньому не перебуваєш.')
            await state.finish()
        else:  await state.finish()  

# async def cancel(message: types.Message, state: FSMContext):
#     if message.chat.type == 'private':
#         await state.finish()
#         await start(message)
        
        
"""=========СТАРТ========="""
async def start(message: types.Message):
    if message.chat.type == 'private':
        if not await user_exists(message.from_user.id):
            await message.answer('''Привіт! \n\nДля повної роботи бота тобі необхідно прив\'язати твій аккаунт 
Clash of Clans до твого аккаунта Telergam. \n\nДля цього натисти кнопку «Прив\'яжи мене!»
''', reply_markup=kb_beginning)
        else: await message.answer('КУ', reply_markup=kb_start)

            
class FSMVerification(StatesGroup):
    tag = State()
    api_token = State()


async def start_process_verify(message: types.Message):
    if message.chat.type == 'private':
        if not await user_exists(message.from_user.id):
            await message.answer('''Для початку відправ мені свій тег, 
ти можеш знайти його у своєму профілі в грі.
\nВін виглядає приблизно так: #YOPLG2LOU
Можеш відправляти як з хештегом, так і без нього :)''', reply_markup=kbi_back)
            await FSMVerification.tag.set()
        else:
            await message.answer('Щоб продовжити роботу з ботом, тобі необхідно прив\'язати свій ігровий аккаунт Clash of Clans до Telegram')
            await start(message)
        
        
async def tag(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        global user_tag
        if message.text[0] == '#': user_tag = message.text.removeprefix('#')
        else: user_tag = message.text
        user_tag = user_tag.replace('O', '0')
        await FSMVerification.api_token.set()
        await message.answer(f'''Твій тег: #{user_tag}. Якщо щось не так, натисни «Назад» 
Тепер мені потрібен твій API Token.
Ти можеш знайти його в налаштунках самої гри.
\nВін виглядає приблизно так: abc123xx
Увага! Не зволікай, тому що токен швидко оновлюється!''', reply_markup=kbi_back)
        
            
async def api_token(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        global user_token
        user_token = message.text
        
        req = requests.post(f'https://api.clashofclans.com/v1/players/%23{user_tag}/verifytoken', json={'token':user_token}, headers=headers)
        res = req.json()['status']
        if res == 'ok':
            await message.answer(f'''Вітаю, все пройшло успішно!
Тепер ваш аккунт Clash of Clan (#{user_tag}) прив\'язаний до 
Telegram\'а (@{message.from_user.username}) ''')
            await add_user(message.from_user.id, message.from_user.username, f'#{user_tag}')
            await set_clan_tag()
            await state.finish()
        else: 
            await message.answer(f'''Сталася помилка.  
Давай спробуємо знову, відправ свій тег,
ти можеш знайти його у своєму профілі в грі.
\nВін виглядає приблизно так: #YOPLG2LOU
Можеш відправляти як з хештегом, так і без нього,
буква О чи цифра 0 - не має різниці :)''')
            await FSMVerification.tag.set()
        
@dp.callback_query_handler(text='back')
async def cancel(call: types.CallbackQuery):
    await call.answer('qqq')  
    
            
"""=========СТОЛИЧНІ РЕЙДИ========="""
class FSMCapitalRaidNotification(StatesGroup):
    capital_raid_notification = State()

              
async def capital_raid_notification(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == 'Відмітити всіх, хто не провів 5 атак':
            req = requests.get(f'https://api.clashofclans.com/v1/clans/%23{clan_tag_cr}/capitalraidseasons', headers=headers)
            res = req.json()['items'][0]
            if res['state'] == 'ongoing':
 
                memebers = res['members']
                memebers_clened_dict={}
                resp_members = []
                
                count = 0
                for m in memebers:
                    count +=1
                    if m['attacks'] < 5: memebers_clened_dict[str(count)]={'name':m['name'], 'tag':m['tag'], 'attacks':m['attacks']}                        
                    elif m['attacks'] >=5: resp_members.append(m['tag'])
                        
                temp_tags_list= []
                for i in memebers_clened_dict:
                    temp_tags_list.append(memebers_clened_dict[i]['tag']) 
                    
                for m in members_cr:
                    count += 1
                    if m['tag'] not in temp_tags_list:
                        if m['tag'] in resp_members: pass
                        else: memebers_clened_dict[str(count)]={'name':m['name'], 'tag':m['tag'], 'attacks':0 }   
                
                message_text_all = 'Люди, які провели не всі атаки в столичних рейдах, покваптесь!\n\n' 
                for m in memebers_clened_dict:
                    username = await get_username(memebers_clened_dict[m]['tag']) 
                    message_text_all +=f'• @{str(username)} (' + memebers_clened_dict[m]['name'] + ') - провів: ' + str(memebers_clened_dict[m]['attacks']) + '/6\n'
                await bot.send_message('-871172410', message_text_all)
                await message.answer('Гравці, що провели менше 5 атак, \nУСПІШНО повідомлені про це в чаті')
                await state.finish()
                
            else: 
                await message.answer('Зараз не проходять дні столичних рейдів')
                await state.finish()
        else:
            await state.finish()
     

"""=========КЛАНОВІ ВІЙНИ========="""
class FSMClanWar(StatesGroup):
    clan_war_notification = State()

async def clan_war_notification(message: types.Message, state: FSMContext):
        if message.chat.type == 'private':
            if message.text == 'Відмітити всіх, хто не провів 2 атаки':
                req = requests.get(f'https://api.clashofclans.com/v1/clans/%232Q8C2Y9GG/currentwar', headers=headers)
                members = req.json()['clan']['members']

                for member in members:
                    message = ''
                    try:
                        if member['attacks']: message += member['name']+': '+str(len(member['attacks']))
                    except: message += member['name']+': 0'
                    print(message)


"""=========КЛАНОВІ ВІЙНИ========="""    
async def settings(message: types.Message, state: FSMContext):
        if message.chat.type == 'private':
            await message.answer('Обери дію:', reply_markup=kb_settings) 

class FSMSettings(StatesGroup):
    set_clan_tag = State()       

async def choise_clan_tag(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Напиши тег клану, який буде використовуватися за замовчуванням:')
        await FSMSettings.set_clan_tag.set()
        
async def set_clan_tag(message: types.Message, state: StatesGroup):
    if message.chat.type == 'private':
        if message.text[0] != '#': clan_tag = message.text
        else: clan_tag = message.text.removeprefix('#')
        req = requests.get(f'https://api.clashofclans.com/v1/clans/%23{clan_tag}/members', headers=headers)
        print(req.status_code)
        if req.status_code == 200:
            await add_clan_tag(message.from_user.id, clan_tag)
            await message.answer(f'Клан з тегом #{clan_tag} успішно додано.\nТи можеш в будь-який момент змінити його на інший.')
        else:
            await message.answer('Клана з таким тегом не існує.', reply_markup=kb_start)
            await state.finish()
        
        
def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(start_process_verify, filters.Text(equals='Прив\'яжи мене!'))
    # dp.register_message_handler(cancel, filters.Text(equals='Відміна'), state='*')
    dp.register_message_handler(clan_tag, state=FSMClanTag.clan_tag)

    dp.register_callback_query_handler(cancel, filters.Text(equals='back'))

    dp.register_message_handler(settings, filters.Text(equals='Налаштунки'))


    dp.register_message_handler(tag, state=FSMVerification.tag)
    dp.register_message_handler(api_token, state=FSMVerification.api_token)
    
    dp.register_message_handler(start_process, filters.Text(equals='Столиця клану'))
    dp.register_message_handler(capital_raid_notification, state=FSMCapitalRaidNotification.capital_raid_notification)
    
    dp.register_message_handler(start_process, filters.Text(equals='Кланова війна'))
    dp.register_message_handler(clan_war_notification, state=FSMClanWar.clan_war_notification)
    
    dp.register_message_handler(choise_clan_tag, filters.Text(equals='Клан тег за замовчуванням'))
    dp.register_message_handler(set_clan_tag, state=FSMSettings.set_clan_tag)

    dp.register_callback_query_handler(callback=cancel, text='back')

    
    





    
    


