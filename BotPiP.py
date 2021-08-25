# -- coding: utf-8 --
#from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from sqllite import SQLighter
from loguru import logger
import cameraScreen as cs
from modbus import Modbus
import LaurentJSON as LJ
#from message import Msg
import control_bot as CB
import modbusread as MR
import keyboards as kb
import requests
import weather
import config
import utils
import time
#import re

# Переменные
banketniy_zal = Modbus(config.Pixel_IP30)
podval = Modbus(config.Pixel_IP31)
kuhnya = Modbus(config.Pixel_IP32)
gostinaya = Modbus(config.Pixel_IP33)
oranjereya = Modbus(config.Pixel_IP34)
L_IP20 = config.Laurent_IP_Pool20
L_IP21 = config.Laurent_IP_Pool21
L_IP22 = config.Laurent_IP_Pool22
L_IP24 = config.Laurent_IP_Pool24
L_Pass = config.Laurent_Pass
P_IP30 = config.Pixel_IP30
P_IP31 = config.Pixel_IP31
P_IP32 = config.Pixel_IP32
P_IP33 = config.Pixel_IP33
P_IP34 = config.Pixel_IP34
ControlPiP_TOKEN = config.ControlPiP_TOKEN
space = 100 * " "

# Иннициализуем бота
bot = Bot(token=ControlPiP_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Подключение к БД
db = SQLighter(config.path_bot + "BotPiP.db")
logger.add(config.config_bot + "BotPiP.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")

""" Формирование сообщения о погоде """
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

""" Формирование сообщения о вентиляции"""
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
        l20_message = f" <b>Вентиляция</b>{space}\n"
        l20_message += utils.smile("N/A") + " <b>Мангал</b>\n"
        l20_message += "Скорость: N/A\n\n"
        l20_message += utils.smile("N/A") + " <b>Пицца</b>\n"
        l20_message += "Скорость: N/A\n\n"
        l20_message += utils.smile("N/A") + " <b>Остров</b>\n"
        l20_message += "Скорость: N/A\n\n"
        l20_message += utils.smile("N/A") + " <b>Смокер</b>\n"
        l20_message += "Скорость: N/A\n\n"
    return l20_message

""" Формирование сообщения о бассейне """
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

""" Формирование сообщения о Веревочном парке """
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

""" Формирование сообщения о установленном времени перключения реле """
@logger.catch
def pool_time_message(DayOfWeek):
    get_pool_time_DayOfWeek = db.get_pool_time_DayOfWeek(DayOfWeek)
    time_message = ""
    for rele in get_pool_time_DayOfWeek:
        time_message += "\nID: " + str(rele[0])
        if rele[4] == "pod_navesom":
            time_message += "     <b>Под навесом</b>\n"
        elif rele[4] == "reklama":
            time_message += "     <b>Реклама</b>\n"
        elif rele[4] == "park":
            time_message += "     <b>Парк</b>\n"
        elif rele[4] == "ekran":
            time_message += "     <b>Экран</b>\n"
        elif rele[4] == "pool_up":
            time_message += "     <b>Бассейн верх</b>\n"
        elif rele[4] == "pool_down":
            time_message += "     <b>Бассейн низ</b>\n"
        elif rele[4] == "pod_zontami":
            time_message += "     <b>Под зонтами</b>\n"
        elif rele[4] == "vodopad":
            time_message += "     <b>Водопад</b>\n"
        time_message += rele[2] + ":" + rele[3]
        if rele[5] == "0":
            time_message += " Отключение"
        elif rele[5] == "1":
            time_message += " Включение"
        if rele[6] == "1":
            time_message += " По рассвету"
        elif rele[6] == "2":
            time_message += " По закату"
        if int(rele[7]) < 0 or int(rele[7]) > 0:
            time_message += "\nКоррекция времени на " + rele[7] + " минут"
        time_message += "\n"
    if len(time_message) == 0:
        time_message = "Нет настроек"
    return time_message


""" Добавление в базу времени переключения реле """
""" Нужно переделать """
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

""" Удаление времеи из базы по его ID """
@logger.catch
def del_time(message_text):
    db.del_time(message_text[5:7])

""" Функция переключения реле """
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

""" Получение данных состояния модуля рекламы в оранжереи """
@logger.catch
def l24_xml_f():
    l24_xml = LJ.l2_xml_read_all(L_IP24)
    if l24_xml == "N/A":
        l24_xml = ('N', 'NNNN', 'NNNNNN', 'NNNNNNNNNNNN', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N')
    return l24_xml

""" Отлов команды добавить """
@dp.message_handler(commands=['add'])
@logger.catch
async def send_welcome(message: types.Message):
    logger.info("Пользователь: " + str(message.from_user.id) + " нажал")
    await message.answer(text=add_time(message.text),
                         reply_markup=kb.menu_time)

""" Отлов команды удаления """
@dp.message_handler(commands=['del'])
@logger.catch
async def send_welcome(message: types.Message):
    logger.info("Пользователь: " + str(message.from_user.id) + " нажал")
    del_time(message.text)
    await message.answer(text="Удалено",
                         reply_markup=kb.menu_time)

""" Отлов сообщений """
@dp.message_handler()
@logger.catch
async def main_vent(message: Message):
    logger.info("Пользователь: " + str(message.from_user.id) + " нажал")
    await message.answer(text=message_pool_sun_f() + message_l22_f() + message_l21_f(), reply_markup=kb.main_menu(message.from_user.id))


""" Меню бассейна """
@dp.callback_query_handler(text="pool_menu")
@logger.catch
async def update(call: CallbackQuery):
#    print(call.message)
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    msg = await call.message.edit_text(text="Обновляю")
#    print(msg)
    message_pool_sun = message_pool_sun_f()
    await call.message.edit_text(text=message_pool_sun)
    message_l22 = message_l22_f()
    await call.message.edit_text(text=message_pool_sun + message_l22)
    message_l21 = message_l21_f()
    await call.message.edit_text(text=message_pool_sun + message_l22 + message_l21)
    await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))

