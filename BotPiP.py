# -- coding: utf-8 --
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Bot, Dispatcher, executor, types
from sqllite import SQLighter
from loguru import logger
import LaurentJSON as LJ
import keyboards as kb
import requests
import weather
import config
import time
import re
import modbusread as MR
import cameraScreen as cs
from aiogram.utils.callback_data import CallbackData
import utils
from modbus import Modbus
from message import Msg

# Переменные
banketniy_zal = Modbus(config.Pixel_IP30)
podval = Modbus(config.Pixel_IP31)
kuhnya = Modbus(config.Pixel_IP32)
gostinaya = Modbus(config.Pixel_IP33)
oranjereya = Modbus(config.Pixel_IP34)
#P_IP30 = config.Pixel_IP30
P_IP31 = config.Pixel_IP31
P_IP32 = config.Pixel_IP32
P_IP33 = config.Pixel_IP33
P_IP34 = config.Pixel_IP34
L_IP20 = config.Laurent_IP_Pool20
L_IP21 = config.Laurent_IP_Pool21
L_IP22 = config.Laurent_IP_Pool22
L_IP24 = config.Laurent_IP_Pool24
L_Pass = config.Laurent_Pass
ControlPiP_TOKEN = config.ControlPiP_TOKEN
space = "                                                                                                    "

