from sqllite import SQLighter
from datetime import datetime
from loguru import logger
from pytz import timezone
import LaurentJSON as LJ
import datetime as dt
#import schedule
#import platform
import requests
import weather
import config
import time

# Подключение к БД
db = SQLighter(config.path_bot + "BotPiP.db")
logger.add(config.path_bot + "ReleTime.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")

# Переменные
L_IP21 = config.Laurent_IP_Pool21
L_IP22 = config.Laurent_IP_Pool22
L_Pass = config.Laurent_Pass

@logger.catch
def set_sunrise_and_sunset_bd():
    now = dt.datetime.now()
    Date = now.strftime("%D")
    s_a_s = weather.check_weather()
    db.update_weather(Date, s_a_s[5], s_a_s[6], s_a_s[7], s_a_s[8])
#    db.update_weather_bottime(s_a_s[5], s_a_s[6], s_a_s[7], s_a_s[8])
    logger.info(f"Добавил в базу время рассвета {s_a_s[5]}:{s_a_s[6]} и заката {s_a_s[7]}:{s_a_s[8]}")

@logger.catch
def main_f():
    t_start = time.monotonic()
    moscow_tz = timezone('Europe/Moscow')
    d = moscow_tz.localize(datetime.now()).strftime("%w")
    h = moscow_tz.localize(datetime.now()).strftime("%H")
    m = moscow_tz.localize(datetime.now()).strftime("%M")
    if h == "01" and "00":
        set_sunrise_and_sunset_bd()
        s_a_s = weather.check_weather()
        db.update_sas(s_a_s[5], s_a_s[6], s_a_s[7], s_a_s[8])
    for rele_in_db in db.get_pool_time_all(d, h, m):
        rele = rele_in_db[4]
        turnOnOff = rele_in_db[5]
        if rele == "podn":
            L_IP = L_IP22
            rele = "1"
        elif rele == "rekl":
            L_IP = L_IP22
            rele = "2"
        elif rele == "park":
            L_IP = L_IP22
            rele = "3"
        elif rele == "ekra":
            L_IP = L_IP22
            rele = "4"
        elif rele == "basv":
            L_IP = L_IP21
            rele = "1"
        elif rele == "basn":
            L_IP = L_IP21
            rele = "2"
        elif rele == "podz":
            L_IP = L_IP21
            rele = "3"
        elif rele == "vodo":
            L_IP = L_IP21
            rele = "4"
        LJ.set_rele(L_IP, L_Pass, rele, turnOnOff)
        requests.get(f"http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{rele},{turnOnOff}")
        logger.info(f"Переключил реле по адресу http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{rele},{turnOnOff}")
    while time.monotonic() - t_start <= 40:
        pass

#schedule.every().day.at("01:00").do(set_sunrise_and_sunset_bd)

# Запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
#            schedule.run_pending()
            main_f()
            time.sleep(5)
        except Exception as err:
            logger.error(err)
            time.sleep(10) # В случае падения