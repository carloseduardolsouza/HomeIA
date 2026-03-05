from __future__ import annotations

import logging
from datetime import datetime

from src.alerts.telegram import TelegramAlerter
from src.config import load_alert_rules, settings
from src.data.fetcher import InfluxEnergyFetcher
from src.jobs.anomaly_detector import run_anomaly_job
from src.jobs.billing_estimator import estimate_monthly_bill
from src.jobs.forecaster import run_forecast_job
from src.jobs.log_analyzer import (
    build_daily_report,
    classify_logs,
    run_log_analyzer_job,
    should_send_daily_report,
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def main() -> None:
    rules = load_alert_rules()
    fetcher = InfluxEnergyFetcher(
        url=settings.influxdb_url,
        token=settings.influxdb_token,
        org=settings.influxdb_org,
        bucket=settings.influxdb_bucket,
    )
    df = fetcher.fetch_energy(hours=24 * 7)

    alerter = TelegramAlerter(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
    )

    decisions = run_anomaly_job(df, rules, alerter)
    forecast, metrics = run_forecast_job(df, periods=24)
    log_summary = run_log_analyzer_job(
        [
            "service started successfully",
            "warning: high latency detected",
            "error: out of memory process killed",
        ],
        alerter,
    )

    last_kwh = float(df["potencia_w"].sum() / 1000.0) if not df.empty else 0.0
    bill = estimate_monthly_bill(last_kwh, dias_decorridos=7, tarifa_kwh=0.95)

    LOGGER.info("Anomaly decisions: %s", len(decisions))
    LOGGER.info("Forecast generated rows: %s", len(forecast))
    LOGGER.info("Forecast metrics: %s", metrics)
    LOGGER.info("Billing projection: %s", bill)
    LOGGER.info("Log summary: %s", log_summary)

    now = datetime.now()
    if should_send_daily_report(now):
        report = build_daily_report(
            classify_logs(
                [
                    "service started successfully",
                    "warning: high latency detected",
                    "error: out of memory process killed",
                ]
            ),
            now=now,
        )
        alerter.send(report)


if __name__ == "__main__":
    main()
