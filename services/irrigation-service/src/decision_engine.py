from __future__ import annotations

from datetime import datetime

from src.models.irrigation_model import IrrigationContext
from src.rules.business_rules import IrrigationRules


class DecisionEngine:
    def __init__(self, rules: IrrigationRules | None = None) -> None:
        self.rules = rules or IrrigationRules()

    def decide(
        self,
        zone: str,
        umidade_pct: float,
        chuva_prevista_mm: float,
        now: datetime,
        ultima_irrigacao: datetime | None,
        duracao_sugerida_min: int,
    ) -> dict:
        contexto = IrrigationContext(
            zone=zone,
            umidade_pct=umidade_pct,
            chuva_prevista_mm=chuva_prevista_mm,
            now=now,
            ultima_irrigacao=ultima_irrigacao,
            duracao_sugerida_min=duracao_sugerida_min,
        )
        pode, motivo = self.rules.pode_irrigar(contexto)
        duracao = min(duracao_sugerida_min, self.rules.DURACAO_MAXIMA_MIN)
        return {
            "pode_irrigar": pode,
            "motivo": motivo,
            "duracao_min": duracao,
            "origem": "ia",
        }
