import cv2
from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor
from loguru import logger
import config

#bot = Bot(token=config.ErrorBot_TOKEN)
#dp = Dispatcher(bot)

#async def send_error(Screen):
#    await bot.send_photo(config.DIx_ID, Screen)

#@logger.catch
#def se(text):
#    executor.start(dp, send_error(text))

def screen_f():
    vidcap = cv2.VideoCapture("rtsp://admin:QazWsx12@172.16.2.205:554/chID=10&streamType=main&linkType=tcp")
    success,image = vidcap.read()
    success = True
    cv2.imwrite("screen0.jpg", image)
    img = cv2.imread("screen0.jpg")
    crop_img = img[38:274, 127:398]
    cv2.imwrite("screen0.jpg", crop_img)
    with open(config.path_bot + "screen0.jpg", 'rb') as Screen:
        pass

#C:\Programs\VideoLAN\VLC\vlc.exe -I http --http-password 1111 -R "rtsp://admin:QazWsx12@172.16.2.205:554/chID=1&streamType=main&linkType=tcp" --sout "#transcode{vcodec=mjpg,vb=2500,scale=1.0,fps=10,acodec=none}:standard{access=http{mime=multipart/x-mixed-replace; boundary=7b3cc56e5f51db803f790dad720ed50a},mux=mpjpeg,dst=:8888/videostream.cgi}"