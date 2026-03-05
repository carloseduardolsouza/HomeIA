import os
from dataclasses import dataclass

DEFAULT_INTERVAL = "10"
IRRIGATION_INTERVAL_KEY = "IRRIGATION_INTERVAL_MIN"


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _env_int(name: str, default: str) -> int:
    return int(_env(name, default))


def _irrigation_interval() -> int:
    return _env_int(IRRIGATION_INTERVAL_KEY, DEFAULT_INTERVAL)


@dataclass
class Settings:
    mqtt_host: str = _env("MQTT_HOST", "localhost")
    mqtt_port: int = _env_int("MQTT_PORT", "1883")
    mqtt_user: str = _env("MQTT_USER", "homeia")
    mqtt_password: str = _env("MQTT_PASSWORD", "homeia123")

    redis_host: str = _env("REDIS_HOST", "localhost")
    redis_port: int = _env_int("REDIS_PORT", "6379")

    openweather_api_key: str = _env("OPENWEATHER_API_KEY", "")
    openweather_city: str = _env("OPENWEATHER_CITY", "Sao Paulo,BR")

    irrigation_interval_min: int = _irrigation_interval()
    postgres_host: str = _env("POSTGRES_HOST", "localhost")
    postgres_port: int = _env_int("POSTGRES_PORT", "5432")
    postgres_db: str = _env("POSTGRES_DB", "ia_preditiva")
    postgres_user: str = _env("POSTGRES_USER", "postgres")
    postgres_password: str = _env("POSTGRES_PASSWORD", "postgres")


settings = Settings()
