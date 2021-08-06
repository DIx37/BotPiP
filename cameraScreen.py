from loguru import logger
import config
import cv2

login = "admin"
password = "QazWsx12"
ip = "172.16.2.205:554"
channel = "chID=10"
link = f"{login}:{password}@{ip}/{channel}"


def screen_f():
    vidcap = cv2.VideoCapture(f"rtsp://{link}&streamType=main&linkType=tcp")
    success, image = vidcap.read()
    success = True
    cv2.imwrite(config.path_bot + "screen0.jpg", image)
    img = cv2.imread(config.path_bot + "screen0.jpg")
    crop_img = img[38:274, 127:398]
    cv2.imwrite(config.path_bot + "screen0.jpg", crop_img)
    with open(config.path_bot + "screen0.jpg", 'rb') as Screen:
        pass
