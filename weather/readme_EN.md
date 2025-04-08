## Overview

This project is a backend implementation for a weather application, primarily managed through the `app.py` file. It handles all request routing, API calls, database operations, and data export functionalities. The project is built using the Flask framework and utilizes SQLAlchemy for ORM-based data management.

## Dependencies

```python
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
```

- **Flask**: Used to create the backend web application.
- **render_template**: For rendering frontend templates.
- **request**: To handle GET and POST request parameters.
- **redirect, url_for**: For implementing page redirection.
- **send_file**: For file export functionality.
- **jsonify**: To convert data structures to JSON format for API responses.

## Additional Modules

```python
from export import export_to_csv, export_to_pdf, export_to_md, export_to_json
from weather_api import get_weather_data, get_five_day_forecast
from models import db, WeatherRecord
from youtube_api import search_youtube_videos
```

- **export.py**: Contains logic for exporting data in CSV, PDF, Markdown, and JSON formats.
- **weather_api.py**: Encapsulates interactions with the OpenWeatherMap API.
- **models.py**: Defines the database schema.
- **youtube_api.py**: Interfaces with the YouTube Data API v3.

## Flask Application Configuration and Database Initialization

```python
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
```

- A Flask application instance is created.
- The SQLite database file is configured to be `weather.db`.
- Modification tracking is disabled to reduce resource consumption.

## Routes and Functionalities

### Home Page (`/`): Weather Query and History Display

```python
@app.route('/', methods=['GET', 'POST'])
def index():
```

- Handles both GET and POST requests for the home page.
- Retrieves the location (city or coordinates) from URL parameters or form data.
- Calls `get_weather_data()` to fetch current weather and `get_five_day_forecast()` for the five-day forecast.
- If successful, the weather data is stored in the database (only for POST requests).
- Displays the latest 10 historical records using `WeatherRecord.query.order_by(...).limit(10)`.

### GPS-Based Weather Query (`/gps`)

```python
@app.route('/gps')
def gps():
```

- Retrieves latitude and longitude from request parameters.
- Constructs a location query string and fetches weather data using `get_weather_data()`.
- Stores the city and temperature in the database and redirects to the home page.
- Includes error handling for missing parameters, failed location detection, and API errors.

### Data Export (`/export/<fmt>`)

```python
@app.route('/export/<fmt>')
def export_format(fmt):
```

- Supports exporting historical query records in four formats: CSV, PDF, Markdown, and JSON.
- The specific export logic is implemented in `export.py`.
- The file is returned as an attachment using `send_file()`.

### Delete a Record (`/delete/<int:record_id>`)

```python
@app.route('/delete/<int:record_id>')
def delete(record_id):
```

- Deletes a historical record based on its primary key ID.
- Redirects back to the home page after deletion.

### Update Temperature (`/update/<int:record_id>`)

```python
@app.route('/update/<int:record_id>', methods=['POST'])
def update(record_id):
```

- Retrieves the new temperature value from the form field `new_temperature`.
- Updates the corresponding database record if the value is valid.
- Redirects back to the home page after submission.

## Obtaining OpenWeather API Key

```python
def get_api_key():
    return os.getenv("OPENWEATHER_API_KEY", "1b71465d8448becc5aacb2e481140af6")
```

- Retrieves the API key from environment variables for security during deployment.
- Uses a default embedded key if no environment variable is set.

