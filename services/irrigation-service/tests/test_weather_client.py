import json
from datetime import datetime, timedelta

from src.weather_client import WeatherClient


class FakeRedis:
    def __init__(self) -> None:
        self.store = {}

    def setex(self, key, _ttl, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)


def test_weather_fallback_to_cache() -> None:
    client = WeatherClient(api_key="", redis_host="localhost", redis_port=6379)
    client.redis = FakeRedis()

    payload = {
        "rain_mm": 7.5,
        "ts": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
    }
    client.redis.setex("weather:Sao Paulo,BR", 1800, json.dumps(payload))

    rain = client.fetch_forecast_mm("Sao Paulo,BR")
    assert rain == 7.5
