"""SQLite log of stage results: the per-stage cost and latency log (C-08), queryable.

Deliberately small: one table, one row per StageResult. Artifacts themselves
live as JSON files next to the project; this indexes how each was made.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from panelweaver.schemas.envelope import StageResult

_SCHEMA = """
CREATE TABLE IF NOT EXISTS stage_results (
    id INTEGER PRIMARY KEY,
    project TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    cache_key TEXT,
    started_at TEXT NOT NULL,
    envelope TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS stage_results_cache ON stage_results (cache_key);
"""


class Store:
    def __init__(self, path: Path | str) -> None:
        self.db = sqlite3.connect(path)
        self.db.executescript(_SCHEMA)

    def record(self, project: str, result: StageResult) -> None:
        self.db.execute(
            "INSERT INTO stage_results (project, stage, status, cache_key, started_at, envelope)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                project,
                result.stage,
                result.status.value,
                result.cache_key,
                result.started_at.isoformat(),
                result.model_dump_json(),
            ),
        )
        self.db.commit()

    def history(self, project: str, stage: str | None = None) -> list[StageResult]:
        sql = "SELECT envelope FROM stage_results WHERE project = ?"
        params: list[str] = [project]
        if stage is not None:
            sql += " AND stage = ?"
            params.append(stage)
        rows = self.db.execute(sql + " ORDER BY id", params).fetchall()
        return [StageResult.model_validate_json(r[0]) for r in rows]

    def close(self) -> None:
        self.db.close()