# Иннициализуем бота
bot = Bot(token=ControlPiP_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Подключение к БД
db = SQLighter(config.path_bot + "BotPiP.db")
logger.add(config.path_bot + "BotPiP.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")

@logger.catch
def check_user_acess(user, rele):
    if bool(len(db.check_user_acess(user))) == True:
        user_acess = db.check_user_acess(user)[0][3]
        result = re.findall(rele + ",", str(user_acess))
        result = bool(len(result))
    else:
        result = False
    return result

@logger.catch
def message_pool_sun_f():
    weaher = weather.check_weather()
    message_pool = "<b>Погода</b> - " + weaher[2] + f"{space}\n"
    message_pool += "<b>Температура</b> " + weaher[0] + " C, <b>ощущается как</b> " + weaher[1] + " C\n"
    message_pool += "<b>Влажность</b> " + weaher[3] + ", <b>Давление</b> " + weaher[4] + "\n"
    message_pool += "<b>Рассвет</b> в " + weaher[5] + ":" + weaher[6] + ", <b>Закат</b> в " + weaher[7] + ":" + weaher[8] + "\n\n"
    if len(message_pool) > 0:
        return message_pool
    else:
        message_pool = "N/A\n"
        return message_pool

@logger.catch
def message_l20_f():
    l20_json = LJ.l5_json_read_all(L_IP20, L_Pass)
    if l20_json != "N/A":
        l20_message = f"<b>Вентиляция</b>{space}\n"
        l20_message += utils.smile(l20_json[8][0]) + " <b>Мангал</b>\n"
        l20_message += "Скорость: " + str(l20_json[14][0]["vlt"]) + "\n\n"
        l20_message += utils.smile(l20_json[8][1]) + " <b>Пицца</b>\n"
        l20_message += "Скорость: " + str(l20_json[14][1]["vlt"]) + "\n\n"
        l20_message += utils.smile(l20_json[8][2]) + " <b>Остров</b>\n"
        l20_message += "Скорость: " + str(l20_json[14][2]["vlt"]) + "\n\n"
        l20_message += utils.smile(l20_json[8][3]) + " <b>Смокер</b>\n"
        l20_message += "Скорость: " + str(l20_json[14][3]["vlt"]) + "\n\n"
    else:
        l20_message = " <b>Вентиляция</b>\n"
        l20_message += utils.smile("N/A") + " <b>Мангал</b>\n"
        l20_message += "Скорость: N/A\n\n"
        l20_message += utils.smile("N/A") + " <b>Пицца</b>\n"
        l20_message += "Скорость: N/A\n\n"
        l20_message += utils.smile("N/A") + " <b>Остров</b>\n"
        l20_message += "Скорость: N/A\n\n"
        l20_message += utils.smile("N/A") + " <b>Смокер</b>\n"
        l20_message += "Скорость: N/A\n\n"
    return l20_message

@logger.catch
def message_l21_f():
    l21_json = LJ.l5_json_read_all(L_IP21, L_Pass)
    if l21_json != "N/A":
        message_l21 = utils.smile(l21_json[8][0]) + " Бассейн верх\n"
        message_l21 += utils.smile(l21_json[8][1]) + " Бассейн низ\n"
        message_l21 += utils.smile(l21_json[8][2]) + " Под зонтами\n"
        message_l21 += utils.smile(l21_json[8][3]) + " Водопад\n"
        message_l21 += "<b>Температура воды</b>: " + str(l21_json[15][0]["t"]) + " C\n\n"
    else:
        message_l21 = utils.smile("N/A") + " Бассейн верх\n"
        message_l21 += utils.smile("N/A") + " Бассейн низ\n"
        message_l21 += utils.smile("N/A") + " Под зонтами\n"
        message_l21 += utils.smile("N/A") + " Водопад\n"
        message_l21 += "<b>Температура воды</b>: N/A C\n\n"
    return message_l21

@logger.catch
def message_l22_f():
    l22_json = LJ.l5_json_read_all(L_IP22, L_Pass)
    if l22_json != "N/A":
        message_l22 = utils.smile(l22_json[8][0]) + " Под навесом\n"
        message_l22 += utils.smile(l22_json[8][1]) + " Реклама\n"
        message_l22 += utils.smile(l22_json[8][2]) + " Парк\n"
        message_l22 += utils.smile(l22_json[8][3]) + " Экран\n"
        message_l22 += "<b>Температура воздуха</b>: " + str(l22_json[15][0]["t"]) + " C\n\n"
    else:
        message_l22 = utils.smile("N/A") + " Реклама\n"
        message_l22 += utils.smile("N/A") + " Парк\n"
        message_l22 += utils.smile("N/A") + " Парк Периметр\n"
        message_l22 += utils.smile("N/A") + " Экран\n"
        message_l22 += "<b>Температура воздуха</b>: N/A C\n\n"
    return message_l22

@logger.catch
def time_message(DayOfWeek):
    get_pool_time_DayOfWeek = db.get_pool_time_DayOfWeek(DayOfWeek)
    i = 0
    time_message = ""
    while i < len(get_pool_time_DayOfWeek):
        if str(get_pool_time_DayOfWeek[i][4]) == "rekl":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Реклама</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        elif str(get_pool_time_DayOfWeek[i][4]) == "par2":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Парк</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        elif str(get_pool_time_DayOfWeek[i][4]) == "par3":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Парк Периметр</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        elif str(get_pool_time_DayOfWeek[i][4]) == "ekra":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Экран</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        elif str(get_pool_time_DayOfWeek[i][4]) == "new1":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Под зонтами</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        elif str(get_pool_time_DayOfWeek[i][4]) == "new2":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Водопад</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        elif str(get_pool_time_DayOfWeek[i][4]) == "new3":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Бассейн верх</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        elif str(get_pool_time_DayOfWeek[i][4]) == "new4":
            time_message += "ID: " + str(get_pool_time_DayOfWeek[i][0]) + "\n"
            time_message += "<b>Бассейн низ</b>\n"
            time_message += get_pool_time_DayOfWeek[i][2] + ":" + get_pool_time_DayOfWeek[i][3] + "\n"
            time_message += get_pool_time_DayOfWeek[i][5] + "\n\n"
        i += 1
    if len(time_message) == 0:
        time_message = "Нет настроек"
    return time_message

@logger.catch
def add_time(message_text):
    if len(message_text) == 19:
        db.add_time((int(message_text[5:6]) - 1), message_text[12:14], message_text[15:17], message_text[7:11], message_text[18:19])
#       db.add_time(DayOfWeek, Hour, Minutes, Rele, OnOrOff)
        res = "<b>Добавлено время:</b>\n"
        if message_text[5:6] == "1":
            res += "Понедельник"
        elif message_text[5:6] == "2":
            res += "Вторник"
        elif message_text[5:6] == "3":
            res += "Среда"
        elif message_text[5:6] == "4":
            res += "Четверг"
        elif message_text[5:6] == "5":
            res += "Пятница"
        elif message_text[5:6] == "6":
            res += "Суббота"
        elif message_text[5:6] == "7":
            res += "Воскресенье"
        if message_text[7:11] == "rekl":
            res += "\nРеклама\n"
        elif message_text[7:11] == "par2":
            res += "\nПарк\n"
        elif message_text[7:11] == "par3":
            res += "\nПарк Периметр\n"
        elif message_text[7:11] == "ekra":
            res += "\nЭкран\n"
        elif message_text[7:11] == "new1":
            res += "\nПод зонтами\n"
        elif message_text[7:11] == "new2":
            res += "\nВодопад\n"
        elif message_text[7:11] == "new3":
            res += "\nБассейн верх\n"
        elif message_text[7:11] == "new4":
            res += "\nБассейн низ\n"
        res += message_text[12:14] + ":" + message_text[15:17]
        if message_text[18:19] == "0":
            res += "\nВЫключить"
        elif message_text[18:19] == "1":
            res += "\nВключить"
    else:
        res = "Неверная запись"
    return res

@logger.catch
def del_time(message_text):
    db.del_time(message_text[5:7])

@logger.catch
def switch_rele():
    code = 404
    while code == 404:
        code = LJ.check_ip(f"{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=REL,1,1")
        time.sleep(0.1)
    code = 404
    while code == 404:
        code = LJ.check_ip(f"{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=REL,1,0")
        time.sleep(1)

@logger.catch
def l24_xml_f():
    l24_xml = LJ.l2_xml_read_all(L_IP24)
    if l24_xml == "N/A":
        l24_xml = ('N', 'NNNN', 'NNNNNN', 'NNNNNNNNNNNN', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N')
    return l24_xml

@dp.message_handler(commands=['add'])
@logger.catch
async def send_welcome(message: types.Message):
    await message.answer(text=add_time(message.text),
                         reply_markup=kb.menu_time)

@dp.message_handler(commands=['del'])
@logger.catch
async def send_welcome(message: types.Message):
    del_time(message.text)
    await message.answer(text="Удалено",
                         reply_markup=kb.menu_time)

# Перехватываем любое сообщение и выводим главное меню
@dp.message_handler()
@logger.catch
async def main_vent(message: Message):
    await message.answer(text=message_pool_sun_f() + message_l22_f() + message_l21_f(), reply_markup=kb.main_menu(message.from_user.id))

@dp.callback_query_handler(text="pool_menu")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "pool_menu") == True:
        await call.answer()
        await call.message.edit_text(text="Обновляю")
        message_pool_sun = message_pool_sun_f()
        await call.message.edit_text(text=message_pool_sun)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_pool_sun + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_pool_sun + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_pool_sun)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.main_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="vent_menu")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "vent_menu") == True:
        await call.answer()
        await call.message.edit_text(text=message_l20_f())
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.main_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="rekup_pri_menu")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "rekup_pri_menu") == True:
        await call.answer()
        banz = f"<b>Рекуператоры и Приточки</b>{space}\n" + utils.smile(str(banketniy_zal.read(14340))) + " Банкетный Зал\n"
        await call.message.edit_text(text=banz)
        podv = utils.smile(str(MR.modbus_get(P_IP31, 14340))) + " Подвал\n"
        await call.message.edit_text(text=banz + podv)
        kuhn = utils.smile(str(MR.modbus_get(P_IP32, 14340))) + " Кухня\n"
        await call.message.edit_text(text=banz + podv + kuhn)
        gost = utils.smile(str(MR.modbus_get(P_IP33, 14340))) + " Гостиная\n"
        await call.message.edit_text(text=banz + podv + kuhn + gost)
        oran = utils.smile(str(MR.modbus_get(P_IP34, 14340))) + " Оранжерея\n"
        await call.message.edit_text(text=banz + podv + kuhn + gost + oran)
        await call.message.edit_reply_markup(reply_markup=kb.rekup_pri_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(banz + podv + kuhn + gost + oran)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.rekup_pri_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="laurent_menu")
