from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo

BOT_TOKEN = '8108748639:AAEb2q4qPj55WlGh8IUByiQJ3aTdZQ8098Q'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start(message: Message):

    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Open App', web_app=WebAppInfo(url="https://moykamap-barkir.amvera.io/"))]],
                                 resize_keyboard=True
                                 )

    await message.answer(text="Hey", reply_markup=markup)


if __name__ == '__main__':
    dp.run_polling(bot)