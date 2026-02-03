from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HttpError(Exception):
    status: int
    reason: str
    body: str
    url: str

    def __str__(self) -> str:  # noqa: D105
        body = self.body.strip()
        if body:
            return f"HTTP {self.status} {self.reason} ({self.url})\n{body}"
        return f"HTTP {self.status} {self.reason} ({self.url})"


def _read_http_error_body(e: urllib.error.HTTPError) -> str:
    try:
        return e.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


def request_bytes(
    *,
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    json_payload: dict[str, Any] | None = None,
    timeout_seconds: float = 180.0,
) -> bytes:
    body: bytes | None = None
    if json_payload is not None:
        body = json.dumps(json_payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        raise HttpError(
            status=int(getattr(e, "code", 0) or 0),
            reason=str(getattr(e, "reason", "") or ""),
            body=_read_http_error_body(e),
            url=url,
        ) from e


def request_json(
    *,
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    json_payload: dict[str, Any] | None = None,
    timeout_seconds: float = 180.0,
) -> dict[str, Any]:
    raw = request_bytes(
        url=url,
        method=method,
        headers=headers,
        json_payload=json_payload,
        timeout_seconds=timeout_seconds,
    )
    return json.loads(raw.decode("utf-8"))

