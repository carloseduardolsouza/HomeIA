from __future__ import annotations

import json
from datetime import datetime

try:
    import psycopg2
except Exception:
    psycopg2 = None


class IrrigationLogRepository:
    def __init__(
        self,
        host: str,
        port: int,
        db: str,
        user: str,
        password: str,
    ) -> None:
        self._conn = None
        if psycopg2 is not None:
            self._conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=db,
                user=user,
                password=password,
            )
            self._conn.autocommit = True
            with self._conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS irrigacao_log (
                      id SERIAL PRIMARY KEY,
                      zone TEXT NOT NULL,
                      started_at TIMESTAMPTZ NOT NULL,
                      ended_at TIMESTAMPTZ,
                      duracao_min INTEGER NOT NULL,
                      origem TEXT NOT NULL,
                      acao TEXT NOT NULL,
                      details JSONB
                    )
                    """
                )

    def log(
        self,
        zone: str,
        started_at: datetime,
        duracao_min: int,
        origem: str,
        acao: str,
        details: dict,
    ) -> None:
        if self._conn is None:
            return
        ended_at = started_at
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO irrigacao_log (
                  zone, started_at, ended_at, duracao_min,
                  origem, acao, details
                ) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
                """,
                (
                    zone,
                    started_at,
                    ended_at,
                    duracao_min,
                    origem,
                    acao,
                    json.dumps(details),
                ),
            )

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
