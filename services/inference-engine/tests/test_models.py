import pandas as pd

from src.models.isolation_forest import IsolationForestModel
from src.models.prophet_model import ProphetEnergyModel


def test_isolation_forest_wrapper_fit_predict() -> None:
    base = pd.Timestamp("2026-03-01T00:00:00Z")
    df = pd.DataFrame(
        {
            "ts": [base + pd.Timedelta(hours=i) for i in range(50)],
            "potencia_w": [900 + (i % 10) * 50 for i in range(50)],
            "hour": [i % 24 for i in range(50)],
            "day_of_week": [i % 7 for i in range(50)],
        }
    )
    model = IsolationForestModel(contamination=0.1)
    model.fit(df)
    labels, scores = model.predict(df)
    assert len(labels) == len(df)
    assert len(scores) == len(df)


def test_prophet_model_fallback_predict() -> None:
    base = pd.Timestamp("2026-03-01T00:00:00Z")
    df = pd.DataFrame(
        {
            "ds": [base + pd.Timedelta(hours=i) for i in range(48)],
            "y": [1000 + i for i in range(48)],
        }
    )
    model = ProphetEnergyModel()
    # Force fallback path to ensure deterministic test.
    model._model = None
    model.fit(df)
    fc = model.predict(periods=6)
    assert len(fc) == 6
    assert "yhat" in fc.columns