""" Меню вентиляции """
@dp.callback_query_handler(text="vent_menu")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=message_l20_f())
    await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))

""" Меню рекуператоров и приточек """
@dp.callback_query_handler(text="rekup_pri_menu")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
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

@dp.callback_query_handler(text="laurent_menu")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    laurent_menu = f"<a href='http://172.16.1.20/protect'>172.16.1.20 Вентиляция</a>{space}\n\n"
    laurent_menu += "\n<a href='http://172.16.1.21/protect'>172.16.1.21 Бассейн Подвал</a>\n\n"
    laurent_menu += "\n<a href='http://172.16.1.22/protect'>172.16.1.22 Бассейн</a>\n\n"
    laurent_menu += "\n<a href='http://172.16.1.23/protect'>172.16.1.23 Серверная</a>\n\n"
    laurent_menu += "\n<a href='http://172.16.1.24/protect'>172.16.1.24 Оранжерея</a>"
    await call.message.edit_text(text=laurent_menu)
    await call.message.edit_reply_markup(reply_markup=kb.laurent_menu(call.from_user.id))

@dp.callback_query_handler(text=["control_bot_menu", "ReleTime", "DeliveryBot", "EmailOrderWritter", "Get_ntv"])
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    if str(call.data) != "control_bot_menu":
        if str(CB.status(call.data)) == "0":
            CB.start(call.data)
        elif str(CB.status(call.data)) == "1":
            CB.stop(call.data)
    BotPiP = utils.smile(str(CB.status("BotPiP"))) + f" BotPiP{space}\n"
    await call.message.edit_text(text=BotPiP)
    ReleTime = utils.smile(str(CB.status("ReleTime"))) + " ReleTime\n"
    await call.message.edit_text(text=BotPiP + ReleTime)
    DeliveryBot = utils.smile(str(CB.status("DeliveryBot"))) + " DeliveryBot\n"
    await call.message.edit_text(text=BotPiP + ReleTime + DeliveryBot)
    EmailOrderWritter = utils.smile(str(CB.status("EmailOrderWritter"))) + " EmailOrderWritter\n"
    await call.message.edit_text(text=BotPiP + ReleTime + DeliveryBot + EmailOrderWritter)
    Get_ntv = utils.smile(str(CB.status("Get_ntv"))) + " Get_ntv\n"
    await call.message.edit_text(text=BotPiP + ReleTime + DeliveryBot + EmailOrderWritter + Get_ntv)
    await call.message.edit_reply_markup(reply_markup=kb.control_bot_menu(call.from_user.id))

@dp.callback_query_handler(text="main_menu")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=f"Главное меню{space}\n .")
    await call.message.edit_reply_markup(reply_markup=kb.main_menu(call.from_user.id))

@dp.callback_query_handler(text=["pod_navesom", "reklama", "park", "ekran", "pool_up", "pool_down", "pod_zontami", "vodopad", "imp_pool_up", "imp_pool_down"])
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    if str(call.data) == "pod_navesom":
        result = LJ.switch_rele("L5", L_IP22, L_Pass, 1)
    elif str(call.data) == "reklama":
        result = LJ.switch_rele("L5", L_IP22, L_Pass, 2)
    elif str(call.data) == "park":
        result = LJ.switch_rele("L5", L_IP22, L_Pass, 3)
    elif str(call.data) == "ekran":
        result = LJ.switch_rele("L5", L_IP22, L_Pass, 4)
    elif str(call.data) == "pool_up":
        result = LJ.switch_rele("L5", L_IP21, L_Pass, 1)
    elif str(call.data) == "pool_down":
        result = LJ.switch_rele("L5", L_IP21, L_Pass, 2)
    elif str(call.data) == "pod_zontami":
        result = LJ.switch_rele("L5", L_IP21, L_Pass, 3)
    elif str(call.data) == "vodopad":
        result = LJ.switch_rele("L5", L_IP21, L_Pass, 4)
    elif str(call.data) == "imp_pool_up":
        l21_json = LJ.l5_json_read_all(L_IP21, L_Pass)
        if l21_json != "N/A":
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
                LJ.set_rele(L_IP21, L_Pass, 1, 0)
                time.sleep(0.5)
                LJ.set_rele(L_IP21, L_Pass, 1, 1)
        else:
            result = 404
    elif str(call.data) == "imp_pool_down":
        l21_json = LJ.l5_json_read_all(L_IP21, L_Pass)
        if l21_json != "N/A":
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
                LJ.set_rele(L_IP21, L_Pass, 2, 0)
                time.sleep(0.5)
                LJ.set_rele(L_IP21, L_Pass, 2, 0)
        else:
            result = 404
    await call.message.edit_text(text="Обновляю")
    message_w = message_pool_sun_f()
    await call.message.edit_text(text=message_w)
    message_l22 = message_l22_f()
    await call.message.edit_text(text=message_w + message_l22)
    message_l21 = message_l21_f()
    await call.message.edit_text(text=message_w + message_l22 + message_l21)
    if result == 404:
        await call.message.edit_text(text=message_w + message_l22 + message_l21 + "\n<b>ВНИМАНИЕ!</b>\nМодуль недоступен, попробуйте ещё раз")
    await call.message.edit_reply_markup(reply_markup=kb.pool_menu(call.from_user.id))


