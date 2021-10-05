from aiogram.types import Message, CallbackQuery, message
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, executor
from aiogram.utils import executor
from utils import keyboards as KB
from utils import message as Msg
from utils import sql as SQL
from loguru import logger
from config import *
import time

# Подключение к БД
db = SQL.SQLighter("BotPiP.db")

# Настройка логгирования, архивация старого лога каждый день
logger.add("log\main.log", format="{time} {level} {message}", level="DEBUG", rotation="1 day", compression="zip")

# Иннициализуем бота
bot = Bot(token=ControlPiP_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


""" Отлов любых сообщений """
@logger.catch
@dp.message_handler()
async def main(message: Message):
    try:
        user_all = db.get_all_user()
        for user in user_all:
            if int(user[1]) == message.from_user.id:
                await bot.delete_message(chat_id=user[1], message_id=user[4])
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await message.answer(text=Msg.main_menu(), reply_markup=KB.main_menu(message.from_user.id))
    except Exception as err:
        await Msg.send_error(bot, err, message.from_user.id, message.message_id, reply_markup=KB.main_menu(message.from_user.id))
    message.message_id = message.message_id + 1
    db.update_last(message.from_user.id, "main_menu", message.message_id)

""" Главное меню """
@logger.catch
@dp.callback_query_handler(text="main_menu")
async def update(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.edit_text(text=Msg.main_menu(), reply_markup=KB.main_menu(call.from_user.id))
    except Exception as err:
        await call.answer()
        await Msg.send_error(bot, err, call.from_user.id, reply_markup=KB.main_menu(call.from_user.id))
    db.update_last(call.from_user.id, "main_menu", call.message.message_id)

""" Меню бассейна """
@logger.catch
@dp.callback_query_handler(text="pool_menu")
async def update(call: CallbackQuery):
    try:
        await call.answer()
        weather = Msg.pool_menu(1)
        await call.message.edit_text(text=weather[0], reply_markup=KB.pool_menu(call.from_user.id))
        l22_json = Msg.pool_menu(2, weather[1])
        await call.message.edit_text(text=l22_json[0], reply_markup=KB.pool_menu(call.from_user.id))
        l21_json = Msg.pool_menu(3, l22_json[1], l22_json[2])
        await call.message.edit_text(text=l21_json[0], reply_markup=KB.pool_menu(call.from_user.id))
    except Exception as err:
        await call.answer()
        await Msg.send_error(bot, err, call.from_user.id, call.message.message_id, reply_markup=KB.main_menu(call.from_user.id))
    db.update_last(call.from_user.id, "pool_menu", call.message.message_id)

""" Меню вентиляции """
@logger.catch
@dp.callback_query_handler(text="vent_menu")
async def update(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.edit_text(text=Msg.vent_menu(), reply_markup=KB.vent_menu(call.from_user.id))
    except Exception as err:
        await call.answer()
        await Msg.send_error(bot, err, call.from_user.id, call.message.message_id, reply_markup=KB.main_menu(call.from_user.id))
    db.update_last(call.from_user.id, "vent_menu", call.message.message_id)

""" Меню рекуператоров и приточек """
@logger.catch
@dp.callback_query_handler(text="rekup_pri_menu")
async def update(call: CallbackQuery):
    try:
        await call.answer()
        banz = Msg.rekup_pri_menu(1)
        await call.message.edit_text(text=banz[0], reply_markup=KB.rekup_pri_menu(call.from_user.id))
        podv = Msg.rekup_pri_menu(2, banz[1])
        await call.message.edit_text(text=podv[0], reply_markup=KB.rekup_pri_menu(call.from_user.id))
        kuhn = Msg.rekup_pri_menu(3, podv[1], podv[2])
        await call.message.edit_text(text=kuhn[0], reply_markup=KB.rekup_pri_menu(call.from_user.id))
        gost = Msg.rekup_pri_menu(4, kuhn[1], kuhn[2], kuhn[3])
        await call.message.edit_text(text=gost[0], reply_markup=KB.rekup_pri_menu(call.from_user.id))
        oran = Msg.rekup_pri_menu(5, gost[1], gost[2], gost[3], gost[4])
        await call.message.edit_text(text=oran[0], reply_markup=KB.rekup_pri_menu(call.from_user.id))
    except Exception as err:
        await call.answer()
        await Msg.send_error(bot, err, call.from_user.id, call.message.message_id, reply_markup=KB.main_menu(call.from_user.id))
    db.update_last(call.from_user.id, "rekup_pri_menu", call.message.message_id)

""" Меню оранжерея реклама """
@logger.catch
@dp.callback_query_handler(text="ad_orangereya")
async def update(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.edit_text(text=Msg.ad_orangereya(), reply_markup=KB.ad_orangereya(call.from_user.id))
    except Exception as err:
        await call.answer()
        await Msg.send_error(bot, err, call.from_user.id, call.message.message_id, reply_markup=KB.main_menu(call.from_user.id))
    db.update_last(call.from_user.id, "ad_orangereya", call.message.message_id)

""" Меню ссылок на Laurent """
@logger.catch
@dp.callback_query_handler(text="laurent_menu")
async def update(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.edit_text(text=Msg.laurent_menu(), reply_markup=KB.rekup_pri_menu(call.from_user.id))
    except Exception as err:
        await call.answer()
        await Msg.send_error(bot, err, call.from_user.id, call.message.message_id, reply_markup=KB.main_menu(call.from_user.id))
    db.update_last(call.from_user.id, "laurent_menu", call.message.message_id)

""" Меню управление ботами """
@logger.catch
@dp.callback_query_handler(text="control_bot_menu")
async def update(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.edit_text(text=Msg.control_bot_menu(), reply_markup=KB.rekup_pri_menu(call.from_user.id))
    except Exception as err:
        await call.answer()
        await Msg.send_error(bot, err, call.from_user.id, call.message.message_id, reply_markup=KB.main_menu(call.from_user.id))
    db.update_last(call.from_user.id, "control_bot_menu", call.message.message_id)

""" Запускаем поллинг """
while True:
    try:
        executor.start_polling(dp, skip_updates=True)
        time.sleep(5)
    except Exception as err:
        print(f"Ошибка: {err}")
        Msg.send_error(bot, err, message.from_user.id, reply_markup=KB.main_menu(message.from_user.id))
        time.sleep(10)