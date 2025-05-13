import sqlite3
import user


def make_db():
    conn = sqlite3.connect('users_table.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                interests TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()


make_db()
user1 = user.User(*input().split(sep=", "), input().split(sep=", "))
user2 = user.User(*input().split(sep=", "), input().split(sep=", "))
user3 = user.User(*input().split(sep=", "), input().split(sep=", "))
print(user1.interests)
print(user2.find_similar_users())
