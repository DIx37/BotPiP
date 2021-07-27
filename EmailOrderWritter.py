# coding=utf-8
import time
import config
import imaplib
import email
import base64
import chardet
import error_sender as es
from imapclient import imap_utf7
from sqllite import SQLighter

# Подключение к почте
mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login(config.orders_mail_login, config.orders_mail_password)


# Подключение к БД
#db = SQLighter("/home/bots/pip/Delivery.db")
db = SQLighter("Delivery.db")

# Добавление письма от сайта и приложени в базу
def get_email(email_id):
    try:
        result, data = mail.fetch(email_id, "(RFC822)")
        # Если всё ОК, то продолжаем
        if result == "OK":
            # Узнаём от кому письмо
            raw_email = data[0][1]
            raw_email_string_check = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string_check)
            sender_email = email_message['To']
            # Если orderspip@yandex.ru, то письмо с сайта
            if sender_email == "orderspip@yandex.ru":
                raw_email_string = raw_email.decode('utf-8').replace(u'\u2212','-')
                email_message = email.message_from_string(raw_email_string)
                if email_message.is_multipart():
                    pass
                else:
                    # Если письмо не составное
                    try:
                        raw_email = email_message.get_payload(decode=True)
                        # Узнаём кодировку письма
                        meta = chardet.detect(raw_email)
                        #print(meta.get('encoding'))
                        # Если кодировка iso-8859-1
                        if meta.get('encoding') == "iso-8859-1":
                            body = email_message.get_payload(decode=True).decode('iso-8859-1')
                            id_email = email_id.decode('utf-8')
                            date_email = email_message['Date']
                            sender_email = email_message['To']
                            from_email = email_message['From']
                            body_email = str(body)
                            bdcod = bytes(body_email, 'utf-8').decode('unicode-escape')
                            db.add_email(id_email, date_email, sender_email, from_email, bdcod)
                        # Если кодировка ascii
                        elif meta.get('encoding') == "ascii":
                            body = email_message.get_payload(decode=True).decode('utf-8')
                            id_email = email_id.decode('utf-8')
                            date_email = email_message['Date']
                            sender_email = email_message['To']
                            from_email = email_message['From']
                            body_email = str(body)
                            bdcod = bytes(body_email, 'ascii').decode('unicode-escape')
                            db.add_email(id_email, date_email, sender_email, from_email, bdcod)
                    except Exception as err:
                        es.se(err)
                        id_email = email_id.decode('utf-8')
                        date_email = email_message['Date']
                        sender_email = email_message['To']
                        from_email = email_message['From']
                        body_email = err
                        db.add_email(id_email, date_email, sender_email, from_email, body_email)
            # Если письмо им, значит письмо от приложения
            elif sender_email == "rubeaconorders@gmail.com, delivery@2253838.ru, orders@pizzafab.ru":
                raw_email_string = raw_email.decode('iso-8859-1')
                email_message = email.message_from_string(raw_email_string)
                if email_message.is_multipart():
                    pass
                # Если письмо не составное
                else:
                    try:
                        body = email_message.get_payload(decode=True).decode('utf-8')
                        id_email = email_id.decode('utf-8')
                        date_email = email_message['Date']
                        sender_email = email_message['To']
                        from_email = email_message['From']
                        db.add_email(id_email, date_email, sender_email, from_email, body)
                    except Exception as err:
                        es.se(err)
                        id_email = email_id.decode('utf-8')
                        date_email = email_message['Date']
                        sender_email = email_message['To']
                        from_email = email_message['From']
                        body_email = err
                        db.add_email(id_email, date_email, sender_email, from_email, body_email)
            # Если письмо для orders@pizzafab.ru, то это повторное письмо для проверки работы
            elif sender_email == "orders@pizzafab.ru":
                    id_email = email_id.decode('utf-8')
                    date_email = email_message['Date']
                    sender_email = email_message['To']
                    from_email = email_message['From']
                    body_email = "Повторное письмо"
                    db.add_email(id_email, date_email, sender_email, from_email, body_email)
            else:
                pass
    except Exception as err:
        es.se(err)