## Application Entry Point

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
```

- Initializes the database by creating the table structure.
- Starts the Flask application.
- For ngrok integration, use `run_with_ngrok` to start the application.

## Summary of Routes

| Route                | Method | Description                              |
|----------------------|--------|------------------------------------------|
| `/`                  | GET/POST | Query weather and display history       |
| `/gps`               | GET    | Fetch weather by GPS coordinates         |
| `/export/<fmt>`      | GET    | Export query records in various formats  |
| `/delete/<id>`       | GET    | Delete a historical record               |
| `/update/<id>`       | POST   | Update temperature information           |

## Tips and Best Practices

- **Request Handling**: Use `request.args` for GET parameters and `request.form` for POST form data.
- **Database Operations**: Utilize SQLAlchemy ORM for simplified CRUD operations and avoid raw SQL queries.
- **Redirection**: Use `redirect` and `url_for` for elegant URL redirection without hardcoding.
- **File Export**: Implement file downloads using `send_file`.
- **Performance Optimization**: Use `limit()` to control the number of records displayed, enhancing performance and UI cleanliness.

## Additional Information

## Additional Information

### run_with_ngrok.py

This script is designed to expose the Flask application to the public internet using ngrok, a tool that creates secure tunnels to localhost. This is particularly useful for testing and demonstrating the application without deploying it to a public server.

#### Script Structure

```python
from flask import Flask
from pyngrok import ngrok
from app import app
```

- **Flask**: The core web framework used in this project.
- **pyngrok**: A Python wrapper for ngrok that simplifies the process of creating tunnels.
- **app**: The Flask application instance imported from `app.py`.

#### Main Function

```python
def main():
    public_url = ngrok.connect(5000)
    print(" * The ngrok tunnel is enabled, and the public IP address:", public_url)
    app.run(debug=True, use_reloader=False)
```

1. **ngrok.connect(5000)**: Establishes an ngrok tunnel that maps the local port `5000` to a public URL. This URL can be accessed from any network.
2. **Print Public URL**: Displays the public URL in the console, making it easy to access the application.
3. **app.run()**: Starts the Flask development server. The `use_reloader=False` argument prevents the server from reloading automatically, which can cause issues with ngrok.

#### Usage

1. **Install ngrok**: Download and install ngrok from the [official website](https://ngrok.com/download).
2. **Install pyngrok**: Run `pip install pyngrok` to install the Python wrapper.
3. **Set ngrok Auth Token**: If you have an ngrok account, set your auth token using `ngrok config add-authtoken <your-ngrok-token>`. This is required for using ngrok's features.
4. **Start the Script**: Run `python run_with_ngrok.py` to start the Flask application with ngrok enabled.

#### Security Note

- The public URL generated by ngrok is temporary and changes on each restart. For a persistent URL, consider upgrading to a paid ngrok plan that supports custom subdomains.
- Be cautious about exposing sensitive endpoints or debug information over the public internet.

### weather_api.py

This module encapsulates the interaction with the OpenWeatherMap API, providing two primary functions: fetching current weather data and retrieving five-day weather forecasts.

#### Configuration

```python
API_KEY = os.getenv("OPENWEATHER_API_KEY", "1b71465d8448becc5aacb2e481140af6")
BASE_URL = "https://api.openweathermap.org/data/2.5"
```

- **API_KEY**: The API key for accessing OpenWeatherMap. It is retrieved from environment variables for security reasons, with a fallback to a default key if not set.
- **BASE_URL**: The base URL for OpenWeatherMap API requests.

#### Functions

1. **get_weather_data(location)**

   - **Purpose**: Fetches the current weather data for a given location.
   - **Parameters**: 
     - `location`: Can be a city name (e.g., "Beijing") or a coordinate string (e.g., "39.90,116.40").
   - **Return**: 
     - A dictionary containing the location, temperature, weather description, and icon URL if successful.
     - `None` if the request fails.
   - **Implementation**: 
     - Detects whether the input is a coordinate string and adjusts the API request parameters accordingly.
     - Uses the `lang=zh_cn` parameter to retrieve weather descriptions in Chinese.
     - Handles API errors gracefully by catching exceptions and logging errors.

2. **get_five_day_forecast(location)**

   - **Purpose**: Retrieves the five-day weather forecast for a given location.
   - **Parameters**: 
     - `location`: Same as above.
   - **Return**: 
     - A list of dictionaries, each representing a day's forecast with date, temperature, description, and icon URL.
     - An empty list if the request fails.
   - **Implementation**: 
     - Fetches the full five-day forecast from OpenWeatherMap, which includes data for every three hours.
     - Filters the results to include only the forecasts for 12:00 PM each day.
     - Ensures that only one entry per day is included by using a set to track seen dates.

#### Example Usage

```python
current_weather = get_weather_data("Beijing")
print(current_weather)
# Output:
# {
#     'location': 'Beijing',
#     'temperature': 26.3,
#     'description': '多云',
#     'icon': 'http://openweathermap.org/img/wn/04d@2x.png'
# }

