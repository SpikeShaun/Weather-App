# -*- coding=utf-8 -*-
# @Time:6/4/2025 上午 11:51
# @Author:席灏铖
# @File:app.PY
# @Software:PyCharm


from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from export import export_to_csv, export_to_pdf, export_to_md, export_to_json
from weather_api import get_weather_data, get_five_day_forecast
from models import db, WeatherRecord
from youtube_api import search_youtube_videos
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast = None
    error = request.args.get('error')

    location = request.args.get('location')
    if request.method == 'POST':
        location = request.form.get('location')

    if location:
        weather_data = get_weather_data(location)
        forecast = get_five_day_forecast(location)

        if weather_data and request.method == 'POST':
            record = WeatherRecord(location=location, temperature=weather_data['temperature'])
            db.session.add(record)
            db.session.commit()
        elif not weather_data:
            error = "The location was not found or the API response error."

    # records = WeatherRecord.query.all()
    # 限制只展示10条历史记录
    records = WeatherRecord.query.order_by(WeatherRecord.id.desc()).limit(10).all()
    return render_template("index.html", weather_data=weather_data, forecast=forecast, records=records, error=error)

@app.route('/gps')
def gps():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return "parameters-are-missing", 400

    try:
        location = f"{lat},{lon}"
        weather_data = get_weather_data(location)
        if weather_data:
            record = WeatherRecord(location=weather_data['location'], temperature=weather_data['temperature'])
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('index', location=weather_data['location']))
        else:
            return redirect(url_for('index', error="Location failed, weather service was unresponsive"))
    except Exception as e:
        print(f"GPS错误: {e}")
        return redirect(url_for('index', error="Positioning failed"))

    # # # YouTube 视频接口（可用于 AJAX）
    # # @app.route('/videos')
    # # def videos():
    # #     location = request.args.get('location')
    # #     if not location:
    # #         return jsonify({"error": "缺少地点参数"}), 400
    # #     try:
    # #         results = search_youtube_videos(location)
    # #         return jsonify(results)
    # #     except Exception as e:
    # #         return jsonify({"error": str(e)}), 500
    #
    #

@app.route('/export/<fmt>')
def export_format(fmt):
    if fmt == 'csv':
        path = export_to_csv()
    elif fmt == 'pdf':
        path = export_to_pdf()
    elif fmt == 'md':
        path = export_to_md()
    elif fmt == 'json':
        path = export_to_json()
    else:
        return "Unsupported formats", 400
    return send_file(path, as_attachment=True)

@app.route('/delete/<int:record_id>')
def delete(record_id):
    record = WeatherRecord.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:record_id>', methods=['POST'])
def update(record_id):
    new_temp = request.form.get('new_temperature')
    try:
        new_temp = float(new_temp)
        record = WeatherRecord.query.get(record_id)
        if record:
            record.temperature = new_temp
            db.session.commit()
    except ValueError:
        pass
    return redirect(url_for('index'))

def get_api_key():
    return os.getenv("OPENWEATHER_API_KEY", "1b71465d8448becc5aacb2e481140af6")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()  # run_with_ngrok 会自动添加 host/port















