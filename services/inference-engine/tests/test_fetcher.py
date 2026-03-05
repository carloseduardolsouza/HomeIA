import pandas as pd

from src.data.fetcher import InfluxEnergyFetcher, now_utc_str, to_prophet_frame


def test_fetcher_fallback_generates_rows() -> None:
    fetcher = InfluxEnergyFetcher(
        url="http://localhost:8086",
        token="",
        org="ia-preditiva",
        bucket="sensores",
    )
    df = fetcher.fetch_energy(hours=10)
    assert len(df) == 10
    assert "potencia_w" in df.columns


def test_to_prophet_frame_and_now_str() -> None:
    df = pd.DataFrame(
        {
            "ts": [pd.Timestamp("2026-03-05T00:00:00Z")],
            "potencia_w": [1234.5],
        }
    )
    out = to_prophet_frame(df)
    assert list(out.columns) == ["ds", "y"]
    assert isinstance(now_utc_str(), str)