@dp.callback_query_handler(text=["mangal", "pizza", "ostrov", "smoker", "smoker_80", "smoker_100"])
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    if str(call.data) == "mangal":
        result = LJ.switch_rele("L5", L_IP20, L_Pass, 1)
    elif str(call.data) == "pizza":
        result = LJ.switch_rele("L5", L_IP20, L_Pass, 2)
    elif str(call.data) == "ostrov":
        result = LJ.switch_rele("L5", L_IP20, L_Pass, 3)
    elif str(call.data) == "smoker":
        result = LJ.switch_rele("L5", L_IP20, L_Pass, 4)
    elif str(call.data) == "smoker_80":
        l20_json = LJ.l5_json_read_all(L_IP20, L_Pass)
        if l20_json != "N/A":
            LJ.set_rele(L_IP20, L_Pass, 4, 1)
            requests.get(f"http://{L_IP20}/cmd.cgi?psw={L_Pass}&cmd=PWM,4,SET,20")
            result = LJ.switch_rele("L5", L_IP20, L_Pass, 1)
    elif str(call.data) == "smoker_100":
        l20_json = LJ.l5_json_read_all(L_IP20, L_Pass)
        if l20_json != "N/A":
            LJ.set_rele(L_IP20, L_Pass, 4, 1)
            requests.get(f"http://{L_IP20}/cmd.cgi?psw={L_Pass}&cmd=PWM,4,SET,0")
            result = LJ.switch_rele("L5", L_IP20, L_Pass, 1)
    await call.message.edit_text(text=message_l20_f())
    if result == 404:
        await call.message.edit_text(text=message_l20_f() + "\n<b>ВНИМАНИЕ!</b>\nМодуль недоступен, попробуйте ещё раз")
    await call.message.edit_reply_markup(reply_markup=kb.vent_menu(call.from_user.id))


@dp.callback_query_handler(text="ad_orangereya")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text="Подсматриеваем за камерой")
    l24_xml = LJ.l2_xml_read_all(L_IP24)
    if l24_xml != "N/A":
        if l24_xml[3][0] == "0":
            await call.message.edit_text(text="Включен режим автоматического переключения каналов")
        elif l24_xml[3][0] == "1":
            await call.message.edit_text(text="Отключен режим автоматического переключения каналов")
        await call.message.edit_reply_markup(reply_markup=kb.ad_orangereya(call.from_user.id))
        cs.screen_f()
        res = await bot.send_photo(photo = open(config.path_bot + 'screen0.jpg', 'rb'), chat_id=call.from_user.id)
        time.sleep(5)
        await bot.delete_message(chat_id=call.from_user.id, message_id = res.message_id)
    else:
        message_l24 = "Недоступен"
        await call.message.edit_text(text=message_l24)
    logger.info(l24_xml)


@dp.callback_query_handler(text="perekl")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    l24_xml = LJ.l2_xml_read_all(L_IP24)
    if l24_xml != "N/A":
        LJ.set_rele(L_IP24, L_Pass, 1, 1)
        time.sleep(0.5)
        LJ.set_rele(L_IP24, L_Pass, 1, 0)
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
    logger.info(l24_xml)

@dp.callback_query_handler(text="po_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    l24_xml = LJ.l2_xml_read_all(L_IP24)
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
    logger.info(l24_xml)

@dp.callback_query_handler(text="banketniy_zal")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
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
    await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal_menu(call.from_user.id))

