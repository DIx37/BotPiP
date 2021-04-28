# coding=utf-8
import time
import config
import imaplib
import email
import base64
from imapclient import imap_utf7
from sqllite import SQLighter
import chardet

# Подключение к почте
mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login(config.orders_mail_login, config.orders_mail_password)

# Подключение к БД
db = SQLighter("Delivery.db")

def get_email(email_id):
    result, data = mail.fetch(email_id, "(RFC822)")
    #print(result)
    raw_email = data[0][1]
    try:
        meta = chardet.detect(raw_email)
        print(meta.get('encoding'))
        if meta.get('encoding') == "ascii":
            raw_email_string = raw_email.decode('iso-8859-1')
        elif meta.get('encoding') == "utf-8":
            raw_email_string = raw_email.decode('utf-8').replace(u'\u2212','-')
        else:
            print("Неизвестная кодировка")
        email_message = email.message_from_string(raw_email_string)
    except Exception as err:
        print(err)

    if email_message.is_multipart():
        try:
            body_email = ""
            for payload in email_message.get_payload():
                body = payload.get_payload(decode=True).decode('utf-8')
                id_email = email_id.decode('utf-8')
                date_email = email_message['Date']
                sender_email = email_message['To']
                from_email = email_message['From']
                body_email = body
            db.add_email(id_email, date_email, sender_email, from_email, body_email)
        except Exception as err:
            print(err)
            id_email = email_id.decode('utf-8')
            date_email = email_message['Date']
            sender_email = email_message['To']
            from_email = email_message['From']
            body_email = "Нет тела письма"
            db.add_email(id_email, date_email, sender_email, from_email, body_email)
    else:
        try:
            print("3")
            body = email_message.get_payload(decode=True).decode('utf-8')
            id_email = email_id.decode('utf-8')
            date_email = email_message['Date']
            sender_email = email_message['To']
            from_email = email_message['From']
            body_email = str(body)
            db.add_email(id_email, date_email, sender_email, from_email, body_email)
        except Exception as err:
            print(err)
            id_email = email_id.decode('utf-8')
            date_email = email_message['Date']
            sender_email = email_message['To']
            from_email = email_message['From']
            body_email = "Нет тела письма"
            db.add_email(id_email, date_email, sender_email, from_email, body_email)
    #time.sleep(60)

def read_email():
    # Выбор папки входящие
    mail.select("Orders")

    # Запрос всех писем
    result, data = mail.search(None, "ALL")
    #print(result)
    ids = data[0]
    id_list = ids.split()
    for email_id in id_list:
        if db.get_id_email(email_id.decode('utf-8')) == True:
            #print("Нашёл " + str(email_id.decode('utf-8')))
            pass
        else:
            print("Не нашёл " + str(email_id.decode('utf-8')))
            get_email(email_id)

if __name__ == '__main__':
    while True:
        try:
            read_email()
            #print("Жду")
            time.sleep(60)
        except Exception as err:
            #print("Ошибка")
            print(err)
            time.sleep(1) # В случае падения