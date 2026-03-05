from src.mqtt.handlers import NormalizedReading
from src.storage.influxdb import InfluxWriter
from src.storage.postgres import PostgresWriter


def test_influx_writer_buffers_when_disabled() -> None:
    writer = InfluxWriter(
        url="http://localhost:8086",
        token="",
        org="ia-preditiva",
        bucket="sensores",
        enabled=False,
    )
    writer.write(
        NormalizedReading(
            measurement="energia_consumo",
            tags={"source": "test"},
            fields={"watts": 100.0},
            ts=1709123456,
        )
    )
    assert len(writer.buffer) == 1


def test_postgres_writer_buffers_when_disabled() -> None:
    writer = PostgresWriter(
        host="localhost",
        port=5432,
        db="ia",
        user="u",
        password="p",
        enabled=False,
    )
    writer.write_event("breaker_events", {"id": "d1", "status": "closed"})
    assert len(writer.events) == 1
