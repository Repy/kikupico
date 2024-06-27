# kikupico

菊潅水装置用ライブラリ

プログラムの一番上に書いて使用しましょう。

```python
import kikupico
```

## 土壌水分センサー

土壌水分センサーの値を取得。

小数で出力される。

```python
# 土壌水分センサー
wet_value = kikupico.sensor.soil.get()
if wet_value > 1.7:
    kikupico.logging.log("パサパサ")
if wet_value < 1.0:
    kikupico.logging.log("べちゃべちゃ")
```

## LED

LEDの点灯/消灯。

目で見える出力はLEDしかないので、ここぞというときに使用する。

```python
# LED ON
kikupico.led.on()
# LED OFF
kikupico.led.off()
# LED 点滅 4回 0.3秒間隔
kikupico.led.tick(4, 0.3)
```

## Wi-Fi

Wi-Fiの接続/切断。

Wi-Fiの接続と切断を行う。Wi-Fi接続の試行中はLEDが0.5秒間隔で点滅する。Wi-Fiは電力消費がとても大きいので使用した後は切断する。

```python
kikupico.wifi.ssid = 'ssid'
kikupico.wifi.key = 'pass'
# wifiの接続
kikupico.wifi.connect()
# wifiの切断
kikupico.wifi.disconnect()
```

## 時刻同期

時刻をサーバーと同期する。

Raspberry Pi Pico Wはシャットダウンすると時刻を失うので、起動時に時刻を同期しないと使えない。ネットワークを使用するのでWi-Fiに接続してから時刻を同期する。

```python
# wifiの接続
kikupico.wifi.connect()
# 時刻の同期
kikupico.clock.init()
# wifiの切断
kikupico.wifi.disconnect()
```

## 時刻取得

時刻を取得。

時刻を取得する前に上記の時刻同期を行わないと取得できない。

```python
# 時刻の取得
now = kikupico.clock.get()
# now.year 年
# now.month 月
# now.date 日
# now.hour 時
# now.minute 分
# now.second 秒
if now.hour == 7:
    kikupico.logging.log("今は7時です")
```

## ログ出力

ログファイルに出力する。

ログファイルはThonnyを使い取り出せる。
Raspberry Pi Pico Wは2MBのストレージで、内1MB強はMicroPythonで使用しているので、500KB程度までしか使えない。

```python
# ログファイルに出力する
kikupico.logging.log("今日は雨の予報なので水をやらない")
```

## 一時停止

一定時間動作を停止する。

電力消費は大きい状態なので、長期間の停止は下記のシャットダウンにすることを推奨する。

```python
# 5秒停止する
kikupico.clock.sleep(5)
```

## シャットダウン

一定時間シャットダウン状態にする。

シャットダウンから復帰後はプログラムの途中からではなく **プログラムの最初から** 実行される。
電力消費を抑えるために動く必要のないときはシャットダウンにすることを推奨する。

```python
# 600秒後までシャットダウンする。
kikupico.clock.deepsleep(600)
```
