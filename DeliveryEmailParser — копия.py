from bs4 import BeautifulSoup as BS
import lxml
import re
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='rir7m')

def parser_from_site(email_text):
    file = open("otus.txt", "w")
    file.write(email_text)
    file.close()
    if len(email_text) > 1000:

        # Поиск ФИО
        try:
            match_fio = re.findall('<div>ФИО получателя:     <b>.*</b></div>', str(email_text))
            if len(match_fio) > 0:
                match_fio = str(match_fio[0][28:-10])
            else:
                match_fio = "-"
        except Exception as err:
            match_fio = err

        # Поиск Телефона
        try:
            match_phone = re.findall('<div>Телефон: <b>.*</b></div>', str(email_text))
            if len(match_phone) > 0:
                match_phone = str(match_phone[0][17:-10])
            else:
                match_phone = "-"
        except Exception as err:
            match_phone = err

        # Поиск Поиск E-Mail
        try:
            match_email = re.findall('<div>e-mail:  <b>.*</b>', str(email_text))
            if len(match_email) > 0:
                match_email = str(match_email[0][17:-4])
            else:
                match_email = "-"
        except Exception as err:
            match_email = err

        # Поиск Комментария
        try:
            match_comment = re.findall('<div>Комментарий: <b>[\s\S]*</b></div>[\s\S]*<h2>', str(email_text))
        except Exception as err:
            match_comment = err
        if len(match_comment) > 0:
            match_comment = str(match_comment[0][21:-101])
        else:
            match_comment = "-"

        # Поиск Города
        try:
            match_city = re.findall('<div>Город:  <b>.*</b></div>', str(email_text))
            if len(match_city) > 0:
                match_city = str(match_city[0][16:-10])
            else:
                match_city = "-"
        except Exception as err:
            match_city = err

        # Поиск Улицы
        try:
            match_street = re.findall('<div>Улица: <b>.*</b></div>', str(email_text))
            if len(match_street) > 0:
                match_street = str(match_street[0][15:-10])
            else:
                match_street = "-"
        except Exception as err:
            match_street = err

        # Поиск Дома
        try:
            match_house = re.findall('<div>Дом: <b>.*</b></div>', str(email_text))
            if len(match_house) > 0:
                match_house = str(match_house[0][13:-10])
            else:
                match_house = "-"
        except Exception as err:
            match_house = err

        # Поиск Квартиры
        try:
            match_app = re.findall('<div>Квартира: <b>.*</b></div>', str(email_text))
            if len(match_app) > 0:
                match_app = str(match_app[0][18:-10])
            else:
                match_app = "-"
        except Exception as err:
            match_app = err

        # Поиск типа Оплаты
        try:
            match_pay = re.findall('<p>Оплата: <b>.*</b></p>', str(email_text))
            if len(match_pay) > 0:
                match_pay = str(match_pay[0][14:-8])
            else:
                match_pay = "-"
        except Exception as err:
            match_pay = err

        # Поиск Комментария к заказу
        try:
            match_comment_z = re.findall('<p>Комментарий к заказу: <b>.*</b></p>', str(email_text))
            if len(match_comment_z) > 0:
                match_comment_z = str(match_comment_z[0][28:-8])
            else:
                match_comment_z = "-"
        except Exception as err:
            match_comment_z = err

        # Поиск Итоговой суммы
        try:
            match_all_price = re.findall('<strong>.*</strong>', str(email_text))
            if len(match_all_price) > 0:
                match_all_price = str(match_all_price[0][8:-9] + " руб.")
            else:
                match_all_price = "-"
        except Exception as err:
            match_all_price = err

        # Поиск Блюд, Количества и Цены
        try:
            match_bludo = re.findall('.html\"[\s\S].*>[\s\S].*</a>', str(email_text))
        except Exception as err:
            match_bludo = err
        try:
            match_bludo_count = re.findall('<td style=\"font-family: Arial;text-align: left;color: #111111;\">.*шт.</td>', str(email_text))
        except Exception as err:
            match_bludo_count = err
        try:
            match_bludo_price = re.findall('<td style=\"font-family: Arial;text-align: left;color: #111111;\">.*руб.</td>', str(email_text))
        except Exception as err:
            match_bludo_price = err

        # Обединение в одно сообщение
        res_text = "<b>ФИО</b>: <code>" + match_fio
        res_text += "</code>\n<b>Телефон</b>: \n<code>" + match_phone
        res_text += "</code>\n<b>E-Mail</b>: \n<code>" + match_email
        res_text += "</code>\n<b>Комментарий</b>: \n" + match_comment
        res_text += "\n<b>Адрес доставки</b>: <code>"
        res_text += "</code>\n   <b>Город</b>: <code>" + match_city
        res_text += "</code>\n   <b>Улица</b>: <code>" + match_street
        res_text += "</code>\n   <b>Дом</b>: <code>" + match_house
        res_text += "</code>\n   <b>Квартира</b>: <code>" + match_app
        res_text += "</code>\n   <b>Оплата</b>: <code>" + match_pay
        res_text += "</code>\n   <b>Комментарий к заказу</b>: <code>" + match_comment_z + "</code>"
        res_text += calc_match_bludo(match_bludo, match_bludo_count, match_bludo_price)
        res_text += "\n\n<b>Итого</b>: <code>" + match_all_price + "</code>"
        location = geolocator.geocode("Птицы и Пчёлы")
        lat = str(location.latitude)
        lon = str(location.longitude)
        #res_text += "\n\n" + location.longitude
        #res_text += "\n\n" + location.raw

        #print(location.address)
        #print(location.latitude, location.longitude)
        #print(location.raw)
    # Если полученное письмо меньше 1000
    else:
        res_text = len(email_text)
    return res_text, lat, lon

