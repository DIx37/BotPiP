import config
#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import LaurentJSON as LJ
#import datetime as dt
from sqllite import SQLighter
#import re
import modbusread as MR
from modbus import Modbus

# Переменные
P_IP30 = config.Pixel_IP30
P_IP31 = config.Pixel_IP31
P_IP32 = config.Pixel_IP32
P_IP33 = config.Pixel_IP33
P_IP34 = config.Pixel_IP34
banketniy_zal = Modbus(P_IP30)
podval = Modbus(P_IP31)
kuhnya = Modbus(P_IP32)
gostinaya = Modbus(P_IP33)
oranjereya = Modbus(P_IP34)
L_IP24 = config.Laurent_IP_Pool24

# Подключение к БД
db = SQLighter(config.path_bot + "BotPiP.db")


# Главное меню
def main_menu(user):
    main_menu = InlineKeyboardMarkup(row_width=2)
    if db.check_user_acess(user, "pool_menu", "pool_menu"):
        pool_menu = InlineKeyboardButton(text="Бассейн и ВП", callback_data="pool_menu")
        main_menu.insert(pool_menu)
    if db.check_user_acess(user, "vent_menu", "vent_menu"):
        vent_menu = InlineKeyboardButton(text="Вентиляция", callback_data="vent_menu")
        main_menu.insert(vent_menu)
    if db.check_user_acess(user, "rekup_pri_menu", "rekup_pri_menu"):
        rekup_pri_menu = InlineKeyboardButton(text="Рекуператоры и Приточки", callback_data="rekup_pri_menu")
        main_menu.insert(rekup_pri_menu)
    if db.check_user_acess(user, "ad_orangereya", "ad_orangereya"):
        ad_orangeteya = InlineKeyboardButton(text="Оранжерея Реклама", callback_data="ad_orangeteya")
        main_menu.add(ad_orangeteya)
    if db.check_user_acess(user, "laurent_menu", "laurent_menu"):
        laurent_menu = InlineKeyboardButton(text="Ссылки на Laurent", callback_data="laurent_menu")
        main_menu.add(laurent_menu)
    if db.check_user_acess(user, "control_bot_menu", "control_bot_menu"):
        control_bot_menu = InlineKeyboardButton(text="Управление ботами", callback_data="control_bot_menu")
        main_menu.add(control_bot_menu)
    return main_menu


# Бассейн и ВП
def pool_menu(user):
    pool_menu = InlineKeyboardMarkup(row_width=2)
    if db.check_user_acess(user, "pool_menu", "pod_navesom"):
        pod_navesom = InlineKeyboardButton(text="Под навесом", callback_data="pod_navesom")
        pool_menu.insert(pod_navesom)
    if db.check_user_acess(user, "pool_menu", "reklama"):
        reklama = InlineKeyboardButton(text="Реклама", callback_data="reklama")
        pool_menu.insert(reklama)
    if db.check_user_acess(user, "pool_menu", "park"):
        park = InlineKeyboardButton(text="Парк", callback_data="park")
        pool_menu.insert(park)
    if db.check_user_acess(user, "pool_menu", "ekran"):
        ekran = InlineKeyboardButton(text="Экран", callback_data="ekran")
        pool_menu.insert(ekran)
    if db.check_user_acess(user, "pool_menu", "pool_up"):
        pool_up = InlineKeyboardButton(text="Бассейн верх", callback_data="pool_up")
        pool_menu.insert(pool_up)
    if db.check_user_acess(user, "pool_menu", "pool_down"):
        pool_down = InlineKeyboardButton(text="Бассейн низ", callback_data="pool_down")
        pool_menu.insert(pool_down)
    if db.check_user_acess(user, "pool_menu", "pod_zontami"):
        pod_zontami = InlineKeyboardButton(text="Под зонтами", callback_data="pod_zontami")
        pool_menu.insert(pod_zontami)
    if db.check_user_acess(user, "pool_menu", "vodopad"):
        vodopad = InlineKeyboardButton(text="Водопад", callback_data="vodopad")
        pool_menu.insert(vodopad)
    if db.check_user_acess(user, "pool_menu", "imp_pool_up"):
        imp_pool_up = InlineKeyboardButton(text="Имп. Бас. верх", callback_data="imp_pool_up")
        pool_menu.insert(imp_pool_up)
    if db.check_user_acess(user, "pool_menu", "imp_pool_down"):
        imp_pool_down = InlineKeyboardButton(text="Имп. Бас. низ", callback_data="imp_pool_down")
        pool_menu.insert(imp_pool_down)
    if db.check_user_acess(user, "pool_menu", "pool_time"):
        pool_time = InlineKeyboardButton(text="Время", callback_data="pool_time")
        pool_menu.insert(pool_time)
    back = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    pool_menu.add(back)
    update = InlineKeyboardButton(text="Обновить", callback_data="pool_menu")
    pool_menu.insert(update)
    return pool_menu


