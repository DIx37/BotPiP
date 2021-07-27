import config
from aiogram.utils import executor
from aiogram import Bot, Dispatcher

bot = Bot(token=config.ErrorBot_TOKEN)
dp = Dispatcher(bot)

async def send_error(text):
    await bot.send_message(config.DIx_ID, text)

def se(text):
    executor.start(dp, send_error(text))