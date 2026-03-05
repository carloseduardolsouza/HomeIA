from __future__ import annotations

from datetime import datetime
from typing import Any

import mlflow
import pandas as pd

from src.alerts.telegram import TelegramAlerter
from src.config import settings
from src.data.preprocessor import preprocess_energy
from src.models.isolation_forest import IsolationForestModel


def run_anomaly_job(
    df: pd.DataFrame,
    rules: dict[str, Any],
    alerter: TelegramAlerter,
    model: IsolationForestModel | None = None,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    if df.empty:
        return []

    now_ref = now or datetime.utcnow()
    processed = preprocess_energy(df)
    anomalia_cfg = rules["energia"]["anomalia"]
    detector = model or IsolationForestModel(
        contamination=float(anomalia_cfg["threshold_score"] * -0.1)
    )
    detector.fit(processed)
    labels, scores = detector.predict(processed)

    threshold = float(anomalia_cfg["threshold_score"])
    cooldown = int(anomalia_cfg["cooldown_minutos"])
    severity = str(anomalia_cfg["severidade"])

    decisions: list[dict[str, Any]] = []
    for idx in range(len(processed)):
        score = float(scores[idx])
        is_anomaly = int(labels[idx]) == -1 and score < threshold
        row = processed.iloc[idx]
        decision = {
            "ts": row["ts"].isoformat(),
            "modelo": "isolation_forest",
            "score": score,
            "is_anomaly": is_anomaly,
        }
        decisions.append(decision)

        if not is_anomaly:
            continue

        key = f"energia:{row.get('medidor_id', 'medidor_01')}"
        if alerter.can_send(key, cooldown_minutes=cooldown, now=now_ref):
            msg = alerter.format_energy_alert(
                medidor_id=str(row.get("medidor_id", "medidor_01")),
                horario=now_ref.strftime("%H:%M | %d/%m/%Y"),
                consumo_atual=float(row["potencia_w"]),
                media_esperada=float(row["rolling_mean_1h"]),
                score_anomalia=score,
                severidade=severity,
            )
            alerter.send(msg)
            alerter.mark_sent(key, now=now_ref)

    if settings.mlflow_enabled:
        try:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            with mlflow.start_run(run_name="energia_anomaly_detection"):
                mlflow.log_param("contamination", detector.contamination)
                mlflow.log_metric(
                    "anomalies_detected",
                    sum(1 for d in decisions if d["is_anomaly"]),
                )
                mlflow.set_tag("modulo", "energia")
                mlflow.set_tag("versao_dados", now_ref.strftime("%Y-%m"))
        except Exception:
            # Keep the job resilient when MLflow is temporarily unavailable.
            pass

    return decisions
