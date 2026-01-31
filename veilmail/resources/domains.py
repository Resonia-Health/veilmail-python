"""Domain verification and management."""

from __future__ import annotations

from typing import Any


class Domains:
    """Domain verification and management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(self, *, domain: str) -> dict[str, Any]:
        """Add a new domain for verification.

        Args:
            domain: Domain name (e.g., mail.example.com).

        Returns:
            Domain object with DNS records to configure.
        """
        response = self._http.post("/v1/domains", {"domain": domain})
        return response["data"]

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all domains.

        Returns:
            Paginated response with domain data.
        """
        return self._http.get("/v1/domains", {"limit": limit, "cursor": cursor})

    def get(self, domain_id: str) -> dict[str, Any]:
        """Get a single domain by ID.

        Args:
            domain_id: The domain ID.

        Returns:
            Domain object.
        """
        response = self._http.get(f"/v1/domains/{domain_id}")
        return response["data"]

    def update(
        self,
        domain_id: str,
        *,
        track_opens: bool | None = None,
        track_clicks: bool | None = None,
    ) -> dict[str, Any]:
        """Update domain settings.

        Args:
            domain_id: The domain ID.
            track_opens: Enable/disable open tracking.
            track_clicks: Enable/disable click tracking.

        Returns:
            Updated domain object.
        """
        body: dict[str, Any] = {}
        if track_opens is not None:
            body["trackOpens"] = track_opens
        if track_clicks is not None:
            body["trackClicks"] = track_clicks
        return self._http.patch(f"/v1/domains/{domain_id}", body)

    def verify(self, domain_id: str) -> dict[str, Any]:
        """Trigger domain verification.

        Args:
            domain_id: The domain ID.

        Returns:
            Domain object with updated status.
        """
        response = self._http.post(f"/v1/domains/{domain_id}/verify")
        return response["data"]

    def delete(self, domain_id: str) -> None:
        """Delete a domain.

        Args:
            domain_id: The domain ID.
        """
        self._http.delete(f"/v1/domains/{domain_id}")


class AsyncDomains:
    """Async domain verification and management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(self, *, domain: str) -> dict[str, Any]:
        """Add a new domain for verification (async)."""
        response = await self._http.post("/v1/domains", {"domain": domain})
        return response["data"]

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all domains (async)."""
        return await self._http.get("/v1/domains", {"limit": limit, "cursor": cursor})

    async def get(self, domain_id: str) -> dict[str, Any]:
        """Get a single domain by ID (async)."""
        response = await self._http.get(f"/v1/domains/{domain_id}")
        return response["data"]

    async def update(
        self,
        domain_id: str,
        *,
        track_opens: bool | None = None,
        track_clicks: bool | None = None,
    ) -> dict[str, Any]:
        """Update domain settings (async)."""
        body: dict[str, Any] = {}
        if track_opens is not None:
            body["trackOpens"] = track_opens
        if track_clicks is not None:
            body["trackClicks"] = track_clicks
        return await self._http.patch(f"/v1/domains/{domain_id}", body)

    async def verify(self, domain_id: str) -> dict[str, Any]:
        """Trigger domain verification (async)."""
        response = await self._http.post(f"/v1/domains/{domain_id}/verify")
        return response["data"]

    async def delete(self, domain_id: str) -> None:
        """Delete a domain (async)."""
        await self._http.delete(f"/v1/domains/{domain_id}")
