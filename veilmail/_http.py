"""HTTP client for Veil Mail API requests."""

from __future__ import annotations

from typing import Any

import httpx

from .errors import (
    NetworkError,
    TimeoutError,
    _parse_error_response,
)

DEFAULT_BASE_URL = "https://api.veilmail.xyz"
DEFAULT_TIMEOUT = 30.0
SDK_VERSION = "0.1.0"


def _to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _convert_keys(obj: Any) -> Any:
    """Recursively convert dict keys from snake_case to camelCase."""
    if isinstance(obj, dict):
        result: dict[str, Any] = {}
        for key, value in obj.items():
            # Handle special "from_" -> "from" mapping
            if key == "from_":
                camel_key = "from"
            else:
                camel_key = _to_camel(key)
            result[camel_key] = _convert_keys(value)
        return result
    if isinstance(obj, list):
        return [_convert_keys(item) for item in obj]
    return obj


class HttpClient:
    """Synchronous HTTP client for the Veil Mail API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not api_key:
            raise ValueError("API key is required")
        if not api_key.startswith(("veil_live_", "veil_test_")):
            raise ValueError(
                "Invalid API key format. API keys should start with veil_live_ or veil_test_"
            )

        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"veilmail-python/{SDK_VERSION}",
            },
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> Any:
        """Make an HTTP request to the API."""
        # Filter out None values from query params
        params = {k: v for k, v in (query or {}).items() if v is not None}
        json_body = _convert_keys(body) if body else None

        try:
            response = self._client.request(
                method,
                path,
                json=json_body,
                params=params or None,
            )
        except httpx.TimeoutException:
            raise TimeoutError(self._client.timeout.connect or DEFAULT_TIMEOUT)
        except httpx.ConnectError as e:
            raise NetworkError(f"Network error: {e}") from e

        if response.status_code == 204:
            return None

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            body_data = response.json()
        else:
            return response.text

        if not response.is_success:
            headers = dict(response.headers)
            raise _parse_error_response(response.status_code, body_data, headers)

        return body_data

    def get(self, path: str, query: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, query=query)

    def post(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return self.request("POST", path, body=body)

    def patch(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return self.request("PATCH", path, body=body)

    def put(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return self.request("PUT", path, body=body)

    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)


class AsyncHttpClient:
    """Asynchronous HTTP client for the Veil Mail API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not api_key:
            raise ValueError("API key is required")
        if not api_key.startswith(("veil_live_", "veil_test_")):
            raise ValueError(
                "Invalid API key format. API keys should start with veil_live_ or veil_test_"
            )

        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"veilmail-python/{SDK_VERSION}",
            },
        )

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> Any:
        """Make an async HTTP request to the API."""
        params = {k: v for k, v in (query or {}).items() if v is not None}
        json_body = _convert_keys(body) if body else None

        try:
            response = await self._client.request(
                method,
                path,
                json=json_body,
                params=params or None,
            )
        except httpx.TimeoutException:
            raise TimeoutError(self._client.timeout.connect or DEFAULT_TIMEOUT)
        except httpx.ConnectError as e:
            raise NetworkError(f"Network error: {e}") from e

        if response.status_code == 204:
            return None

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            body_data = response.json()
        else:
            return response.text

        if not response.is_success:
            headers = dict(response.headers)
            raise _parse_error_response(response.status_code, body_data, headers)

        return body_data

    async def get(self, path: str, query: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, query=query)

    async def post(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return await self.request("POST", path, body=body)

    async def patch(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return await self.request("PATCH", path, body=body)

    async def put(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return await self.request("PUT", path, body=body)

    async def delete(self, path: str) -> Any:
        return await self.request("DELETE", path)
