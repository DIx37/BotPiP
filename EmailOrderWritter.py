# coding=utf-8
import time
import config
import imaplib
import email
import base64
from imapclient import imap_utf7
from sqllite import SQLighter

# Подключение к почте
mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login(config.orders_mail_login, config.orders_mail_password)

# Подключение к БД
db = SQLighter("Delivery.db")

def get_email(email_id):
    result, data = mail.fetch(email_id, "(RFC822)")
    raw_email = data[0][1]
    try:
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
    except Exception as err:
        print(err)

    if email_message.is_multipart():
        try:
            for payload in email_message.get_payload():
                body = payload.get_payload(decode=True).decode('utf-8')
                id_email = email_id
                date_email = email_message['Date']
                sender_email = email_message['To']
                body_email = body
                db.add_email(id_email, date_email, sender_email, body_email)
        except Exception as err:
            print(err)
            id_email = email_id
            date_email = email_message['Date']
            sender_email = email_message['To']
            body_email = "Нет тела письма"
            db.add_email(id_email, date_email, sender_email, body_email)
    else:
        try:
            body = email_message.get_payload(decode=True).decode('utf-8')
            id_email = email_id
            date_email = email_message['Date']
            sender_email = email_message['To']
            body_email = body
            db.add_email(id_email, date_email, sender_email, body_email)
        except Exception as err:
            print(err)
            id_email = email_id
            date_email = email_message['Date']
            sender_email = email_message['To']
            body_email = "Нет тела письма"
            db.add_email(id_email, date_email, sender_email, body_email)

def read_email():
    # Выбор папки входящие
    mail.select("inbox")

    # Запрос всех писем
    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    for email_id in id_list:
        if db.get_id_email(email_id) == True:
            #print("Нашёл" + str(email_id))
            pass
        else:
            print("Не нашёл" + str(email_id))
            get_email(email_id)

if __name__ == '__main__':
    while True:
        try:
            read_email()
            print("Жду")
            time.sleep(60)
        except Exception as err:
            print("Ошибка")
            print(err)
            time.sleep(10) # В случае падения