@dp.callback_query_handler(text="podval")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    message_podval=f"Подвал:{space}\n"
    await call.message.edit_text(text=message_podval)
    pust = podval.read(14340)
    if pust == "0":
        message_podval += utils.smile(pust) + "   Стоп\n"
    elif pust == "1":
        message_podval += utils.smile(pust) + "   Пуск\n"
    else:
        message_podval += "N/A   Пуск/Стоп\n"
    await call.message.edit_text(text=message_podval)
    zile = podval.read(14336)
    if zile == "0":
        message_podval += "☀️" + "   Лето\n"
    elif zile == "1":
        message_podval += "❄️" + "   Зима\n"
    else:
        message_podval += "N/A   Зима/Лето\n"
    await call.message.edit_text(text=message_podval)
    dime = podval.read(14337)
    if dime == "0":
        message_podval += utils.smile(dime) + "   Мест\n"
    elif dime == "1":
        message_podval += utils.smile(dime) + "   Дист\n"
    else:
        message_podval += "N/A   Дист/Мест\n"
    await call.message.edit_text(text=message_podval)
    avar = podval.read(14342)
    if avar == "1":
        message_podval += "❌" + "   Авария\n"
        await call.message.edit_text(text=message_podval)
    blok = podval.read(14339)
    if blok == "1":
        message_podval += "❌" + "   Блокировка\n"
        await call.message.edit_text(text=message_podval)
    message_podval += podval.read(41023, "float") + " C   Уставка t\n"
    await call.message.edit_text(text=message_podval)
    message_podval += podval.read(40995, "float") + " C   t Канала\n"
    await call.message.edit_text(text=message_podval)
    message_podval += podval.read(40993, "float") + " C   t Наружная\n"
    await call.message.edit_text(text=message_podval)
    message_podval += podval.read(40997, "float") + " C   t Обр. воды\n"
    await call.message.edit_text(text=message_podval)
    message_podval += podval.read(41106, "holding") + "   Скорость ВП\n"
    await call.message.edit_text(text=message_podval)
    await call.message.edit_reply_markup(reply_markup=kb.podval_menu(call.from_user.id))

@dp.callback_query_handler(text="kuhnya")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    message_kuhnya=f"Кухня:{space}\n"
    await call.message.edit_text(text=message_kuhnya)
    pust = kuhnya.read(14340)
    if pust == "0":
        message_kuhnya += utils.smile(pust) + "   Стоп\n"
    elif pust == "1":
        message_kuhnya += utils.smile(pust) + "   Пуск\n"
    else:
        message_kuhnya += "N/A   Пуск/Стоп\n"
    await call.message.edit_text(text=message_kuhnya)
    zile = kuhnya.read(14336)
    if zile == "0":
        message_kuhnya += "☀️" + "   Лето\n"
    elif zile == "1":
        message_kuhnya += "❄️" + "   Зима\n"
    else:
        message_kuhnya += "N/A   Зима/Лето\n"
    await call.message.edit_text(text=message_kuhnya)
    dime = kuhnya.read(14337)
    if dime == "0":
        message_kuhnya += utils.smile(dime) + "   Мест\n"
    elif dime == "1":
        message_kuhnya += utils.smile(dime) + "   Дист\n"
    else:
        message_kuhnya += "N/A   Дист/Мест\n"
    await call.message.edit_text(text=message_kuhnya)
    avar = kuhnya.read(14342)
    if avar == "1":
        message_kuhnya += "❌" + "   Авария\n"
        await call.message.edit_text(text=message_kuhnya)
    blok = kuhnya.read(14339)
    if blok == "1":
        message_kuhnya += "❌" + "   Блокировка\n"
        await call.message.edit_text(text=message_kuhnya)
    message_kuhnya += kuhnya.read(41023, "float") + " C   Уставка t\n"
    await call.message.edit_text(text=message_kuhnya)
    message_kuhnya += kuhnya.read(40995, "float") + " C   t Канала\n"
    await call.message.edit_text(text=message_kuhnya)
    message_kuhnya += kuhnya.read(40993, "float") + " C   t Наружная\n"
    await call.message.edit_text(text=message_kuhnya)
    message_kuhnya += kuhnya.read(40997, "float") + " C   t Обр. воды\n"
    await call.message.edit_text(text=message_kuhnya)
    message_kuhnya += kuhnya.read(41106, "holding") + "   Скорость ВП\n"
    await call.message.edit_text(text=message_kuhnya)
    await call.message.edit_reply_markup(reply_markup=kb.kuhnya_menu(call.from_user.id))

