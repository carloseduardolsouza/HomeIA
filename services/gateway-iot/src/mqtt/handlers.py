import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from prometheus_client import Counter

LOGGER = logging.getLogger(__name__)

mqtt_messages_received_total = Counter(
    "mqtt_messages_received_total", "Total MQTT messages received"
)
mqtt_parse_errors_total = Counter(
    "mqtt_parse_errors_total", "Total MQTT parse/validation errors"
)

MAX_TS_DRIFT_SECONDS = 60


@dataclass
class NormalizedReading:
    measurement: str
    tags: Dict[str, str]
    fields: Dict[str, float | str]
    ts: int


def _validate_ts(ts: int, now: Optional[int] = None) -> None:
    reference = int(now or time.time())
    if abs(reference - ts) > MAX_TS_DRIFT_SECONDS:
        raise ValueError("timestamp out of allowed window (+/- 60s)")


def _require(payload: Dict[str, Any], key: str) -> Any:
    if key not in payload:
        raise ValueError(f"missing required key: {key}")
    return payload[key]


def _range(name: str, value: float, minimum: float, maximum: float) -> None:
    if value < minimum or value > maximum:
        raise ValueError(f"{name} out of range [{minimum}, {maximum}]")


def parse_topic_payload(
    topic: str, payload: Dict[str, Any], now: Optional[int] = None
) -> NormalizedReading:
    ts = int(_require(payload, "ts"))
    _validate_ts(ts, now=now)

    if topic.startswith("casa/energia/medidor/"):
        medidor_id = str(_require(payload, "id"))
        local = str(payload.get("local", "desconhecido"))
        tensao_v = float(_require(payload, "tensao_v"))
        corrente_a = float(_require(payload, "corrente_a"))
        potencia_w = float(_require(payload, "potencia_w"))
        potencia_va = float(_require(payload, "potencia_va"))
        fator_potencia = float(_require(payload, "fator_potencia"))
        frequencia_hz = float(_require(payload, "frequencia_hz"))
        energia_kwh = float(_require(payload, "energia_kwh"))

        _range("tensao_v", tensao_v, 0, 300)
        _range("corrente_a", corrente_a, 0, 250)
        _range("potencia_w", potencia_w, 0, 50000)
        _range("potencia_va", potencia_va, 0, 50000)
        _range("fator_potencia", fator_potencia, 0, 1)
        _range("frequencia_hz", frequencia_hz, 45, 75)
        _range("energia_kwh", energia_kwh, 0, 1000000000)

        return NormalizedReading(
            measurement="energia_consumo",
            tags={"medidor_id": medidor_id, "local": local, "topic": topic},
            fields={
                "tensao_v": tensao_v,
                "corrente_a": corrente_a,
                "potencia_w": potencia_w,
                "potencia_va": potencia_va,
                "fator_potencia": fator_potencia,
                "frequencia_hz": frequencia_hz,
                "energia_kwh": energia_kwh,
            },
            ts=ts,
        )

    if topic == "casa/energia/consumo":
        watts = float(_require(payload, "watts"))
        volts = float(_require(payload, "volts"))
        amperes = float(_require(payload, "amperes"))
        _range("watts", watts, 0, 50000)
        _range("volts", volts, 0, 300)
        _range("amperes", amperes, 0, 250)
        return NormalizedReading(
            measurement="energia_consumo",
            tags={"source": "esp32", "topic": topic},
            fields={"watts": watts, "volts": volts, "amperes": amperes},
            ts=ts,
        )

    if topic == "casa/energia/disjuntor":
        breaker_id = str(_require(payload, "id"))
        status = str(_require(payload, "status"))
        if status not in {"open", "closed"}:
            raise ValueError("disjuntor status must be open|closed")
        return NormalizedReading(
            measurement="energia_disjuntor",
            tags={"id": breaker_id, "topic": topic},
            fields={"status": status},
            ts=ts,
        )

    if topic == "jardim/solo/umidade":
        sensor_id = str(_require(payload, "sensor_id"))
        umidade_pct = float(_require(payload, "umidade_pct"))
        _range("umidade_pct", umidade_pct, 0, 100)
        return NormalizedReading(
            measurement="jardim_solo",
            tags={"sensor_id": sensor_id, "topic": topic},
            fields={"umidade_pct": umidade_pct},
            ts=ts,
        )

    if topic == "jardim/solo/temperatura":
        sensor_id = str(_require(payload, "sensor_id"))
        temp_c = float(_require(payload, "temp_c"))
        _range("temp_c", temp_c, -40, 85)
        return NormalizedReading(
            measurement="jardim_solo",
            tags={"sensor_id": sensor_id, "topic": topic},
            fields={"temp_c": temp_c},
            ts=ts,
        )

    if topic == "casa/ambiente/temperatura":
        sensor_id = str(_require(payload, "sensor_id"))
        temp_c = float(_require(payload, "temp_c"))
        umidade_pct = float(_require(payload, "umidade_pct"))
        _range("temp_c", temp_c, -40, 85)
        _range("umidade_pct", umidade_pct, 0, 100)
        return NormalizedReading(
            measurement="ambiente_temperatura",
            tags={"sensor_id": sensor_id, "topic": topic},
            fields={"temp_c": temp_c, "umidade_pct": umidade_pct},
            ts=ts,
        )

    raise ValueError(f"unsupported topic: {topic}")


def handle_message(
    topic: str,
    payload: Dict[str, Any],
    influx_writer,
    postgres_writer,
    now: Optional[int] = None,
) -> bool:
    mqtt_messages_received_total.inc()
    try:
        reading = parse_topic_payload(topic, payload, now=now)
        influx_writer.write(reading)
        if topic == "casa/energia/disjuntor":
            postgres_writer.write_event(
                "breaker_events",
                {
                    "id": payload["id"],
                    "status": payload["status"],
                    "ts": payload["ts"],
                },
            )
        return True
    except Exception as exc:  # noqa: BLE001
        mqtt_parse_errors_total.inc()
        LOGGER.error("Validation/parsing error for topic=%s: %s", topic, exc)
        return False
