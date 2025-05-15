import json
import sqlite3
from config import db_table


class User:
    def __init__(self, tg_id, name, interests, description, photo, likes, i):
        self.tg_id = tg_id
        self.name = name
        if type(interests) is str:
            interests = interests.split(", ")
            self.interests = interests
        elif type(interests) is list:
            self.interests = interests
        self.photo = photo
        self.description = description
        self.db_table = db_table
        self.likes = []
        self.similars = []
        self.i = i
        self.update()

    def db(self):
        try:
            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()

            interests_json = json.dumps(self.interests)
            likes = json.dumps(self.likes) if self.likes else None
            cursor.execute('INSERT OR REPLACE INTO users (tg_id, name, interests, description, photo, likes, i)'
                           ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (self.tg_id, self.name, interests_json, self.description, self.photo, likes, self.i))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def change_name(self, name):
        try:
            self.name = name
            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET name = ? WHERE tg_id = ?', (self.name, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def add_i(self):
        try:
            self.i += 1
            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET i = ? WHERE tg_id = ?', (self.i, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def nul_i(self):
        try:
            self.i = -1
            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET i = ? WHERE tg_id = ?', (self.i, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def change_interests(self, interests):
        try:
            if type(interests) is str:
                interests = interests.split(", ")
                self.interests = interests
            elif type(interests) is list:
                self.interests = interests
            interests_json = json.dumps(self.interests)

            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET interests = ? WHERE tg_id = ?', (interests_json, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def change_photo(self, photo):
        try:
            self.photo = photo

            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET photo = ? WHERE tg_id = ?', (self.photo, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def change_description(self, description):
        try:
            self.description = description

            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET description = ? WHERE tg_id = ?', (self.description, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def update(self):
        print(self.db())

    def find_similar_users(self):
        try:
            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('SELECT tg_id, name, interests FROM users WHERE tg_id != ?', (self.tg_id,))
            users = cursor.fetchall()
            conn.close()

            similarities = []
            for other_id, name, interests_json in users:
                if other_id not in self.likes:
                    other_interests = json.loads(interests_json)
                    similarity = jaccard_similarity(self.interests, other_interests)
                    similarities.append((other_id, str(int(similarity * 100)) + "%"))

            similarities.sort(key=lambda x: x[1], reverse=True)
            self.similars = similarities
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def pop_user(self):
        if self.i + 1 < len(self.similars):
            self.add_i()
            return self.similars[self.i]
        else:
            return None, None

    def similar(self):
        if self.i < len(self.similars):
            return self.similars[self.i]
        else:
            return None, None

    def delete_user(self):
        try:
            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE tg_id = ?', (self.tg_id,))
            conn.commit()
            conn.close()
            del self
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def check_db(self):
        try:
            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE id = ?', (self.tg_id,))
            if not cursor.fetchone():
                conn.close()
                return False, "Пользователь не найден."
            return True
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def add_like(self, user):
        try:
            self.likes.append(user.tg_id)
            likes_json = json.dumps(self.likes)

            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET likes = ? WHERE tg_id = ?', (likes_json, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def del_like(self, user):
        try:
            self.likes.remove(user.tg_id)
            likes_json = json.dumps(self.likes)

            conn = sqlite3.connect(self.db_table)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET likes = ? WHERE tg_id = ?', (likes_json, self.tg_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return False, f"Ошибка базы данных: {e}"

    def like(self, user):
        if self.tg_id in user.likes:
            user.del_like(self)
            self.del_like(user)
            return True
        else:
            self.add_like(user)
            return False

    def get_likes(self):
        return [get_user(i) for i in self.likes]


def get_user(tg_id):
    try:
        conn = sqlite3.connect(db_table)
        cursor = conn.cursor()
        cursor.execute('SELECT tg_id, name, interests, description, photo, likes, i FROM users WHERE tg_id = ?', (tg_id,))
        ans = cursor.fetchone()
        conn.close()
        if ans:
            interests = json.loads(ans[2])
            likes = json.loads(ans[5]) if ans[5] else ans[5]
            return User(ans[0], ans[1], interests, ans[3], ans[4], likes, ans[-1])
        else:
            return None
    except sqlite3.Error as e:
        return False, f"Ошибка базы данных: {e}"


def jaccard_similarity(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0
