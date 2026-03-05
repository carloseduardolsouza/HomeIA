from __future__ import annotations

from typing import List

try:
    from influxdb_client import InfluxDBClient, Point, WritePrecision
except Exception:  # noqa: BLE001
    InfluxDBClient = None
    Point = None
    WritePrecision = None


class InfluxWriter:
    def __init__(
        self, url: str, token: str, org: str, bucket: str, enabled: bool = True
    ) -> None:
        self.enabled = enabled and bool(token)
        self.org = org
        self.bucket = bucket
        self._buffer: List[dict] = []
        self._client = None
        self._write_api = None

        if self.enabled and InfluxDBClient is not None:
            self._client = InfluxDBClient(url=url, token=token, org=org)
            self._write_api = self._client.write_api()

    @property
    def buffer(self) -> List[dict]:
        return self._buffer

    def write(self, reading) -> None:
        if not self.enabled or self._write_api is None or Point is None:
            self._buffer.append(
                {
                    "measurement": reading.measurement,
                    "tags": reading.tags,
                    "fields": reading.fields,
                    "ts": reading.ts,
                }
            )
            return

        point = Point(reading.measurement)
        for key, value in reading.tags.items():
            point = point.tag(key, value)
        for key, value in reading.fields.items():
            point = point.field(key, value)
        point = point.time(reading.ts, WritePrecision.S)
        self._write_api.write(bucket=self.bucket, org=self.org, record=point)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
