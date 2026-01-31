"""Webhook configuration and management."""

from __future__ import annotations

from typing import Any


class Webhooks:
    """Webhook configuration and management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        url: str,
        events: list[str],
        description: str | None = None,
        enabled: bool | None = None,
    ) -> dict[str, Any]:
        """Create a new webhook.

        Args:
            url: Webhook endpoint URL.
            events: Events to subscribe to.
            description: Optional description.
            enabled: Whether the webhook is enabled (default: True).

        Returns:
            Webhook object with signing secret.
        """
        body: dict[str, Any] = {"url": url, "events": events}
        if description is not None:
            body["description"] = description
        if enabled is not None:
            body["enabled"] = enabled

        response = self._http.post("/v1/webhooks", body)
        return response["data"]

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all webhooks.

        Returns:
            Paginated response with webhook data.
        """
        return self._http.get("/v1/webhooks", {"limit": limit, "cursor": cursor})

    def get(self, webhook_id: str) -> dict[str, Any]:
        """Get a single webhook by ID.

        Args:
            webhook_id: The webhook ID.

        Returns:
            Webhook object.
        """
        response = self._http.get(f"/v1/webhooks/{webhook_id}")
        return response["data"]

    def update(
        self,
        webhook_id: str,
        *,
        url: str | None = None,
        events: list[str] | None = None,
        description: str | None = None,
        enabled: bool | None = None,
    ) -> dict[str, Any]:
        """Update a webhook.

        Args:
            webhook_id: The webhook ID.
            url: New URL.
            events: New event list.
            description: New description.
            enabled: New enabled state.

        Returns:
            Updated webhook object.
        """
        body: dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if description is not None:
            body["description"] = description
        if enabled is not None:
            body["enabled"] = enabled

        response = self._http.patch(f"/v1/webhooks/{webhook_id}", body)
        return response["data"]

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook.

        Args:
            webhook_id: The webhook ID.
        """
        self._http.delete(f"/v1/webhooks/{webhook_id}")

    def test(self, webhook_id: str) -> dict[str, Any]:
        """Test a webhook by sending a test event.

        Args:
            webhook_id: The webhook ID.

        Returns:
            Test result with success, statusCode, responseTime.
        """
        response = self._http.post(f"/v1/webhooks/{webhook_id}/test")
        return response["data"]

    def rotate_secret(self, webhook_id: str) -> dict[str, Any]:
        """Rotate the webhook signing secret.

        Args:
            webhook_id: The webhook ID.

        Returns:
            Webhook object with new secret.
        """
        response = self._http.post(f"/v1/webhooks/{webhook_id}/rotate-secret")
        return response["data"]


class AsyncWebhooks:
    """Async webhook configuration and management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        url: str,
        events: list[str],
        description: str | None = None,
        enabled: bool | None = None,
    ) -> dict[str, Any]:
        """Create a new webhook (async)."""
        body: dict[str, Any] = {"url": url, "events": events}
        if description is not None:
            body["description"] = description
        if enabled is not None:
            body["enabled"] = enabled

        response = await self._http.post("/v1/webhooks", body)
        return response["data"]

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all webhooks (async)."""
        return await self._http.get("/v1/webhooks", {"limit": limit, "cursor": cursor})

    async def get(self, webhook_id: str) -> dict[str, Any]:
        """Get a single webhook by ID (async)."""
        response = await self._http.get(f"/v1/webhooks/{webhook_id}")
        return response["data"]

    async def update(
        self,
        webhook_id: str,
        *,
        url: str | None = None,
        events: list[str] | None = None,
        description: str | None = None,
        enabled: bool | None = None,
    ) -> dict[str, Any]:
        """Update a webhook (async)."""
        body: dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if events is not None:
            body["events"] = events
        if description is not None:
            body["description"] = description
        if enabled is not None:
            body["enabled"] = enabled

        response = await self._http.patch(f"/v1/webhooks/{webhook_id}", body)
        return response["data"]

    async def delete(self, webhook_id: str) -> None:
        """Delete a webhook (async)."""
        await self._http.delete(f"/v1/webhooks/{webhook_id}")

    async def test(self, webhook_id: str) -> dict[str, Any]:
        """Test a webhook (async)."""
        response = await self._http.post(f"/v1/webhooks/{webhook_id}/test")
        return response["data"]

    async def rotate_secret(self, webhook_id: str) -> dict[str, Any]:
        """Rotate the webhook signing secret (async)."""
        response = await self._http.post(f"/v1/webhooks/{webhook_id}/rotate-secret")
        return response["data"]
