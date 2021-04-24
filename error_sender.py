import config
import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

# Уровень логгов
logging.basicConfig(level=logging.INFO)

# Иннициализуем бота
bot = Bot(token=config.ErrorBot_TOKEN)
dp = Dispatcher(bot)

# Эхо
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
    await message.answer(message.from_user.id)

async def sheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        now = datetime.utcnow()
        await bot.send_message(config.DIx_ID, f"{now}", disable_notification = True)

# Запускаем лонг поллинг
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(sheduled(10)) # поставим 10 секунд, в качестве теста
    executor.start_polling(dp, skip_updates=True)