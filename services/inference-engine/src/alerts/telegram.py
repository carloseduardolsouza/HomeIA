from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict

import requests


class TelegramAlerter:
    def __init__(self, bot_token: str, chat_id: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self._last_alerts: Dict[str, datetime] = {}

    def can_send(
        self, key: str, cooldown_minutes: int, now: datetime | None = None
    ) -> bool:
        now_ref = now or datetime.utcnow()
        last = self._last_alerts.get(key)
        if last is None:
            return True
        return now_ref - last >= timedelta(minutes=cooldown_minutes)

    def mark_sent(self, key: str, now: datetime | None = None) -> None:
        self._last_alerts[key] = now or datetime.utcnow()

    def format_energy_alert(
        self,
        medidor_id: str,
        horario: str,
        consumo_atual: float,
        media_esperada: float,
        score_anomalia: float,
        severidade: str,
    ) -> str:
        delta = consumo_atual - media_esperada
        perc = (delta / max(media_esperada, 1.0)) * 100
        return (
            f"ALERTA DE ENERGIA - {severidade}\n\n"
            f"Medidor: {medidor_id}\n"
            f"Horario: {horario}\n"
            f"Consumo atual: {consumo_atual:.0f} W\n"
            f"Media esperada: {media_esperada:.0f} W ({perc:+.0f}%)\n"
            f"Score anomalia: {score_anomalia:.2f}\n\n"
            "-> Verifique equipamentos na sala/cozinha\n"
            "-> Dashboard: http://grafana:3000/d/energia"
        )

    def send(self, text: str) -> bool:
        if not self.bot_token or not self.chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        resp = requests.post(
            url,
            json={"chat_id": self.chat_id, "text": text},
            timeout=10,
        )
        return resp.status_code == 200
