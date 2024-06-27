import network
import machine
from . import led

ssid = ""
key = ""

nic = network.WLAN(network.STA_IF)

def connect():
    machine.Pin(23, machine.Pin.OUT).high()
    nic.active(True)
    nic.connect(ssid, key)
    while not nic.isconnected() and nic.status() >= 0:
        led.tick(1, 0.5)
    
def disconnect():
    nic.disconnect()
    nic.active(False)
    machine.Pin(23, machine.Pin.OUT).low()
