from datetime import datetime as dt
from sqllite import SQLighter
from loguru import logger
from pytz import timezone
import LaurentJSON as LJ
import weather
import config
import time

# Подключение к БД
db = SQLighter(config.path_bot + "BotPiP.db")
logger.add(config.config_bot + "ReleTime.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")

# Переменные
L_IP21 = config.Laurent_IP_Pool21
L_IP22 = config.Laurent_IP_Pool22
L_Pass = config.Laurent_Pass

@logger.catch
def main_f():
    t_start = time.monotonic()
    moscow_tz = timezone('Europe/Moscow')
    d = moscow_tz.localize(dt.now()).strftime("%w")
    h = moscow_tz.localize(dt.now()).strftime("%H")
    m = moscow_tz.localize(dt.now()).strftime("%M")
    # h = "01"
    # m = "00"
    if h == "01" and m == "00":
        s_a_s = weather.check_weather()
        sunrise_h = s_a_s["sunrise"].strftime("%H")
        sunrise_m = s_a_s["sunrise"].strftime("%M")
        sunset_h = s_a_s["sunset"].strftime("%H")
        sunset_m = s_a_s["sunset"].strftime("%M")
        db.update_sas(sunrise_h, sunrise_m, sunset_h, sunset_m)
        logger.info(f"Добавил в базу время восхода {sunrise_h}:{sunrise_m} и заката {sunset_h}:{sunset_m}")
    for rele_in_db in db.get_pool_time_all(d, h, m):
        rele = rele_in_db[4]
        turnOnOff = rele_in_db[5]
        if rele == "pod_navesom":
            L_IP = L_IP22
            rele = "1"
        elif rele == "reklama":
            L_IP = L_IP22
            rele = "2"
        elif rele == "park":
            L_IP = L_IP22
            rele = "3"
        elif rele == "ekran":
            L_IP = L_IP22
            rele = "4"
        elif rele == "pool_up":
            L_IP = L_IP21
            rele = "1"
        elif rele == "pool_down":
            L_IP = L_IP21
            rele = "2"
        elif rele == "pod_zontami":
            L_IP = L_IP21
            rele = "3"
        elif rele == "vodopad":
            L_IP = L_IP21
            rele = "4"
        LJ.set_rele(L_IP, L_Pass, rele, turnOnOff)
        logger.info(f"Переключил реле по адресу http://{L_IP}/cmd.cgi?psw={L_Pass}&cmd=REL,{rele},{turnOnOff}")
    while time.monotonic() - t_start <= 40:
        pass


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