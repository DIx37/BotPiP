import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.defines as cst

class Modbus:
    """Работа с протоколом modbus"""
    def __init__(self, ip=None):
        self.ip = ip

    """Чтение протокола modbus"""
    def read(self, adress, type_modbus=None):
        master = modbus_tcp.TcpMaster(host=self.ip, port=502)
        master.set_timeout(1.0)
        try:
            if type_modbus == "float":
                modbus_res = master.execute(1,cst.READ_INPUT_REGISTERS, adress, 2)
                modbus_res = tofloat(modbus_res)
            elif type_modbus == "holding":
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
        return str(modbus_res)

    """Записть по протоколу modbus"""
    def write(self, adress, number, type_modbus=None):
        master = modbus_tcp.TcpMaster(host=adress, port=502)
        master.set_timeout(1.0)
        try:
            if type_modbus == "float":
                set_numb_float = 16640 + number * 8
                master.execute(1,cst.WRITE_MULTIPLE_REGISTERS, adress, output_value=(0, set_numb_float))
            else:
                master.execute(1,cst.WRITE_SINGLE_REGISTER, adress, output_value=number)
        except Exception as err:
            print("Это ошибка функции modbus_set" + err)

"""Функция преобразования двух адресов в число с плавающей запятой"""
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