five_day_forecast = get_five_day_forecast("Beijing")
print(five_day_forecast)
# Output:
# [
#     {
#         'date': '2025-04-08',
#         'temp': 25.0,
#         'description': '小雨',
#         'icon': 'http://openweathermap.org/img/wn/10d@2x.png'
#     },
#     ...
# ]
```

### models.py

This module defines the database schema using SQLAlchemy, which is used to store weather records queried by users.

#### Database Initialization

```python
db = SQLAlchemy()
```

- The `SQLAlchemy` instance is created without binding to an application. This allows for more flexible application structure and easier integration with Flask.

#### WeatherRecord Model

```python
class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
```

- **id**: A unique identifier for each record, set as the primary key.
- **location**: The location for which the weather was queried. This can be a city name or GPS coordinates.
- **temperature**: The temperature recorded at the time of the query.

#### Representation Method

```python
def __repr__(self):
    return f"<WeatherRecord {self.location} - {self.temperature}°C>"
```

- This method provides a human-readable representation of each record, which is useful for debugging and logging.

#### Example Operations

- **Create a Record**:
  ```python
  record = WeatherRecord(location="Shanghai", temperature=23.5)
  db.session.add(record)
  db.session.commit()
  ```

- **Retrieve Records**:
  ```python
  all_records = WeatherRecord.query.all()
  latest_records = WeatherRecord.query.order_by(WeatherRecord.id.desc()).limit(10).all()
  ```

- **Delete a Record**:
  ```python
  record_to_delete = WeatherRecord.query.get(3)
  db.session.delete(record_to_delete)
  db.session.commit()
  ```

- **Update a Record**:
  ```python
  record_to_update = WeatherRecord.query.get(2)
  record_to_update.temperature = 29.9
  db.session.commit()
  ```

### export.py

This module provides functionality to export weather records stored in the database into various formats, including CSV, JSON, Markdown, and PDF.

#### Dependencies

```python
import csv
import json
from fpdf import FPDF
from pathlib import Path
from models import WeatherRecord
```

- **csv**: For writing CSV files.
- **json**: For writing JSON files.
- **FPDF**: For generating PDF documents.
- **Path**: For handling file paths in a cross-platform manner.
- **WeatherRecord**: The database model for weather records.

#### Export Functions

1. **export_to_csv()**

   - **Purpose**: Exports all weather records to a CSV file.
   - **Output**: A CSV file named `weather_data.csv` in the `exports/` directory.
   - **Content**:
     ```
     ID,Location,Temperature
     1,Beijing,26.5
     2,Shanghai,29.0
     ```

2. **export_to_json()**

   - **Purpose**: Exports all weather records to a JSON file.
   - **Output**: A JSON file named `weather_data.json` in the `exports/` directory.
   - **Content**:
     ```json
     [
         {
             "id": 1,
             "location": "Beijing",
             "temperature": 26.5
         },
         ...
     ]
     ```

3. **export_to_md()**

   - **Purpose**: Exports all weather records to a Markdown table.
   - **Output**: A Markdown file named `weather_data.md` in the `exports/` directory.
   - **Content**:
     ```markdown
     # Weather Data Export

     | ID | Location | Temperature (°C) |
     |----|----------|------------------|
     | 1  | Beijing  | 26.50            |
     | 2  | Tokyo    | 30.20            |
     ```

4. **export_to_pdf()**

   - **Purpose**: Exports all weather records to a PDF document.
   - **Output**: A PDF file named `weather_data.pdf` in the `exports/` directory.
   - **Content**:
     ```
     Weather Data Export

     ID: 1 | Location: Beijing | Temperature: 26.50°C
     ID: 2 | Location: Tokyo   | Temperature: 30.20°C
     ```

#### Example Usage in Flask

```python
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
    return send_file(path, as_attachment=True)
```

This route in `app.py` allows users to download weather records in their preferred format by accessing `/export/<fmt>`, where `<fmt>` can be `csv`, `pdf`, `md`, or `json`.

### Summary

- **run_with_ngrok.py**: Exposes the Flask application to the public internet using ngrok.
- **weather_api.py**: Interacts with the OpenWeatherMap API to fetch current weather data and five-day forecasts.
- **models.py**: Defines the database schema using SQLAlchemy to store weather records.
- **export.py**: Provides functionality to export weather records in various formats (CSV, JSON, Markdown, PDF).