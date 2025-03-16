import sqlite3
import asyncio
from functions import sub_ended
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


BOT_TOKEN = '8108748639:AAEb2q4qPj55WlGh8IUByiQJ3aTdZQ8098Q'
photo_url = "https://png.pngtree.com/png-vector/20230107/ourmid/pngtree-new-original-transparent-car-png-image_6554552.png"  

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


conn = sqlite3.connect('bot_users.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM users')

users = cursor.fetchall()

for user in users:
    print(user)
    if user[4] == 1:
        end_date = datetime.strptime(user[6], "%Y-%m-%d %H:%M:%S")
    
        if datetime.now() > end_date:
            print('adwnkldawd')
            cursor.execute('''UPDATE users SET is_subscribed = ? WHERE user_id = ?''', (0, user[0]))
            cursor.execute('''UPDATE users SET end_date = ? WHERE user_id = ?''', ("None", user[0]))
            conn.commit() 

            asyncio.run(sub_ended(user))
       

cursor.close()
