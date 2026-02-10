from __future__ import annotations

import base64
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from toc.http import HttpError, request_bytes, request_json


def _env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def _guess_mime(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".png":
        return "image/png"
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".webp":
        return "image/webp"
    return "application/octet-stream"


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _lookup_path(data: Any, path: str) -> Any:
    current: Any = data
    for raw_part in path.split("."):
        part = raw_part.strip()
        if part == "":
            return None

        if isinstance(current, list):
            if not part.isdigit():
                return None
            index = int(part)
            if index < 0 or index >= len(current):
                return None
            current = current[index]
            continue

        if isinstance(current, dict):
            if part not in current:
                return None
            current = current.get(part)
            continue

        return None
    return current


def _first_non_empty(data: dict[str, Any], paths: list[str]) -> Any:
    for path in paths:
        value = _lookup_path(data, path)
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        return value
    return None


@dataclass(frozen=True)
class KlingConfig:
    api_key: str
    api_base: str = "https://api.klingai.com"
    video_model: str = "kling-3.0"
    submit_path: str = "/v1/videos/generations"
    status_path_template: str = "/v1/videos/generations/{operation_id}"
    api_key_header: str = "authorization"
    api_key_prefix: str = "Bearer "

    @staticmethod
    def from_env(
        *,
        api_key: str | None = None,
        api_base: str | None = None,
        video_model: str | None = None,
        submit_path: str | None = None,
        status_path_template: str | None = None,
        api_key_header: str | None = None,
        api_key_prefix: str | None = None,
    ) -> "KlingConfig":
        key = api_key or _env("KLING_API_KEY")
        if not key:
            raise ValueError("Missing KLING_API_KEY")

        return KlingConfig(
            api_key=key,
            api_base=api_base or _env("KLING_API_BASE", "https://api.klingai.com") or "",
            video_model=video_model or _env("KLING_VIDEO_MODEL", "kling-3.0") or "",
            submit_path=submit_path or _env("KLING_VIDEO_SUBMIT_PATH", "/v1/videos/generations") or "",
            status_path_template=status_path_template
            or _env("KLING_VIDEO_STATUS_PATH_TEMPLATE", "/v1/videos/generations/{operation_id}")
            or "",
            api_key_header=api_key_header or _env("KLING_API_KEY_HEADER", "authorization") or "",
            api_key_prefix=api_key_prefix or _env("KLING_API_KEY_PREFIX", "Bearer ") or "",
        )


class KlingClient:
    def __init__(self, config: KlingConfig):
        self.config = config

    @staticmethod
    def from_env(**overrides: Any) -> "KlingClient":
        return KlingClient(KlingConfig.from_env(**overrides))

    def _headers(self) -> dict[str, str]:
        key_header = self.config.api_key_header.strip()
        if key_header.lower() == "authorization":
            return {"authorization": f"{self.config.api_key_prefix}{self.config.api_key}"}
        return {key_header: self.config.api_key}

    def _resolve_url(self, path_or_url: str, *, operation_id: str | None = None) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url

        resolved_path = path_or_url
        if operation_id is not None:
            resolved_path = resolved_path.format(operation_id=operation_id)

        if resolved_path.startswith("/"):
            return f"{self.config.api_base.rstrip('/')}{resolved_path}"
        return f"{self.config.api_base.rstrip('/')}/{resolved_path}"

    def build_video_payload(
        self,
        *,
        prompt: str,
        duration_seconds: int,
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
        input_image: Path | None = None,
        last_frame_image: Path | None = None,
        negative_prompt: str | None = None,
        model: str | None = None,
        extra_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model or self.config.video_model,
            "prompt": prompt,
            "duration_seconds": int(duration_seconds),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }

        if negative_prompt and negative_prompt.strip():
            payload["negative_prompt"] = negative_prompt.strip()

        if input_image is not None:
            payload["first_frame_image"] = {
                "mime_type": _guess_mime(input_image),
                "data": base64.b64encode(input_image.read_bytes()).decode("ascii"),
            }

        if last_frame_image is not None:
            payload["last_frame_image"] = {
                "mime_type": _guess_mime(last_frame_image),
                "data": base64.b64encode(last_frame_image.read_bytes()).decode("ascii"),
            }

        if extra_payload:
            payload = _deep_merge(payload, extra_payload)

        return payload

    def start_video_generation(
        self,
        *,
        prompt: str,
        duration_seconds: int,
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
        input_image: Path | None = None,
        last_frame_image: Path | None = None,
        negative_prompt: str | None = None,
        model: str | None = None,
        extra_payload: dict[str, Any] | None = None,
        timeout_seconds: float = 180.0,
    ) -> dict[str, Any]:
        payload = self.build_video_payload(
            prompt=prompt,
            duration_seconds=duration_seconds,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            input_image=input_image,
            last_frame_image=last_frame_image,
            negative_prompt=negative_prompt,
            model=model,
            extra_payload=extra_payload,
        )
        return request_json(
            url=self._resolve_url(self.config.submit_path),
            method="POST",
            headers={"content-type": "application/json", **self._headers()},
            json_payload=payload,
            timeout_seconds=timeout_seconds,
        )

    def extract_operation_id(
        self,
        response: dict[str, Any],
        *,
        id_paths: list[str] | None = None,
    ) -> str:
        paths = id_paths or _split_csv(_env("KLING_OPERATION_ID_PATHS", "data.id,id,task_id,data.task_id"))
        operation_id = _first_non_empty(response, paths)
        if operation_id is None:
            raise ValueError(
                "No operation id found in Kling submit response. "
                f"Tried paths={paths}. Response keys={list(response.keys())}"
            )
        return str(operation_id)

    def extract_status(
        self,
        operation: dict[str, Any],
        *,
        status_paths: list[str] | None = None,
    ) -> str | None:
        paths = status_paths or _split_csv(_env("KLING_STATUS_PATHS", "status,data.status,task.status,data.task_status"))
        status = _first_non_empty(operation, paths)
        if status is None:
            return None
        return str(status).strip().lower()

    def is_failed_operation(
        self,
        operation: dict[str, Any],
        *,
        status_paths: list[str] | None = None,
        failed_statuses: list[str] | None = None,
    ) -> bool:
        statuses = set(
            s.lower().strip()
            for s in (
                failed_statuses
                or _split_csv(_env("KLING_FAILED_STATUSES", "failed,error,cancelled,canceled,rejected"))
            )
            if s.strip()
        )

        if operation.get("error"):
            return True

        status = self.extract_status(operation, status_paths=status_paths)
        if status and status in statuses:
            return True
        return False

    def is_done_operation(
        self,
        operation: dict[str, Any],
        *,
        status_paths: list[str] | None = None,
        done_statuses: list[str] | None = None,
    ) -> bool:
        done_flag = operation.get("done")
        if isinstance(done_flag, bool):
            return done_flag

        statuses = set(
            s.lower().strip()
            for s in (
                done_statuses
                or _split_csv(_env("KLING_DONE_STATUSES", "succeeded,success,completed,done,finished"))
            )
            if s.strip()
        )
        status = self.extract_status(operation, status_paths=status_paths)
        if status and status in statuses:
            return True
        return False

    def poll_operation(
        self,
        *,
        operation_id_or_url: str,
        status_paths: list[str] | None = None,
        done_statuses: list[str] | None = None,
        failed_statuses: list[str] | None = None,
        poll_every_seconds: float = 5.0,
        timeout_seconds: float = 900.0,
    ) -> dict[str, Any]:
        operation_url = (
            operation_id_or_url
            if operation_id_or_url.startswith("http://") or operation_id_or_url.startswith("https://")
            else self._resolve_url(self.config.status_path_template, operation_id=operation_id_or_url)
        )

        deadline = time.time() + float(timeout_seconds)
        while True:
            op = request_json(
                url=operation_url,
                method="GET",
                headers=self._headers(),
                timeout_seconds=180.0,
            )
            if self.is_failed_operation(op, status_paths=status_paths, failed_statuses=failed_statuses):
                return op
            if self.is_done_operation(op, status_paths=status_paths, done_statuses=done_statuses):
                return op

            if time.time() > deadline:
                raise TimeoutError(f"Timed out waiting for operation: {operation_id_or_url}")
            time.sleep(float(poll_every_seconds))

    def extract_video_uri(
        self,
        operation: dict[str, Any],
        *,
        video_url_paths: list[str] | None = None,
    ) -> str:
        paths = video_url_paths or _split_csv(
            _env(
                "KLING_VIDEO_URL_PATHS",
                "data.video.url,data.video_url,data.output.url,video.url,video_url,output.video_url,result.video.url",
            )
        )

        value = _first_non_empty(operation, paths)
        if value is None:
            raise ValueError(
                "Operation completed but no video URL found. "
                f"Tried paths={paths}. Response keys={list(operation.keys())}"
            )

        if isinstance(value, dict):
            for key in ("url", "uri", "download_url", "downloadUrl"):
                nested = value.get(key)
                if isinstance(nested, str) and nested.strip():
                    return nested.strip()
            raise ValueError("Video URL field resolved to an object without a URL-like key.")

        if isinstance(value, str):
            return value.strip()

        raise ValueError(f"Video URL value has unsupported type: {type(value).__name__}")

    def download_to_file(self, *, uri: str, out_path: Path, timeout_seconds: float = 600.0) -> None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = request_bytes(url=uri, method="GET", headers=self._headers(), timeout_seconds=timeout_seconds)
        except HttpError:
            data = request_bytes(url=uri, method="GET", headers=None, timeout_seconds=timeout_seconds)
        out_path.write_bytes(data)
