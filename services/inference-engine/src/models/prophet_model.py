from __future__ import annotations

import pandas as pd

from src.models.base_model import BaseEnergyModel


class ProphetEnergyModel(BaseEnergyModel):
    """Wrapper de forecast.

    Usa Prophet quando disponivel. Se nao estiver instalado,
    faz fallback para previsao simples com media dos ultimos pontos.
    """

    def __init__(self) -> None:
        self._model = None
        self._fallback_mean = 0.0
        try:
            from prophet import Prophet  # type: ignore

            self._model = Prophet()
        except Exception:
            self._model = None

    def fit(self, df: pd.DataFrame) -> None:
        if self._model is not None:
            train = df[["ds", "y"]].copy()
            self._model.fit(train)
        else:
            self._fallback_mean = float(df["y"].tail(24).mean())

    def predict(self, periods: int = 24, freq: str = "h") -> pd.DataFrame:
        if self._model is not None:
            future = self._model.make_future_dataframe(
                periods=periods,
                freq=freq,
            )
            fc = self._model.predict(future)
            return fc[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)

        rng = pd.date_range(
            start=pd.Timestamp.now(),
            periods=periods,
            freq=freq,
        )
        return pd.DataFrame(
            {
                "ds": rng,
                "yhat": [self._fallback_mean] * periods,
                "yhat_lower": [self._fallback_mean * 0.9] * periods,
                "yhat_upper": [self._fallback_mean * 1.1] * periods,
            }
        )
