from bs4 import BeautifulSoup as BS
import lxml
import re

def parser_from_site(email_text):
    file = open("otus.txt", "w")
    file.write(email_text)
    file.close()
    if len(email_text) > 1000:
        # Поиск ФИО
        match_fio = re.findall('<div>ФИО получателя:     <b>.*</b></div>', str(email_text))
        if len(match_fio) > 0:
            match_fio = str(match_fio[0][28:-10])
        else:
            match_fio = "-"
        # Поиск Телефона
        match_phone = re.findall('<div>Телефон: <b>.*</b></div>', str(email_text))
        if len(match_phone) > 0:
            match_phone = str(match_phone[0][17:-10])
        else:
            match_phone = "-"
        # Поиск Поиск E-Mail
        match_email = re.findall('<div>e-mail:  <b>.*</b>', str(email_text))
        if len(match_email) > 0:
            match_email = str(match_email[0][17:-4])
        else:
            match_email = "-"
        # Поиск Комментария
        match_comment = re.findall('<div>Комментарий: <b>[\s\S]*</b></div>[\s\S]*<h2>', str(email_text))
        if len(match_comment) > 0:
            match_comment = str(match_comment[0][21:-101])
        else:
            match_comment = "-"
        # Поиск Города
        match_city = re.findall('<div>Город:  <b>.*</b></div>', str(email_text))
        if len(match_city) > 0:
            match_city = str(match_city[0][16:-10])
        else:
            match_city = "-"
        # Поиск Улицы
        match_street = re.findall('<div>Улица: <b>.*</b></div>', str(email_text))
        if len(match_street) > 0:
            match_street = str(match_street[0][15:-10])
        else:
            match_street = "-"
        # Поиск Дома
        match_house = re.findall('<div>Дом: <b>.*</b></div>', str(email_text))
        if len(match_house) > 0:
            match_house = str(match_house[0][13:-10])
        else:
            match_house = "-"
        # Поиск Квартиры
        match_app = re.findall('<div>Квартира: <b>.*</b></div>', str(email_text))
        if len(match_app) > 0:
            match_app = str(match_app[0][18:-10])
        else:
            match_app = "-"
        # Поиск типа Оплаты
        match_pay = re.findall('<p>Оплата: <b>.*</b></p>', str(email_text))
        if len(match_pay) > 0:
            match_pay = str(match_pay[0][14:-8])
        else:
            match_pay = "-"
        # Поиск Комментария к заказу
        match_comment_z = re.findall('<p>Комментарий к заказу: <b>.*</b></p>', str(email_text))
        if len(match_comment_z) > 0:
            match_comment_z = str(match_comment_z[0][28:-8])
        else:
            match_comment_z = "-"
        # Поиск Итоговой суммы
        match_all_price = re.findall('<strong>.*</strong>', str(email_text))
        if len(match_all_price) > 0:
            match_all_price = str(match_all_price[0][8:-9] + " руб.")
        else:
            match_all_price = "-"
        # Поиск Блюд, Количества и Цены
        match_bludo = re.findall('.html\"[\s\S].*>[\s\S].*</a>', str(email_text))
        match_bludo_count = re.findall('<td style=\"font-family: Arial;text-align: left;color: #111111;\">.*шт.</td>', str(email_text))
        match_bludo_price = re.findall('<td style=\"font-family: Arial;text-align: left;color: #111111;\">.*руб.</td>', str(email_text))

        # Обединение в одно сообщение
        res_text = "*ФИО*: _" + match_fio
        res_text += "_\n*Телефон*: \n" + match_phone
        res_text += "\n*E-Mail*: \n" + match_email
        res_text += "\n*Комментарий*: \n_" + match_comment
        res_text += "_\n*Адрес доставки*:"
        res_text += "\n   *Город*: _" + match_city
        res_text += "_\n   *Улица*: _" + match_street
        res_text += "_\n   *Дом*: " + match_house
        res_text += "\n   *Квартира*: " + match_app
        res_text += "\n   *Оплата*: _" + match_pay
        res_text += "_\n   *Комментарий к заказу*: _" + match_comment_z + "_"
        res_text += calc_match_bludo(match_bludo, match_bludo_count, match_bludo_price)
        res_text += "\n\n*Итого*: " + match_all_price
    # Если полученное письмо меньше 1000
    else:
        res_text = len(email_text)
    return res_text

def calc_match_bludo(match_bludo, match_bludo_count, match_bludo_price):
    # Проверка нашлись ли блюда, количество и цены
    if len(match_bludo) > 0 and len(match_bludo_count) > 0 and len(match_bludo_price) > 0:
        i = 0
        res = ""
        while i < len(match_bludo):
            res += "\n\n*" + str(match_bludo[i][150:-4])
            res += "*\n  Количество: " + str(match_bludo_count[i][64:-6])
            res += "\n  Цена: " + str(match_bludo_price[i][64:-6])
            i += 1
    else:
        res = "\n\nБлюда не найдены"
    return res

