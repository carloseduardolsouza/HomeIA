from __future__ import annotations

import json
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from src.config import settings
from src.decision_engine import DecisionEngine
from src.repository import IrrigationLogRepository
from src.weather_client import WeatherClient


def _publish_command(client: mqtt.Client, zone: str, command: dict) -> None:
    topic = f"jardim/irrigacao/{zone}/comando"
    client.publish(topic, json.dumps(command))


def run_scheduler_loop() -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(settings.mqtt_user, settings.mqtt_password)
    client.connect(settings.mqtt_host, settings.mqtt_port, 60)
    client.loop_start()

    engine = DecisionEngine()
    repo = IrrigationLogRepository(
        host=settings.postgres_host,
        port=settings.postgres_port,
        db=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
    )
    weather = WeatherClient(
        api_key=settings.openweather_api_key,
        redis_host=settings.redis_host,
        redis_port=settings.redis_port,
    )

    last_irrigation: dict[str, datetime | None] = {"A": None}

    try:
        while True:
            zone = "A"
            umidade_pct = 35.0
            city = settings.openweather_city
            chuva_prevista_mm = weather.fetch_forecast_mm(city)
            now = datetime.now()

            decision = engine.decide(
                zone=zone,
                umidade_pct=umidade_pct,
                chuva_prevista_mm=chuva_prevista_mm,
                now=now,
                ultima_irrigacao=last_irrigation.get(zone),
                duracao_sugerida_min=20,
            )

            if decision["pode_irrigar"]:
                _publish_command(
                    client,
                    zone,
                    {
                        "acao": "ligar",
                        "duracao_minutos": decision["duracao_min"],
                        "origem": decision["origem"],
                    },
                )
                last_irrigation[zone] = now
                repo.log(
                    zone=zone,
                    started_at=now,
                    duracao_min=decision["duracao_min"],
                    origem=decision["origem"],
                    acao="ligar",
                    details={
                        "chuva_prevista_mm": chuva_prevista_mm,
                        "umidade_pct": umidade_pct,
                    },
                )
            else:
                repo.log(
                    zone=zone,
                    started_at=now,
                    duracao_min=decision["duracao_min"],
                    origem=decision["origem"],
                    acao="bloqueado",
                    details={
                        "motivo": decision["motivo"],
                        "chuva_prevista_mm": chuva_prevista_mm,
                        "umidade_pct": umidade_pct,
                    },
                )

            time.sleep(settings.irrigation_interval_min * 60)
    finally:
        repo.close()
        client.loop_stop()
        client.disconnect()
