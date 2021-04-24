# coding=utf-8

import imaplib
import email
import base64
from imapclient import imap_utf7

mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login('orders@pizzafab.ru', 'orders12')

response = mail.list()
mail.select("inbox")
result, data = mail.search(None, "ALL")
ids = data[0]
id_list = ids.split()
latest_email_id = id_list[-1]
#print(latest_email_id)
result, data = mail.fetch(latest_email_id, "(RFC822)")
raw_email = data[0][1]
raw_email_string = raw_email.decode('utf-8')
#print(raw_email_string)
email_message = email.message_from_string(raw_email_string)
print(email_message['To'])
print(email.utils.parseaddr(email_message['From']))
print(email_message['Date'])
print(email_message['Subject'])
print(email_message['Message-Id'])
if email_message.is_multipart():
    for payload in email_message.get_payload():
        body = payload.get_payload(decode=True).decode('utf-8')
        print(body)
else:    
    body = email_message.get_payload(decode=True).decode('utf-8')
    print(body)