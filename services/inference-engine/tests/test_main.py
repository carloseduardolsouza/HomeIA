import pandas as pd

import src.main as main_module


class DummyFetcher:
    def __init__(self, *_args, **_kwargs):
        pass

    def fetch_energy(self, hours=24):
        base = pd.Timestamp("2026-03-05T00:00:00Z")
        return pd.DataFrame(
            {
                "ts": [base + pd.Timedelta(hours=i) for i in range(24)],
                "potencia_w": [1000 + i for i in range(24)],
                "medidor_id": ["medidor_01"] * 24,
            }
        )


def test_main_executes_with_monkeypatch(monkeypatch) -> None:
    monkeypatch.setattr(
        main_module,
        "load_alert_rules",
        lambda: {
            "energia": {
                "anomalia": {
                    "threshold_score": -0.3,
                    "cooldown_minutos": 15,
                    "severidade": "CRITICO",
                }
            }
        },
    )
    monkeypatch.setattr(main_module, "InfluxEnergyFetcher", DummyFetcher)
    monkeypatch.setattr(main_module, "run_anomaly_job", lambda *_a, **_k: [])
    monkeypatch.setattr(
        main_module,
        "run_forecast_job",
        lambda *_a, **_k: (
            pd.DataFrame({"yhat": [1, 2, 3]}),
            {"mae": 1, "mape": 2},
        ),
    )

    def send_stub(*_a, **_k):
        return True

    monkeypatch.setattr(main_module.TelegramAlerter, "send", send_stub)

    main_module.main()
