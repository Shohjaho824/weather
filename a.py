import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
import asyncio

API_TOKEN = ''
WEATHER_API_KEY = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Reply markup - klaviatura menyusi yaratish
main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Beshariq")],
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salom! Ob-havo ma'lumotlarini olish uchun shahar nomini yuboring.", reply_markup=main_menu)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Shahar nomini yuboring va men sizga ob-havo ma'lumotlarini beraman.", reply_markup=main_menu)

@dp.message(F.text)
async def get_weather(message: types.Message):
    city_name = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        
        temperature = main['temp']
        description = weather['description']
        await message.answer(f"{city_name} shahrida ob-havo: {temperature}°C, {description}.", reply_markup=main_menu)
    else:
        await message.answer("Shahar topilmadi. Iltimos, yana urinib ko'ring.", reply_markup=main_menu)

async def main():
    await dp.start_polling(bot)

# if __name__ == '__main__':
asyncio.run(main())