def calc_match_bludo(match_bludo, match_bludo_count, match_bludo_price):
    # Проверка нашлись ли блюда, количество и цены
    if len(match_bludo) > 0 and len(match_bludo_count) > 0 and len(match_bludo_price) > 0:
        i = 0
        res = ""
        while i < len(match_bludo):
            res += "\n\n<b>" + str(match_bludo[i][150:-4])
            res += "</b>\n  <b>Количество</b>: <code>" + str(match_bludo_count[i][64:-6])
            res += "</code>\n  <b>Цена</b>: <code>" + str(match_bludo_price[i][64:-6]) + "</code>"
            i += 1
    else:
        res = "\n\nНе смог распарсить блюда, проверьте почту вручную"
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
        res_text = "<b>ФИО</b>: <code>" + match_fio
        res_text += "</code>\n<b>Телефон</b>: \n<code>" + match_phone
        res_text += "</code>\n<b>Комментарий</b>: \n<code>" + match_comment
        res_text += "</code>\n<b>Адрес доставки</b>:<code>"
        res_text += "</code>\n   <b>Город</b>: <code>" + match_city
        res_text += "</code>\n   <b>Улица</b>: <code>" + match_street
        res_text += "</code>\n   <b>Дом</b>: <code>" + match_house
        res_text += "</code>\n   <b>Квартира</b>: <code>" + match_app
        res_text += "</code>\n   <b>Подъезд</b>: <code>" + match_parad
        res_text += "</code>\n   <b>Оплата</b>: <code>" + match_pay
        res_text += "</code>\n   <b>Комментарий к заказу</b>: <code>" + match_comment_z + "</code>\n"
        #res_text += "\n   Время доставки: " + match_time
        #res_text += calc_match_bludo_rubeacon(match_bludo, match_bludo_count)
        i = 0
        while i < len(match_bludo):
            #your_string = "it's a toy,isn't a tool.i don't know anything."
            #removal_list = ["it's","didn't","isn't","don't"]
            #for word in removal_list:
            #    your_string = your_string.replace(word, "")
            res_text += "\n<b>" + str(match_bludo[i]) + "</b>\n"
            res_text = res_text.replace("<br>", "")
            i += 1
        res_text += "\n<b>Итого</b>: <code>" + match_all_price + "</code>"
    # Если полученное письмо меньше 1000
    else:
        res_text = len(email_text)
    return res_text