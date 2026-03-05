from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

import yaml

DEFAULT_MLFLOW_URI = "http://localhost:5000"
DEFAULT_ALERT_RULES_PATH = "config/alert_rules.yml"


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _env_bool(name: str, default: str = "true") -> bool:
    return _env(name, default).lower() == "true"


@dataclass
class Settings:
    influxdb_url: str = _env("INFLUXDB_URL", "http://localhost:8086")
    influxdb_token: str = _env("INFLUXDB_TOKEN", "")
    influxdb_org: str = _env("INFLUXDB_ORG", "ia-preditiva")
    influxdb_bucket: str = _env("INFLUXDB_BUCKET", "sensores")

    mlflow_tracking_uri: str = _env("MLFLOW_TRACKING_URI", DEFAULT_MLFLOW_URI)
    mlflow_enabled: bool = _env_bool("MLFLOW_ENABLED", "true")

    telegram_bot_token: str = _env("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = _env("TELEGRAM_CHAT_ID", "")

    alert_rules_path: str = _env("ALERT_RULES_PATH", DEFAULT_ALERT_RULES_PATH)


settings = Settings()


def load_alert_rules(path: str | None = None) -> dict[str, Any]:
    rules_path = Path(path or settings.alert_rules_path)
    with rules_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
