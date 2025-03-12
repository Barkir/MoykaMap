from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
import sqlite3

BOT_TOKEN = '8108748639:AAEb2q4qPj55WlGh8IUByiQJ3aTdZQ8098Q'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

last_message_id = None
photo_url = "https://png.pngtree.com/png-vector/20230107/ourmid/pngtree-new-original-transparent-car-png-image_6554552.png"  

def get_db_connection():
    return sqlite3.connect('bot_users.db')


@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    global last_message_id, photo_url

    if last_message_id is not None:
        await bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)

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
    sub_status = cursor.execute('SELECT is_subscribed FROM users WHERE user_id = ?', (message.from_user.id,)).fetchone()
    link = cursor.execute('SELECT link FROM users WHERE user_id = ?', (message.from_user.id,)).fetchone()
    conn.commit()

    # Обработка случая повтороного вызова start с полученным подарком
    if sub_status[0]:
        support_btn = InlineKeyboardButton(text="Техподдержка", callback_data="support_btn")
        app_btn = InlineKeyboardButton(text="Открыть приложение", web_app=WebAppInfo(url=link[0]))

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
    conn.close()
    

@dp.callback_query(F.data == "gift_btn")
async def gift_cmd(callback: CallbackQuery):
    global last_message_id, photo_url

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
    await callback.answer()

    # Изменение статуса подписки
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE users SET is_subscribed = ? WHERE user_id = ?''', (int(1), callback.from_user.id))
    cursor.execute('''UPDATE users SET link = ? WHERE user_id = ?''', ("https://moykamap-barkir.amvera.io/", callback.from_user.id))
    conn.commit()

    cursor.execute('SELECT link FROM users WHERE user_id = ?', (callback.from_user.id,))
    link = cursor.fetchone()
    conn.close()


    app_btn = InlineKeyboardButton(text="Открыть приложение", web_app=WebAppInfo(url=link[0]), callback_data="web_app_btn")
    support_btn = InlineKeyboardButton(text="Техподдержка", callback_data="support_btn")
    kbd = InlineKeyboardMarkup(inline_keyboard=[[support_btn], [app_btn]])


    msg = await callback.message.answer_photo(
        caption="🥳Поздравляем!!!\n\n Вы получили месяц бесплатной подписки",
        reply_markup=kbd,
        photo=photo_url
        )   
    last_message_id = msg.message_id 


@dp.callback_query(F.data == "support_btn")
async def gift_cmd(callback: CallbackQuery):
    global photo_url, last_message_id

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
    await callback.answer()

    msg = await callback.message.answer_photo(
        photo=photo_url,
        caption="Если у вас возникли проблемы, то вы можете написать на наш официальный аккаунт\n\n@danilxl"
    )
    last_message_id = msg.message_id 



if __name__ == '__main__':
    dp.run_polling(bot)
