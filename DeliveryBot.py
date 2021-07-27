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

# Включение тестового бота
ID_Delivery_Bot = config.DIx_ID
DeliveryBot_TOKEN = config.ErrorBot_TOKEN
# Подключение бота доставки
#DeliveryBot_TOKEN = config.DeliveryBot_TOKEN
#ID_Delivery_Bot = config.ID_Delivery_Bot

# Уровень логгов
logging.basicConfig(level=logging.INFO)

# Подключение к БД
#db = SQLighter("/home/bots/pip/Delivery.db")
db = SQLighter("Delivery.db")

# Иннициализуем бота
bot = Bot(token=DeliveryBot_TOKEN)
dp = Dispatcher(bot)

async def get_email_for_base_from_site():
    i = 0
    email = "orderspip@yandex.ru"
    while i < len(db.get_send_group(email)):
        id_email = db.get_send_group(email)[i][0]
        data_email = db.get_send_group(email)[i][1]
        print(id_email)
        zapros = DEP.parser_from_site(db.get_send_group(email)[i][4])
        #print(zapros[0])
        #await send_msg("Источник заказа <b>Сайт</b>\n<code>" + str(data_email) + "</code>\n\n" + str(zapros[0]))
        await send_msg("<b>Номер заказа</b>: <code>" + str(id_email) + "</code>\nИсточник заказа <b>Сайт</b>\n\n" + str(zapros[0]))
        #print(zapros[1])
        #print(zapros[2])
        #print(zapros[3])
        #print(zapros[4])
        await send_location(zapros[1], zapros[2], zapros[3], zapros[4])
        db.set_send_group(id_email)
        i += 1
        time.sleep(30)

async def get_email_for_base_from_rubeacon():
    i = 0
    email = "rubeaconorders@gmail.com, delivery@2253838.ru, orders@pizzafab.ru"
    while i < len(db.get_send_group(email)):
        id_email = db.get_send_group(email)[i][0]
        data_email = db.get_send_group(email)[i][1]
        print(id_email)
        #await send_msg("Источник заказа <b>Приложение</b>\n<code>" + str(data_email) + "</code>\n\n" + str(DEP.parser_from_rubeacon(db.get_send_group(email)[i][4])))
        await send_msg("<b>Номер заказа</b>: <code>" + str(id_email) + "</code>\nИсточник заказа <b>Приложение</b>\n\n" + str(DEP.parser_from_rubeacon(db.get_send_group(email)[i][4])))
        db.set_send_group(id_email)
        i += 1
        time.sleep(30)

async def get_email_for_base_from_delivery_club():
    i = 0
    email = "rubeaconorders@gmail.com, delivery@2253838.ru, orders@pizzafab.ru"
    while i < len(db.get_send_group(email)):
        id_email = db.get_send_group(email)[i][0]
        data_email = db.get_send_group(email)[i][1]
        print(id_email)
        #await send_msg("Источник заказа <b>Приложение</b>\n<code>" + str(data_email) + "</code>\n\n" + str(DEP.parser_from_rubeacon(db.get_send_group(email)[i][4])))
        await send_msg("<b>Номер заказа</b>: <code>" + str(id_email) + "</code>\nИсточник заказа <b>Приложение</b>\n\n" + str(DEP.parser_from_rubeacon(db.get_send_group(email)[i][4])))
        db.set_send_group(id_email)
        i += 1
        time.sleep(30)

async def send_msg(text):
    await bot.send_message(ID_Delivery_Bot, text, parse_mode=ParseMode.HTML)
    #await bot.send_message(ID_Delivery_Bot, text)

async def send_location(found_loc, lat, lon, address):
    #lat = "55.5806952"
    #lon = "37.651705105554285"
    #await bot.send_message(ID_Delivery_Bot, address)
    #print(address)
    #await bot.send_message(ID_Delivery_Bot, lat)
    #print(lat)
    #await bot.send_message(ID_Delivery_Bot, lon)
    #print(lon)
    #print(found_loc)
    if found_loc == True:
        await bot.send_location(ID_Delivery_Bot, lat, lon)
    else:
        pass

# Запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
            executor.start(dp, get_email_for_base_from_site())
            executor.start(dp, get_email_for_base_from_rubeacon())
            time.sleep(5)
        except Exception as err:
            print("Ошибка")
            print(err)
            time.sleep(10) # В случае падения