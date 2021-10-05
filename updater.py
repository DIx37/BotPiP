from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils import executor
from aiogram.types import Message, CallbackQuery, message
from utils import weather as Weather
from utils import keyboards as KB
from utils import message as Msg
from config import *
import time
from utils import sql as SQL


# Подключение к БД
db = SQL.SQLighter("BotPiP.db")

# Иннициализуем бота
bot = Bot(token=ControlPiP_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


# def weather_text():
#     weather = Weather.check_weather()
#     text = f"<b>В Сосенках:</b>{space}\n"
#     text += f"<b>Погода</b> - {weather['weather_weather']}\n"
#     text += f"<b>Темп.</b> {weather['temp']} C°, <b>ощущается как</b> {weather['feels_like']} C°\n"
#     text += f"<b>Влажность:</b> {weather['humidity']}%, <b>Давление:</b> {weather['pressure']} мм.рт.ст.\n"
#     text += f"<b>Скорость ветра:</b> {weather['wind_speed']} м/с\n"
#     text += f"<b>Восход</b> в {weather['sunrise'].strftime('%H:%M:%S')}\n"
#     text += f"<b>Закат</b> в {weather['sunset'].strftime('%H:%M:%S')}"
#     return text

async def update_message(chat_id, message_id, menu, reply_markup):
    try:
        if menu == "main_menu":
            # weather_t = weather_text()
            weather_t = Msg.main_menu()
            await bot.edit_message_text(text=f".{weather_t}", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
            time.sleep(1)
            await bot.edit_message_text(text=f"...{weather_t}", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
            time.sleep(1)
            await bot.edit_message_text(text=weather_t, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
            print("Отредактировал")
        elif menu == "pool_menu":
            pool_menu_t = Msg.pool_menu(4)[0]
            await bot.edit_message_text(text=f".{pool_menu_t}", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
            time.sleep(1)
            await bot.edit_message_text(text=f"...{pool_menu_t}", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
            time.sleep(1)
            await bot.edit_message_text(text=pool_menu_t, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
            print("Отредактировал")
    except Exception as err:
        if str(err) == "Message to edit not found":
            print("Ошибка масага ту едит нот фунд")
        print(f"err {err}")

async def main():
    user_all = db.get_all_user()
    for user in user_all:
        if user[4] != None:
            await update_message(user[1], user[4], user[3], KB.pool_menu(user[1]))
    time.sleep(10)

while True:
    executor.start(dp, main())