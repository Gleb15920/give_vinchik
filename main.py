import sqlite3
import user


def make_db():
    conn = sqlite3.connect('users_table.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                interests TEXT NOT NULL,
                description TEXT,
                photo TEXT NOT NULL,
                likes TEXT
            )
        ''')
    conn.commit()
    conn.close()


make_db()
# tg_id = input()
# name = input("Напишите имя ")
# interests = input("Напишите интересы ")
# photo = input("Отправьте фото ")
# description = input("Отправьте описание ")
# user1 = user.User(tg_id, name, interests, description, photo)
# print(user1.interests)
# user1.change_interests("fgfg, gfgfg, sdksakl, qwodeiqwdfj, 123")
# print(user1.interests)
# tg_id = input()
# name = input("Напишите имя ")
# interests = input("Напишите интересы ").split()
# photo = input("Отправьте фото ")
# description = input("Отправьте  ")
# user2 = user.User(tg_id, name, interests, description, photo)
# tg_id = input()
# name = input("Напишите имя ")
# interests = input("Напишите интересы ").split()
# photo = input("Отправьте фото ")
# description = input("Отправьте описание ")
# user3 = user.User(tg_id, name, interests, description, photo)
user2 = user.get_user("3124234")
print(user2.description)
print(user2.delete_user())
print(user.get_user("23423"))
