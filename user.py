import json
import sqlite3


db_table = 'users_table.db'

class User:
    def __init__(self, tg_id, name, interests):
        self.tg_id = tg_id
        self.name = name
        self.interests = interests
        self.db_table = db_table
        self.update()
        # self.photo = photo

    def db(self):
        conn = sqlite3.connect(self.db_table)
        cursor = conn.cursor()

        interests_json = json.dumps(self.interests)
        cursor.execute('INSERT OR REPLACE INTO users (tg_id, name, interests) VALUES (?, ?, ?)',
                       (self.tg_id, self.name, interests_json))

        conn.commit()
        conn.close()

    def change_name(self, name):
        pass

    def change_interests(self):
        pass

    def change_photo(self):
        pass

    def update(self):
        self.db()

    def find_similar_users(self):
        conn = sqlite3.connect(self.db_table)
        cursor = conn.cursor()
        cursor.execute('SELECT tg_id, name, interests FROM users WHERE tg_id != ?', (self.tg_id,))
        users = cursor.fetchall()
        conn.close()

        similarities = []
        for other_id, name, interests_json in users:
            other_interests = json.loads(interests_json)
            similarity = jaccard_similarity(self.interests, other_interests)
            similarities.append((name, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities


def get_user(tg_id):
    conn = sqlite3.connect(db_table)
    cursor = conn.cursor()
    cursor.execute('SELECT tg_id, name, interests FROM users WHERE tg_id = ?', (tg_id,))
    ans = cursor.fetchone()
    conn.close()
    if ans:
        return User(ans[0], ans[1], ans[2])
    else:
        return None

def jaccard_similarity(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0
