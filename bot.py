from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo

BOT_TOKEN = '7649004045:AAFm316zw82zPpu4ZYuuWRQ6tDIB3niAuYo'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start(message: Message):

    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Open App', web_app=WebAppInfo(url='https://blindj1.github.io/Moyka-Map/'))]],
                                 resize_keyboard=True
                                 )

    await message.answer(text="Hey", reply_markup=markup)


if __name__ == '__main__':
    dp.run_polling(bot)