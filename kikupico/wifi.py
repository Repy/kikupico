import network
import machine
from . import led
from . import logging

ssid = ""
key = ""

nic = None
wifipin = machine.Pin(23, machine.Pin.OUT)

__retry = 3
__timeout = 15

def connect():
    try:
        wifipin.high()
        nic = network.WLAN(network.STA_IF)
        nic.active(True)
        for i in range(__retry):
            nic.connect(ssid, key)
            for j in range(__timeout):
                led.tick(1, 0.5)
                if nic.status() == network.STAT_GOT_IP:
                    return
        raise Exception("Failed to connect: "+str(nic.status()))
    except Exception as e:
        logging.error(e)

def disconnect():
    try:
        nic.disconnect()
        nic.active(False)
        nic = None
        wifipin.low()
    except Exception as e:
        logging.error(e)
