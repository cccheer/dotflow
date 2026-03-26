import logging

import httpx

from app.core.config import settings


logger = logging.getLogger(__name__)


class DotClient:
    def __init__(self) -> None:
        self._mock = settings.dot_api_mock
        self._base_url = settings.dot_api_base_url.rstrip("/")
        self._timeout = settings.dot_api_timeout_seconds
        self._headers = {"Authorization": f"Bearer {settings.dot_api_key}"} if settings.dot_api_key else {}

    def list_devices(self) -> list[dict]:
        if self._mock:
            return [
                {"id": "dot-001", "name": "Mock Dot 1", "api_base_url": self._base_url},
                {"id": "dot-002", "name": "Mock Dot 2", "api_base_url": self._base_url},
            ]

        response = self._request("GET", "/api/authV2/open/devices")
        return response.get("devices", [])

    def get_device_status(self, device_id: str) -> dict:
        if self._mock:
            return {"id": device_id, "status": "online"}

        return self._request("GET", f"/api/authV2/open/device/{device_id}/status")

    def push_text(self, device_id: str, payload: dict) -> dict:
        if self._mock:
            logger.info("Mock push text to device %s", device_id)
            return {"ok": True, "deviceId": device_id, "echo": payload}

        return self._request("POST", f"/api/authV2/open/device/{device_id}/text", json=payload)

    def push_image(self, device_id: str, payload: dict) -> dict:
        if self._mock:
            logger.info("Mock push image to device %s", device_id)
            return {"ok": True, "deviceId": device_id, "echo": payload}

        return self._request("POST", f"/api/authV2/open/device/{device_id}/image", json=payload)

    def _request(self, method: str, path: str, json: dict | None = None) -> dict:
        url = f"{self._base_url}{path}"
        with httpx.Client(timeout=self._timeout, headers=self._headers) as client:
            response = client.request(method=method, url=url, json=json)
            response.raise_for_status()
            return response.json()
