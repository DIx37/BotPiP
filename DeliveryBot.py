import config
import logging
import asyncio
import time
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
import error_sender as es

# Уровень логгов
logging.basicConfig(level=logging.INFO)

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