# Вентиляция
def vent_menu(user):
    vent_menu = InlineKeyboardMarkup(row_width=2)
    if db.check_user_acess(user, "vent_menu", "mangal"):
        mangal = InlineKeyboardButton(text="Мангал", callback_data="mangal")
        vent_menu.insert(mangal)
    if db.check_user_acess(user, "vent_menu", "pizza"):
        pizza = InlineKeyboardButton(text="Пицца", callback_data="pizza")
        vent_menu.insert(pizza)
    if db.check_user_acess(user, "vent_menu", "ostrov"):
        ostrov = InlineKeyboardButton(text="Остров", callback_data="ostrov")
        vent_menu.add(ostrov)
    if db.check_user_acess(user, "vent_menu", "smoker"):
        smoker = InlineKeyboardButton(text="Смокер", callback_data="smoker")
        vent_menu.insert(smoker)
    if db.check_user_acess(user, "vent_menu", "smoker_80"):
        smoker_80 = InlineKeyboardButton(text="Смокер 80", callback_data="smoker_80")
        vent_menu.add(smoker_80)
    if db.check_user_acess(user, "vent_menu", "smoker_100"):
        smoker_100 = InlineKeyboardButton(text="Смокер 100", callback_data="smoker_100")
        vent_menu.insert(smoker_100)
    main_menu = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    vent_menu.insert(main_menu)
    vent_menu_u = InlineKeyboardButton(text="Обновить", callback_data="vent_menu")
    vent_menu.insert(vent_menu_u)
    return vent_menu


# Рекуператоры и Приточки
def rekup_pri_menu(user):
    rekup_pri_menu = InlineKeyboardMarkup(resize_keyboard=False, row_width=2)
    if db.check_user_acess(user, "rekup_pri_menu", "banketniy_zal"):
        banketniy_zal = InlineKeyboardButton(text="Банкетный зал", callback_data="banketniy_zal")
        rekup_pri_menu.insert(banketniy_zal)
    if db.check_user_acess(user, "rekup_pri_menu", "podval"):
        podval = InlineKeyboardButton(text="Подвал", callback_data="podval")
        rekup_pri_menu.add(podval)
    if db.check_user_acess(user, "rekup_pri_menu", "kuhnya"):
        kuhnya = InlineKeyboardButton(text="Кухня", callback_data="kuhnya")
        rekup_pri_menu.add(kuhnya)
    if db.check_user_acess(user, "rekup_pri_menu", "gostinaya"):
        gostinaya = InlineKeyboardButton(text="Гостиная", callback_data="gostinaya")
        rekup_pri_menu.add(gostinaya)
    if db.check_user_acess(user, "rekup_pri_menu", "oranjereya"):
        oranjereya = InlineKeyboardButton(text="Оранжерея", callback_data="oranjereya")
        rekup_pri_menu.add(oranjereya)
    main_menu = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    rekup_pri_menu.add(main_menu)
    rekup_pri_menu_u = InlineKeyboardButton(text="Обновить", callback_data="rekup_pri_menu")
    rekup_pri_menu.insert(rekup_pri_menu_u)
    return rekup_pri_menu


# Оранжерея Реклама
def ad_orangereya(user):
    ad_orangereya = InlineKeyboardMarkup(row_width=2)
    if db.check_user_acess(user, "ad_orangereya", "perekl"):
        po_time = InlineKeyboardButton(text="Переключить", callback_data="perekl")
        ad_orangereya.add(po_time)
    if db.check_user_acess(user, "ad_orangereya", "po_time"):
        l24_xml = LJ.l2_xml_read_all(L_IP24)
        print(l24_xml[3][0])
        if l24_xml[3][0] == "0":
            po_time = InlineKeyboardButton(text="Отключить режим по времени", callback_data="po_time")
            ad_orangereya.add(po_time)
        elif l24_xml[3][0] == "1":
            po_time = InlineKeyboardButton(text="Включить режим по времени", callback_data="po_time")
            ad_orangereya.add(po_time)
    back = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    ad_orangereya.add(back)
    back = InlineKeyboardButton(text="Обновить", callback_data="ad_orangereya")
    ad_orangereya.insert(back)
    return ad_orangereya


