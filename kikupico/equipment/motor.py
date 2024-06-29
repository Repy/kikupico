import machine
from .. import clock

motor = machine.Pin(16, machine.Pin.OUT)


def on():
    motor.high()


def off():
    motor.low()


def run(sec=0):
    motor.high()
    clock.sleep(sec)
    motor.low()
