from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseEnergyModel(ABC):
    @abstractmethod
    def fit(self, df: pd.DataFrame) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, df: pd.DataFrame):
        raise NotImplementedError