@dp.callback_query_handler(text="gostinaya")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    message_gostinaya=f"Гостиная:{space}\n"
    await call.message.edit_text(text=message_gostinaya)
    pust = gostinaya.read(14340)
    if pust == "0":
        message_gostinaya += utils.smile(pust) + "   Стоп\n"
    elif pust == "1":
        message_gostinaya += utils.smile(pust) + "   Пуск\n"
    else:
        message_gostinaya += "N/A   Пуск/Стоп\n"
    await call.message.edit_text(text=message_gostinaya)
    zile = gostinaya.read(14336)
    if zile == "0":
        message_gostinaya += "☀️" + "   Лето\n"
    elif zile == "1":
        message_gostinaya += "❄️" + "   Зима\n"
    else:
        message_gostinaya += "N/A   Зима/Лето\n"
    await call.message.edit_text(text=message_gostinaya)
    dime = gostinaya.read(14337)
    if dime == "0":
        message_gostinaya += utils.smile(dime) + "   Мест\n"
    elif dime == "1":
        message_gostinaya += utils.smile(dime) + "   Дист\n"
    else:
        message_gostinaya += "N/A   Дист/Мест\n"
    await call.message.edit_text(text=message_gostinaya)
    avar = gostinaya.read(14342)
    if avar == "1":
        message_gostinaya += "❌" + "   Авария\n"
        await call.message.edit_text(text=message_gostinaya)
    blok = gostinaya.read(14339)
    if blok == "1":
        message_gostinaya += "❌" + "   Блокировка\n"
        await call.message.edit_text(text=message_gostinaya)
    message_gostinaya += gostinaya.read(41023, "float") + " C   Уставка t\n"
    await call.message.edit_text(text=message_gostinaya)
    message_gostinaya += gostinaya.read(40995, "float") + " C   t Канала\n"
    await call.message.edit_text(text=message_gostinaya)
    message_gostinaya += gostinaya.read(40993, "float") + " C   t Наружная\n"
    await call.message.edit_text(text=message_gostinaya)
    message_gostinaya += gostinaya.read(40997, "float") + " C   t Обр. воды\n"
    await call.message.edit_text(text=message_gostinaya)
    message_gostinaya += gostinaya.read(41106, "holding") + "   Скорость ВП\n"
    await call.message.edit_text(text=message_gostinaya)
    await call.message.edit_reply_markup(reply_markup=kb.gostinaya_menu(call.from_user.id))

@dp.callback_query_handler(text="oranjereya")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    message_oranjereya=f"Оранжерея:{space}\n"
    await call.message.edit_text(text=message_oranjereya)
    pust = str(MR.modbus_get(P_IP34, 14340))
    if pust == "0":
        message_oranjereya += utils.smile(pust) + "   Стоп\n"
    elif pust == "1":
        message_oranjereya += utils.smile(pust) + "   Пуск\n"
    else:
        message_oranjereya += "N/A   Пуск/Стоп\n"
    await call.message.edit_text(text=message_oranjereya)
    zile = str(MR.modbus_get(P_IP34, 14336))
    if zile == "0":
        message_oranjereya += "☀️" + "   Лето\n"
    elif zile == "1":
        message_oranjereya += "❄️" + "   Зима\n"
    else:
        message_oranjereya += "N/A   Зима/Лето\n"
    await call.message.edit_text(text=message_oranjereya)
    dime = str(MR.modbus_get(P_IP34, 14337))
    if dime == "0":
        message_oranjereya += utils.smile(dime) + "   Мест\n"
    elif dime == "1":
        message_oranjereya += utils.smile(dime) + "   Дист\n"
    else:
        message_oranjereya += "N/A   Дист/Мест\n"
    await call.message.edit_text(text=message_oranjereya)
    avar = str(MR.modbus_get(P_IP34, 14342))
    if avar == "1":
        message_oranjereya += "❌" + "   Авария\n"
        await call.message.edit_text(text=message_oranjereya)
    blok = str(MR.modbus_get(P_IP34, 14339))
    if blok == "1":
        message_oranjereya += "❌" + "   Блокировка\n"
        await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 41023, float)) + " C   Уставка t\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 40995, float)) + " C   t Канала\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 40993, float)) + " C   t Наружная\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 40997, float)) + " C   t Обр. воды\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 41001, float)) + " C   t Вытяжки\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 40999, float)) + " C   t Помещения\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 15366)) + "   Остановка ВВ\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 41106, "holding")) + "   Скорость ВП\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 41107, "holding")) + "   Скорость ВВ\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 41103, "holding")) + "   Мощность Рекуп.\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 41099, "holding")) + "   Мощность В. Калор.\n"
    await call.message.edit_text(text=message_oranjereya)
    message_oranjereya += str(MR.modbus_get(P_IP34, 41100, "holding")) + "   Мощность Э. Калор.\n"
    await call.message.edit_text(text=message_oranjereya)
    await call.message.edit_reply_markup(reply_markup=kb.oranjereya_menu(call.from_user.id))

