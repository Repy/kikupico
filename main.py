import kikupico

# LED点滅
kikupico.led.tick(10)

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

# 現在時刻の取得
now = kikupico.clock.get()

# 気温センサー
tempval = kikupico.sensor.temperature.get()

# 土壌センサー
soilval = kikupico.sensor.soil.get()

# log
kikupico.logging.log(str(now))
kikupico.logging.log(str(tempval))
kikupico.logging.log(str(soilval))

# スリープ
kikupico.clock.sleep(10)

# モーターで水やり
kikupico.equipment.motor.run(6)

# 次回何秒後に実行するか
kikupico.clock.deepsleep(30)
