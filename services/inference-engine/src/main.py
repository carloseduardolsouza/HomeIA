from __future__ import annotations

import logging

from src.alerts.telegram import TelegramAlerter
from src.config import load_alert_rules, settings
from src.data.fetcher import InfluxEnergyFetcher
from src.jobs.anomaly_detector import run_anomaly_job
from src.jobs.billing_estimator import estimate_monthly_bill
from src.jobs.forecaster import run_forecast_job

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

    last_kwh = float(df["potencia_w"].sum() / 1000.0) if not df.empty else 0.0
    bill = estimate_monthly_bill(last_kwh, dias_decorridos=7, tarifa_kwh=0.95)

    LOGGER.info("Anomaly decisions: %s", len(decisions))
    LOGGER.info("Forecast generated rows: %s", len(forecast))
    LOGGER.info("Forecast metrics: %s", metrics)
    LOGGER.info("Billing projection: %s", bill)


if __name__ == "__main__":
    main()