# Ссылки на Laurent
def laurent_menu(user):
    laurent_menu = InlineKeyboardMarkup(row_width=1)
    main_menu = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    laurent_menu.insert(main_menu)
    return laurent_menu


# Управление ботами
def control_bot_menu(user):
    control_bot_menu = InlineKeyboardMarkup(row_width=2)
    if db.check_user_acess(user, "control_bot_menu", "control_bot_menu"):
        ReleTime = InlineKeyboardButton(text="ReleTime", callback_data="ReleTime")
        control_bot_menu.insert(ReleTime)
        DeliveryBot = InlineKeyboardButton(text="DeliveryBot", callback_data="DeliveryBot")
        control_bot_menu.insert(DeliveryBot)
        EmailOrderWritter = InlineKeyboardButton(text="EmailOrderWritter", callback_data="EmailOrderWritter")
        control_bot_menu.insert(EmailOrderWritter)
        Get_ntv = InlineKeyboardButton(text="Get_ntv", callback_data="Get_ntv")
        control_bot_menu.insert(Get_ntv)
    main_menu = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    control_bot_menu.add(main_menu)
    control_bot_menu_u = InlineKeyboardButton(text="Обновить", callback_data="control_bot_menu")
    control_bot_menu.insert(control_bot_menu_u)
    return control_bot_menu


def banketniy_zal_menu(user):
    callback_rap = CallbackData("set", "action", "number", "IP")
    banketniy_zal_menu = InlineKeyboardMarkup(row_width=2)

    pusk_stop_now = banketniy_zal.read(14340)
    if pusk_stop_now == "WinError 10054" or pusk_stop_now == "N/A":
        pass
    else:
        if pusk_stop_now == "0":
            pusk_stop = InlineKeyboardButton(text="Запустить", callback_data=callback_rap.new(number="None", action="pusk", IP=P_IP30))
            banketniy_zal_menu.insert(pusk_stop)
        elif pusk_stop_now == "1":
            pusk_stop = InlineKeyboardButton(text="Остановить", callback_data=callback_rap.new(number="None", action="stop", IP=P_IP30))
            banketniy_zal_menu.insert(pusk_stop)

    sbros_error_now = banketniy_zal.read(14342)
    if sbros_error_now == "WinError 10054" or sbros_error_now == "N/A":
        pass
    else:
        if sbros_error_now == "1":
            sbros_error = InlineKeyboardButton(text="Сбросить аварию", callback_data=callback_rap.new(number="None", action="sbros_error", IP=P_IP30))
            banketniy_zal_menu.add(sbros_error)

    stop_start_vv_now = banketniy_zal.read(15366)
    if stop_start_vv_now == "WinError 10054" or stop_start_vv_now == "N/A":
        pass
    else:
        if stop_start_vv_now == "0":
            stop_vv = InlineKeyboardButton(text="Остановить ВВ", callback_data=callback_rap.new(number="None", action="stop_vv", IP=P_IP30))
            banketniy_zal_menu.add(stop_vv)
        elif stop_start_vv_now == "1":
            start_vv = InlineKeyboardButton(text="Включить ВВ", callback_data=callback_rap.new(number="None", action="start_vv", IP=P_IP30))
            banketniy_zal_menu.add(start_vv)

    temp_ust_now = banketniy_zal.read(41023, "float", "int")
    if temp_ust_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if temp_ust_now > 16:
            ust_minus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now - 1), callback_data=callback_rap.new(number=temp_ust_now - 1, action="ust_minus", IP=P_IP30))
            banketniy_zal_menu.add(ust_minus)
        if temp_ust_now < 30:
            ust_plus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now + 1), callback_data=callback_rap.new(number=temp_ust_now + 1, action="ust_plus", IP=P_IP30))
            banketniy_zal_menu.insert(ust_plus)

    set_speed_ventP_now = banketniy_zal.read(41993, "holding", "int")
    if set_speed_ventP_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if set_speed_ventP_now < 400:
            set_speed_ventP_now = 400
        if set_speed_ventP_now > 400:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 - 10)), callback_data=callback_rap.new(number=set_speed_ventP_now - 100, action="set_speed_ventP_minus", IP=P_IP30))
            banketniy_zal_menu.add(set_speed_ventP)
        if set_speed_ventP_now < 1000:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 + 10)), callback_data=callback_rap.new(number=set_speed_ventP_now + 100, action="set_speed_ventP_plus", IP=P_IP30))
            if set_speed_ventP_now == 400:
                banketniy_zal_menu.add(set_speed_ventP)
            else:
                banketniy_zal_menu.insert(set_speed_ventP)

    set_speed_ventV_now = banketniy_zal.read(41992, "holding", "int")
    if set_speed_ventV_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if set_speed_ventV_now < 400:
            set_speed_ventV_now = 400
        if set_speed_ventV_now > 400:
            set_speed_ventV = InlineKeyboardButton(text="Скорость ВВ:   " + str(round(set_speed_ventV_now/10 - 10)), callback_data=callback_rap.new(number=set_speed_ventV_now - 100, action="set_speed_ventV_minus", IP=P_IP30))
            banketniy_zal_menu.add(set_speed_ventV)
        if set_speed_ventV_now < 1000:
            set_speed_ventV = InlineKeyboardButton(text="Скорость ВВ:   " + str(round(set_speed_ventV_now/10 + 10)), callback_data=callback_rap.new(number=set_speed_ventV_now + 100, action="set_speed_ventV_plus", IP=P_IP30))
            if set_speed_ventV_now == 400:
                banketniy_zal_menu.add(set_speed_ventV)
            else:
                banketniy_zal_menu.insert(set_speed_ventV)

    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    banketniy_zal_menu.add(rekup_pri_menu)
    banketniy_zal_menu_u = InlineKeyboardButton(text="Обновить", callback_data="banketniy_zal")
    banketniy_zal_menu.insert(banketniy_zal_menu_u)
    return banketniy_zal_menu


