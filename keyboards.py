import config
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import LaurentJSON as LJ
import datetime as dt
from sqllite import SQLighter
import re
import modbusread as MR

P_IP30 = config.Pixel_IP30
P_IP31 = config.Pixel_IP31
P_IP32 = config.Pixel_IP32
P_IP33 = config.Pixel_IP33
P_IP34 = config.Pixel_IP34
L_IP24 = config.Laurent_IP_Pool24

# Подключение к БД
db = SQLighter(config.path_bot + "BotPiP.db")

def check_user_acess(user, rele):
    if bool(len(db.check_user_acess(user))) == True:
        user_acess = db.check_user_acess(user)[0][3]
        result = re.findall(rele + ",", str(user_acess))
        result = bool(len(result))
    else:
        result = False
    return result

def pool_menu(user):
    pool_menu = InlineKeyboardMarkup(row_width=2)
    if check_user_acess(user, "podn"):
        re = InlineKeyboardButton(text="Под навесом", callback_data="podn")
        pool_menu.insert(re)
    if check_user_acess(user, "rekl"):
        pa2 = InlineKeyboardButton(text="Реклама", callback_data="rekl")
        pool_menu.insert(pa2)
    if check_user_acess(user, "park"):
        pa3 = InlineKeyboardButton(text="Парк", callback_data="park")
        pool_menu.insert(pa3)
    if check_user_acess(user, "ekra"):
        ek = InlineKeyboardButton(text="Экран", callback_data="ekra")
        pool_menu.insert(ek)
    if check_user_acess(user, "basv"):
        new1 = InlineKeyboardButton(text="Бассейн верх", callback_data="basv")
        pool_menu.insert(new1)
    if check_user_acess(user, "basn"):
        new2 = InlineKeyboardButton(text="Бассейн низ", callback_data="basn")
        pool_menu.insert(new2)
    if check_user_acess(user, "podz"):
        new3 = InlineKeyboardButton(text="Под зонтами", callback_data="podz")
        pool_menu.insert(new3)
    if check_user_acess(user, "vodo"):
        new4 = InlineKeyboardButton(text="Водопад", callback_data="vodo")
        pool_menu.insert(new4)
    if check_user_acess(user, "ibav"):
        new5 = InlineKeyboardButton(text="Имп. Бас. верх", callback_data="ibav")
        pool_menu.insert(new5)
    if check_user_acess(user, "iban"):
        new6 = InlineKeyboardButton(text="Имп. Бас. низ", callback_data="iban")
        pool_menu.insert(new6)
    if check_user_acess(user, "time"):
        time = InlineKeyboardButton(text="Время", callback_data="time")
        pool_menu.insert(time)
    back = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    pool_menu.add(back)
    update = InlineKeyboardButton(text="Обновить", callback_data="pool_menu")
    pool_menu.insert(update)
    return pool_menu

def main_menu(user):
    main_menu = InlineKeyboardMarkup(row_width=2)
    pool_menu = InlineKeyboardButton(text="Бассейн и ВП", callback_data="pool_menu")
    main_menu.insert(pool_menu)
    vent_menu = InlineKeyboardButton(text="Вентиляция", callback_data="vent_menu")
    main_menu.insert(vent_menu)
    rekup_pri_menu = InlineKeyboardButton(text="Рекуператоры и Приточки", callback_data="rekup_pri_menu")
    main_menu.insert(rekup_pri_menu)
    re_orang = InlineKeyboardButton(text="Оранжерея Реклама", callback_data="re_orang")
    main_menu.add(re_orang)
    laurent_menu = InlineKeyboardButton(text="Ссылки на Laurent", callback_data="laurent_menu")
    main_menu.add(laurent_menu)
    return main_menu

def re_orang(user):
    re_orang = InlineKeyboardMarkup(row_width=2)
    if check_user_acess(user, "perekl"):
        po_time = InlineKeyboardButton(text="Переключить", callback_data="perekl")
        re_orang.add(po_time)
    if check_user_acess(user, "po_time"):
        l24_xml = LJ.l2_xml_read_all(L_IP24)
        print(l24_xml[3][0])
        if l24_xml[3][0] == "0":
            po_time = InlineKeyboardButton(text="Отключить режим по времени", callback_data="po_time")
            re_orang.add(po_time)
        elif l24_xml[3][0] == "1":
            po_time = InlineKeyboardButton(text="Включить режим по времени", callback_data="po_time")
            re_orang.add(po_time)
    back = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    re_orang.add(back)
    back = InlineKeyboardButton(text="Обновить", callback_data="re_orang")
    re_orang.insert(back)
    return re_orang

