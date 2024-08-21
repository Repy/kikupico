import network
import machine
from . import led
from . import logging
from . import clock

ssid = ""
key = ""

nic = network.WLAN(network.STA_IF)
wifipin = machine.Pin(23, machine.Pin.OUT)

__retry = 3
__timeout = 15


def connect():
    try:
        for i in range(__retry):
            wifipin.high()
            nic.active(True)
            nic.connect(ssid, key)
            for j in range(__timeout):
                led.tick(1, 0.5)
                if nic.status() == network.STAT_GOT_IP:
                    return
            nic.disconnect()
            nic.active(False)
            wifipin.low()
            led.tick(1, 0.5)
        raise Exception("Failed to connect: " + str(nic.status()))
    except Exception as e:
        logging.error(e)


def disconnect():
    try:
        nic.disconnect()
        nic.active(False)
        wifipin.low()
    except Exception as e:
        logging.error(e)
