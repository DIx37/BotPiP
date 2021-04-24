import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_email(self, id_email, date_email, sender_email, body_email, send_group = False):
        """Добавление нового письма в базу"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `delivery` (`id_email`, `date_email`, `sender_email`, `body_email`, `send_group`) VALUES(?,?,?,?,?)", (id_email, date_email, sender_email, body_email, send_group))

    def get_id_email(self, id_email):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `delivery` WHERE `id_email` = ?', (id_email,)).fetchall()
            return bool(len(result))

    def get_send_group(self, sender_email = "orderspip@yandex.ru", send_group = False):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `delivery` WHERE `sender_email` = ? AND `send_group` = ?", (sender_email, send_group,)).fetchall()

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

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()