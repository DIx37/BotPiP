import config
import logging
import asyncio
import time
import error_sender as es
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from sqllite import SQLighter

# Уровень логгов
logging.basicConfig(level=logging.INFO)

# Подключение к БД
db = SQLighter("Delivery.db")

# Иннициализуем бота
bot = Bot(token=config.ErrorBot_TOKEN)
dp = Dispatcher(bot)


async def get_email_for_base():
    i = 0
    while i < len(db.get_send_group()):
#        print(db.get_send_group()[i][0])
#        send_error(text)
        i += 1
async def send_error():
    await bot.send_message(config.DIx_ID, db.get_send_group()[0][0])

# Запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
            executor.start(dp, get_email_for_base())
        except Exception as err:
            print("Ошибка")
            print(err)
            time.sleep(10) # В случае падения

#db.get_id_email(email_id)
#print(len(db.get_send_group()))