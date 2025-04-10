import sqlite3
from datetime import datetime

# Подключаемся к базе данных (или создаем её, если она не существует)
conn = sqlite3.connect('bot_users.db')
cursor = conn.cursor()

# Создаем таблицу пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    is_subscribed INTEGER DEFAULT 0,
    link TEXT DEFAULT "https://appstorrent.ru/tags/ableton/",
    end_date TEXT,
    gift INTEGER DEFAULT 0,
    last_message_id INTEGER DEFAULT 0
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()