# from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
# from flask_sqlalchemy import SQLAlchemy
# import requests
# from export import export_to_csv, export_to_pdf, export_to_md, export_to_json
# from weather_api import get_weather_data, get_five_day_forecast
# from models import db, WeatherRecord
# from youtube_api import search_youtube_videos  # 👈 新增引入
#
# import os
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # db = SQLAlchemy(app)
# db.init_app(app)  # 这句必须加上，告知 models 使用的 app 实例
# # 数据模型
# # 首页路由
# # @app.route('/', methods=['GET', 'POST'])
# # def index():
# #     weather_data = None
# #     forecast = None
# #     error = request.args.get('error')
# #     youtube_videos = []  # ✅ 初始化视频变量
# #
# #     location = request.args.get('location')  # 支持 /gps 跳转传参
# #     if request.method == 'POST':
# #         location = request.form.get('location')
# #
# #     if location:
# #         weather_data = get_weather_data(location)
# #         forecast = get_five_day_forecast(location)
# #         youtube_videos = search_youtube_videos(location)  # ✅ 获取对应视频列表
# #
# #         if weather_data and request.method == 'POST':
# #             record = WeatherRecord(location=location, temperature=weather_data['temperature'])
# #             db.session.add(record)
# #             db.session.commit()
# #         elif not weather_data:
# #             error = "未找到该位置或API响应错误。"
# #
# #     records = WeatherRecord.query.all()
# #     return render_template("index.html",
# #                            weather_data=weather_data,
# #                            forecast=forecast,
# #                            records=records,
# #                            error=error,
# #                            youtube_videos=youtube_videos)  # ✅ 传入视频内容
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     weather_data = None
#     forecast = None
#     error = request.args.get('error')
#
#     location = request.args.get('location')  # 👉 接收从 /gps 跳转来的 location
#     if request.method == 'POST':
#         location = request.form.get('location')
#
#     if location:
#         weather_data = get_weather_data(location)
#         forecast = get_five_day_forecast(location)
#
#         if weather_data and request.method == 'POST':
#             record = WeatherRecord(location=location, temperature=weather_data['temperature'])
#             db.session.add(record)
#             db.session.commit()
#         elif not weather_data:
#             error = "未找到该位置或API响应错误。"
#
#     records = WeatherRecord.query.all()
#     return render_template("index.html", weather_data=weather_data, forecast=forecast, records=records, error=error)
#
#
# # GPS查询
# @app.route('/gps')
# def gps():
#     lat = request.args.get('lat')
#     lon = request.args.get('lon')
#     if not lat or not lon:
#         return "参数缺失", 400
#
#     try:
#         location = f"{lat},{lon}"
#         weather_data = get_weather_data(location)
#         if weather_data:
#             record = WeatherRecord(location=weather_data['location'], temperature=weather_data['temperature'])
#             db.session.add(record)
#             db.session.commit()
#             # 👇 用重定向，把城市名带回首页
#             return redirect(url_for('index', location=weather_data['location']))
#         else:
#             return redirect(url_for('index', error="定位失败，天气服务无响应"))
#     except Exception as e:
#         print(f"GPS错误: {e}")
#         return redirect(url_for('index', error="定位失败"))
#
#

# # 导出数据
# @app.route('/export/<fmt>')
# def export_format(fmt):
#     if fmt == 'csv':
#         path = export_to_csv()
#     elif fmt == 'pdf':
#         path = export_to_pdf()
#     elif fmt == 'md':
#         path = export_to_md()
#     elif fmt == 'json':
#         path = export_to_json()
#     else:
#         return "不支持的格式", 400
#     return send_file(path, as_attachment=True)
#
# # 删除记录
# @app.route('/delete/<int:record_id>')
# def delete(record_id):
#     record = WeatherRecord.query.get(record_id)
#     if record:
#         db.session.delete(record)
#         db.session.commit()
#     return redirect(url_for('index'))
#
# # 更新温度记录
# @app.route('/update/<int:record_id>', methods=['POST'])
# def update(record_id):
#     new_temp = request.form.get('new_temperature')
#     try:
#         new_temp = float(new_temp)
#         record = WeatherRecord.query.get(record_id)
#         if record:
#             record.temperature = new_temp
#             db.session.commit()
#     except ValueError:
#         pass
#     return redirect(url_for('index'))
#
# # 获取 OpenWeatherMap API 密钥
# def get_api_key():
#     return os.getenv("OPENWEATHER_API_KEY", "1b71465d8448becc5aacb2e481140af6")
#
# # 启动应用
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # 确保数据库表已创建
#     app.run(host='0.0.0.0',port=5000,debug=True)
#
