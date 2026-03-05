from dataclasses import dataclass
from datetime import datetime


@dataclass
class IrrigationContext:
    zone: str
    umidade_pct: float
    chuva_prevista_mm: float
    now: datetime
    ultima_irrigacao: datetime | None
    duracao_sugerida_min: int
