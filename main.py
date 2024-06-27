import kikupico

# LED点滅
kikupico.led.tick(10)
kikupico.led.tick(3, 1)

# LED点灯消灯
kikupico.led.on()
kikupico.clock.sleep(1)
kikupico.led.off()

# wifiの接続
kikupico.wifi.connect()
# 時刻の同期
kikupico.clock.init()
# wifiの切断
kikupico.wifi.disconnect()

kikupico.led.tick(10, 0.2)

# 土壌センサー
val = kikupico.sensor.soil.get()

# log
kikupico.logging.log(str(kikupico.clock.get()))
kikupico.logging.log(str(val))

# スリープ
kikupico.clock.sleep(10)

# 次回何秒後に実行するか
kikupico.clock.deepsleep(30)
