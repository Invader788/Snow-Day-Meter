
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

LATITUDE = 44.05
LONGITUDE = -79.46


def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": (
            "temperature_2m,"
            "snowfall,"
            "wind_speed_10m,"
            "precipitation_probability,"
            "freezing_rain_probability"
        ),
        "timezone": "America/Toronto",
        "forecast_days": 3
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()
    hourly = data["hourly"]

    tomorrow = (
        datetime.now(ZoneInfo("America/Toronto")).date()
        + timedelta(days=1)
    )

    morning = []

    for i, timestamp in enumerate(hourly["time"]):
        forecast_time = datetime.fromisoformat(timestamp)

        if (
            forecast_time.date() == tomorrow
            and 0 <= forecast_time.hour <= 9
        ):
            morning.append(i)

    if not morning:
        raise ValueError("No forecast data for tomorrow morning")

    def valid_values(key):
        return [
            hourly[key][i]
            for i in morning
            if hourly[key][i] is not None
        ]

    snowfall_values = valid_values("snowfall")
    temperature_values = valid_values("temperature_2m")
    wind_values = valid_values("wind_speed_10m")
    freezing_values = valid_values("freezing_rain_probability")
    precipitation_values = valid_values("precipitation_probability")

    if not temperature_values or not snowfall_values or not wind_values:
        raise ValueError("Essential weather data is missing")

    snowfall = sum(snowfall_values)
    temperature = min(temperature_values)
    wind = max(wind_values)

    freezing_rain = max(freezing_values) if freezing_values else 0
    precipitation = max(precipitation_values) if precipitation_values else 0

    return {
        "snowfall": round(snowfall, 1),
        "temperature": round(temperature, 1),
        "wind": round(wind, 1),
        "precipitation": precipitation,
        "freezing_rain": freezing_rain
    }

