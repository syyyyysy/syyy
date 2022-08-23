from datetime import date, datetime, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now() + timedelta(hours=8)
start_date = os.environ['START_DATE']
city = os.environ['CITY']
city2 = os.environ['CITY2']
birthday = os.environ['BIRTHDAY']
birthday2 = os.environ['BIRTHDAY2']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

def get_weather2():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city2
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_wea_war():
  tem_wea,tem_a,tem_b,tem_c=get_weather()
  if str(tem_wea) == "晴":
    return "宝今天天气好，出去记得防晒噢"
  elif str(tem_wea) == "阴":
    return "今天可以出去走走噢宝~"
  else :
    return "今天可能会下雨哎，宝记得带伞呢"

def get_wea_war2():
  tem_wea,tem_a,tem_b,tem_c=get_weather2()
  if str(tem_wea) == "晴":
    return "宝今天天气好，出去记得防晒噢"
  elif str(tem_wea) == "阴":
    return "今天可以出去走走噢宝~"
  else :
    return "今天可能会下雨哎，宝记得带伞呢"

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, highest, lowest = get_weather()
wea2, temperature2, highest2, lowest2 = get_weather2()
now_year = today.year
now_month = today.month
now_day = today.day
data = {"weather_warning":{"value": get_wea_war()},
        "date_D":{"value":now_day},
        "date_M":{"value":now_month},
        "date_Y":{"value":now_year},
        "weather":{"value":wea},
        "temperature":{"value":temperature},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},
        "birthday_left2":{"value":get_birthday2(), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()},
        "highest":{"value":highest, "color":get_random_color()},
        "lowest":{"value":lowest,"color":get_random_color()}
        }

data2 = {"weather_warning":{"value": get_wea_war2()},
        "date_D":{"value":now_day},
        "date_M":{"value":now_month},
        "date_Y":{"value":now_year},
        "weather":{"value":wea2},
        "temperature":{"value":temperature2},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},
        "birthday_left2":{"value":get_birthday2(), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()},
        "highest":{"value":highest2, "color":get_random_color()},
        "lowest":{"value":lowest2,"color":get_random_color()}
        }


res = wm.send_template(user_ids[0], template_id, data)
res = wm.send_template(user_ids[1], template_id, data2)

