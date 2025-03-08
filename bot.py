from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo

BOT_TOKEN = '8108748639:AAEb2q4qPj55WlGh8IUByiQJ3aTdZQ8098Q'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    photo_url = "https://png.pngtree.com/png-vector/20230107/ourmid/pngtree-new-original-transparent-car-png-image_6554552.png"  # Пример URL изображения
    app_btn = InlineKeyboardButton(text="Open app", web_app=WebAppInfo(url="https://moykamap-barkir.amvera.io/"))
    support_btn = InlineKeyboardButton(text="Техподдержка", callback_data="support_btn")
    inline_kbd = InlineKeyboardMarkup(inline_keyboard=[[support_btn], [app_btn]])

    await message.answer_photo(photo=photo_url,
                               reply_markup=inline_kbd,
                               caption="Привет! Этот бот поможет тебе найти "
                                       "близжайшую свободную автомойку, которая подойдет "
                                       "именно для тебя"
                               )


if __name__ == '__main__':
    dp.run_polling(bot)
