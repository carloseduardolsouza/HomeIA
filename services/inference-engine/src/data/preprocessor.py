from __future__ import annotations

import pandas as pd


def preprocess_energy(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()
    out["ts"] = pd.to_datetime(out["ts"], utc=True)
    out["hour"] = out["ts"].dt.hour
    out["day_of_week"] = out["ts"].dt.dayofweek
    rolling = out["potencia_w"].rolling(window=12, min_periods=1)
    out["rolling_mean_1h"] = rolling.mean()
    out = out.bfill().ffill()
    return out
