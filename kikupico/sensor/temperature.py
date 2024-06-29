import machine
import time
import ustruct
import micropython
class Temperature:
    def __init__(self, temperature, pressure, humidity):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

class CalibrationData:
    def __init__(self, data88, dataE1):
        (self.t1, self.t2, self.t3) = ustruct.unpack("<Hhh", data88[0:6])
        (self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.p9) = ustruct.unpack("<Hhhhhhhhh", data88[6:24])
        (self.h1) = ustruct.unpack("<B", data88[25:26])
        (self.h2, self.h3) = ustruct.unpack("<hB", data88[0:3])
        (h4,) = ustruct.unpack("<b", data88[3:4])
        self.h4 = (h4 << 4) | (data88[4] & 0xF)
        (h5,) = ustruct.unpack("<b", data88[5:6])
        self.h5 = (h5 << 4) | (data88[4] >> 4)
        (self.h6) = ustruct.unpack("<b", dataE1[6:7])

    def compensate_temperature(self, adc_T, adc_P, adc_H):

        var1 = ((((adc_T >> 3) - (self.t1 << 1))) * (self.t2)) >> 11
        var2 = (((((adc_T >> 4) - (self.t1)) * ((adc_T >> 4) - (self.t1))) >> 12) * (self.t3)) >> 14
        t_fine = var1 + var2
        T = (t_fine * 5 + 128) >> 8
    

        var1 = t_fine - 128000
        var2 = var1 * var1 * self.p6
        var2 = var2 + ((var1 * self.p5) << 17)
        var2 = var2 + ((self.p4) << 35)
        var1 = ((var1 * var1 * self.p3) >> 8) + ((var1 * self.p2) << 12)
        var1 = ((((1) << 47) + var1)) * (self.p1) >> 33
        if (var1 != 0):
            p = 1048576 - adc_P
            p = (((p << 31) - var2) * 3125) // var1
            var1 = ((self.p9) * (p >> 13) * (p >> 13)) >> 25
            var2 = ((self.p8) * p) >> 19
            p = ((p + var1 + var2) >> 8) + ((self.p7) << 4)

        micropython.mem_info()
        v_x1_u32r = (t_fine - 76800)
        v_x1_u32r = (((((adc_H << 14) - ((self.h4) << 20) - ((self.h5) * v_x1_u32r)) + (16384)) >> 15) * (((((((v_x1_u32r * (self.h6)) >> 10) * (((v_x1_u32r * (self.h3)) >> 11) + (32768))) >> 10) + (2097152)) * (self.h2) + 8192) >> 14))
        micropython.mem_info()

        v_x1_u32r = (v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * (self.h1)) >> 4))
        if v_x1_u32r < 0:
            v_x1_u32r = 0
        if v_x1_u32r > 419430400:
            v_x1_u32r = 419430400
        H = v_x1_u32r >> 12

        return Temperature(T / 100, p / 256 / 100, H / 1024)
        # return Temperature(T / 100, p / 256 / 100, 0)

class TemperatureSensor:
    def __init__(self):
        self.spi = machine.SPI(
            0,
            baudrate=9600,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=machine.SPI.MSB,
            sck=machine.Pin(18),
            miso=machine.Pin(16),
            mosi=machine.Pin(19),
        )
        self.cs = machine.Pin(17, machine.Pin.OUT)
        self.cs.high()
        self.__set_over_sampling(OVER_SAMPLING_1, OVER_SAMPLING_1, OVER_SAMPLING_1)
        data88 = self.__read_bytes(0x88, 26)
        dataE1 = self.__read_bytes(0xE1, 7)
        self.calibration_data = CalibrationData(data88, dataE1)

    def __read_bytes(self, address, len):
        self.cs.low()
        self.spi.write(bytes([address]))
        data = self.spi.read(len)
        self.cs.high()
        return data

    def __read_byte(self, address):
        bys = self.__read_bytes(address, 1)
        return bys[0]

    def __write_byte(self, address, data):
        write_address = address & 0x7F
        self.cs.low()
        self.spi.write(bytes([write_address, data]))
        self.cs.high()

    def __get_status(self):
        data = self.__read_byte(0xFC)
        status = data & 0x04
        if status == 0:
            return False
        return True

    def __get_mode(self):
        data = self.__read_byte(0xF4)
        mode = data & 0x03
        return mode

    def __set_over_sampling(self, temperature, pressure, humidity):
        data = self.__read_byte(0xF4)
        data = data & 0x03
        data = data | (temperature << 5) | (pressure << 2)
        self.__write_byte(0xF4, data)
        data = self.__read_byte(0xF2)
        data = data & 0xF8
        data = data | humidity
        self.__write_byte(0xF2, data)

    def __set_mode(self, mode):
        data = self.__read_byte(0xF4)
        data = data & 0xFC
        data = data | mode
        self.__write_byte(0xF4, data)


    def get(self):
        self.__set_mode(MODE_ONETIME)
        while self.__get_status():
            time.sleep(0.1)            
        data = self.__read_bytes(0xF7, 8)
        press_raw = self.__byte3(data[0:3])
        temp_raw = self.__byte3(data[3:6])
        humi_raw = (data[6] << 8) | data[7]
        return self.calibration_data.compensate_temperature(temp_raw, press_raw, humi_raw)

    def __byte3(self, data):
        data_msb = data[0] << 12
        data_lsb = data[1] << 4
        data_xlsb = data[2] >> 0
        return data_msb | data_lsb | data_xlsb

MODE_SLEEP = 0x00
MODE_NORMAL = 0x03
MODE_ONETIME = 0x01

OVER_SAMPLING_SKIP = 0x00
OVER_SAMPLING_1 = 0x01
OVER_SAMPLING_2 = 0x02
OVER_SAMPLING_4 = 0x03
OVER_SAMPLING_8 = 0x04
OVER_SAMPLING_16 = 0x05
