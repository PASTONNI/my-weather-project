import os
from dotenv import load_dotenv

load_dotenv()

url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,apparent_temperature,wind_speed_10m,precipitation,weather_code&models=icon_seamless&timezone=Europe%2FBerlin&forecast_days=1'  # noqa: E501

bucket_name = "my-weather-pipeline-bucket"
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Weather codes created from the open meteo website
weather_codes = {
    'code': [0, 1, 2, 3, 45, 48, 51, 53, 55, 61, 63, 65, 71, 73, 75, 80, 81, 82, 95, 96, 99],  # noqa: E501
    'description': ['Clear sky', 'Mainly clear', 'Partly cloudy', 'Overcast', 'Foggy', 'Icy fog', 'Light drizzle', 'Moderate drizzle', 'Dense drizzle', 'Slight rain', 'Moderate rain', 'Heavy rain', 'Slight snow', 'Moderate snow', 'Heavy snow', 'Slight showers', 'Moderate showers', 'Heavy showers', 'Thunderstorm', 'Thunderstorm with hail', 'Thunderstorm with heavy hail']  # noqa: E501
}

notification_recipient = os.getenv("NOTIFICATION_RECIPIENT")