# Добавление письма от Delivery Club в базу
def get_email_dc(email_id):
    try:
        result, data = mail.fetch(email_id, "(RFC822)")
        # Если всё ОК, то продолжаем
        if result == "OK":
            # Узнаём от кому письмо
            raw_email = data[0][1]
            raw_email_string_check = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string_check)
            sender_email = email_message['To']
            # Если orderspip@yandex.ru, то письмо с сайта
            if sender_email == "orderspip@yandex.ru":
                raw_email_string = raw_email.decode('utf-8').replace(u'\u2212','-')
                email_message = email.message_from_string(raw_email_string)
                if email_message.is_multipart():
                    pass
                else:
                    # Если письмо не составное
                    try:
                        raw_email = email_message.get_payload(decode=True)
                        # Узнаём кодировку письма
                        meta = chardet.detect(raw_email)
                        #print(meta.get('encoding'))
                        # Если кодировка iso-8859-1
                        if meta.get('encoding') == "iso-8859-1":
                            body = email_message.get_payload(decode=True).decode('iso-8859-1')
                            id_email = email_id.decode('utf-8')
                            date_email = email_message['Date']
                            sender_email = email_message['To']
                            from_email = email_message['From']
                            body_email = str(body)
                            bdcod = bytes(body_email, 'utf-8').decode('unicode-escape')
                            db.add_email(id_email, date_email, sender_email, from_email, bdcod)
                        # Если кодировка ascii
                        elif meta.get('encoding') == "ascii":
                            body = email_message.get_payload(decode=True).decode('utf-8')
                            id_email = email_id.decode('utf-8')
                            date_email = email_message['Date']
                            sender_email = email_message['To']
                            from_email = email_message['From']
                            body_email = str(body)
                            bdcod = bytes(body_email, 'ascii').decode('unicode-escape')
                            db.add_email(id_email, date_email, sender_email, from_email, bdcod)
                    except Exception as err:
                        es.se(err)
                        id_email = email_id.decode('utf-8')
                        date_email = email_message['Date']
                        sender_email = email_message['To']
                        from_email = email_message['From']
                        body_email = err
                        db.add_email(id_email, date_email, sender_email, from_email, body_email)
            # Если письмо им, значит письмо от приложения
            elif sender_email == "rubeaconorders@gmail.com, delivery@2253838.ru, orders@pizzafab.ru":
                raw_email_string = raw_email.decode('iso-8859-1')
                email_message = email.message_from_string(raw_email_string)
                if email_message.is_multipart():
                    pass
                # Если письмо не составное
                else:
                    try:
                        body = email_message.get_payload(decode=True).decode('utf-8')
                        id_email = email_id.decode('utf-8')
                        date_email = email_message['Date']
                        sender_email = email_message['To']
                        from_email = email_message['From']
                        db.add_email(id_email, date_email, sender_email, from_email, body)
                    except Exception as err:
                        es.se(err)
                        id_email = email_id.decode('utf-8')
                        date_email = email_message['Date']
                        sender_email = email_message['To']
                        from_email = email_message['From']
                        body_email = err
                        db.add_email(id_email, date_email, sender_email, from_email, body_email)
            # Если письмо для orders@pizzafab.ru, то это повторное письмо для проверки работы
            elif sender_email == "orders@pizzafab.ru":
                    id_email = email_id.decode('utf-8')
                    date_email = email_message['Date']
                    sender_email = email_message['To']
                    from_email = email_message['From']
                    body_email = "Повторное письмо"
                    db.add_email(id_email, date_email, sender_email, from_email, body_email)
            else:
                pass
    except Exception as err:
        es.se(err)

def read_email():
    # Выбор папки входящие
    mail.select("Orders")

    # Запрос всех писем
    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    for email_id in id_list:
        if db.get_id_email(email_id.decode('utf-8')) == True:
            #print("Нашёл " + str(email_id.decode('utf-8')))
            pass
        else:
            print("Не нашёл " + str(email_id.decode('utf-8')))
            get_email(email_id)
            get_email_dc(email_id)

# Отправка ошибок в бота
async def send_msg(text):
    await bot.send_message(ID_Delivery_Bot, text, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    while True:
        try:
            read_email()
            time.sleep(60)
        except Exception as err:
            print(err)
            es.se(err)
            time.sleep(10) # В случае падения