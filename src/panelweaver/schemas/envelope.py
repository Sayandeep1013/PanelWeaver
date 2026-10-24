"""The stage result envelope (register measure 7, C-20).

Every pipeline stage returns one of these alongside its artifact. One record
covers model routing (§64), reproducibility (§66), cost (§84), observability
(§89) and prompt versioning (§94).
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from panelweaver import __version__


class Status(StrEnum):
    OK = "ok"
    WARN = "warn"  # finished, but something needs a look (low confidence, QA warnings)
    FAILED = "failed"
    SKIPPED = "skipped"  # cache hit or not applicable


class ErrorClass(StrEnum):
    # The register's five (C-20)...
    INGEST_FAILED = "INGEST_FAILED"
    DETECTION_LOW_CONFIDENCE = "DETECTION_LOW_CONFIDENCE"
    OCR_FAILED = "OCR_FAILED"
    STORY_DIVERGED = "STORY_DIVERGED"
    RENDER_FAILED = "RENDER_FAILED"
    # ...plus two we expect to hit often: free-tier quotas and rate limits,
    # and model output that fails its schema (C-07: valid JSON is table stakes).
    PROVIDER_ERROR = "PROVIDER_ERROR"
    SCHEMA_INVALID = "SCHEMA_INVALID"


class StageResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: str
    status: Status
    error_class: ErrorClass | None = None
    error: str | None = None
    # Derived from measurable proxies, never from a model's self-report (C-07).
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    cost_usd: float = Field(default=0.0, ge=0.0)
    latency_ms: int = Field(default=0, ge=0)
    provider: str | None = None
    model_id: str | None = None
    prompt_hash: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    input_ids: list[str] = Field(default_factory=list)
    output_ids: list[str] = Field(default_factory=list)
    cache_key: str | None = None
    software_version: str = __version__
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def prompt_hash(prompt: str) -> str:
    """Hash of a prompt template, recorded in every artifact it produces (C-19)."""
    return sha256_text(prompt)[:16]


def cache_key(
    input_hashes: list[str], model_id: str | None, prompt: str | None, params: dict[str, Any]
) -> str:
    """Input hashes + model + prompt version + parameters (spec §65)."""
    payload = json.dumps(
        {
            "inputs": sorted(input_hashes),
            "model": model_id,
            "prompt": prompt_hash(prompt) if prompt is not None else None,
            "params": params,
        },
        sort_keys=True,
    )
    return sha256_text(payload)