def podval_menu(user):
    callback_rap = CallbackData("set", "action", "number", "IP")
    podval_menu = InlineKeyboardMarkup(row_width=2)

    pusk_stop_now = podval.read(14340)
    if pusk_stop_now == "WinError 10054" or pusk_stop_now == "N/A":
        pass
    else:
        if pusk_stop_now == "0":
            pusk_stop = InlineKeyboardButton(text="Запустить", callback_data=callback_rap.new(number="None", action="pusk", IP=P_IP31))
            podval_menu.insert(pusk_stop)
        elif pusk_stop_now == "1":
            pusk_stop = InlineKeyboardButton(text="Остановить", callback_data=callback_rap.new(number="None", action="stop", IP=P_IP31))
            podval_menu.insert(pusk_stop)

    sbros_error_now = podval.read(14342)
    if sbros_error_now == "WinError 10054" or sbros_error_now == "N/A":
        pass
    else:
        if sbros_error_now == "1":
            sbros_error = InlineKeyboardButton(text="Сбросить аварию", callback_data=callback_rap.new(number="None", action="sbros_error", IP=P_IP31))
            podval_menu.add(sbros_error)

    temp_ust_now = podval.read(41023, "float", "int")
    if temp_ust_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if temp_ust_now > 16:
            ust_minus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now - 1), callback_data=callback_rap.new(number=temp_ust_now - 1, action="ust_minus", IP=P_IP31))
            podval_menu.add(ust_minus)
        if temp_ust_now < 30:
            ust_plus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now + 1), callback_data=callback_rap.new(number=temp_ust_now + 1, action="ust_plus", IP=P_IP31))
            podval_menu.insert(ust_plus)

    set_speed_ventP_now = podval.read(41993, "holding", "int")
    if set_speed_ventP_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if set_speed_ventP_now < 400:
            set_speed_ventP_now = 400
        if set_speed_ventP_now > 400:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 - 10)), callback_data=callback_rap.new(number=set_speed_ventP_now - 100, action="set_speed_ventP_minus", IP=P_IP31))
            podval_menu.add(set_speed_ventP)
        if set_speed_ventP_now < 1000:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 + 10)), callback_data=callback_rap.new(number=set_speed_ventP_now + 100, action="set_speed_ventP_plus", IP=P_IP31))
            if set_speed_ventP_now == 400:
                podval_menu.add(set_speed_ventP)
            else:
                podval_menu.insert(set_speed_ventP)

    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    podval_menu.add(rekup_pri_menu)
    podval_menu_u = InlineKeyboardButton(text="Обновить", callback_data="podval")
    podval_menu.insert(podval_menu_u)
    return podval_menu