def vent_menu(user):
    vent_menu = InlineKeyboardMarkup(row_width=2)
    mang = InlineKeyboardButton(text="Мангал", callback_data="mang")
    vent_menu.insert(mang)
    pizz = InlineKeyboardButton(text="Пицца", callback_data="pizz")
    vent_menu.insert(pizz)
    ostr = InlineKeyboardButton(text="Остров", callback_data="ostr")
    vent_menu.add(ostr)
    smok = InlineKeyboardButton(text="Смокер", callback_data="smok")
    vent_menu.insert(smok)
    smok80 = InlineKeyboardButton(text="Смокер 80", callback_data="smok80")
    vent_menu.add(smok80)
    smok100 = InlineKeyboardButton(text="Смокер 100", callback_data="smok100")
    vent_menu.insert(smok100)
    main_menu = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    vent_menu.insert(main_menu)
    vent_menu_u = InlineKeyboardButton(text="Обновить", callback_data="vent_menu")
    vent_menu.insert(vent_menu_u)
    return vent_menu

def rekup_pri_menu(user):
    rekup_pri_menu = InlineKeyboardMarkup(resize_keyboard=False, row_width=2)
    bank = InlineKeyboardButton(text="Банкетный зал", callback_data="bank")
    rekup_pri_menu.insert(bank)
    pizz = InlineKeyboardButton(text="Подвал", callback_data="podv")
    rekup_pri_menu.add(pizz)
    ostr = InlineKeyboardButton(text="Кухня", callback_data="kuhn")
    rekup_pri_menu.insert(ostr)
    smok = InlineKeyboardButton(text="Гостиная", callback_data="gost")
    rekup_pri_menu.insert(smok)
    smok80 = InlineKeyboardButton(text="Оранжерея", callback_data="oran")
    rekup_pri_menu.insert(smok80)
    main_menu = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    rekup_pri_menu.insert(main_menu)
    rekup_pri_menu_u = InlineKeyboardButton(text="Обновить", callback_data="rekup_pri_menu")
    rekup_pri_menu.insert(rekup_pri_menu_u)
    return rekup_pri_menu

def bank(user):
    callback_rap = CallbackData("ustan", "temp_ust", "action", "IP")
    bank = InlineKeyboardMarkup(row_width=2)
    temp_ust_now = int(MR.modbus_get(P_IP30, 41023, float))
    if temp_ust_now > 16:
        ust_minus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now - 1), callback_data=callback_rap.new(temp_ust=temp_ust_now - 1, action="ust_minus", IP=P_IP30))
        bank.insert(ust_minus)
    ust_plus = InlineKeyboardButton(text="Уставка t:   " + str(temp_ust_now + 1), callback_data=callback_rap.new(temp_ust=temp_ust_now + 1, action="ust_plus", IP=P_IP30))
    bank.insert(ust_plus)
    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    bank.add(rekup_pri_menu)
    bank_u = InlineKeyboardButton(text="Обновить", callback_data="bank")
    bank.insert(bank_u)
    return bank

def podv(user):
    podv = InlineKeyboardMarkup(row_width=2)
    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    podv.insert(rekup_pri_menu)
    podv_u = InlineKeyboardButton(text="Обновить", callback_data="podv")
    podv.insert(podv_u)
    return podv

def kuhn(user):
    kuhn = InlineKeyboardMarkup(row_width=2)
    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    kuhn.insert(rekup_pri_menu)
    kuhn_u = InlineKeyboardButton(text="Обновить", callback_data="kuhn")
    kuhn.insert(kuhn_u)
    return kuhn

def gost(user):
    gost = InlineKeyboardMarkup(row_width=2)
    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    gost.insert(rekup_pri_menu)
    gost_u = InlineKeyboardButton(text="Обновить", callback_data="gost")
    gost.insert(gost_u)
    return gost

def oran(user):
    oran = InlineKeyboardMarkup(row_width=2)
    rekup_pri_menu = InlineKeyboardButton(text="Назад", callback_data="rekup_pri_menu")
    oran.insert(rekup_pri_menu)
    oran_u = InlineKeyboardButton(text="Обновить", callback_data="oran")
    oran.insert(oran_u)
    return oran

def laurent_menu(user):
    laurent_menu = InlineKeyboardMarkup(row_width=1)
    main_menu = InlineKeyboardButton(text="Назад", callback_data="main_menu")
    laurent_menu.insert(main_menu)
    return laurent_menu

menu_time = InlineKeyboardMarkup(row_width=2)
update = InlineKeyboardButton(text="Понедельник", callback_data="pon")
menu_time.insert(update)
update = InlineKeyboardButton(text="Вторник", callback_data="vto")
menu_time.insert(update)
update = InlineKeyboardButton(text="Среда", callback_data="sre")
menu_time.insert(update)
update = InlineKeyboardButton(text="Четверг", callback_data="che")
menu_time.insert(update)
update = InlineKeyboardButton(text="Пятница", callback_data="pya")
menu_time.insert(update)
update = InlineKeyboardButton(text="Суббота", callback_data="sub")
menu_time.insert(update)
update = InlineKeyboardButton(text="Воскресенье", callback_data="vos")
menu_time.insert(update)
time = InlineKeyboardButton(text="Обновить", callback_data="time")
menu_time.insert(time)
update = InlineKeyboardButton(text="Назад", callback_data="pool_menu")
menu_time.insert(update)