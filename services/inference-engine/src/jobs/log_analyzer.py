from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from src.alerts.telegram import TelegramAlerter


LABEL_NORMAL = "NORMAL"
LABEL_WARNING = "AVISO"
LABEL_CRITICAL = "CRITICO"


@dataclass
class LogClassification:
    line: str
    label: str
    score: float


def _training_dataset() -> tuple[list[str], list[str]]:
    lines = [
        "service started successfully",
        "connection established",
        "info: heartbeat ok",
        "warn: retrying database connection",
        "warning: high latency detected",
        "timeout talking to upstream api",
        "error: out of memory process killed",
        "critical: disk failure imminent",
        "panic: kernel deadlock detected",
    ]
    labels = [
        LABEL_NORMAL,
        LABEL_NORMAL,
        LABEL_NORMAL,
        LABEL_WARNING,
        LABEL_WARNING,
        LABEL_WARNING,
        LABEL_CRITICAL,
        LABEL_CRITICAL,
        LABEL_CRITICAL,
    ]
    return lines, labels


def train_log_classifier() -> Pipeline:
    x_train, y_train = _training_dataset()
    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=300, multi_class="auto")),
        ]
    )
    model.fit(x_train, y_train)
    return model


def classify_logs(
    lines: Iterable[str], model: Pipeline | None = None
) -> list[LogClassification]:
    model_ref = model or train_log_classifier()
    seq = list(lines)
    if not seq:
        return []

    probs = model_ref.predict_proba(seq)
    labels = model_ref.predict(seq)
    out: list[LogClassification] = []
    for idx, line in enumerate(seq):
        out.append(
            LogClassification(
                line=line,
                label=str(labels[idx]),
                score=float(max(probs[idx])),
            )
        )
    return out


def run_log_analyzer_job(
    lines: Iterable[str],
    alerter: TelegramAlerter,
    now: datetime | None = None,
    model: Pipeline | None = None,
) -> dict:
    now_ref = now or datetime.utcnow()
    classified = classify_logs(lines, model=model)

    criticals = [c for c in classified if c.label == LABEL_CRITICAL]
    warnings = [c for c in classified if c.label == LABEL_WARNING]

    for entry in criticals:
        msg = (
            "ALERTA DE LOG - CRITICO\n\n"
            f"Horario: {now_ref.strftime('%H:%M | %d/%m/%Y')}\n"
            f"Linha: {entry.line}\n"
            f"Confianca: {entry.score:.2f}"
        )
        alerter.send(msg)

    return {
        "timestamp": now_ref.isoformat(),
        "total": len(classified),
        "normal": sum(1 for c in classified if c.label == LABEL_NORMAL),
        "aviso": len(warnings),
        "critico": len(criticals),
    }


def build_daily_report(
    classified_last_24h: list[LogClassification], now: datetime
) -> str:
    total = len(classified_last_24h)
    normais = sum(1 for c in classified_last_24h if c.label == LABEL_NORMAL)
    avisos = sum(1 for c in classified_last_24h if c.label == LABEL_WARNING)
    criticos = sum(1 for c in classified_last_24h if c.label == LABEL_CRITICAL)

    return (
        "RELATORIO DIARIO DE LOGS\n\n"
        f"Horario: {now.strftime('%H:%M | %d/%m/%Y')}\n"
        f"Total linhas: {total}\n"
        f"NORMAL: {normais}\n"
        f"AVISO: {avisos}\n"
        f"CRITICO: {criticos}"
    )


def should_send_daily_report(now: datetime) -> bool:
    return now.hour == 8 and now.minute < 5
