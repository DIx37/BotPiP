# -- coding: utf-8 --
from astral import LocationInfo
#from logging import exception
from astral.sun import sun
from loguru import logger
import requests
import re

# off, yandex, astral
settings_weaher = "astral"

#https://yandex.ru/pogoda/sosenki-novomoskovsky-administrative-district
city = "sosenki-novomoskovsky-administrative-district"

@logger.catch
def check_weather():
    if settings_weaher == "yandex":
        raw_html = requests.get(f"https://yandex.ru/pogoda/{city}")
        content_html = raw_html.content
        decode_html = content_html.decode('utf-8').replace(u'\u2212','-')

        #Температура json.temp.ul
        try:
            match_temp_ul = re.findall("Текущая температура</span><span class=\"temp__value temp__value_with-unit\">\D?\d+</span></div>", str(decode_html))
            match_temp_ul2 = re.findall("\D?\d+", str(match_temp_ul))
            temp_ul = match_temp_ul2[0]
        except Exception:
            temp_ul = "N/A"

        #Ощущается как json.aptmp
        try:
            match_aptmp = re.findall("Ощущается как</div><div class=\"term__value\"><div class=\"temp\" role=\"text\"><span class=\"temp__value temp__value_with-unit\">\D?\d+<", str(decode_html))
            match_aptmp2 = re.findall("\D?\d+", str(match_aptmp))
            aptmp = match_aptmp2[0]
        except Exception:
            aptmp = "N/A"

        #Погода json.tstm
        try:
            match_tstm = re.findall("<div class=\"link__condition day-anchor i-bem\" data-bem='{\"day-anchor\":{\"anchor\":\d+}}'>.{,30}<", str(decode_html))
            tstm = match_tstm[0][85:-7]
            if tstm[0] == ">":
                tstm = tstm[1:]
        except Exception:
            tstm = "N/A"

        #Относительная влажность json.hum
        try:
            match_hum = re.findall("<i class=\"icon icon_humidity-white term__fact-icon\" aria-hidden=\"true\"></i>.\d+%<", str(decode_html))
            hum = match_hum[0][75:-2]
        except Exception:
            hum = "N/A"

        #Поверхносное давление json.sp
        try:
            match_sp = re.findall("<i class=\"icon icon_pressure-white term__fact-icon\" aria-hidden=\"true\"></i>.\d+", str(decode_html))
            sp = match_sp[0][75:]
        except Exception:
            sp = "N/A"

        #Восход html_sunrise
        try:
            match_html_sunrise = re.findall("Восход</div>.\d+:.\d+", str(decode_html))
            html_sunrise = match_html_sunrise[0][12:]
            sunrise_h = html_sunrise[0:2]
            sunrise_m = html_sunrise[3:5]
        except Exception:
            sunrise_h = "N/A"
            sunrise_m = "N/A"

        #Закат html_sunset
        try:
            match_html_sunset = re.findall("Закат</div>.\d+:.\d+", str(decode_html))
            html_sunset = match_html_sunset[0][11:]
            sunset_h = html_sunset[0:2]
            sunset_m = html_sunset[3:5]
        except Exception:
            sunset_h = "N/A"
            sunset_m = "N/A"
        return temp_ul, aptmp, tstm, hum, sp, sunrise_h, sunrise_m, sunset_h, sunset_m,
    elif settings_weaher == "astral":
        loc = LocationInfo(timezone='Europe/Moscow', latitude = 55.560105, longitude = 37.438028)
        s = sun(loc.observer, tzinfo=loc.timezone)
#        print(s["dawn"].strftime("%H:%M"))
#        print(s["dusk"].strftime("%H:%M"))
#        print(s["noon"].strftime("%H:%M"))
#        print(s["sunrise"].strftime("%H:%M"))
#        print(s["sunset"].strftime("%H:%M"))
        temp_ul = "N/A"
        aptmp = "N/A"
        tstm = "N/A"
        hum = "N/A"
        sp = "N/A"
        sunrise_h = s["sunrise"].strftime("%H")
        sunrise_m = s["sunrise"].strftime("%M")
        sunset_h = s["sunset"].strftime("%H")
        sunset_m = s["sunset"].strftime("%M")
        return temp_ul, aptmp, tstm, hum, sp, sunrise_h, sunrise_m, sunset_h, sunset_m,
    elif settings_weaher == "off":
        temp_ul = "N/A"
        aptmp = "N/A"
        tstm = "N/A"
        hum = "N/A"
        sp = "N/A"
        sunrise_h = "N/A"
        sunrise_m = "N/A"
        sunset_h = "N/A"
        sunset_m = "N/A"
        return temp_ul, aptmp, tstm, hum, sp, sunrise_h, sunrise_m, sunset_h, sunset_m,