def parser_from_rubeacon(email_text):
    file = open("otus.txt", "w")
    file.write(email_text)
    file.close()
    if len(email_text) > 1000:
        # Поиск ФИО
        match_fio = re.findall('Имя клиента: .*<br>', str(email_text))
        if len(match_fio) > 0:
            match_fio = str(match_fio[0][13:-4])
        else:
            match_fio = "-"
        # Поиск Телефона
        match_phone = re.findall('Телефон: .*<br>', str(email_text))
        if len(match_phone) > 0:
            match_phone = str(match_phone[0][9:-4])
        else:
            match_phone = "-"
        # Поиск Комментария
        match_comment = re.findall('примечание: .*', str(email_text))
        if len(match_comment) > 0:
            match_comment = str(match_comment[0][12:-1])
        else:
            match_comment = "-"
        # Поиск Города
        match_city = re.findall('город: .*<br>', str(email_text))
        if len(match_city) > 0:
            match_city = str(match_city[0][7:-4])
        else:
            match_city = "-"
        # Поиск Улицы
        match_street = re.findall('улица: .*<br>', str(email_text))
        if len(match_street) > 0:
            match_street = str(match_street[0][7:-4])
        else:
            match_street = "-"
        # Поиск Дома
        match_house = re.findall('дом: .*<br>', str(email_text))
        if len(match_house) > 0:
            match_house = str(match_house[0][5:-4])
        else:
            match_house = "-"
        # Поиск Квартиры
        match_app = re.findall('квартира: .*<br>', str(email_text))
        if len(match_app) > 0:
            match_app = str(match_app[0][10:-4])
        else:
            match_app = "-"
        # Поиск Подъезда
        match_parad = re.findall('подъезд: .*<br>', str(email_text))
        if len(match_parad) > 0:
            match_parad = str(match_parad[0][9:-4])
        else:
            match_parad = "-"
        # Поиск типа Оплаты
        match_pay = re.findall('<p>Тип оплаты:\s*.*', str(email_text))
        if len(match_pay) > 0:
            match_pay = str(match_pay[0][30:-2])
        else:
            match_pay = "-"
        # Поиск Комментария к заказу
        match_comment_z = re.findall('Комментарий клиента:<br>\s*.*', str(email_text))
        if len(match_comment_z) > 0:
            match_comment_z = str(match_comment_z[0][24:-1])
        else:
            match_comment_z = "-"
        # Поиск Времени доставки
        #match_time = re.findall('Время доставки:[\s\S]*\d\d.\d\d.\d\d\d\d \d\d:\d\d', str(email_text))
        #if len(match_time) > 0:
        #    match_time = str(match_time[0][16:-2])
        #else:
        #    match_time = "-"
        # Поиск Итоговой суммы
        match_all_price = re.findall('<p>Сумма заказа: .*</p>', str(email_text))
        if len(match_all_price) > 0:
            match_all_price = str(match_all_price[0][17:-4] + " руб.")
        else:
            match_all_price = "-"
        # Поиск Блюд, Количества
        match_bludo = re.findall('\d*шт. .*', str(email_text))
        #match_bludo = re.findall('шт. .*\s*<br>', str(email_text))
        #match_bludo_count = re.findall('<br>\s*.*шт. ', str(email_text))

        # Обединение в одно сообщение
        res_text = "*ФИО*: " + match_fio
        res_text += "\n*Телефон*: \n" + match_phone
        res_text += "\n*Комментарий*: \n" + match_comment
        res_text += "\n*Адрес доставки*:"
        res_text += "\n   *Город*: " + match_city
        res_text += "\n   *Улица*: " + match_street
        res_text += "\n   *Дом*: " + match_house
        res_text += "\n   *Квартира*: " + match_app
        res_text += "\n   *Подъезд*: " + match_parad
        res_text += "\n   *Оплата*: " + match_pay
        res_text += "\n   *Комментарий к заказу*: " + match_comment_z + "\n"
        #res_text += "\n   Время доставки: " + match_time
        #res_text += calc_match_bludo_rubeacon(match_bludo, match_bludo_count)
        i = 0
        while i < len(match_bludo):
            res_text += "\n*" + str(match_bludo[i]) + "*\n"
            i += 1
        res_text += "\n*Итого*: " + match_all_price
    # Если полученное письмо меньше 1000
    else:
        res_text = len(email_text)
    return res_text