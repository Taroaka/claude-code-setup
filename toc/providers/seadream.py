from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any

from toc.http import request_bytes, request_json


def _env(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    if v is None or v == "":
        return default
    return v


def _guess_mime_from_bytes(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith(b"RIFF") and b"WEBP" in data[8:16]:
        return "image/webp"
    return None


@dataclass(frozen=True)
class SeaDreamConfig:
    api_key: str
    api_base: str = "https://ark.ap-southeast.bytepluses.com/api/v3"
    image_model: str = "seedream-4-5-251128"

    @staticmethod
    def from_env(
        *,
        api_key: str | None = None,
        api_base: str | None = None,
        image_model: str | None = None,
    ) -> "SeaDreamConfig":
        key = api_key or _env("SEADREAM_API_KEY")
        if not key:
            raise ValueError("Missing SEADREAM_API_KEY")
        return SeaDreamConfig(
            api_key=key,
            api_base=api_base or _env("SEADREAM_API_BASE", "https://ark.ap-southeast.bytepluses.com/api/v3") or "",
            image_model=image_model or _env("SEADREAM_MODEL", "seedream-4-5-251128") or "",
        )


class SeaDreamClient:
    """
    OpenAI-compatible image generation client.

    Defaults are configured for BytePlus ModelArk (Seedream 4.5) but can be pointed to any
    OpenAI Images API compatible endpoint by changing api_base.
    """

    def __init__(self, config: SeaDreamConfig):
        self.config = config

    @staticmethod
    def from_env(**overrides: Any) -> "SeaDreamClient":
        return SeaDreamClient(SeaDreamConfig.from_env(**overrides))

    def _headers(self) -> dict[str, str]:
        return {"authorization": f"Bearer {self.config.api_key}"}

    def generate_image(
        self,
        *,
        prompt: str,
        size: str = "1024x1536",
        n: int = 1,
        response_format: str = "b64_json",
        model: str | None = None,
        timeout_seconds: float = 180.0,
        extra_payload: dict[str, Any] | None = None,
    ) -> tuple[bytes, str | None, dict[str, Any]]:
        model_name = model or self.config.image_model
        url = f"{self.config.api_base.rstrip('/')}/images/generations"
        payload: dict[str, Any] = {
            "model": model_name,
            "prompt": prompt,
            "n": int(n),
            "size": size,
            "response_format": response_format,
        }
        if extra_payload:
            payload.update(extra_payload)

        resp = request_json(
            url=url,
            method="POST",
            headers={"content-type": "application/json", **self._headers()},
            json_payload=payload,
            timeout_seconds=timeout_seconds,
        )

        data_list = resp.get("data") or []
        for item in data_list:
            if not isinstance(item, dict):
                continue
            b64 = item.get("b64_json") or item.get("b64") or item.get("image_base64")
            if b64:
                image = base64.b64decode(b64)
                return image, _guess_mime_from_bytes(image), resp
            url_field = item.get("url") or item.get("image_url")
            if url_field:
                image = request_bytes(
                    url=str(url_field),
                    method="GET",
                    headers=self._headers(),
                    timeout_seconds=max(60.0, float(timeout_seconds)),
                )
                return image, _guess_mime_from_bytes(image), resp

        raise ValueError("No image data found in SeaDream response.")

