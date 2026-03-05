from __future__ import annotations

import json
from typing import List

try:
    import psycopg2
except Exception:  # noqa: BLE001
    psycopg2 = None


class PostgresWriter:
    def __init__(
        self,
        host: str,
        port: int,
        db: str,
        user: str,
        password: str,
        enabled: bool = True,
    ) -> None:
        self.enabled = enabled
        self._events: List[dict] = []
        self._conn = None

        if self.enabled and psycopg2 is not None:
            self._conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=db,
                user=user,
                password=password,
            )
            self._conn.autocommit = True

    @property
    def events(self) -> List[dict]:
        return self._events

    def write_event(self, table: str, payload: dict) -> None:
        if not self.enabled or self._conn is None:
            self._events.append({"table": table, "payload": payload})
            return

        with self._conn.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {table} (payload) VALUES (%s::jsonb)",
                (json.dumps(payload),),
            )

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
