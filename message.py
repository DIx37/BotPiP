# -- coding: utf-8 --
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from sqllite import SQLighter
from loguru import logger
from modbus import Modbus
import cameraScreen as cs
import LaurentJSON as LJ
import modbusread as MR
import keyboards as kb
import requests
import weather
import config
import utils
import time
import re

class Msg:
    """Работа с протоколом modbus"""
    def __init__(self, call):
        pass

    def send_msg(call: CallbackQuery):
        call.message.edit_text(text="Обновляю")
        print(call.from_user)
#await call.message.edit_text(text=message_w)