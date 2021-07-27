import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def check_user_acess(self, id_user):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `User` WHERE `id_user` = ?", (id_user,)).fetchall()

    def get_pool_time(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `BotTime`").fetchall()

    def get_pool_time_DayOfWeek(self, DayOfWeek):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `BotTime` WHERE `DayOfWeek` = ? ORDER BY Rele", (DayOfWeek,)).fetchall()

    def get_pool_time_all(self, DayOfWeek, Hour, Minutes):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `BotTime` WHERE `DayOfWeek` = ? AND `Hour` = ? AND `Minutes` = ?", (DayOfWeek, Hour, Minutes)).fetchall()

    def add_time(self, DayOfWeek, Hour, Minutes, Rele, OnOrOff):
        """Добавление нового письма в базу"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `BotTime` (`DayOfWeek`, `Hour`, `Minutes`, `Rele`, `OnOrOff`) VALUES(?,?,?,?,?)", (DayOfWeek, Hour, Minutes, Rele, OnOrOff))

    def del_time(self, id):
        """Добавление нового письма в базу"""
        with self.connection:
            result = self.cursor.execute('DELETE FROM `BotTime` WHERE `id` = ?', (id,)).fetchall()
            return bool(len(result))

    def get_weather_time(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `Weather`").fetchall()

    def update_weather_bottime(self, Sunrise_h, Sunrise_m, Sunset_h, Sunset_m):
        with self.connection:
            Rele = "rekl"
            OnOrOff = 0
            self.cursor.execute("UPDATE `BotTime` SET `Hour` = ? WHERE `Rele` = ? AND `OnOrOff` = ?", (Sunrise_h, Rele, OnOrOff))
            self.cursor.execute("UPDATE `BotTime` SET `Minutes` = ? WHERE `Rele` = ? AND `OnOrOff` = ?", (Sunrise_m, Rele, OnOrOff))
            Rele = "rekl"
            OnOrOff = 1
            self.cursor.execute("UPDATE `BotTime` SET `Hour` = ? WHERE `Rele` = ? AND `OnOrOff` = ?", (Sunset_h, Rele, OnOrOff))
            self.cursor.execute("UPDATE `BotTime` SET `Minutes` = ? WHERE `Rele` = ? AND `OnOrOff` = ?", (Sunset_m, Rele, OnOrOff))

    def update_weather(self, Date, Sunrise_h, Sunrise_m, Sunset_h, Sunset_m):
        id = 1
        if int(Sunrise_h) < 10:
            Sunrise_h = "0" + str(int(Sunrise_h))
        if int(Sunrise_m) < 10:
            Sunrise_h = "0" + str(int(Sunrise_h))
        if int(Sunset_h) < 10:
            Sunrise_h = "0" + str(int(Sunrise_h))
        if int(Sunrise_h) < 10:
            Sunset_m = "0" + str(int(Sunrise_h))
        with self.connection:
            self.cursor.execute("UPDATE `Weather` SET `Date` = ? WHERE `id` = ?", (Date, id))
            self.cursor.execute("UPDATE `Weather` SET `Sunrise_h` = ? WHERE `id` = ?", (Sunrise_h, id))
            self.cursor.execute("UPDATE `Weather` SET `Sunrise_m` = ? WHERE `id` = ?", (Sunrise_m, id))
            self.cursor.execute("UPDATE `Weather` SET `Sunset_h` = ? WHERE `id` = ?", (Sunset_h, id))
            self.cursor.execute("UPDATE `Weather` SET `Sunset_m` = ? WHERE `id` = ?", (Sunset_m, id))

#    def get_pool_time(self, id):
#        """Проверка, есть ли в базе письмо с таким id"""
#        with self.connection:
#            return self.cursor.execute("SELECT * FROM `BotTime` WHERE `id` = ?", (id,)).fetchall()

    def add_email(self, id_email, date_email, sender_email, from_email, body_email, send_group = False):
        """Добавление нового письма в базу"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `delivery` (`id_email`, `date_email`, `sender_email`, `from_email`, `body_email`, `send_group`) VALUES(?,?,?,?,?,?)", (id_email, date_email, sender_email, from_email, body_email, send_group))

    def get_id_email(self, id_email):
        """Проверка, есть ли в базе письмо с таким id"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `delivery` WHERE `id_email` = ?', (id_email,)).fetchall()
            return bool(len(result))

    def get_send_group(self, sender_email, send_group = False):
        """Проверяем письма от sender_email и были ли они отправлены в чат"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `delivery` WHERE `sender_email` = ? AND `send_group` = ?", (sender_email, send_group,)).fetchall()

    def set_send_group(self, id_email, send_group = True):
        with self.connection:
            return self.cursor.execute("UPDATE `delivery` SET `send_group` = ? WHERE `id_email` = ?", (send_group, id_email))

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription(self, id_email, send_group):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `delivery` SET `send_group` = ? WHERE `id_email` = ?", (send_group, id_email))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()