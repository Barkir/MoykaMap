from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from datetime import *
import asyncio
import sqlite3

BOT_TOKEN = '8108748639:AAEb2q4qPj55WlGh8IUByiQJ3aTdZQ8098Q'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

last_message_id = 0
link = "https://moykamap-barkir.amvera.io/"
photo_url = "https://png.pngtree.com/png-vector/20230107/ourmid/pngtree-new-original-transparent-car-png-image_6554552.png"  

def get_db_connection():
    return sqlite3.connect('bot_users.db')


@dp.message(Command(commands=['start', 'tart']))    
async def send_welcome(message: Message):
    global last_message_id, photo_url, link

    # Добавление пользователя в базу данных
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    is_subscribed = False

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))

    last_message_id = cursor.execute('SELECT last_message_id FROM users WHERE user_id = ?', (message.from_user.id,)).fetchone()

    if last_message_id[0] != 0:
        await bot.delete_message(chat_id=message.chat.id, message_id=last_message_id[0])

    gift = cursor.execute('SELECT gift FROM users WHERE user_id = ?', (message.from_user.id,)).fetchone()
    link = cursor.execute('SELECT link FROM users WHERE user_id = ?', (message.from_user.id,)).fetchone()
    status_sub = cursor.execute('SELECT is_subscribed FROM users WHERE user_id = ?', (message.from_user.id,)).fetchone()
    conn.commit()

    # Обработка случая повтороного вызова start с полученным подарком
    if gift[0]:
        if status_sub[0]:
            app_btn = InlineKeyboardButton(text="Открыть приложение", web_app=WebAppInfo(url=link[0]))
        else: 
            app_btn = InlineKeyboardButton(text="Открыть приложение", callback_data="web_app_btn")

        support_btn = InlineKeyboardButton(text="Техподдержка", callback_data="support_btn")

        inline_kbd = InlineKeyboardMarkup(inline_keyboard=[[support_btn], [app_btn]])

        msg = await message.answer_photo(
            photo=photo_url,
            reply_markup=inline_kbd,
            caption="👋Привет!\n\n"
            "Этот бот поможет тебе найти ближайшую свободную автомойку."
        )
    else: # Вызывается до получения подарка
        gift_btn = InlineKeyboardButton(text="Получить подарок", callback_data="gift_btn")
        inline_kbd = InlineKeyboardMarkup(inline_keyboard=[[gift_btn]])

        msg = await message.answer_photo(photo=photo_url,
                                reply_markup=inline_kbd,
                                caption="👋Привет!\n\n"
                                "Этот бот поможет тебе найти ближайшую свободную автомойку.\n\n"
                                "🎁Месяц бесплатной подписки для новых клиентов"
                                )    
    last_message_id = msg.message_id

    cursor.execute('''UPDATE users SET last_message_id = ? WHERE user_id = ?''', (last_message_id, message.from_user.id))
    conn.commit()

    conn.close()
    

@dp.callback_query(F.data == "gift_btn")
async def gift_cmd(callback: CallbackQuery):
    global last_message_id, photo_url

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
    await callback.answer()

    # Изменение статуса подписки
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    gift = cursor.execute("SELECT gift FROM users WHERE user_id = ?", (callback.from_user.id,)).fetchone()

    if not gift[0]:
        current_time = datetime.now()
        end_time = (current_time + timedelta(seconds=15)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''UPDATE users SET is_subscribed = ? WHERE user_id = ?''', (int(1), callback.from_user.id))
        cursor.execute('''UPDATE users SET link = ? WHERE user_id = ?''', ("https://moykamap-barkir.amvera.io/", callback.from_user.id))
        cursor.execute('''UPDATE users SET end_date = ? WHERE user_id = ?''', (end_time, callback.from_user.id))
        cursor.execute('''UPDATE users SET gift = ? WHERE user_id = ?''', (1, callback.from_user.id))
        conn.commit()

        cursor.execute('SELECT end_date FROM users WHERE user_id = ?', (callback.from_user.id,))
        end_date = cursor.fetchone()

    if end_date != "None":
        app_btn = InlineKeyboardButton(text="Открыть приложение", web_app=WebAppInfo(url=link[0]))
    else:
        app_btn = InlineKeyboardButton(text="Открыть приложение", callback_data="web_app_btn")
    support_btn = InlineKeyboardButton(text="Техподдержка", callback_data="support_btn")
    kbd = InlineKeyboardMarkup(inline_keyboard=[[support_btn], [app_btn]])


    msg = await callback.message.answer_photo(
        caption="🥳Поздравляем!!!\n\n Вы получили месяц бесплатной подписки",
        reply_markup=kbd,
        photo=photo_url
        )   
    last_message_id = msg.message_id 

    cursor.execute('''UPDATE users SET last_message_id = ? WHERE user_id = ?''', (last_message_id, callback.from_user.id))
    conn.commit()

    conn.close()


@dp.callback_query(F.data == "support_btn")
async def support_cmd(callback: CallbackQuery):
    global photo_url, last_message_id

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
    await callback.answer()

    msg = await callback.message.answer_photo(
        photo=photo_url,
        caption="Если у вас возникли проблемы, то вы можете написать на наш официальный аккаунт\n\n@danilxl"
    )
    last_message_id = msg.message_id 

    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE users SET last_message_id = ? WHERE user_id = ?''', (last_message_id, callback.from_user.id))
    conn.commit()

    conn.close()


# Вызывается если при нажатии на приложение, в случае если подписки нет
@dp.callback_query(F.data == "web_app_btn")
async def web_app_cancel_btn(callback: CallbackQuery):
    global photo_url, last_message_id

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
    await callback.answer()

    month_1_btn = InlineKeyboardButton(text="1 месяц    99 рублей", callback_data="month_1_btn")
    month_6_btn = InlineKeyboardButton(text="6 месяцев  499 рублей", callback_data="month_6_btn")
    month_12_btn = InlineKeyboardButton(text="1 год     899 рублей", callback_data="month_12_btn")
    kbd = InlineKeyboardMarkup(inline_keyboard=[[month_1_btn], [month_6_btn], [month_12_btn]])

    msg = await callback.message.answer_photo(
        caption="😢 Извините, ваша подписка закончилась\n\nВы можете ее продлить ",
        photo=photo_url,
        reply_markup=kbd
    )
    last_message_id = msg.message_id

    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE users SET last_message_id = ? WHERE user_id = ?''', (last_message_id, callback.from_user.id))
    conn.commit()

    conn.close()


if __name__ == '__main__':
    dp.run_polling(bot)
