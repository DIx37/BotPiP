# Импорт библиотек
import time
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import math
import json
import requests
from subprocess import check_output
import datetime as dt

# Отправка в Zabbix сообщения
def zabbix_send_m(user, message):
    check_output('zabbix_sender -z 172.16.2.107 -p 10051 -s "Bot" -k bot.id1 -o "{user}: {message}"'.format(user=user, message=message), shell = True)

# Отправка в Zabbix значений при проверках состояния
def zabbix_send(value, item, key):
    check_output('zabbix_sender -z 172.16.2.107 -p 10051 -s {item} -k {key} -o {value}'.format(value=value, item=item, key=key), shell = True)

# Преобразование для отправки в Zabbix
def z_send(modbus_ip, adress, modbus_res):
    value = modbus_res
    if modbus_ip == "172.16.1.30":
        item = '"Rekuperator bz"'
    elif modbus_ip == "172.16.1.34":
        item = '"Rekuperator o"'
    elif modbus_ip == "172.16.1.31":
        item = '"Pritochka Podval"'
    elif modbus_ip == "172.16.1.32":
        item = '"Pritochka Kuhnya"'
    elif modbus_ip == "172.16.1.33":
        item = '"Pritochka Gostinaya"'
    key = "pri.t.{adress}".format(adress=adress)
    zabbix_send(value, item, key)

# Запрос всех данных по одной приточке
def pritochka(modbus_name, modbus_ip):
    pritochka_res = modbus_name + '\nПуск/Стоп   =   ' + str(smile(modbus_get(modbus_ip, 14340))) + '\nЗима/Лето   =   ' + str(smile(modbus_get(modbus_ip, 14336), 1)) + '\nДист/Мест   =   ' + str(smile(modbus_get(modbus_ip, 14337))) + '\nАвария   =   ' + str(smile(modbus_get(modbus_ip, 14342), 2)) + '\nБлокировка   =   ' + str(smile(modbus_get(modbus_ip, 14339), 2)) + '\nt Канала   =   ' + str(modbus_get(modbus_ip, 40995, float)) + '\nt Наружная   =   ' + str(modbus_get(modbus_ip, 40993, float)) + '\nt Обр. воды   =   ' + str(modbus_get(modbus_ip, 40997, float)) + '\nУставка t   =   ' + str(modbus_get(modbus_ip, 41023, float)) + '\nСкорость ВП   =   ' + str(modbus_get(modbus_ip, 41106, "holding"))
    return pritochka_res

# Запрос всех данных по одному рекуператору
def rekuperator(modbus_name, modbus_ip):
    rekuperator_res = modbus_name + '\nПуск/Стоп   =   ' + str(smile(modbus_get(modbus_ip, 14340))) + '\nЗима/Лето   =   ' + str(smile(modbus_get(modbus_ip, 14336), 1)) + '\nДист/Мест   =   ' + str(smile(modbus_get(modbus_ip, 14337))) + '\nАвария   =   ' + str(smile(modbus_get(modbus_ip, 14342), 2)) + '\nБлокировка   =   ' + str(smile(modbus_get(modbus_ip, 14339), 2)) + '\nОстановка ВВ   =   ' + str(smile(modbus_get(modbus_ip, 15366), 2)) + '\nt Канала   =   ' + str(modbus_get(modbus_ip, 40995, float)) + '\nt Наружная   =   ' + str(modbus_get(modbus_ip, 40993, float)) + '\nt Обр. воды   =   ' + str(modbus_get(modbus_ip, 40997, float)) + '\nt Помещения   =   ' + str(modbus_get(modbus_ip, 40999, float)) + '\nУставка t   =   ' + str(modbus_get(modbus_ip, 41023, float)) + '\nСкорость ВП   =   ' + str(modbus_get(modbus_ip, 41106, "holding")) + '\nСкорость ВВ   =   ' + str(modbus_get(modbus_ip, 41107, "holding")) + '\nМощность Рекуп.   =   ' + str(modbus_get(modbus_ip, 41103, "holding")) + '\nМощность В. Калор.   =   ' + str(modbus_get(modbus_ip, 41099, "holding")) + '\nМощность Э. Калор.   =   ' + str(modbus_get(modbus_ip, 41100, "holding"))
    return rekuperator_res

