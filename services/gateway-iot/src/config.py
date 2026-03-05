import os
from dataclasses import dataclass


def _env_bool(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).lower() == "true"


@dataclass
class Settings:
    mqtt_host: str = os.getenv("MQTT_HOST", "localhost")
    mqtt_port: int = int(os.getenv("MQTT_PORT", "1883"))
    mqtt_user: str = os.getenv("MQTT_USER", "homeia")
    mqtt_password: str = os.getenv("MQTT_PASSWORD", "homeia123")
    mqtt_keepalive: int = int(os.getenv("MQTT_KEEPALIVE", "60"))
    mqtt_enabled: bool = _env_bool("MQTT_ENABLED")

    influxdb_url: str = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    influxdb_token: str = os.getenv("INFLUXDB_TOKEN", "")
    influxdb_org: str = os.getenv("INFLUXDB_ORG", "ia-preditiva")
    influxdb_bucket: str = os.getenv("INFLUXDB_BUCKET", "sensores")
    influxdb_enabled: bool = _env_bool("INFLUXDB_ENABLED")

    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "ia_preditiva")
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_enabled: bool = _env_bool("POSTGRES_ENABLED")


settings = Settings()
