import sqlite3 as sq

db = sq.connect('database.db')
cur = db.cursor()  

member = {
    'attacks':6,
    'name': 'fritch',
    'tag': '#YOPLG2LOU'
}

def get_user_id_sql(game_tag):
    
    return cur.execute('SELECT user_id FROM users WHERE game_tag = ?',(game_tag,)).fetchone()[0]

print(get_user_id_sql(member['tag']))