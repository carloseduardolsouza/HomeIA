from __future__ import annotations


def estimate_monthly_bill(
    consumo_kwh_acumulado: float,
    dias_decorridos: int,
    tarifa_kwh: float,
    dias_no_mes: int = 30,
) -> dict[str, float]:
    dias_seguro = max(dias_decorridos, 1)
    consumo_diario = consumo_kwh_acumulado / dias_seguro
    projecao_kwh = consumo_diario * dias_no_mes
    projecao_fatura = projecao_kwh * tarifa_kwh
    return {
        "consumo_diario_medio": round(consumo_diario, 3),
        "projecao_kwh": round(projecao_kwh, 3),
        "projecao_fatura": round(projecao_fatura, 2),
    }