def kuhnya_menu(user):
    callback_rap = CallbackData("set", "action", "number", "IP")
    kuhnya_menu = InlineKeyboardMarkup(row_width=2)

    pusk_stop_now = kuhnya.read(14340)
    if pusk_stop_now == "WinError 10054" or pusk_stop_now == "N/A":
        pass
    else:
        if pusk_stop_now == "0":
            pusk_stop = InlineKeyboardButton(text="Запустить", callback_data=callback_rap.new(number="None", action="pusk", IP=P_IP32))
            kuhnya_menu.insert(pusk_stop)
        elif pusk_stop_now == "1":
            pusk_stop = InlineKeyboardButton(text="Остановить", callback_data=callback_rap.new(number="None", action="stop", IP=P_IP32))
            kuhnya_menu.insert(pusk_stop)

    sbros_error_now = kuhnya.read(14342)
    if sbros_error_now == "WinError 10054" or sbros_error_now == "N/A":
        pass
    else:
        if sbros_error_now == "1":
            sbros_error = InlineKeyboardButton(text="Сбросить аварию", callback_data=callback_rap.new(number="None", action="sbros_error", IP=P_IP32))
            kuhnya_menu.add(sbros_error)

    temp_ust_now = kuhnya.read(41023, "float", "int")
    if temp_ust_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if temp_ust_now > 16:
            ust_minus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now - 1), callback_data=callback_rap.new(number=temp_ust_now - 1, action="ust_minus", IP=P_IP32))
            kuhnya_menu.add(ust_minus)
        if temp_ust_now < 30:
            ust_plus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now + 1), callback_data=callback_rap.new(number=temp_ust_now + 1, action="ust_plus", IP=P_IP32))
            kuhnya_menu.insert(ust_plus)

    set_speed_ventP_now = kuhnya.read(41993, "holding", "int")
    if set_speed_ventP_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if set_speed_ventP_now < 400:
            set_speed_ventP_now = 400
        if set_speed_ventP_now > 400:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 - 10)), callback_data=callback_rap.new(number=set_speed_ventP_now - 100, action="set_speed_ventP_minus", IP=P_IP32))
            kuhnya_menu.add(set_speed_ventP)
        if set_speed_ventP_now < 1000:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 + 10)), callback_data=callback_rap.new(number=set_speed_ventP_now + 100, action="set_speed_ventP_plus", IP=P_IP32))
            if set_speed_ventP_now == 400:
                kuhnya_menu.add(set_speed_ventP)
            else:
                kuhnya_menu.insert(set_speed_ventP)

    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    kuhnya_menu.add(rekup_pri_menu)
    kuhnya_menu_u = InlineKeyboardButton(text="Обновить", callback_data="kuhnya")
    kuhnya_menu.insert(kuhnya_menu_u)
    return kuhnya_menu