callback_rap = CallbackData("set", "action", "number", "IP")
@dp.callback_query_handler(callback_rap.filter(action=["pusk", "stop", "dist_mest", "ust_plus", "ust_minus", "set_speed_ventP_plus", "set_speed_ventP_minus", "set_speed_ventV_plus", "set_speed_ventV_minus", "sbros_error", "stop_vv", "start_vv"]))
@logger.catch
async def update(call: CallbackQuery, callback_data: dict):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    if callback_data["IP"] == P_IP30:
        if callback_data["action"] == "pusk":
            MR.modbus_set(callback_data["IP"], 15362, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15362, 0)
            time.sleep(1)
            db.update_rele_status(P_IP30, "1", Stop_start = "1")
        elif callback_data["action"] == "stop":
            MR.modbus_set(callback_data["IP"], 15363, 0)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15363, 1)
            time.sleep(1)
            db.update_rele_status(P_IP30, "1", Stop_start = "0")
    #        elif callback_data["action"] == "dist_mest":
    #            MR.modbus_set(callback_data["IP"], 15360, 1)
    #            time.sleep(2)
    #            MR.modbus_set(callback_data["IP"], 15360, 0)
        elif callback_data["action"] == "sbros_error":
            MR.modbus_set(callback_data["IP"], 15364, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15364, 0)
            time.sleep(1)
        elif callback_data["action"] == "stop_vv":
            MR.modbus_set(callback_data["IP"], 15366, 1)
        elif callback_data["action"] == "start_vv":
            MR.modbus_set(callback_data["IP"], 15366, 0)
        elif callback_data["action"] == "set_speed_ventP_plus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP30, "1", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventP_minus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP30, "1", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_plus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP30, "1", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_minus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP30, "1", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "ust_plus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        elif callback_data["action"] == "ust_minus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
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
        await call.message.edit_reply_markup(reply_markup=kb.banketniy_zal_menu(call.from_user.id))
    elif callback_data["IP"] == P_IP31:
        if callback_data["action"] == "pusk":
            MR.modbus_set(callback_data["IP"], 15362, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15362, 0)
            time.sleep(1)
            db.update_rele_status(P_IP31, "2", Stop_start = "1")
        elif callback_data["action"] == "stop":
            MR.modbus_set(callback_data["IP"], 15363, 0)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15363, 1)
            time.sleep(1)
            db.update_rele_status(P_IP31, "2", Stop_start = "0")
        elif callback_data["action"] == "sbros_error":
            MR.modbus_set(callback_data["IP"], 15364, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15364, 0)
            time.sleep(1)
        elif callback_data["action"] == "stop_vv":
            MR.modbus_set(callback_data["IP"], 15366, 1)
        elif callback_data["action"] == "start_vv":
            MR.modbus_set(callback_data["IP"], 15366, 0)
        elif callback_data["action"] == "set_speed_ventP_plus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP31, "2", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventP_minus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP31, "2", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_plus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP31, "2", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_minus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP31, "2", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "ust_plus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        elif callback_data["action"] == "ust_minus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        message_podval=f"Подвал:{space}\n"
        await call.message.edit_text(text=message_podval)
        pust = podval.read(14340)
        if pust == "0":
            message_podval += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_podval += utils.smile(pust) + "   Пуск\n"
        else:
            message_podval += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_podval)
        zile = podval.read(14336)
        if zile == "0":
            message_podval += "☀️" + "   Лето\n"
        elif zile == "1":
            message_podval += "❄️" + "   Зима\n"
        else:
            message_podval += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_podval)
        dime = podval.read(14337)
        if dime == "0":
            message_podval += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_podval += utils.smile(dime) + "   Дист\n"
        else:
            message_podval += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_podval)
        avar = podval.read(14342)
        if avar == "1":
            message_podval += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_podval)
        blok = podval.read(14339)
        if blok == "1":
            message_podval += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_podval)
        message_podval += podval.read(41023, "float") + " C   Уставка t\n"
        await call.message.edit_text(text=message_podval)
        message_podval += podval.read(40995, "float") + " C   t Канала\n"
        await call.message.edit_text(text=message_podval)
        message_podval += podval.read(40993, "float") + " C   t Наружная\n"
        await call.message.edit_text(text=message_podval)
        message_podval += podval.read(40997, "float") + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_podval)
        message_podval += podval.read(41106, "holding") + "   Скорость ВП\n"
        await call.message.edit_text(text=message_podval)
        await call.message.edit_reply_markup(reply_markup=kb.podval_menu(call.from_user.id))
    elif callback_data["IP"] == P_IP32:
        if callback_data["action"] == "pusk":
            MR.modbus_set(callback_data["IP"], 15362, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15362, 0)
            time.sleep(1)
            db.update_rele_status(P_IP32, "3", Stop_start = "1")
        elif callback_data["action"] == "stop":
            MR.modbus_set(callback_data["IP"], 15363, 0)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15363, 1)
            time.sleep(1)
            db.update_rele_status(P_IP32, "3", Stop_start = "0")
        elif callback_data["action"] == "sbros_error":
            MR.modbus_set(callback_data["IP"], 15364, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15364, 0)
            time.sleep(1)
        elif callback_data["action"] == "stop_vv":
            MR.modbus_set(callback_data["IP"], 15366, 1)
        elif callback_data["action"] == "start_vv":
            MR.modbus_set(callback_data["IP"], 15366, 0)
        elif callback_data["action"] == "set_speed_ventP_plus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP32, "3", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventP_minus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP32, "3", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_plus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP32, "3", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_minus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP32, "3", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "ust_plus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        elif callback_data["action"] == "ust_minus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        message_kuhnya=f"Кухня:{space}\n"
        await call.message.edit_text(text=message_kuhnya)
        pust = kuhnya.read(14340)
        if pust == "0":
            message_kuhnya += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_kuhnya += utils.smile(pust) + "   Пуск\n"
        else:
            message_kuhnya += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_kuhnya)
        zile = kuhnya.read(14336)
        if zile == "0":
            message_kuhnya += "☀️" + "   Лето\n"
        elif zile == "1":
            message_kuhnya += "❄️" + "   Зима\n"
        else:
            message_kuhnya += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_kuhnya)
        dime = kuhnya.read(14337)
        if dime == "0":
            message_kuhnya += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_kuhnya += utils.smile(dime) + "   Дист\n"
        else:
            message_kuhnya += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_kuhnya)
        avar = kuhnya.read(14342)
        if avar == "1":
            message_kuhnya += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_kuhnya)
        blok = kuhnya.read(14339)
        if blok == "1":
            message_kuhnya += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_kuhnya)
        message_kuhnya += kuhnya.read(41023, "float") + " C   Уставка t\n"
        await call.message.edit_text(text=message_kuhnya)
        message_kuhnya += kuhnya.read(40995, "float") + " C   t Канала\n"
        await call.message.edit_text(text=message_kuhnya)
        message_kuhnya += kuhnya.read(40993, "float") + " C   t Наружная\n"
        await call.message.edit_text(text=message_kuhnya)
        message_kuhnya += kuhnya.read(40997, "float") + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_kuhnya)
        message_kuhnya += kuhnya.read(41106, "holding") + "   Скорость ВП\n"
        await call.message.edit_text(text=message_kuhnya)
        await call.message.edit_reply_markup(reply_markup=kb.kuhnya_menu(call.from_user.id))
    elif callback_data["IP"] == P_IP33:
        if callback_data["action"] == "pusk":
            MR.modbus_set(callback_data["IP"], 15362, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15362, 0)
            time.sleep(1)
            db.update_rele_status(P_IP33, "4", Stop_start = "1")
        elif callback_data["action"] == "stop":
            MR.modbus_set(callback_data["IP"], 15363, 0)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15363, 1)
            time.sleep(1)
            db.update_rele_status(P_IP33, "4", Stop_start = "0")
        elif callback_data["action"] == "sbros_error":
            MR.modbus_set(callback_data["IP"], 15364, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15364, 0)
            time.sleep(1)
        elif callback_data["action"] == "stop_vv":
            MR.modbus_set(callback_data["IP"], 15366, 1)
        elif callback_data["action"] == "start_vv":
            MR.modbus_set(callback_data["IP"], 15366, 0)
        elif callback_data["action"] == "set_speed_ventP_plus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP33, "4", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventP_minus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP33, "4", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_plus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP33, "4", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_minus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP33, "4", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "ust_plus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        elif callback_data["action"] == "ust_minus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        message_gostinaya=f"Гостиная:{space}\n"
        await call.message.edit_text(text=message_gostinaya)
        pust = gostinaya.read(14340)
        if pust == "0":
            message_gostinaya += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_gostinaya += utils.smile(pust) + "   Пуск\n"
        else:
            message_gostinaya += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_gostinaya)
        zile = gostinaya.read(14336)
        if zile == "0":
            message_gostinaya += "☀️" + "   Лето\n"
        elif zile == "1":
            message_gostinaya += "❄️" + "   Зима\n"
        else:
            message_gostinaya += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_gostinaya)
        dime = gostinaya.read(14337)
        if dime == "0":
            message_gostinaya += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_gostinaya += utils.smile(dime) + "   Дист\n"
        else:
            message_gostinaya += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_gostinaya)
        avar = gostinaya.read(14342)
        if avar == "1":
            message_gostinaya += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_gostinaya)
        blok = gostinaya.read(14339)
        if blok == "1":
            message_gostinaya += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_gostinaya)
        message_gostinaya += gostinaya.read(41023, "float") + " C   Уставка t\n"
        await call.message.edit_text(text=message_gostinaya)
        message_gostinaya += gostinaya.read(40995, "float") + " C   t Канала\n"
        await call.message.edit_text(text=message_gostinaya)
        message_gostinaya += gostinaya.read(40993, "float") + " C   t Наружная\n"
        await call.message.edit_text(text=message_gostinaya)
        message_gostinaya += gostinaya.read(40997, "float") + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_gostinaya)
        message_gostinaya += gostinaya.read(41106, "holding") + "   Скорость ВП\n"
        await call.message.edit_text(text=message_gostinaya)
        await call.message.edit_reply_markup(reply_markup=kb.gostinaya_menu(call.from_user.id))
    elif callback_data["IP"] == P_IP34:
        if callback_data["action"] == "pusk":
            MR.modbus_set(callback_data["IP"], 15362, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15362, 0)
            time.sleep(1)
            db.update_rele_status(P_IP34, "5", Stop_start = "1")
        elif callback_data["action"] == "stop":
            MR.modbus_set(callback_data["IP"], 15363, 0)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15363, 1)
            time.sleep(1)
            db.update_rele_status(P_IP34, "5", Stop_start = "0")
        elif callback_data["action"] == "sbros_error":
            MR.modbus_set(callback_data["IP"], 15364, 1)
            time.sleep(2)
            MR.modbus_set(callback_data["IP"], 15364, 0)
            time.sleep(1)
        elif callback_data["action"] == "stop_vv":
            MR.modbus_set(callback_data["IP"], 15366, 1)
        elif callback_data["action"] == "start_vv":
            MR.modbus_set(callback_data["IP"], 15366, 0)
        elif callback_data["action"] == "set_speed_ventP_plus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP34, "5", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventP_minus":
            MR.modbus_set(callback_data["IP"], 41993, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP34, "5", Speed_VP = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_plus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP34, "5", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "set_speed_ventV_minus":
            MR.modbus_set(callback_data["IP"], 41992, int(callback_data["number"]), "holding")
            db.update_rele_status(P_IP34, "5", Speed_VV = round(int(callback_data["number"]) / 10))
        elif callback_data["action"] == "ust_plus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        elif callback_data["action"] == "ust_minus":
            MR.modbus_set(callback_data["IP"], 41984, int(callback_data["number"]), "float")
        message_oranjereya=f"Оранжерея:{space}\n"
        await call.message.edit_text(text=message_oranjereya)
        pust = str(MR.modbus_get(P_IP34, 14340))
        if pust == "0":
            message_oranjereya += utils.smile(pust) + "   Стоп\n"
        elif pust == "1":
            message_oranjereya += utils.smile(pust) + "   Пуск\n"
        else:
            message_oranjereya += "N/A   Пуск/Стоп\n"
        await call.message.edit_text(text=message_oranjereya)
        zile = str(MR.modbus_get(P_IP34, 14336))
        if zile == "0":
            message_oranjereya += "☀️" + "   Лето\n"
        elif zile == "1":
            message_oranjereya += "❄️" + "   Зима\n"
        else:
            message_oranjereya += "N/A   Зима/Лето\n"
        await call.message.edit_text(text=message_oranjereya)
        dime = str(MR.modbus_get(P_IP34, 14337))
        if dime == "0":
            message_oranjereya += utils.smile(dime) + "   Мест\n"
        elif dime == "1":
            message_oranjereya += utils.smile(dime) + "   Дист\n"
        else:
            message_oranjereya += "N/A   Дист/Мест\n"
        await call.message.edit_text(text=message_oranjereya)
        avar = str(MR.modbus_get(P_IP34, 14342))
        if avar == "1":
            message_oranjereya += "❌" + "   Авария\n"
            await call.message.edit_text(text=message_oranjereya)
        blok = str(MR.modbus_get(P_IP34, 14339))
        if blok == "1":
            message_oranjereya += "❌" + "   Блокировка\n"
            await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 41023, float)) + " C   Уставка t\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 40995, float)) + " C   t Канала\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 40993, float)) + " C   t Наружная\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 40997, float)) + " C   t Обр. воды\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 41001, float)) + " C   t Вытяжки\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 40999, float)) + " C   t Помещения\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 15366)) + "   Остановка ВВ\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 41106, "holding")) + "   Скорость ВП\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 41107, "holding")) + "   Скорость ВВ\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 41103, "holding")) + "   Мощность Рекуп.\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 41099, "holding")) + "   Мощность В. Калор.\n"
        await call.message.edit_text(text=message_oranjereya)
        message_oranjereya += str(MR.modbus_get(P_IP34, 41100, "holding")) + "   Мощность Э. Калор.\n"
        await call.message.edit_text(text=message_oranjereya)
        await call.message.edit_reply_markup(reply_markup=kb.oranjereya_menu(call.from_user.id))

