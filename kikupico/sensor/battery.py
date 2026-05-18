import machine

# Pico Wでバッテリー電圧(VSYS)を測定するための設定 [1]
# Pin 29をADC入力として使用できるように設定
vsys_pin = machine.Pin(29, machine.Pin.IN)
battery_sensor = machine.ADC(3)

def get():
    """
    バッテリー電圧を一度だけ取得し、電圧値として返します。
    """
    # 1度だけ読み取りを実行
    battery_u16 = battery_sensor.read_u16()
    
    # 電圧に変換する計算式を適用 [1]
    # 計算式: read_u16 * 3 * 3.3 / 65535
    battery_volt = battery_u16 * 3 * 3.3 / 65535
    
    return battery_volt
