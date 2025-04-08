# -*- coding=utf-8 -*-
# @Time:6/4/2025 上午 11:52
# @Author:席灏铖
# @File:models.PY
# @Software:PyCharm


from flask_sqlalchemy import SQLAlchemy


# 使用的是 SQLAlchemy + SQLite 作为数据库后端

# 不初始化 app
db = SQLAlchemy()

class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<WeatherRecord {self.location} - {self.temperature}°C>"
