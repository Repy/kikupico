import machine
from .. import clock

conversion_factor = 3.3 / 65535
avg_count = 5

def get():
    wet_sensor = machine.ADC(0)
    wet_voltage = 0
    for i in range(avg_count):
        clock.sleep(0.2)
        wet_value = wet_sensor.read_u16()
        wet_voltage += wet_value * conversion_factor
    return wet_voltage / avg_count
