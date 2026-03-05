import pandas as pd

from src.jobs.forecaster import run_forecast_job


def test_forecaster_generates_24_points_and_metrics() -> None:
    base = pd.Timestamp("2026-03-01T00:00:00Z")
    df = pd.DataFrame(
        {
            "ts": [base + pd.Timedelta(hours=i) for i in range(72)],
            "potencia_w": [1000 + (i % 24) * 10 for i in range(72)],
            "medidor_id": ["medidor_01"] * 72,
        }
    )

    forecast, metrics = run_forecast_job(df, periods=24)
    assert len(forecast) == 24
    assert "mae" in metrics
    assert "mape" in metrics
    assert metrics["mae"] >= 0