# Запрос данных по modbus, преобразование в float
def modbus_get(modbus_ip, adress, type=0):
    master = modbus_tcp.TcpMaster(host=modbus_ip, port=502)
    master.set_timeout(1.0)
    try:
        if type == float:
            modbus_res = master.execute(1,cst.READ_INPUT_REGISTERS, adress, 2)
            modbus_res = tofloat(modbus_res)
        elif type == "holding":
            modbus_res = master.execute(1,cst.READ_HOLDING_REGISTERS, adress, 1)
            modbus_res = modbus_res[0]
        else:
            modbus_res = master.execute(1,cst.READ_COILS, adress, 1)
            modbus_res = modbus_res[0]
        try:
            z_send(modbus_ip, adress, modbus_res)
        except Exception as err_text:
            #print(err_text)
            pass
    except Exception as err_text:
        if str(err_text) == "timed out":
            modbus_res = "Недоступен"
        else:
            err_send(err_text, user_id, "101 - Ошибка функции modbus_get", keyboardFull)
            modbus_res = err_text
    return modbus_res

# Запись данных по modbus
def modbus_set(modbus_ip, adress, numb, type=0):
    master = modbus_tcp.TcpMaster(host=modbus_ip, port=502)
    master.set_timeout(1.0)
    try:
        if type == float:
            set_numb_float = 16640 + numb * 8
            master.execute(1,cst.WRITE_MULTIPLE_REGISTERS, adress, output_value=(0, set_numb_float))
        else:
            master.execute(1,cst.WRITE_SINGLE_REGISTER, adress, output_value=numb)
    except Exception as err:
        print("Это ошибка функции modbus_set" + err)

# Запись уставки
def set_temp_ust(modbus_ip, math):
    temp_ust = int(modbus_get(modbus_ip, 41023, float))
    if math == 0:
        temp_ust = temp_ust - 1
    elif math == 1:
        temp_ust = temp_ust + 1
    modbus_set(modbus_ip, 41984, temp_ust, float)

