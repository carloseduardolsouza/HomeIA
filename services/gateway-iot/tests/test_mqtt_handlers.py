from src.mqtt.handlers import handle_message


class DummyInflux:
    def __init__(self) -> None:
        self.items = []

    def write(self, reading) -> None:
        self.items.append(reading)


class DummyPostgres:
    def __init__(self) -> None:
        self.events = []

    def write_event(self, table: str, payload: dict) -> None:
        self.events.append((table, payload))


def test_handle_message_accepts_valid_energy_payload() -> None:
    influx = DummyInflux()
    postgres = DummyPostgres()
    ok = handle_message(
        "casa/energia/consumo",
        {"watts": 1240.5, "volts": 220.1, "amperes": 5.64, "ts": 1709123456},
        influx,
        postgres,
        now=1709123456,
    )
    assert ok is True
    assert len(influx.items) == 1


def test_handle_message_rejects_invalid_range() -> None:
    influx = DummyInflux()
    postgres = DummyPostgres()
    ok = handle_message(
        "jardim/solo/umidade",
        {"sensor_id": "solo_01", "umidade_pct": 140.0, "ts": 1709123456},
        influx,
        postgres,
        now=1709123456,
    )
    assert ok is False
    assert len(influx.items) == 0


def test_handle_message_rejects_timestamp_outside_window() -> None:
    influx = DummyInflux()
    postgres = DummyPostgres()
    ok = handle_message(
        "casa/ambiente/temperatura",
        {
            "sensor_id": "amb_01",
            "temp_c": 24.1,
            "umidade_pct": 65.0,
            "ts": 1709123000,
        },
        influx,
        postgres,
        now=1709123456,
    )
    assert ok is False


def test_disjuntor_generates_relational_event() -> None:
    influx = DummyInflux()
    postgres = DummyPostgres()
    ok = handle_message(
        "casa/energia/disjuntor",
        {"id": "disjuntor_01", "status": "closed", "ts": 1709123456},
        influx,
        postgres,
        now=1709123456,
    )
    assert ok is True
    assert len(postgres.events) == 1


def test_medidor_topic_is_accepted_and_normalized() -> None:
    influx = DummyInflux()
    postgres = DummyPostgres()
    ok = handle_message(
        "casa/energia/medidor/medidor_01",
        {
            "id": "medidor_01",
            "local": "sala",
            "tensao_v": 220.3,
            "corrente_a": 5.61,
            "potencia_w": 1234.5,
            "potencia_va": 1240.0,
            "fator_potencia": 0.995,
            "frequencia_hz": 60.0,
            "energia_kwh": 542.3,
            "ts": 1709123456,
        },
        influx,
        postgres,
        now=1709123456,
    )
    assert ok is True
    assert len(influx.items) == 1
