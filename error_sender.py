import config
from aiogram.utils import executor
from aiogram import Bot, Dispatcher

bot = Bot(token=config.ErrorBot_TOKEN)
dp = Dispatcher(bot)

async def send_error():
    await bot.send_message(config.DIx_ID, "Привет")

def se():
    executor.start(dp, send_error())