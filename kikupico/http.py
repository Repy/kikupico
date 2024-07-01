import urequests
import ujson

def get_json(url):
    res = urequests.get(url)
    ret = res.json()
    res.close()
    return ret

def post_json(url, json):
    res = urequests.post(url, data = ujson.dumps(json))
    ret = res.json()
    res.close()
    return ret
