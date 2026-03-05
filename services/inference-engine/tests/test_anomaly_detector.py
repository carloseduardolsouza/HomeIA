from datetime import datetime

import pandas as pd

from src.alerts.telegram import TelegramAlerter
from src.jobs.anomaly_detector import run_anomaly_job


def _sample_df() -> pd.DataFrame:
    base = pd.Timestamp("2026-03-05T00:00:00Z")
    rows = []
    for i in range(40):
        rows.append(
            {
                "ts": base + pd.Timedelta(minutes=5 * i),
                "potencia_w": 1000.0 if i < 39 else 5000.0,
                "medidor_id": "medidor_01",
            }
        )
    return pd.DataFrame(rows)


class DummyModel:
    contamination = 0.05

    def fit(self, _df):
        return None

    def predict(self, df):
        labels = [1] * len(df)
        scores = [0.2] * len(df)
        labels[-1] = -1
        scores[-1] = -0.5
        return labels, scores


def test_anomaly_detector_sends_single_alert_with_cooldown() -> None:
    df = _sample_df()
    rules = {
        "energia": {
            "anomalia": {
                "threshold_score": -0.3,
                "cooldown_minutos": 15,
                "severidade": "CRITICO",
            }
        }
    }
    alerter = TelegramAlerter(bot_token="", chat_id="")
    decisions = run_anomaly_job(
        df,
        rules,
        alerter,
        model=DummyModel(),
        now=datetime(2026, 3, 5, 14, 32),
    )
    assert len(decisions) == len(df)
    assert sum(1 for d in decisions if d["is_anomaly"]) == 1

    # within cooldown no extra send
    decisions_2 = run_anomaly_job(
        df,
        rules,
        alerter,
        model=DummyModel(),
        now=datetime(2026, 3, 5, 14, 40),
    )
    assert sum(1 for d in decisions_2 if d["is_anomaly"]) == 1