@logger.catch
async def update(call: CallbackQuery):
    laurent_menu = f"<a href='http://172.16.1.20/protect'>172.16.1.20 Вентиляция</a>{space}\n\n"
    laurent_menu += "\n<a href='http://172.16.1.21/protect'>172.16.1.21 Бассейн Подвал</a>\n\n"
    laurent_menu += "\n<a href='http://172.16.1.22/protect'>172.16.1.22 Бассейн</a>\n\n"
    laurent_menu += "\n<a href='http://172.16.1.23/protect'>172.16.1.23 Серверная</a>\n\n"
    laurent_menu += "\n<a href='http://172.16.1.24/protect'>172.16.1.24 Оранжерея</a>"
    if check_user_acess(call.from_user.id, "laurent_menu") == True:
        await call.answer()
        await call.message.edit_text(text=laurent_menu)
        await call.message.edit_reply_markup(reply_markup=kb.laurent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(laurent_menu)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.main_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="main_menu")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=f"Главное меню{space}\n .")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=kb.main_menu(call.from_user.id))
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="podn")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "podn") == True:
        await call.answer()
        switch_rele("L5", L_IP22, L_Pass, 1)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="rekl")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "rekl") == True:
        await call.answer()
        switch_rele("L5", L_IP22, L_Pass, 2)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="park")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "park") == True:
        await call.answer()
        switch_rele("L5", L_IP22, L_Pass, 3)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="ekra")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "ekra") == True:
        await call.answer()
        switch_rele("L5", L_IP22, L_Pass, 4)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="basv")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "basv") == True:
        await call.answer()
        switch_rele("L5", L_IP21, L_Pass, 1)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="basn")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "basn") == True:
        await call.answer()
        switch_rele("L5", L_IP21, L_Pass, 2)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="podz")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "podz") == True:
        await call.answer()
        switch_rele("L5", L_IP21, L_Pass, 3)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="vodo")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "vodo") == True:
        await call.answer()
        switch_rele("L5", L_IP21, L_Pass, 4)
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="ibav")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "ibav") == True:
        await call.answer()
        l21_json = LJ.l5_json_read_all(L_IP21, L_Pass)
        if l21_json[8][0] == "0":
            await call.message.edit_text(text="Бассейн верх выключен, импульс невозможен\n\n\n-= 3 =-")
            time.sleep(1)
            await call.message.edit_text(text="Бассейн верх выключен, импульс невозможен\n💣\n-= 2 =-")
            time.sleep(1)
            await call.message.edit_text(text="Бассейн верх выключен, импульс невозможен\n💣\n-= 1 =-")
            time.sleep(1)
            await call.message.edit_text(text="💣")
            time.sleep(2)
            await call.message.edit_text(text="💥")
            time.sleep(2)
            await call.message.edit_text(text=f"{call.from_user.first_name}, ну вот что ты наделал?")
            time.sleep(2)
        elif l21_json[8][0] == "1":
            requests.get(f"http://{L_IP21}/cmd.cgi?psw={L_Pass}&cmd=REL,1,0")
            time.sleep(0.5)
            requests.get(f"http://{L_IP21}/cmd.cgi?psw={L_Pass}&cmd=REL,1,1")
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="iban")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "iban") == True:
        await call.answer()
        l21_json = LJ.l5_json_read_all(L_IP21, L_Pass)
        if l21_json[8][1] == "0":
            await call.message.edit_text(text="Бассейн низ выключен, импульс невозможен\n\n\n-= 3 =-")
            time.sleep(1)
            await call.message.edit_text(text="Бассейн низ выключен, импульс невозможен\n💣\n-= 2 =-")
            time.sleep(1)
            await call.message.edit_text(text="Бассейн низ выключен, импульс невозможен\n💣\n-= 1 =-")
            time.sleep(1)
            await call.message.edit_text(text="💣")
            time.sleep(2)
            await call.message.edit_text(text="💥")
            time.sleep(2)
            await call.message.edit_text(text=f"{call.from_user.first_name}, ну вот что ты наделал?")
            time.sleep(2)
        elif l21_json[8][1] == "1":
            requests.get(f"http://{L_IP21}/cmd.cgi?psw={L_Pass}&cmd=REL,2,0")
            time.sleep(0.5)
            requests.get(f"http://{L_IP21}/cmd.cgi?psw={L_Pass}&cmd=REL,2,1")
        await call.message.edit_text(text="Обновляю")
        message_w = message_pool_sun_f()
        await call.message.edit_text(text=message_w)
        message_l22 = message_l22_f()
        await call.message.edit_text(text=message_w + message_l22)
        message_l21 = message_l21_f()
        await call.message.edit_text(text=message_w + message_l22 + message_l21)
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_w)
        logger.info(message_l21)
        logger.info(message_l22)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="mang")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "mang") == True:
        await call.answer()
        switch_rele("L5", L_IP20, L_Pass, 1)
        await call.message.edit_text(text=message_l20_f())
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="pizz")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "pizz") == True:
        await call.answer()
        switch_rele("L5", L_IP20, L_Pass, 2)
        await call.message.edit_text(text=message_l20_f())
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="ostr")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "ostr") == True:
        await call.answer()
        switch_rele("L5", L_IP20, L_Pass, 3)
        await call.message.edit_text(text=message_l20_f())
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="smok")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "smok") == True:
        await call.answer()
        switch_rele("L5", L_IP20, L_Pass, 4)
        await call.message.edit_text(text=message_l20_f())
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="smok80")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "smok80") == True:
        await call.answer()
        l20_json = LJ.l5_json_read_all(L_IP20, L_Pass)
        if l20_json != "N/A":
            requests.get(f"http://{L_IP20}/cmd.cgi?psw={L_Pass}&cmd=PWM,4,SET,20")
        await call.message.edit_text(text=message_l20_f())
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(l20_json)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="smok100")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "smok80") == True:
        await call.answer()
        l20_json = LJ.l5_json_read_all(L_IP20, L_Pass)
        if l20_json != "N/A":
            requests.get("http://{L_IP20}/cmd.cgi?psw={L_Pass}&cmd=PWM,4,SET,0")
        await call.message.edit_text(text=message_l20_f())
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(l20_json)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="re_orang")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "re_orang") == True:
        await call.answer()
        await call.message.edit_text(text="Подсматриеваем за камерой")
        cs.screen_f()
        l24_xml = LJ.l2_xml_read_all(L_IP24)
        if l24_xml != "N/A":
            if l24_xml[3][0] == "0":
                await call.message.edit_text(text="Включен режим автоматического переключения каналов")
            elif l24_xml[3][0] == "1":
                await call.message.edit_text(text="Отключен режим автоматического переключения каналов")
            await call.message.edit_reply_markup(reply_markup=kb.re_orang(call.from_user.id))
            res = await bot.send_photo(photo = open(config.path_bot + 'screen0.jpg', 'rb'), chat_id=call.from_user.id)
            time.sleep(5)
            await bot.delete_message(chat_id=call.from_user.id, message_id = res.message_id)
        else:
            message_l24 = "Недоступен"
            await call.message.edit_text(text=message_l24)
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(l24_xml)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.re_orang(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="perekl")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "perekl") == True:
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        await call.answer()
        l24_xml = LJ.l2_xml_read_all(L_IP24)
        if l24_xml != "N/A":
            requests.get(f"http://{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=REL,1,1")
            time.sleep(0.5)
            requests.get(f"http://{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=REL,1,0")
            if l24_xml[3][0] == "0":
                await call.message.edit_text(text="Включен режим автоматического переключения каналов")
            elif l24_xml[3][0] == "1":
                await call.message.edit_text(text="ВЫключен режим автоматического переключения каналов")
            await call.message.edit_reply_markup(reply_markup=kb.re_orang(call.from_user.id))
            time.sleep(5)
            cs.screen_f()
            res = await bot.send_photo(photo = open(config.path_bot + 'screen0.jpg', 'rb'), chat_id=call.from_user.id)
            time.sleep(5)
            await bot.delete_message(chat_id=call.from_user.id, message_id = res.message_id)
        else:
            message_l24 = "Недоступен"
            await call.message.edit_text(text=message_l24)
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(l24_xml)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.re_orang(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="po_time")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "po_time") == True:
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        await call.answer()
        l24_xml = LJ.l2_xml_read_all(L_IP24)
        print(l24_xml)
        if l24_xml != "N/A":
            if l24_xml[3][0] == "0":
                requests.get(f"http://{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=OUT,1,1")
                await call.message.edit_text(text="ВЫключен режим автоматического переключения каналов")
            elif l24_xml[3][0] == "1":
                requests.get(f"http://{L_IP24}/cmd.cgi?psw={L_Pass}&cmd=OUT,1,0")
                await call.message.edit_text(text="Включен режим автоматического переключения каналов")
            await call.message.edit_reply_markup(reply_markup=kb.re_orang(call.from_user.id))
        else:
            message_l24 = "Недоступен"
            await call.message.edit_text(text=message_l24)
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(l24_xml)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.re_orang(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="banketniy_zal")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "banketniy_zal") == True:
        await call.answer()
        message_bank=f"Банкетный зал:{space}\n"
        await call.message.edit_text(text=message_bank)
        pust = banketniy_zal.read(14340)
        if pust == "0":
            message_bank += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_bank += utils.smile(pust) + "   Пуск\n"
        else:
            message_bank += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_bank)
        zile = banketniy_zal.read(14336)
        if zile == "0":
            message_bank += "☀️" + "   Лето\n"
        elif zile == "1":
            message_bank += "❄️" + "   Зима\n"
        else:
            message_bank += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_bank)
        dime = banketniy_zal.read(14337)
        if dime == "0":
            message_bank += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_bank += utils.smile(dime) + "   Дист\n"
        else:
            message_bank += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_bank)
        avar = banketniy_zal.read(14342)
        if avar == "1":
            message_bank += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_bank)
        blok = banketniy_zal.read(14339)
        if blok == "1":
            message_bank += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41023, "float") + " C   Уставка t\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40995, "float") + " C   t Канала\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40993, "float") + " C   t Наружная\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40997, "float") + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41001, "float") + " C   t Вытяжки\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40999, "float") + " C   t Помещения\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(15366) + "   Остановка ВВ\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41106, "holding") + "   Скорость ВП\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41107, "holding") + "   Скорость ВВ\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41103, "holding") + "   Мощность Рекуп.\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41099, "holding") + "   Мощность В. Калор.\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41100, "holding") + "   Мощность Э. Калор.\n"
        await call.message.edit_text(text=message_bank)
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_bank)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="podv")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "podv") == True:
        await call.answer()
        message_bank=f"Подвал:{space}\n"
        await call.message.edit_text(text=message_bank)
        pust = str(MR.modbus_get(P_IP31, 14340))
        if pust == "0":
            message_bank += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_bank += utils.smile(pust) + "   Пуск\n"
        else:
            message_bank += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_bank)
        zile = str(MR.modbus_get(P_IP31, 14336))
        if zile == "0":
            message_bank += "☀️" + "   Лето\n"
        elif zile == "1":
            message_bank += "❄️" + "   Зима\n"
        else:
            message_bank += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_bank)
        dime = str(MR.modbus_get(P_IP31, 14337))
        if dime == "0":
            message_bank += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_bank += utils.smile(dime) + "   Дист\n"
        else:
            message_bank += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_bank)
        avar = str(MR.modbus_get(P_IP31, 14342))
        if avar == "1":
            message_bank += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_bank)
        blok = str(MR.modbus_get(P_IP31, 14339))
        if blok == "1":
            message_bank += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP31, 41023, float)) + " C   Уставка t\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP31, 40995, float)) + " C   t Канала\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP31, 40993, float)) + " C   t Наружная\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP31, 40997, float)) + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP31, 41106, "holding")) + "   Скорость ВП\n"
        await call.message.edit_text(text=message_bank)
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_bank)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="kuhn")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "kuhn") == True:
        await call.answer()
        message_bank=f"Кухня:{space}\n"
        await call.message.edit_text(text=message_bank)
        pust = str(MR.modbus_get(P_IP32, 14340))
        if pust == "0":
            message_bank += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_bank += utils.smile(pust) + "   Пуск\n"
        else:
            message_bank += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_bank)
        zile = str(MR.modbus_get(P_IP32, 14336))
        if zile == "0":
            message_bank += "☀️" + "   Лето\n"
        elif zile == "1":
            message_bank += "❄️" + "   Зима\n"
        else:
            message_bank += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_bank)
        dime = str(MR.modbus_get(P_IP32, 14337))
        if dime == "0":
            message_bank += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_bank += utils.smile(dime) + "   Дист\n"
        else:
            message_bank += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_bank)
        avar = str(MR.modbus_get(P_IP32, 14342))
        if avar == "1":
            message_bank += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_bank)
        blok = str(MR.modbus_get(P_IP32, 14339))
        if blok == "1":
            message_bank += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP32, 41023, float)) + " C   Уставка t\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP32, 40995, float)) + " C   t Канала\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP32, 40993, float)) + " C   t Наружная\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP32, 40997, float)) + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP32, 41106, "holding")) + "   Скорость ВП\n"
        await call.message.edit_text(text=message_bank)
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_bank)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="gost")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "gost") == True:
        await call.answer()
        message_bank=f"Гостиная:{space}\n"
        await call.message.edit_text(text=message_bank)
        pust = str(MR.modbus_get(P_IP33, 14340))
        if pust == "0":
            message_bank += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_bank += utils.smile(pust) + "   Пуск\n"
        else:
            message_bank += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_bank)
        zile = str(MR.modbus_get(P_IP33, 14336))
        if zile == "0":
            message_bank += "☀️" + "   Лето\n"
        elif zile == "1":
            message_bank += "❄️" + "   Зима\n"
        else:
            message_bank += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_bank)
        dime = str(MR.modbus_get(P_IP33, 14337))
        if dime == "0":
            message_bank += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_bank += utils.smile(dime) + "   Дист\n"
        else:
            message_bank += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_bank)
        avar = str(MR.modbus_get(P_IP33, 14342))
        if avar == "1":
            message_bank += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_bank)
        blok = str(MR.modbus_get(P_IP33, 14339))
        if blok == "1":
            message_bank += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP33, 41023, float)) + " C   Уставка t\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP33, 40995, float)) + " C   t Канала\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP33, 40993, float)) + " C   t Наружная\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP33, 40997, float)) + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP33, 41106, "holding")) + "   Скорость ВП\n"
        await call.message.edit_text(text=message_bank)
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_bank)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="oran")
@logger.catch
async def update(call: CallbackQuery):
    if check_user_acess(call.from_user.id, "oran") == True:
        await call.answer()
        message_bank=f"Оранжерея:{space}\n"
        await call.message.edit_text(text=message_bank)
        pust = str(MR.modbus_get(P_IP34, 14340))
        if pust == "0":
            message_bank += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_bank += utils.smile(pust) + "   Пуск\n"
        else:
            message_bank += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_bank)
        zile = str(MR.modbus_get(P_IP34, 14336))
        if zile == "0":
            message_bank += "☀️" + "   Лето\n"
        elif zile == "1":
            message_bank += "❄️" + "   Зима\n"
        else:
            message_bank += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_bank)
        dime = str(MR.modbus_get(P_IP34, 14337))
        if dime == "0":
            message_bank += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_bank += utils.smile(dime) + "   Дист\n"
        else:
            message_bank += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_bank)
        avar = str(MR.modbus_get(P_IP34, 14342))
        if avar == "1":
            message_bank += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_bank)
        blok = str(MR.modbus_get(P_IP34, 14339))
        if blok == "1":
            message_bank += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 41023, float)) + " C   Уставка t\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 40995, float)) + " C   t Канала\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 40993, float)) + " C   t Наружная\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 40997, float)) + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 41001, float)) + " C   t Вытяжки\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 40999, float)) + " C   t Помещения\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 15366)) + "   Остановка ВВ\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 41106, "holding")) + "   Скорость ВП\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 41107, "holding")) + "   Скорость ВВ\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 41103, "holding")) + "   Мощность Рекуп.\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 41099, "holding")) + "   Мощность В. Калор.\n"
        await call.message.edit_text(text=message_bank)
        message_bank += str(MR.modbus_get(P_IP34, 41100, "holding")) + "   Мощность Э. Калор.\n"
        await call.message.edit_text(text=message_bank)
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_bank)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

