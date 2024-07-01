# 各種Webデータを取得する

## 気象庁の降水量データの取得

気象庁の降水量データの取得

気象庁のアメダスのAPIはJSONで配信されているので取得しやすい。

- https://www.jma.go.jp/bosai/amedas/#amdno=40191&area_type=offices&area_code=080000&format=table1h&elems=53400
- ここに表示されるデータを取得する
- https://www.jma.go.jp/bosai/amedas/data/point/40191/20240628_15.json
- 笠間のアメダスのIDは40191
- 2024/06/28 15～18時のデータは、20240628_15.json
- 2024/06/28 16:00:00のデータは、20240628160000
- 前1時間の降水量のデータは、precipitation1h
- 前1時間以外にも温度や湿度などのデータがあるのでJSONの中身を見て選ぼう。

```python
# 2024/06/28 15～18時のデータ
res = kikupico.http.get_json("https://www.jma.go.jp/bosai/amedas/data/point/40191/20240628_15.json")
value = res["20240628160000"]["precipitation1h"][0]
```

## 気象庁の天気予報の取得

気象庁の天気予報の取得

天気予報のAPIは少し構造が特殊で使いにくい。

- https://www.jma.go.jp/bosai/forecast/#area_type=class20s&area_code=0821600
- ここに表示されるデータを取得する
- https://www.jma.go.jp/bosai/forecast/data/forecast/080000.json
- 茨城県のIDは080000
- res[0]は直近の天気予報、res[1]は週間天気が取得可能

```python
# 予想降水確率
res = kikupico.http.get_json("https://www.jma.go.jp/bosai/amedas/data/point/40191/20240628_15.json")
time = res[1]["timeSeries"][1]["timeDefines"][0]
data = res[1]["timeSeries"][1]["areas"][0]["pops"][0]
```

## 気象庁の天気予報を簡単なJSONに変換してくれるサービスから取得

気象庁の予報APIは使いにくいのでそれを使いやすいJSONにしてくれているサービス

- https://weather.tsukumijima.net/api/forecast/city/080010
- 茨城県北部のIDは080010
- res["forecasts"][0]は今日、res["forecasts"][1]は明日
- "chanceOfRain"は降水確率
- "T18_24"は18時～24時

```python
# 今日の
res = kikupico.http.get_json("https://www.jma.go.jp/bosai/amedas/data/point/40191/20240628_15.json")
value = res["forecasts"][0]["chanceOfRain"]["T18_24"]
```
