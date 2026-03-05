from datetime import datetime

from src.decision_engine import DecisionEngine


def test_blocked_by_rain_rn10() -> None:
    engine = DecisionEngine()
    decision = engine.decide(
        zone="A",
        umidade_pct=20.0,
        chuva_prevista_mm=6.0,
        now=datetime(2026, 3, 5, 6, 0),
        ultima_irrigacao=None,
        duracao_sugerida_min=20,
    )
    assert decision["pode_irrigar"] is False
    assert decision["motivo"] == "chuva_prevista_acima_limite"


def test_blocked_by_time_rn11() -> None:
    engine = DecisionEngine()
    decision = engine.decide(
        zone="A",
        umidade_pct=20.0,
        chuva_prevista_mm=0.0,
        now=datetime(2026, 3, 5, 14, 0),
        ultima_irrigacao=None,
        duracao_sugerida_min=20,
    )
    assert decision["pode_irrigar"] is False
    assert decision["motivo"] == "fora_horario_permitido"


def test_duration_capped_rn12() -> None:
    engine = DecisionEngine()
    decision = engine.decide(
        zone="A",
        umidade_pct=20.0,
        chuva_prevista_mm=0.0,
        now=datetime(2026, 3, 5, 6, 0),
        ultima_irrigacao=None,
        duracao_sugerida_min=90,
    )
    assert decision["duracao_min"] == 60


def test_blocked_by_min_interval_rn13() -> None:
    engine = DecisionEngine()
    decision = engine.decide(
        zone="A",
        umidade_pct=20.0,
        chuva_prevista_mm=0.0,
        now=datetime(2026, 3, 5, 8, 0),
        ultima_irrigacao=datetime(2026, 3, 5, 6, 30),
        duracao_sugerida_min=20,
    )
    assert decision["pode_irrigar"] is False
    assert decision["motivo"] == "intervalo_minimo_nao_respeitado"


def test_allowed_case() -> None:
    engine = DecisionEngine()
    decision = engine.decide(
        zone="A",
        umidade_pct=30.0,
        chuva_prevista_mm=0.0,
        now=datetime(2026, 3, 5, 6, 0),
        ultima_irrigacao=datetime(2026, 3, 5, 0, 0),
        duracao_sugerida_min=20,
    )
    assert decision["pode_irrigar"] is True
    assert decision["motivo"] == "ok"
