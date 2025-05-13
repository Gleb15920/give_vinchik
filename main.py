import sqlite3

def make_db():
    conn = sqlite3.connect('users_table.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                interests_array TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()


