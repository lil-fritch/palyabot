import sqlite3 as sq

def start_sql():
    global db, cur
    db = sq.connect('database.db')
    cur = db.cursor()   
    
    db.execute('CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY, username, game_tag)')
    db.execute('CREATE TABLE IF NOT EXISTS clan_tag(user_id PRIMARY KEY, clan_tag)')


    db.commit()
   
async def add_user(user_id, username=None, game_tag=None):
    try:
        cur.execute('INSERT INTO users VALUES(?, ?, ?)', (user_id, username, game_tag))
        db.commit()
    except:
        pass
    
async def user_exists(user_id):
    r = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
    return bool(len(r)) 


async def get_user_tag(user_id):
    return cur.execute('SELECT game_tag FROM users WHERE user_id = ?',(user_id,)).fetchone()[0]

async def get_user_id(game_tag):
    try:
        return cur.execute('SELECT user_id FROM users WHERE game_tag = ?',(game_tag,)).fetchone()[0]
    except:
        return None

async def get_username(game_tag):
    try:
        return cur.execute('SELECT username FROM users WHERE game_tag = ?',(game_tag,)).fetchone()[0]
    except:
        return None
    
async def add_clan_tag(user_id, clan_tag):
    cur.execute('INSERT INTO clan_tag VALUES(?, ?)', (user_id, clan_tag))
    db.commit()