# -*- coding=utf-8 -*-
# @Time:6/4/2025 上午 11:52
# @Author:席灏铖
# @File:weather_api.PY
# @Software:PyCharm


import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY", "1b71465d8448becc5aacb2e481140af6")
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_weather_data(location):
    """
    获取当前天气
    :param location: 可以是城市名、坐标（lat,lon）等
    :return: dict 包含 location、temperature、description、icon
    """
    url = f"{BASE_URL}/weather"
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh_cn'
    }

    # 如果是坐标形式 location="lat,lon"
    if ',' in location and location.replace('.', '').replace(',', '').replace('-', '').isdigit():
        lat, lon = location.split(',')
        params = {
            'lat': lat.strip(),
            'lon': lon.strip(),
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'zh_cn'
        }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                'location': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            }
        else:
            print(f"[Weather Error] {data}")
            return None
    except Exception as e:
        print(f"[Weather Exception] {e}")
        return None

def get_five_day_forecast(location):
    """
    获取未来五天天气预报（每 3 小时一次，取每天中午的数据）
    :param location: 城市名或坐标
    :return: list of dicts，包含 date、temp、description、icon
    """
    url = f"{BASE_URL}/forecast"
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh_cn'
    }

    # 处理坐标输入
    if ',' in location and location.replace('.', '').replace(',', '').replace('-', '').isdigit():
        lat, lon = location.split(',')
        params = {
            'lat': lat.strip(),
            'lon': lon.strip(),
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'zh_cn'
        }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        forecast_list = []

        if response.status_code == 200:
            seen_dates = set()
            for entry in data['list']:
                date = entry['dt_txt'].split(' ')[0]
                hour = entry['dt_txt'].split(' ')[1]

                # 只取每天中午12点的预报数据
                if hour.startswith("12") and date not in seen_dates:
                    seen_dates.add(date)
                    forecast_list.append({
                        'date': date,
                        'temp': entry['main']['temp'],
                        'description': entry['weather'][0]['description'],
                        'icon': f"http://openweathermap.org/img/wn/{entry['weather'][0]['icon']}@2x.png"
                    })

                if len(forecast_list) == 5:
                    break
            return forecast_list
        else:
            print(f"[Forecast Error] {data}")
            return []
    except Exception as e:
        print(f"[Forecast Exception] {e}")
        return []
