from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
import sqlite3


BOT_TOKEN = '8108748639:AAEb2q4qPj55WlGh8IUByiQJ3aTdZQ8098Q'
photo_url = "https://png.pngtree.com/png-vector/20230107/ourmid/pngtree-new-original-transparent-car-png-image_6554552.png"  

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def sub_ended(user):

    await bot.delete_message(chat_id=user[0], message_id=user[8])

    msg = await bot.send_photo(
        chat_id=user[0],
        caption="Ваша подписка закончилась", 
        photo=photo_url
    )

    last_message_id = msg.message_id

    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE users SET last_message_id = ? WHERE user_id = ?''', (last_message_id, user[0]))
    conn.commit()

    print(last_message_id)
    print(cursor.execute('SELECT last_message_id FROM users WHERE user_id = ?', (user[0],)).fetchone())

    conn.close()