def gostinaya_menu(user):
    callback_rap = CallbackData("set", "action", "number", "IP")
    gostinaya_menu = InlineKeyboardMarkup(row_width=2)

    pusk_stop_now = gostinaya.read(14340)
    if pusk_stop_now == "WinError 10054" or pusk_stop_now == "N/A":
        pass
    else:
        if pusk_stop_now == "0":
            pusk_stop = InlineKeyboardButton(text="Запустить", callback_data=callback_rap.new(number="None", action="pusk", IP=P_IP33))
            gostinaya_menu.insert(pusk_stop)
        elif pusk_stop_now == "1":
            pusk_stop = InlineKeyboardButton(text="Остановить", callback_data=callback_rap.new(number="None", action="stop", IP=P_IP33))
            gostinaya_menu.insert(pusk_stop)

    sbros_error_now = gostinaya.read(14342)
    if sbros_error_now == "WinError 10054" or sbros_error_now == "N/A":
        pass
    else:
        if sbros_error_now == "1":
            sbros_error = InlineKeyboardButton(text="Сбросить аварию", callback_data=callback_rap.new(number="None", action="sbros_error", IP=P_IP33))
            gostinaya_menu.add(sbros_error)

    temp_ust_now = gostinaya.read(41023, "float", "int")
    if temp_ust_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if temp_ust_now > 16:
            ust_minus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now - 1), callback_data=callback_rap.new(number=temp_ust_now - 1, action="ust_minus", IP=P_IP33))
            gostinaya_menu.add(ust_minus)
        if temp_ust_now < 30:
            ust_plus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now + 1), callback_data=callback_rap.new(number=temp_ust_now + 1, action="ust_plus", IP=P_IP33))
            gostinaya_menu.insert(ust_plus)

    set_speed_ventP_now = gostinaya.read(41993, "holding", "int")
    if set_speed_ventP_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if set_speed_ventP_now < 400:
            set_speed_ventP_now = 400
        if set_speed_ventP_now > 400:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 - 10)), callback_data=callback_rap.new(number=set_speed_ventP_now - 100, action="set_speed_ventP_minus", IP=P_IP33))
            gostinaya_menu.add(set_speed_ventP)
        if set_speed_ventP_now < 1000:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 + 10)), callback_data=callback_rap.new(number=set_speed_ventP_now + 100, action="set_speed_ventP_plus", IP=P_IP33))
            if set_speed_ventP_now == 400:
                gostinaya_menu.add(set_speed_ventP)
            else:
                gostinaya_menu.insert(set_speed_ventP)

    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    gostinaya_menu.add(rekup_pri_menu)
    gostinaya_menu_u = InlineKeyboardButton(text="Обновить", callback_data="gostinaya")
    gostinaya_menu.insert(gostinaya_menu_u)
    return gostinaya_menu


def oranjereya_menu(user):
    callback_rap = CallbackData("set", "action", "number", "IP")
    oranjereya_menu_menu = InlineKeyboardMarkup(row_width=2)

    pusk_stop_now = oranjereya.read(14340)
    if pusk_stop_now == "WinError 10054" or pusk_stop_now == "N/A":
        pass
    else:
        if pusk_stop_now == "0":
            pusk_stop = InlineKeyboardButton(text="Запустить", callback_data=callback_rap.new(number="None", action="pusk", IP=P_IP34))
            oranjereya_menu_menu.insert(pusk_stop)
        elif pusk_stop_now == "1":
            pusk_stop = InlineKeyboardButton(text="Остановить", callback_data=callback_rap.new(number="None", action="stop", IP=P_IP34))
            oranjereya_menu_menu.insert(pusk_stop)

    sbros_error_now = oranjereya.read(14342)
    if sbros_error_now == "WinError 10054" or sbros_error_now == "N/A":
        pass
    else:
        if sbros_error_now == "1":
            sbros_error = InlineKeyboardButton(text="Сбросить аварию", callback_data=callback_rap.new(number="None", action="sbros_error", IP=P_IP34))
            oranjereya_menu_menu.add(sbros_error)

    stop_start_vv_now = oranjereya.read(15366)
    if stop_start_vv_now == "WinError 10054" or stop_start_vv_now == "N/A":
        pass
    else:
        if stop_start_vv_now == "0":
            stop_vv = InlineKeyboardButton(text="Остановить ВВ", callback_data=callback_rap.new(number="None", action="stop_vv", IP=P_IP34))
            oranjereya_menu_menu.add(stop_vv)
        elif stop_start_vv_now == "1":
            start_vv = InlineKeyboardButton(text="Включить ВВ", callback_data=callback_rap.new(number="None", action="start_vv", IP=P_IP34))
            oranjereya_menu_menu.add(start_vv)

    temp_ust_now = oranjereya.read(41023, "float", "int")
    if temp_ust_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if temp_ust_now > 16:
            ust_minus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now - 1), callback_data=callback_rap.new(number=temp_ust_now - 1, action="ust_minus", IP=P_IP34))
            oranjereya_menu_menu.add(ust_minus)
        if temp_ust_now < 30:
            ust_plus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now + 1), callback_data=callback_rap.new(number=temp_ust_now + 1, action="ust_plus", IP=P_IP34))
            oranjereya_menu_menu.insert(ust_plus)

    set_speed_ventP_now = oranjereya.read(41993, "holding", "int")
    if set_speed_ventP_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if set_speed_ventP_now < 400:
            set_speed_ventP_now = 400
        if set_speed_ventP_now > 400:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 - 10)), callback_data=callback_rap.new(number=set_speed_ventP_now - 100, action="set_speed_ventP_minus", IP=P_IP34))
            oranjereya_menu_menu.add(set_speed_ventP)
        if set_speed_ventP_now < 1000:
            set_speed_ventP = InlineKeyboardButton(text="Скорость ВП:   " + str(round(set_speed_ventP_now/10 + 10)), callback_data=callback_rap.new(number=set_speed_ventP_now + 100, action="set_speed_ventP_plus", IP=P_IP34))
            if set_speed_ventP_now == 400:
                oranjereya_menu_menu.add(set_speed_ventP)
            else:
                oranjereya_menu_menu.insert(set_speed_ventP)

    set_speed_ventV_now = oranjereya.read(41992, "holding", "int")
    if set_speed_ventV_now == "WinError 10054" or temp_ust_now == "N/A":
        pass
    else:
        if set_speed_ventV_now < 400:
            set_speed_ventV_now = 400
        if set_speed_ventV_now > 400:
            set_speed_ventV = InlineKeyboardButton(text="Скорость ВВ:   " + str(round(set_speed_ventV_now/10 - 10)), callback_data=callback_rap.new(number=set_speed_ventV_now - 100, action="set_speed_ventV_minus", IP=P_IP34))
            oranjereya_menu_menu.add(set_speed_ventV)
        if set_speed_ventV_now < 1000:
            set_speed_ventV = InlineKeyboardButton(text="Скорость ВВ:   " + str(round(set_speed_ventV_now/10 + 10)), callback_data=callback_rap.new(number=set_speed_ventV_now + 100, action="set_speed_ventV_plus", IP=P_IP34))
            if set_speed_ventV_now == 400:
                oranjereya_menu_menu.add(set_speed_ventV)
            else:
                oranjereya_menu_menu.insert(set_speed_ventV)

    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    oranjereya_menu_menu.add(rekup_pri_menu)
    oranjereya_menu_menu_u = InlineKeyboardButton(text="Обновить", callback_data="oranjereya")
    oranjereya_menu_menu.insert(oranjereya_menu_menu_u)
    return oranjereya_menu_menu


