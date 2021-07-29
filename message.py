# -- coding: utf-8 --
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Bot, Dispatcher, executor, types
from sqllite import SQLighter
from loguru import logger
import LaurentJSON as LJ
import keyboards as kb
import requests
import weather
import config
import time
import re
import modbusread as MR
import cameraScreen as cs
from aiogram.utils.callback_data import CallbackData
import utils
from modbus import Modbus

class Msg:
    """Работа с протоколом modbus"""
    def __init__(self, call):
        pass

    def send_msg(call: CallbackQuery):
        call.message.edit_text(text="Обновляю")
        print(call.from_user)
#await call.message.edit_text(text=message_w)