# Запись вентилятора вытяжки и приточки
def set_speed_fun(modbus_ip, adress, math):
    speed_fun = int(str(modbus_get(modbus_ip, adress, "holding")))
    if speed_fun == 0:
        speed_fun = 400
    if math == 0:
        speed_fun = speed_fun - 100
        speed_fun = int(speed_fun)
    elif math == 1:
        speed_fun = speed_fun + 100
        speed_fun = int(speed_fun)
    modbus_set(modbus_ip, adress, speed_fun)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Меню банкетного зала
        elif message.text.lower() == "банкетный зал" or message.text.lower() == "бз. сост.":
            try:
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err_text:
                err_send(err_text, message.chat.id, "002 - Меню опроса банкетного зала", keyboard30)
            # Устоновка уставки +1
        elif message.text.lower() == "бз. уставка +1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.30", 1)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err_text:
                err_send(err_text, message.chat.id, "003 - Меню уставки +1 банкетного зала", keyboard30)
            # Устоновка уставки -1
        elif message.text.lower() == "бз. уставка -1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.30", 0)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err_text:
                err_send(err_text, message.chat.id, "003 - Меню уставки -1 банкетного зала", keyboard30)
            # Устоновка скорости вентилятора приточки +10%
        elif message.text.lower() == "бз. вп +10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.30", 41993, 1)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err_text:
                err_send(err_text, message.chat.id, "003 - Меню установки скорости вентилятора +10% банкетного зала", keyboard30)
            # Устоновка скорости вентилятора приточки -10%
        elif message.text.lower() == "бз. вп -10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.30", 41993, 0)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err_text:
                err_send(err_text, message.chat.id, "003 - Меню установки скорости вентилятора -10% банкетного зала", keyboard30)
            # Устоновка скорости вентилятора вытяжки +10%
        elif message.text.lower() == "бз. вв +10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.30", 41992, 1)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard30)
            # Устоновка скорости вентилятора вытяжки -10%
        elif message.text.lower() == "бз. вв -10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.30", 41992, 0)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard30)
            # Пуск/Стоп
        elif message.text.lower() == "бз. пус/сто" and acess_status < 2:
            try:
                mget = modbus_get("172.16.1.30", 14340)
                if mget == 0:
                    modbus_set("172.16.1.30", 15362, 1)
                    time.sleep(2)
                    modbus_set("172.16.1.30", 15362, 0)
                elif mget == 1:
                    modbus_set("172.16.1.30", 15363, 0)
                    time.sleep(2)
                    modbus_set("172.16.1.30", 15363, 1)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard30)
            # Дист/Мест
        elif message.text.lower() == "бз. дис/мес" and acess_status == 0:
            try:
                modbus_set("172.16.1.30", 15360, 1)
                time.sleep(2)
                modbus_set("172.16.1.30", 15360, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard30)
            # Сброс аварии
        elif message.text.lower() == "бз. сброс" and acess_status == 0:
            try:
                modbus_set("172.16.1.30", 15364, 1)
                time.sleep(2)
                modbus_set("172.16.1.30", 15364, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard30)
            # Стоп ВВ
        elif message.text.lower() == "бз. стоп вв" and acess_status == 0:
            try:
                mget = modbus_get("172.16.1.30", 15366)
                if mget == 0:
                    modbus_set("172.16.1.30", 15366, 1)
                elif mget == 1:
                    modbus_set("172.16.1.30", 15366, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,rekuperator("Банкетный Зал: ", "172.16.1.30"),reply_markup=keyboard30, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard30)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Меню подвала
        elif message.text.lower() == "подвал" or message.text.lower() == "п. состояние":
            try:
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)
            # Устоновка уставки +1
        elif message.text.lower() == "п. уставка +1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.31", 1)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)
            # Устоновка уставки -1
        elif message.text.lower() == "п. уставка -1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.31", 0)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)
            # Устоновка скорости вентилятора приточки +10%
        elif message.text.lower() == "п. вп +10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.31", 41993, 1)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)
            # Устоновка скорости вентилятора приточки -10%
        elif message.text.lower() == "п. вп -10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.31", 41993, 0)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)
            # Пуск/Стоп
        elif message.text.lower() == "п. пуск/стоп" and acess_status < 2:
            try:
                mget = modbus_get("172.16.1.31", 14340)
                if mget == 0:
                    modbus_set("172.16.1.31", 15362, 1)
                    time.sleep(2)
                    modbus_set("172.16.1.31", 15362, 0)
                elif mget == 1:
                    modbus_set("172.16.1.31", 15363, 0)
                    time.sleep(2)
                    modbus_set("172.16.1.31", 15363, 1)
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)
            # Дист/Мест
        elif message.text.lower() == "п. дист/мест" and acess_status == 0:
            try:
                modbus_set("172.16.1.31", 15360, 1)
                time.sleep(2)
                modbus_set("172.16.1.31", 15360, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)
            # Сброс аварии
        elif message.text.lower() == "п. сброс" and acess_status == 0:
            try:
                modbus_set("172.16.1.31", 15364, 1)
                time.sleep(2)
                modbus_set("172.16.1.31", 15364, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,pritochka("Подвал: ", "172.16.1.31"),reply_markup=keyboard31, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard31)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Меню кухни
        elif message.text.lower() == "кухня" or message.text.lower() == "к. состояние":
            try:
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)
            # Устоновка уставки +1
        elif message.text.lower() == "к. уставка +1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.32", 1)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)
            # Устоновка уставки -1
        elif message.text.lower() == "к. уставка -1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.32", 0)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)
            # Устоновка скорости вентилятора приточки +10%
        elif message.text.lower() == "к. вп +10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.32", 41993, 1)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)
            # Устоновка скорости вентилятора приточки -10%
        elif message.text.lower() == "к. вп -10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.32", 41993, 0)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)
            # Пуск/Стоп
        elif message.text.lower() == "к. пуск/стоп" and acess_status < 2:
            try:
                mget = modbus_get("172.16.1.32", 14340)
                if mget == 0:
                    modbus_set("172.16.1.32", 15362, 1)
                    time.sleep(2)
                    modbus_set("172.16.1.32", 15362, 0)
                elif mget == 1:
                    modbus_set("172.16.1.32", 15363, 0)
                    time.sleep(2)
                    modbus_set("172.16.1.32", 15363, 1)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)
            # Дист/Мест
        elif message.text.lower() == "к. дист/мест" and acess_status == 0:
            try:
                modbus_set("172.16.1.32", 15360, 1)
                time.sleep(2)
                modbus_set("172.16.1.32", 15360, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)
            # Сброс аварии
        elif message.text.lower() == "к. сброс" and acess_status == 0:
            try:
                modbus_set("172.16.1.32", 15364, 1)
                time.sleep(2)
                modbus_set("172.16.1.32", 15364, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.32"),reply_markup=keyboard32, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard32)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Меню гостиной
        elif message.text.lower() == "гостиная" or message.text.lower() == "г. состояние":
            try:
                bot.send_message(message.chat.id,pritochka("Гостиная: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)
            # Устоновка уставки +1
        elif message.text.lower() == "г. уставка +1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.33", 1)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Гостиная: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)
            # Устоновка уставки -1
        elif message.text.lower() == "г. уставка -1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.33", 0)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Гостиная: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)
            # Устоновка скорости вентилятора приточки +10%
        elif message.text.lower() == "г. вп +10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.33", 41993, 1)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Гостиная: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)
            # Устоновка скорости вентилятора приточки -10%
        elif message.text.lower() == "г. вп -10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.33", 41993, 0)
                time.sleep(2)
                bot.send_message(message.chat.id,pritochka("Гостиная: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)
            # Пуск/Стоп
        elif message.text.lower() == "г. пуск/стоп" and acess_status < 2:
            try:
                mget = modbus_get("172.16.1.33", 14340)
                if mget == 0:
                    modbus_set("172.16.1.33", 15362, 1)
                    time.sleep(2)
                    modbus_set("172.16.1.33", 15362, 0)
                elif mget == 1:
                    modbus_set("172.16.1.33", 15363, 0)
                    time.sleep(2)
                    modbus_set("172.16.1.33", 15363, 1)
                bot.send_message(message.chat.id,pritochka("Гостиная: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)
            # Дист/Мест
        elif message.text.lower() == "г. дист/мест" and acess_status == 0:
            try:
                modbus_set("172.16.1.33", 15360, 1)
                time.sleep(2)
                modbus_set("172.16.1.33", 15360, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,pritochka("Гостиная: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)
            # Сброс аварии
        elif message.text.lower() == "г. сброс" and acess_status == 0:
            try:
                modbus_set("172.16.1.33", 15364, 1)
                time.sleep(2)
                modbus_set("172.16.1.33", 15364, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,pritochka("Кухня: ", "172.16.1.33"),reply_markup=keyboard33, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard33)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Меню оранжереи
        elif message.text.lower() == "оранжерея" or message.text.lower() == "о. сост.":
            try:
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Устоновка уставки +1
        elif message.text.lower() == "о. уставка +1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.34", 1)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Устоновка уставки -1
        elif message.text.lower() == "о. уставка -1" and acess_status < 2:
            try:
                set_temp_ust("172.16.1.34", 0)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Устоновка скорости вентилятора приточки +10%
        elif message.text.lower() == "о. вп +10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.34", 41993, 1)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Устоновка скорости вентилятора приточки -10%
        elif message.text.lower() == "о. вп -10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.34", 41993, 0)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Устоновка скорости вентилятора вытяжки +10%
        elif message.text.lower() == "о. вв +10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.34", 41992, 1)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Устоновка скорости вентилятора вытяжки -10%
        elif message.text.lower() == "о. вв -10%" and acess_status == 0:
            try:
                set_speed_fun("172.16.1.34", 41992, 0)
                time.sleep(2)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Пуск/Стоп
        elif message.text.lower() == "о. пус/сто" and acess_status < 2:
            try:
                mget = modbus_get("172.16.1.34", 14340)
                if mget == 0:
                    modbus_set("172.16.1.34", 15362, 1)
                    time.sleep(2)
                    modbus_set("172.16.1.34", 15362, 0)
                elif mget == 1:
                    modbus_set("172.16.1.34", 15363, 0)
                    time.sleep(2)
                    modbus_set("172.16.1.34", 15363, 1)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Дист/Мест
        elif message.text.lower() == "о. дис/мес" and acess_status == 0:
            try:
                modbus_set("172.16.1.34", 15360, 1)
                time.sleep(2)
                modbus_set("172.16.1.34", 15360, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Сброс аварии
        elif message.text.lower() == "о. сброс" and acess_status == 0:
            try:
                modbus_set("172.16.1.34", 15364, 1)
                time.sleep(2)
                modbus_set("172.16.1.34", 15364, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
            # Стоп ВВ
        elif message.text.lower() == "о. стоп вв" and acess_status == 0:
            try:
                mget = modbus_get("172.16.1.34", 15366)
                if mget == 0:
                    modbus_set("172.16.1.34", 15366, 1)
                elif mget == 1:
                    modbus_set("172.16.1.34", 15366, 0)
                time.sleep(1)
                bot.send_message(message.chat.id,rekuperator("Оранжерея: ", "172.16.1.34"),reply_markup=keyboard34, parse_mode="Markdown")
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboard34)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            # Вентиляция главное меню
        elif message.text.lower() == "вентиляция":
            try:
                send_laurent(message.chat.id)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            # Мангал
        elif message.text.lower() == "мангал выкл" and acess_status < 2:
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,1,0")
                time.sleep(1)
                send_laurent(message.chat.id)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "мангал вкл" and acess_status < 2:
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,1,1")
                time.sleep(1)
                send_laurent(message.chat.id)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "пицца выкл" and acess_status < 2:
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,2,0")
                time.sleep(1)
                send_laurent(message.chat.id)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "пицца вкл" and acess_status < 2:
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,2,1")
                time.sleep(1)
                send_laurent(message.chat.id)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "остров выкл" and acess_status < 2:
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,3,0")
                time.sleep(1)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "остров вкл" and acess_status < 2:
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,3,1")
                time.sleep(1)
                send_laurent(message.chat.id)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "смокер выкл":
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,4,0")
                time.sleep(1)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "смокер 80":
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,4,1")
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=PWM,4,SET,20")
                time.sleep(1)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
        elif message.text.lower() == "смокер 100":
            try:
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=REL,4,1")
                requests.get("http://172.16.1.20/cmd.cgi?psw=Laurent&cmd=PWM,4,SET,0")
                time.sleep(1)
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardVent)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Главное меню
        elif message.text.lower() == "главное меню" or message.text.lower() == "состояние":
            try:
                zabbix_send_m(message.chat.id, message.text)
                bot.send_message(
                    message.chat.id,
                    str(smile(modbus_get("172.16.1.30", 14340))) + '   *Банкетный зал*\n' +
                    str(smile(modbus_get("172.16.1.31", 14340))) + '   *Подвал*\n' +
                    str(smile(modbus_get("172.16.1.32", 14340))) + '   *Кухня*\n' +
                    str(smile(modbus_get("172.16.1.33", 14340))) + '   *Гостиная*\n' +
                    str(smile(modbus_get("172.16.1.34", 14340))) + '   *Оранжерея*\n' +
                    smile(int(laurent_json.l_json_read(laurent_json_get(), "rele")[0])) + "   *Мангал*\n" +
                    smile(int(laurent_json.l_json_read(laurent_json_get(), "rele")[1])) + "   *Пицца*\n" +
                    smile(int(laurent_json.l_json_read(laurent_json_get(), "rele")[2])) + "   *Остров*\n" +
                    smile(int(laurent_json.l_json_read(laurent_json_get(), "rele")[3])) + "   *Смокер*\n",
                    reply_markup=keyboardFull, parse_mode="Markdown"
                    )
            except Exception as err:
                bot.send_message(message.chat.id, err, reply_markup=keyboardFull)


        # Всё что не подходит под другие условия
        else:
            bot.send_message(message.chat.id, "Что желаете?", reply_markup=keyboardFull)
    # Если ID человека не записан
    else:
        bot.send_message(message.chat.id, "Я тебя не знаю!")

# Главный цикл, перезапуск при ошибке
if __name__ == '__main__':
    while True:
        try: # Добавляем try для отлова ошибок
            bot.polling(none_stop=True) # Запуск бота
        except Exception as err:
            time.sleep(10) # В случае падения