menu_pool_time = InlineKeyboardMarkup(row_width=2)
update = InlineKeyboardButton(text="Понедельник", callback_data="pon_pool_time")
menu_pool_time.insert(update)
update = InlineKeyboardButton(text="Вторник", callback_data="vto_pool_time")
menu_pool_time.insert(update)
update = InlineKeyboardButton(text="Среда", callback_data="sre_pool_time")
menu_pool_time.insert(update)
update = InlineKeyboardButton(text="Четверг", callback_data="che_pool_time")
menu_pool_time.insert(update)
update = InlineKeyboardButton(text="Пятница", callback_data="pya_pool_time")
menu_pool_time.insert(update)
update = InlineKeyboardButton(text="Суббота", callback_data="sub_pool_time")
menu_pool_time.insert(update)
update = InlineKeyboardButton(text="Воскресенье", callback_data="vos_pool_time")
menu_pool_time.insert(update)
pool_time = InlineKeyboardButton(text="Обновить", callback_data="menu_pool_time")
menu_pool_time.insert(pool_time)
update = InlineKeyboardButton(text="Назад", callback_data="pool_menu")
menu_pool_time.insert(update)


menu_vent_time = InlineKeyboardMarkup(row_width=2)
update = InlineKeyboardButton(text="Понедельник", callback_data="pon_vent_time")
menu_vent_time.insert(update)
update = InlineKeyboardButton(text="Вторник", callback_data="vto_vent_time")
menu_vent_time.insert(update)
update = InlineKeyboardButton(text="Среда", callback_data="sre_vent_time")
menu_vent_time.insert(update)
update = InlineKeyboardButton(text="Четверг", callback_data="che_vent_time")
menu_vent_time.insert(update)
update = InlineKeyboardButton(text="Пятница", callback_data="pya_vent_time")
menu_vent_time.insert(update)
update = InlineKeyboardButton(text="Суббота", callback_data="sub_vent_time")
menu_vent_time.insert(update)
update = InlineKeyboardButton(text="Воскресенье", callback_data="vos_vent_time")
menu_vent_time.insert(update)
vent_time = InlineKeyboardButton(text="Обновить", callback_data="menu_vent_time")
menu_vent_time.insert(vent_time)
update = InlineKeyboardButton(text="Назад", callback_data="vent_menu")
menu_vent_time.insert(update)