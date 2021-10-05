# -- coding: utf-8 --
from datetime import datetime as dt
from astral.sun import sun
from loguru import logger
import requests
from config import *

# Координаты ресторана
lat = 55.560105
lon = 37.438028

@logger.catch
def check_weather():
    code_to_smile = {
        "Clear": " \U00002600",
        "Clouds": " \U00002601",
        "Rain": " \U00002614",
        "Drizzle": " \U00002614",
        "Thunderstorm": " \U000026A1",
        "Snow": " \U0001F328",
        "Mist": " \U0001F32B"
        }
    try:
        req = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={Weather_TOKEN}&units=metric&lang=ru")
        weather = req.json()
        weather_now = dict()
        if weather["weather"][0]["main"] in code_to_smile:
            wd = code_to_smile[weather["weather"][0]["main"]]
            weather_now['weather_weather'] = weather["weather"][0]["description"].capitalize() + wd
        else:
            weather_now['weather_weather'] = weather["weather"][0]["description"].capitalize()
        weather_now['temp'] = str(weather["main"]["temp"])
        weather_now['feels_like'] = str(weather["main"]["feels_like"])
        weather_now['humidity'] = str(weather["main"]["humidity"])
        weather_now['pressure'] = str(round(weather["main"]["pressure"]/1.333))
        weather_now['wind_speed'] = str(weather["wind"]["speed"])
        weather_now['wind_deg'] = str(weather["wind"]["deg"])
        weather_now['sunrise'] = dt.fromtimestamp(int(weather["sys"]["sunrise"]))
        weather_now['sunset'] = dt.fromtimestamp(int(weather["sys"]["sunset"]))
        weather_now['visibility'] = str(weather["visibility"])
    except Exception:
        weather_now['weather_weather'] = "N/A"
        weather_now['temp'] = "N/A"
        weather_now['feels_like'] = "N/A"
        weather_now['humidity'] = "N/A"
        weather_now['pressure'] = "N/A"
        weather_now['wind_speed'] = "N/A"
        weather_now['wind_deg'] = "N/A"
        weather_now['sunrise'] = "N/A"
        weather_now['sunset'] = "N/A"
        weather_now['visibility'] = "N/A"
    return weather_now