# -*- coding=utf-8 -*-
# @Time:6/4/2025 上午 11:53
# @Author:席灏铖
# @File:export.PY
# @Software:PyCharm


import csv
import json
from fpdf import FPDF
from models import WeatherRecord, db
from pathlib import Path

def export_to_csv():
    file_path = Path("exports/weather_data.csv")
    file_path.parent.mkdir(exist_ok=True)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Location', 'Temperature'])

        for record in WeatherRecord.query.all():
            writer.writerow([record.id, record.location, record.temperature])

    return file_path

def export_to_json():
    file_path = Path("exports/weather_data.json")
    file_path.parent.mkdir(exist_ok=True)

    data = []
    for record in WeatherRecord.query.all():
        data.append({
            'id': record.id,
            'location': record.location,
            'temperature': record.temperature
        })

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return file_path

def export_to_md():
    file_path = Path("exports/weather_data.md")
    file_path.parent.mkdir(exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("# 🌤️ Weather Data (Markdown Export)\n\n")
        f.write("| ID | Location | Temperature (°C) |\n")
        f.write("|----|----------|------------------|\n")
        for record in WeatherRecord.query.all():
            f.write(f"| {record.id} | {record.location} | {record.temperature:.2f} |\n")

    return file_path

def export_to_pdf():
    file_path = Path("exports/weather_data.pdf")
    file_path.parent.mkdir(exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weather Data Export", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", size=10)

    for record in WeatherRecord.query.all():
        line = f"ID: {record.id} | Location: {record.location} | Temperature: {record.temperature:.2f}°C"
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(file_path)
    return file_path
