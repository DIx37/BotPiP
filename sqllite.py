import sqlite3
import math
import re

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def check_user_acess(self, id_user, menu, user_acess):
        """Проверка доступа к кнопкам"""
        with self.connection:
            acess = self.cursor.execute(f"SELECT {menu} FROM `UserAcess` WHERE `id_user` = {id_user}").fetchall()
            if bool(len(acess)):
                result = re.findall(user_acess + ",", str(acess))
                result = bool(len(result))
            else:
                result = False
            return result

    def get_pool_time(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `BotTime`").fetchall()

    def get_pool_time_DayOfWeek(self, DayOfWeek):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `BotTime` WHERE `DayOfWeek` = ? ORDER BY id", (DayOfWeek,)).fetchall()

    def get_pool_time_all(self, DayOfWeek, Hour, Minutes):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `BotTime` WHERE `DayOfWeek` = ? AND `Hour` = ? AND `Minutes` = ?", (DayOfWeek, Hour, Minutes)).fetchall()

    def add_time(self, DayOfWeek, Hour, Minutes, Rele, OnOrOff, s_a_s):
        with self.connection:
            return self.cursor.execute("INSERT INTO `BotTime` (`DayOfWeek`, `Hour`, `Minutes`, `Rele`, `OnOrOff`) VALUES(?,?,?,?,?,?)", (DayOfWeek, Hour, Minutes, Rele, OnOrOff, s_a_s))

    def del_time(self, id):
        """Удаление времени по id"""
        with self.connection:
            result = self.cursor.execute('DELETE FROM `BotTime` WHERE `id` = ?', (id,)).fetchall()
            return bool(len(result))

    def update_sas(self, Sunrise_h, Sunrise_m, Sunset_h, Sunset_m):
        """Обновление времени рассвета и заката"""
        with self.connection:
            self.cursor.execute(f"UPDATE `BotTime` SET `Hour` = '{Sunrise_h}' WHERE `s_a_s` = '1'")
            self.cursor.execute(f"UPDATE `BotTime` SET `Minutes` = '{Sunrise_m}' WHERE `s_a_s` = '1'")
            self.cursor.execute(f"UPDATE `BotTime` SET `Hour` = '{Sunset_h}' WHERE `s_a_s` = '2'")
            self.cursor.execute(f"UPDATE `BotTime` SET `Minutes` = '{Sunset_m}' WHERE `s_a_s` = '2'")
            for time_sas in self.cursor.execute("SELECT * FROM `BotTime` WHERE `s_a_s` = '1' OR `s_a_s` = '2' ORDER BY Rele").fetchall():
                if int(time_sas[7]) > 0 or int(time_sas[7]) < 0:
                    Time_in_min = int(time_sas[2]) * 60 + int(time_sas[3]) + int(time_sas[7])
                    Result_h = math.floor(Time_in_min / 60)
                    if Result_h < 10:
                        Result_h = "0" + str(Result_h)
                    Resilt_m = Time_in_min - int(Result_h) * 60
                    if Resilt_m < 10:
                        Resilt_m = "0" + str(Resilt_m)
                    self.cursor.execute(f"UPDATE `BotTime` SET `Hour` = '{Result_h}' WHERE `id` = '{time_sas[0]}'")
                    self.cursor.execute(f"UPDATE `BotTime` SET `Minutes` = '{Resilt_m}' WHERE `id` = '{time_sas[0]}'")

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()