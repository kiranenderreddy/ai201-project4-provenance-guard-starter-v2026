"""
Capstone structured instrumentation for Provenance Guard.

Each POST /submit request is recorded as one JSON object in:

    logs/capstone_runs.jsonl

The record includes:
- timestamp
- input
- output
- HTTP status
- duration in milliseconds

This log is separate from the existing audit log so the original
Provenance Guard behavior remains unchanged.
"""

import json
import threading
from datetime import datetime, timezone
from pathlib import Path


LOG_PATH = Path("logs") / "capstone_runs.jsonl"

_lock = threading.Lock()

MAX_TEXT_PREVIEW = 500


def _timestamp():
    """Return a UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).isoformat()


def summarize_input(payload):
    """
    Convert the incoming request body into a structured,
    reasonably sized representation for the run log.
    """

    if not isinstance(payload, dict):
        return {
            "type": type(payload).__name__,
            "value": payload,
        }

    text = payload.get("text")
    creator_id = payload.get("creator_id")

    if isinstance(text, str):
        preview = text[:MAX_TEXT_PREVIEW]

        return {
            "creator_id": creator_id,
            "text_preview": preview,
            "text_length": len(text),
            "text_truncated": len(text) > MAX_TEXT_PREVIEW,
        }

    return {
        "creator_id": creator_id,
        "text": text,
    }


def write_run(
    *,
    input_data,
    output_data,
    status_code,
    duration_ms,
):
    """
    Write one structured run record to disk.
    """

    record = {
        "timestamp": _timestamp(),
        "input": input_data,
        "output": output_data,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 3),
    }

    LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    line = json.dumps(
        record,
        ensure_ascii=False,
    )

    with _lock:
        with LOG_PATH.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(line + "\n")

    return record