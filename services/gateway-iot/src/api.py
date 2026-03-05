import os

import uvicorn
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.config import settings
from src.models.sensor_reading import BatchIngestRequest, IngestRequest
from src.mqtt.client import MQTTGatewayClient
from src.mqtt.handlers import handle_message
from src.storage.influxdb import InfluxWriter
from src.storage.postgres import PostgresWriter

influx_writer = InfluxWriter(
    url=settings.influxdb_url,
    token=settings.influxdb_token,
    org=settings.influxdb_org,
    bucket=settings.influxdb_bucket,
    enabled=settings.influxdb_enabled,
)
postgres_writer = PostgresWriter(
    host=settings.postgres_host,
    port=settings.postgres_port,
    db=settings.postgres_db,
    user=settings.postgres_user,
    password=settings.postgres_password,
    enabled=settings.postgres_enabled,
)

mqtt_client: MQTTGatewayClient | None = None

app = FastAPI(title="Gateway IoT", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    global mqtt_client
    mqtt_disabled = os.getenv("DISABLE_MQTT", "false").lower() == "true"
    if settings.mqtt_enabled and not mqtt_disabled:
        mqtt_client = MQTTGatewayClient(
            on_payload=lambda topic, payload: handle_message(
                topic, payload, influx_writer, postgres_writer
            )
        )
        mqtt_client.start()


@app.on_event("shutdown")
def on_shutdown() -> None:
    if mqtt_client is not None:
        mqtt_client.stop()
    influx_writer.close()
    postgres_writer.close()


@app.post("/api/v1/ingest/sensor")
def ingest_sensor(body: IngestRequest) -> dict:
    topic = body.topic
    payload = body.payload
    ok = handle_message(topic, payload, influx_writer, postgres_writer)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid sensor payload")
    return {"status": "accepted"}


@app.post("/api/v1/ingest/batch")
def ingest_batch(body: BatchIngestRequest) -> dict:
    accepted = 0
    rejected = 0
    for reading in body.readings:
        ok = handle_message(
            reading.topic, reading.payload, influx_writer, postgres_writer
        )
        if ok:
            accepted += 1
        else:
            rejected += 1
    return {"accepted": accepted, "rejected": rejected}


@app.get("/api/v1/health")
def health() -> dict:
    return {
        "status": "ok",
        "mqtt_enabled": settings.mqtt_enabled,
        "influxdb_enabled": settings.influxdb_enabled,
        "postgres_enabled": settings.postgres_enabled,
    }


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=False)
