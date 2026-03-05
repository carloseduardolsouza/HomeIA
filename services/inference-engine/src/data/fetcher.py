from __future__ import annotations

from datetime import datetime

import pandas as pd

try:
    from influxdb_client import InfluxDBClient
except Exception:
    InfluxDBClient = None


class InfluxEnergyFetcher:
    def __init__(self, url: str, token: str, org: str, bucket: str) -> None:
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

    def fetch_energy(self, hours: int = 24) -> pd.DataFrame:
        if not self.token or InfluxDBClient is None:
            now = pd.Timestamp.utcnow().floor("h")
            data = []
            for i in range(hours):
                ts = now - pd.Timedelta(hours=hours - i)
                data.append({"ts": ts, "potencia_w": 1000 + (i % 24) * 20})
            return pd.DataFrame(data)

        query = f"""from(bucket: "{self.bucket}")
  |> range(start: -{hours}h)
  |> filter(fn: (r) => r._measurement == "energia_consumo")
  |> filter(fn: (r) => r._field == "potencia_w")
  |> keep(columns: ["_time", "_value", "medidor_id"])"""

        conn_args = {"url": self.url, "token": self.token, "org": self.org}
        with InfluxDBClient(**conn_args) as client:
            result = client.query_api().query_data_frame(query)

        if isinstance(result, list):
            result = pd.concat(result, ignore_index=True)

        if result.empty:
            return pd.DataFrame(columns=["ts", "potencia_w", "medidor_id"])

        result = result.rename(columns={"_time": "ts", "_value": "potencia_w"})
        result["ts"] = pd.to_datetime(result["ts"], utc=True)
        if "medidor_id" not in result.columns:
            result["medidor_id"] = "medidor_01"
        return result[["ts", "potencia_w", "medidor_id"]]


def to_prophet_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame()
    out["ds"] = pd.to_datetime(df["ts"])
    out["y"] = df["potencia_w"].astype(float)
    return out.sort_values("ds")


def now_utc_str() -> str:
    return datetime.utcnow().strftime("%H:%M | %d/%m/%Y")
