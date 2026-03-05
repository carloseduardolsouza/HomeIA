from datetime import datetime

from src.alerts.telegram import TelegramAlerter
from src.jobs.log_analyzer import (
    LABEL_CRITICAL,
    LABEL_NORMAL,
    build_daily_report,
    classify_logs,
    run_log_analyzer_job,
    should_send_daily_report,
)


def test_log_classifier_labels_known_patterns() -> None:
    lines = [
        "service started successfully",
        "warning: high latency detected",
        "critical: disk failure imminent",
    ]
    out = classify_logs(lines)
    labels = [c.label for c in out]
    assert LABEL_NORMAL in labels
    assert LABEL_CRITICAL in labels


def test_run_log_analyzer_critical_alerting(monkeypatch) -> None:
    sent = []
    alerter = TelegramAlerter(bot_token="", chat_id="")

    def _fake_send(text: str) -> bool:
        sent.append(text)
        return True

    monkeypatch.setattr(alerter, "send", _fake_send)

    summary = run_log_analyzer_job(
        [
            "error: out of memory process killed",
            "service started successfully",
        ],
        alerter,
        now=datetime(2026, 3, 5, 12, 0),
    )
    assert summary["total"] == 2
    assert summary["critico"] >= 1
    assert len(sent) >= 1


def test_daily_report_helpers() -> None:
    classified = classify_logs(
        [
            "service started successfully",
            "warning: high latency detected",
            "panic: kernel deadlock detected",
        ]
    )
    report = build_daily_report(classified, now=datetime(2026, 3, 6, 8, 0))
    assert "RELATORIO DIARIO DE LOGS" in report
    assert should_send_daily_report(datetime(2026, 3, 6, 8, 1)) is True
    assert should_send_daily_report(datetime(2026, 3, 6, 9, 0)) is False
