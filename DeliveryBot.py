import config
import logging
import asyncio
import time
import error_sender as es
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from sqllite import SQLighter

db.get_id_email(email_id)

# Уровень логгов
logging.basicConfig(level=logging.INFO)

# Подключение к БД
db = SQLighter("Delivery.db")

# Иннициализуем бота
bot = Bot(token=config.ErrorBot_TOKEN)
dp = Dispatcher(bot)

async def send_error():
    await bot.send_message(config.DIx_ID, "Привет")

# Запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
            executor.start(dp, send_error())
        except Exception as err:
            print("Ошибка")
            print(err)
            time.sleep(10) # В случае падения