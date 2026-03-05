from __future__ import annotations

from typing import Any

import mlflow
import pandas as pd

from src.config import settings
from src.data.fetcher import to_prophet_frame
from src.models.prophet_model import ProphetEnergyModel


def _mape(y_true: pd.Series, y_pred: pd.Series) -> float:
    denom = y_true.replace(0, 1)
    return float((((y_true - y_pred).abs() / denom).mean()) * 100)


def run_forecast_job(
    df: pd.DataFrame,
    periods: int = 24,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    if df.empty:
        return pd.DataFrame(), {"mae": 0.0, "mape": 0.0}

    prophet_df = to_prophet_frame(df)
    model = ProphetEnergyModel()
    model.fit(prophet_df)
    forecast = model.predict(periods=periods)

    tail_size = min(len(prophet_df), len(forecast), 24)
    baseline = prophet_df.tail(tail_size).reset_index(drop=True)
    pred = forecast.head(tail_size).reset_index(drop=True)

    mae = float((baseline["y"] - pred["yhat"]).abs().mean())
    mape = _mape(baseline["y"], pred["yhat"])

    if settings.mlflow_enabled:
        try:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            with mlflow.start_run(run_name="energia_forecast"):
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("mape", mape)
                mlflow.set_tag("modulo", "energia")
        except Exception:
            # Keep the job resilient when MLflow is temporarily unavailable.
            pass

    return forecast, {"mae": mae, "mape": mape}