callback_rap = CallbackData("ustan", "temp_ust", "action", "IP")

@dp.callback_query_handler(callback_rap.filter(action=["ust_minus", "ust_plus"]))
@logger.catch
async def update(call: CallbackQuery, callback_data: dict):
    if check_user_acess(call.from_user.id, "temp_ust_plus") == True:
        await call.answer()
        if callback_data["action"] == "ust_plus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["temp_ust"]), float)
        elif callback_data["action"] == "ust_minus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["temp_ust"]), float)
        message_bank=f"Банкетный зал:{space}\n"
        await call.message.edit_text(text=message_bank)
        pust = banketniy_zal.read(14340)
        if pust == "0":
            message_bank += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_bank += utils.smile(pust) + "   Пуск\n"
        else:
            message_bank += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_bank)
        zile = banketniy_zal.read(14336)
        if zile == "0":
            message_bank += "☀️" + "   Лето\n"
        elif zile == "1":
            message_bank += "❄️" + "   Зима\n"
        else:
            message_bank += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_bank)
        dime = banketniy_zal.read(14337)
        if dime == "0":
            message_bank += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_bank += utils.smile(dime) + "   Дист\n"
        else:
            message_bank += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_bank)
        avar = banketniy_zal.read(14342)
        if avar == "1":
            message_bank += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_bank)
        blok = banketniy_zal.read(14339)
        if blok == "1":
            message_bank += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41023, "float") + " C   Уставка t\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40995, "float") + " C   t Канала\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40993, "float") + " C   t Наружная\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40997, "float") + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41001, "float") + " C   t Вытяжки\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(40999, "float") + " C   t Помещения\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(15366) + "   Остановка ВВ\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41106, "holding") + "   Скорость ВП\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41107, "holding") + "   Скорость ВВ\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41103, "holding") + "   Мощность Рекуп.\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41099, "holding") + "   Мощность В. Калор.\n"
        await call.message.edit_text(text=message_bank)
        message_bank += banketniy_zal.read(41100, "holding") + "   Мощность Э. Калор.\n"
        await call.message.edit_text(text=message_bank)
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и получил доступ")
        logger.info(message_bank)
    else:
        await call.answer()
        await call.message.edit_text(text=f"<b>ДОСТУП ЗАПРЕЩЁН!</b>\n\n{call.from_user.first_name}, хватит тыкать кнопки!")
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal(call.from_user.id))
        logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data) + " и НЕ получил доступ")

@dp.callback_query_handler(text="time")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Выберите день недели для отображения настроек на выбранный день.\nДля удаление наберите:\n<code>/del id</code>.\nДля добавления наберите:\n<code>/add ДеньНедели Реле Час Минута Вкл/Выкл</code>\nНапример:\n<code>/add 1 rekl 10 00 1</code>\nДень недели 1-7\nРеле:\nРеклама - <code>rekl</code>\nПарк - <code>par2</code>\nПарк периметр - <code>par3</code>\nЭкран - <code>ekra</code>\nПод зонтами - <code>new1</code>\nВодопад - <code>new2</code>\nБассейн верх - <code>new3</code>\nБассейн низ - <code>new4</code>")
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="pon")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=time_message(0))
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="vto")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=time_message(1))
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="sre")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=time_message(2))
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="che")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=time_message(3))
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="pya")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=time_message(4))
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="sub")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=time_message(5))
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

@dp.callback_query_handler(text="vos")
@logger.catch
async def update(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=time_message(6))
    await call.message.edit_reply_markup(reply_markup=kb.menu_time)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))

# Запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
            time.sleep(5)
        except Exception as err:
            logger.error(err)
            time.sleep(10) # В случае падения