from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=" + city
  res = requests.get(url).json()
  weather = res['today']

  return weather['weatherEnd'], math.floor(weather['tempMax']), math.floor(weather['tempMin']), weather["date"]

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_dujitang():
  words = requests.get("https://api.shadiao.pro/du")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_pengyouquan():
  words = requests.get("https://api.shadiao.pro/pyq")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color

random_color = generate_random_color()

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, min_temperature, current_date = get_weather()

love_days = (today -datetime.strptime("2024-2-16", "%Y-%m-%d")).days
data = {
  "date": {"value": current_date, "color": random_color},
  "city": {"value": "北京 昌平", "color": random_color},
  "weather":{"value":wea, "color": generate_random_color()},
  "temperature":{"value":temperature, "color": "#fc5531"},
  "min_temperature":{"value":min_temperature, "color": "#388bfd"},
  "love_days":{"value": love_days, "color": generate_random_color()},
  "birthday_left":{"value": get_birthday(), "color": generate_random_color()},
  "words":{"value":get_words(), "color": generate_random_color()},
  "dujitang":{"value":get_dujitang(), "color": generate_random_color()},
  "pengyouquan":{"value":get_pengyouquan(), "color": generate_random_color()},
}
res = wm.send_template(user_id, template_id, data)
print(res)
