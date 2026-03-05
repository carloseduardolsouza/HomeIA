from datetime import datetime

from src.alerts.telegram import TelegramAlerter
from src.jobs.billing_estimator import estimate_monthly_bill


def test_telegram_alert_format() -> None:
    alerter = TelegramAlerter(bot_token="", chat_id="")
    msg = alerter.format_energy_alert(
        medidor_id="medidor_01",
        horario="14:32 | 05/03/2026",
        consumo_atual=3840,
        media_esperada=1240,
        score_anomalia=-0.47,
        severidade="CRITICO",
    )
    assert "ALERTA DE ENERGIA" in msg
    assert "medidor_01" in msg
    assert "Score anomalia" in msg


def test_telegram_cooldown_logic() -> None:
    alerter = TelegramAlerter(bot_token="", chat_id="")
    now = datetime(2026, 3, 5, 14, 32)
    assert alerter.can_send("k", 15, now=now) is True
    alerter.mark_sent("k", now=now)
    assert alerter.can_send("k", 15, now=datetime(2026, 3, 5, 14, 40)) is False
    assert alerter.can_send("k", 15, now=datetime(2026, 3, 5, 14, 50)) is True


def test_billing_estimator_projection() -> None:
    bill = estimate_monthly_bill(120.0, dias_decorridos=10, tarifa_kwh=0.95)
    assert bill["consumo_diario_medio"] == 12.0
    assert bill["projecao_kwh"] == 360.0
    assert bill["projecao_fatura"] == 342.0
