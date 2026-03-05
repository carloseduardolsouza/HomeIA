from __future__ import annotations

from datetime import datetime, timedelta
import json

import redis
import requests


class WeatherClient:
    def __init__(self, api_key: str, redis_host: str, redis_port: int) -> None:
        self.api_key = api_key
        self.redis = redis.Redis(
            host=redis_host, port=redis_port, decode_responses=True
        )

    def _cache_key(self, city: str) -> str:
        return f"weather:{city}"

    def fetch_forecast_mm(self, city: str) -> float:
        key = self._cache_key(city)

        if self.api_key:
            try:
                url = "https://api.openweathermap.org/data/2.5/forecast"
                params = {"q": city, "appid": self.api_key, "units": "metric"}
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    rain_mm = 0.0
                    for item in data.get("list", [])[:8]:
                        rain_mm += float(item.get("rain", {}).get("3h", 0.0))

                    payload = {
                        "rain_mm": rain_mm,
                        "ts": datetime.utcnow().isoformat(),
                    }
                    cache_ttl = timedelta(minutes=30)
                    self.redis.setex(key, cache_ttl, json.dumps(payload))
                    return rain_mm
            except Exception:
                pass

        cached = self.redis.get(key)
        if cached:
            parsed = json.loads(cached)
            ts = datetime.fromisoformat(parsed["ts"])
            if datetime.utcnow() - ts <= timedelta(hours=2):
                return float(parsed["rain_mm"])

        return 0.0
