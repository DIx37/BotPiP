from utils import weather as Weather
from utils import lauren_json as LJ
from utils import util as U
from utils import modbus as Mb
from utils import modbus as MR
from loguru import logger
from config import space
from config import *
import time

# Переменные
banketniy_zal = Mb.Modbus(Pixel_IP30)
podval = Mb.Modbus(Pixel_IP31)
kuhnya = Mb.Modbus(Pixel_IP32)
gostinaya = Mb.Modbus(Pixel_IP33)
oranjereya = Mb.Modbus(Pixel_IP34)


# Отправка текста ошибки пользователю и добавление её в лог
@logger.catch
async def send_error(bot, err, chat_id, message_id, reply_markup):
    logger.info(f"Пользователь: {chat_id} вызвал ошибку\n{err}")
    try:
        await bot.edit_message_text(text=f"<b>ВНИМАНИЕ!</b>{space}\nОшибка!", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
        time.sleep(2)
        await bot.edit_message_text(text=f"Ошибка:{space}\n{err}", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
    except Exception as err:
        pass

""" Формирование сообщения о погоде """
@logger.catch
def main_menu():
    weather = Weather.check_weather()
    text = f"<b>В Сосенках:</b>{space}\n"
    text += f"<b>Погода</b> - {weather['weather_weather']}\n"
    text += f"<b>Темп.</b> {weather['temp']} C°, <b>ощущается как</b> {weather['feels_like']} C°\n"
    text += f"<b>Влажность:</b> {weather['humidity']}%, <b>Давление:</b> {weather['pressure']} мм.рт.ст.\n"
    text += f"<b>Скорость ветра:</b> {weather['wind_speed']} м/с\n"
    text += f"<b>Восход</b> в {weather['sunrise'].strftime('%H:%M:%S')}\n"
    text += f"<b>Закат</b> в {weather['sunset'].strftime('%H:%M:%S')}"
    return text

""" Формирование сообщения о Бассейне и Веревочном Парке"""
@logger.catch
def pool_menu(msg, weather=None, l22_json=None, l21_json=None):
    if msg == 1:
        weather = Weather.check_weather()
    elif msg == 2:
        l22_json = LJ.l5_json_read_all(Laurent_IP_Pool22, Laurent_Pass)
    elif msg == 3:
        l21_json = LJ.l5_json_read_all(Laurent_IP_Pool21, Laurent_Pass)
    elif msg == 4:
        weather = Weather.check_weather()
        l22_json = LJ.l5_json_read_all(Laurent_IP_Pool22, Laurent_Pass)
        l21_json = LJ.l5_json_read_all(Laurent_IP_Pool21, Laurent_Pass)
    text = pool_menu_text(weather, l22_json, l21_json)
    return text, weather, l22_json, l21_json

@logger.catch
def pool_menu_text(weather, l22_json, l21_json):
    if weather == None:
        weather['weather_weather'] = "-"
        weather['temp'] = "-"
        weather['feels_like'] = "-"
        weather['weather_weather'] = "-"
        weather['sunrise'] = "-"
        weather['sunset'] = "-"
    if l21_json == None:
        l21_json = (0, 0, 0, 0, 0, 0, 0, 0, '----', 0, 0, 0, 0, 0, 0, [{'t': '-'}])
    if l22_json == None:
        l22_json = (0, 0, 0, 0, 0, 0, 0, 0, '----', 0, 0, 0, 0, 0, 0, [{'t': '-'}])
    text = f"<b>Погода</b> - {weather['weather_weather']}{space}\n"
    text += f"<b>Темп.</b> {weather['temp']} C°, <b>ощущается как</b> {weather['feels_like']} C°\n"
    text += f"<b>Восход</b> в {weather['sunrise'].strftime('%H:%M')}  :  "
    text += f"<b>Закат</b> в {weather['sunset'].strftime('%H:%M')}\n\n"
    text += f"<b>Температура воздуха</b>: {str(l22_json[15][0]['t'])} C\n"
    text += f"<b>Температура воды</b>: {str(l21_json[15][0]['t'])} C\n\n"
    text += f"{U.smile(l22_json[8][0])} Под навесом\n"
    text += f"{U.smile(l22_json[8][1])} Реклама\n"
    text += f"{U.smile(l22_json[8][2])} Парк\n"
    text += f"{U.smile(l22_json[8][3])} Экран\n"
    text += f"{U.smile(l21_json[8][0])} Бассейн верх\n"
    text += f"{U.smile(l21_json[8][1])} Бассейн низ\n"
    text += f"{U.smile(l21_json[8][2])} Под зонтами\n"
    text += f"{U.smile(l21_json[8][3])} Водопад\n"
    return text

""" Формирование сообщения о Рекуператорах и Приточках"""
@logger.catch
def rekup_pri_menu(msg, banz="-", podv="-", kuhn="-", gost="-", oran="-"):
    if msg == 1:
        banz = str(MR.modbus_get(Pixel_IP30, 14340))
    elif msg == 2:
        podv = str(MR.modbus_get(Pixel_IP31, 14340))
    elif msg == 3:
        kuhn = str(MR.modbus_get(Pixel_IP32, 14340))
    elif msg == 4:
        gost = str(MR.modbus_get(Pixel_IP33, 14340))
    elif msg == 5:
        oran = str(MR.modbus_get(Pixel_IP34, 14340))
    elif msg == 6:
        banz = str(MR.modbus_get(Pixel_IP30, 14340))
        podv = str(MR.modbus_get(Pixel_IP31, 14340))
        kuhn = str(MR.modbus_get(Pixel_IP32, 14340))
        gost = str(MR.modbus_get(Pixel_IP33, 14340))
        oran = str(MR.modbus_get(Pixel_IP34, 14340))
    text = rekup_pri_menu_text(banz, podv, kuhn, gost, oran)
    return text, banz, podv, kuhn, gost, oran

@logger.catch
def rekup_pri_menu_text(banz, podv, kuhn, gost, oran):
    text = f"{U.smile(banz)} Банкетный Зал{space}\n"
    text += f"{U.smile(podv)} Подвал\n"
    text += f"{U.smile(kuhn)} Кухня\n"
    text += f"{U.smile(gost)} Гостиная\n"
    text += f"{U.smile(oran)} Оранжерея\n"
    print(text)
    return text


# """ Меню рекуператоров и приточек """
# @dp.callback_query_handler(text="rekup_pri_menu")
# @logger.catch
# async def update(call: CallbackQuery):
#     logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
#     await call.answer()
#     banz = f"<b>Рекуператоры и Приточки</b>{space}\n" + utils.smile(str(banketniy_zal.read(14340))) + " Банкетный Зал\n"
#     await call.message.edit_text(text=banz)
#     podv = utils.smile(str(MR.modbus_get(P_IP31, 14340))) + " Подвал\n"
#     await call.message.edit_text(text=banz + podv)
#     kuhn = utils.smile(str(MR.modbus_get(P_IP32, 14340))) + " Кухня\n"
#     await call.message.edit_text(text=banz + podv + kuhn)
#     gost = utils.smile(str(MR.modbus_get(P_IP33, 14340))) + " Гостиная\n"
#     await call.message.edit_text(text=banz + podv + kuhn + gost)
#     oran = utils.smile(str(MR.modbus_get(P_IP34, 14340))) + " Оранжерея\n"
#     await call.message.edit_text(text=banz + podv + kuhn + gost + oran)
#     await call.message.edit_reply_markup(reply_markup=kb.rekup_pri_menu(call.from_user.id))