@dp.callback_query_handler(text="pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text="Выберите день недели для отображения настроек на выбранный день.\nДля удаление наберите:\n<code>/del id</code>.\nДля добавления наберите:\n<code>/add ДеньНедели Реле Час Минута Вкл/Выкл</code>\nНапример:\n<code>/add 1 rekl 10 00 1</code>\nДень недели 1-7\nРеле:\nРеклама - <code>rekl</code>\nПарк - <code>par2</code>\nПарк периметр - <code>par3</code>\nЭкран - <code>ekra</code>\nПод зонтами - <code>new1</code>\nВодопад - <code>new2</code>\nБассейн верх - <code>new3</code>\nБассейн низ - <code>new4</code>")
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

@dp.callback_query_handler(text="pon_pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=pool_time_message(0))
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

@dp.callback_query_handler(text="vto_pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=pool_time_message(1))
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

@dp.callback_query_handler(text="sre_pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=pool_time_message(2))
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

@dp.callback_query_handler(text="che_pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=pool_time_message(3))
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

@dp.callback_query_handler(text="pya_pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=pool_time_message(4))
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

@dp.callback_query_handler(text="sub_pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=pool_time_message(5))
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

@dp.callback_query_handler(text="vos_pool_time")
@logger.catch
async def update(call: CallbackQuery):
    logger.info("Пользователь: " + str(call.from_user.id) + " нажал " + str(call.data))
    await call.answer()
    await call.message.edit_text(text=pool_time_message(6))
    await call.message.edit_reply_markup(reply_markup=kb.menu_pool_time)

# Запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
            time.sleep(5)
        except Exception as err:
            logger.error("Критическая ошибка")
            logger.error(err)
            time.sleep(10) # В случае падения