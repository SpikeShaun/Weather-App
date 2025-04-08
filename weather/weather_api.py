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
    url = f"{BASE_URL}/weather"
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh_cn'
    }

    # 如果是坐标形式 location="lattitude,lontitude"
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
