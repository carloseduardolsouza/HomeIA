from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from src.models.base_model import BaseEnergyModel


class IsolationForestModel(BaseEnergyModel):
    def __init__(
        self,
        contamination: float = 0.05,
        random_state: int = 42,
    ) -> None:
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=200,
        )
        self.features = ["potencia_w", "hour", "day_of_week"]

    def fit(self, df: pd.DataFrame) -> None:
        self.model.fit(df[self.features])

    def predict(self, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        labels = self.model.predict(df[self.features])
        scores = self.model.decision_function(df[self.features])
        return labels, scores
