import config
import logging
import asyncio
import time
import error_sender as es
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from sqllite import SQLighter
import DeliveryEmailParser as DEP
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions

# Уровень логгов
logging.basicConfig(level=logging.INFO)

# Подключение к БД
db = SQLighter("Delivery.db")

# Иннициализуем бота
bot = Bot(token=config.DeliveryBot_TOKEN)
dp = Dispatcher(bot)

async def get_email_for_base_from_site():
    i = 0
    email = "orderspip@yandex.ru"
    while i < len(db.get_send_group(email)):
        id_email = db.get_send_group(email)[i][0]
        data_email = db.get_send_group(email)[i][1]
        print(id_email)
        await send_msg("_Источник заказа_ - *Сайт*\n_" + str(data_email) + "_\n\n" + str(DEP.parser_from_site(db.get_send_group(email)[i][4])))
        db.set_send_group(id_email)
        i += 1
        time.sleep(5)

async def get_email_for_base_from_rubeacon():
    i = 0
    email = "rubeaconorders@gmail.com, delivery@2253838.ru, orders@pizzafab.ru"
    while i < len(db.get_send_group(email)):
        id_email = db.get_send_group(email)[i][0]
        data_email = db.get_send_group(email)[i][1]
        print(id_email)
        await send_msg("Источник заказа - *Приложение*\n_" + str(data_email) + "_\n\n" + str(DEP.parser_from_rubeacon(db.get_send_group(email)[i][4])))
        db.set_send_group(id_email)
        i += 1
        time.sleep(5)

async def send_msg(text):
    #await bot.send_message(config.ID_Delivery_Bot, text)
    await bot.send_message(config.ID_Delivery_Bot, text, parse_mode=ParseMode.MARKDOWN)

# Запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
            executor.start(dp, get_email_for_base_from_site())
            executor.start(dp, get_email_for_base_from_rubeacon())
        except Exception as err:
            print("Ошибка")
            print(err)
            time.sleep(10) # В случае падения