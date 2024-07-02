import ntptime
import machine
import time
from . import logging

ntptime.host = "ntp.nict.jp"


class Time:
    year = 2020
    month = 12
    date = 31
    hour = 23
    minute = 58
    second = 59

    def __str__(self):
        return "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
            self.year, self.month, self.date, self.hour, self.minute, self.second
        )


def init():
    try:
        ntptime.settime()
    except Exception as e:
        logging.error(e)


def get():
    now = time.localtime(time.mktime(time.localtime()) + 9 * 60 * 60)  # type: ignore
    t = Time()
    t.year = now[0]
    t.month = now[1]
    t.date = now[2]
    t.hour = now[3]
    t.minute = now[4]
    t.second = now[5]
    return t


def sleep(sec):
    time.sleep(sec)


def deepsleep(sec):
    machine.deepsleep(int(sec * 1000))
