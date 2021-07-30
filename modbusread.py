import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import math
import json
import requests
import datetime as dt
from loguru import logger
import platform
import config

class Modbus:
    """Работа с протоколом modbus"""
    def __init__(self, ip=None, adress=None, type=None):

        self.ip = ip
        self.adress = adress
        self.type = type
    
    def read(self):
        master = modbus_tcp.TcpMaster(host=self.ip, port=502)
        master.set_timeout(1.0)
        try:
            if type == "float":
                modbus_res = master.execute(1,cst.READ_INPUT_REGISTERS, self.adress, 2)
                modbus_res = tofloat(modbus_res)
            elif type == "holding":
                modbus_res = master.execute(1,cst.READ_HOLDING_REGISTERS, self.adress, 1)
                modbus_res = modbus_res[0]
            else:
                modbus_res = master.execute(1,cst.READ_COILS, self.adress, 1)
                modbus_res = modbus_res[0]
        except Exception as err_text:
            if str(err_text) == "timed out":
                modbus_res = "N/A"
            elif str(err_text) == "[WinError 10054] Удаленный хост принудительно разорвал существующее подключение":
                modbus_res = "WinError 10054"
            else:
                modbus_res = err_text
        return modbus_res

    def write(self):
        pass


# Запрос данных
@logger.catch
def modbus_get(modbus_ip, adress, type=0):
    master = modbus_tcp.TcpMaster(host=modbus_ip, port=502)
    master.set_timeout(1.0)
    try:
        if type == "float":
            modbus_res = master.execute(1,cst.READ_INPUT_REGISTERS, adress, 2)
            modbus_res = tofloat(modbus_res)
        elif type == "holding":
            modbus_res = master.execute(1,cst.READ_HOLDING_REGISTERS, adress, 1)
            modbus_res = modbus_res[0]
        else:
            modbus_res = master.execute(1,cst.READ_COILS, adress, 1)
            modbus_res = modbus_res[0]
    except Exception as err_text:
        if str(err_text) == "timed out":
            modbus_res = "N/A"
        elif str(err_text) == "[WinError 10054] Удаленный хост принудительно разорвал существующее подключение":
            modbus_res = "WinError 10054"
        else:
            modbus_res = err_text
    return modbus_res

# Запись данных по modbus
def modbus_set(modbus_ip, adress, numb, type=0):
    master = modbus_tcp.TcpMaster(host=modbus_ip, port=502)
    master.set_timeout(1.0)
    try:
        if type == "float":
            set_numb_float = 16640 + numb * 8
            master.execute(1,cst.WRITE_MULTIPLE_REGISTERS, adress, output_value=(0, set_numb_float))
        else:
            master.execute(1,cst.WRITE_SINGLE_REGISTER, adress, output_value=numb)
    except Exception as err:
        print("Это ошибка функции modbus_set" + err)

# Запись уставки
def set_temp_ust(modbus_ip, math):
    temp_ust = int(modbus_get(modbus_ip, 41023, "float"))
    if math == 0:
        temp_ust = temp_ust - 1
    elif math == 1:
        temp_ust = temp_ust + 1
    modbus_set(modbus_ip, 41984, temp_ust, "float")

# Функция преобразования двух адресов в число с плавающей запятой
def tofloat(getDI):
    Num1 = str(bin(getDI[1]))[2:]
    while len(Num1) < 16:
        Num1 = '0' + Num1
    Num2 = str(bin(getDI[0]))[2:]
    while len(Num2) < 16:
        Num2 = '0' + Num2
    res = Num1 + Num2
    znak = int(res[0], 2)
    znak2 = (0 - 1) ** znak
    e = int(res[1:9], 2) - 127
    exp = 2 ** e
    m = 1 + (int(res[9:], 2) / float(2 ** 23))
    F = znak2 * exp * m
    res = round(F, 1)
    return res

"""
# Пуск/Стоп
modbus_get(modbus_ip, 14340)
# Зима/Лето
modbus_get(modbus_ip, 14336)
# Дист/Мест
modbus_get(modbus_ip, 14337)
# Авария
modbus_get(modbus_ip, 14342)
# Блокировка
modbus_get(modbus_ip, 14339)
# t Канала
modbus_get(modbus_ip, 40995, float)
# t Наружная
modbus_get(modbus_ip, 40993, float)
# t Обр. воды
modbus_get(modbus_ip, 40997, float)
# Уставка t
modbus_get(modbus_ip, 41023, float)
# Скорость ВП
modbus_get(modbus_ip, 41106, "holding")
# t Вытяжки
modbus_get(modbus_ip, 41001, float)
# t Помещения
modbus_get(modbus_ip, 40999, float)
# Остановка ВВ
modbus_get(modbus_ip, 15366)
# Скорость ВВ
modbus_get(modbus_ip, 41107, "holding")
# Мощность Рекуп.
modbus_get(modbus_ip, 41103, "holding")
# Мощность В. Калор.
modbus_get(modbus_ip, 41099, "holding")
# Мощность Э. Калор.
modbus_get(modbus_ip, 41100, "holding")
"""