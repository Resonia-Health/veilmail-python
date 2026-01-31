"""Geo and device analytics."""

from __future__ import annotations

from typing import Any


class Analytics:
    """Geo and device analytics."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def geo(
        self,
        *,
        days: int | None = None,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get organization-level geo analytics.

        Args:
            days: Number of days to look back (max 90, default 30).
            event_type: Filter by event type ('OPENED' or 'CLICKED', default 'OPENED').

        Returns:
            Geo analytics data with country breakdowns.
        """
        return self._http.get("/v1/analytics/geo", {
            "days": days,
            "eventType": event_type,
        })

    def devices(
        self,
        *,
        days: int | None = None,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get organization-level device analytics.

        Args:
            days: Number of days to look back (max 90, default 30).
            event_type: Filter by event type ('OPENED' or 'CLICKED', default 'OPENED').

        Returns:
            Device analytics data with type, OS, browser breakdowns.
        """
        return self._http.get("/v1/analytics/devices", {
            "days": days,
            "eventType": event_type,
        })

    def campaign_geo(
        self,
        campaign_id: str,
        *,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get campaign-level geo analytics.

        Args:
            campaign_id: The campaign ID.
            event_type: Filter by event type ('OPENED' or 'CLICKED').

        Returns:
            Geo analytics data for the campaign.
        """
        return self._http.get(
            f"/v1/campaigns/{campaign_id}/analytics/geo",
            {"eventType": event_type},
        )

    def campaign_devices(
        self,
        campaign_id: str,
        *,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get campaign-level device analytics.

        Args:
            campaign_id: The campaign ID.
            event_type: Filter by event type ('OPENED' or 'CLICKED').

        Returns:
            Device analytics data for the campaign.
        """
        return self._http.get(
            f"/v1/campaigns/{campaign_id}/analytics/devices",
            {"eventType": event_type},
        )


class AsyncAnalytics:
    """Async geo and device analytics."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def geo(
        self,
        *,
        days: int | None = None,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get organization-level geo analytics (async)."""
        return await self._http.get("/v1/analytics/geo", {
            "days": days,
            "eventType": event_type,
        })

    async def devices(
        self,
        *,
        days: int | None = None,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get organization-level device analytics (async)."""
        return await self._http.get("/v1/analytics/devices", {
            "days": days,
            "eventType": event_type,
        })

    async def campaign_geo(
        self,
        campaign_id: str,
        *,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get campaign-level geo analytics (async)."""
        return await self._http.get(
            f"/v1/campaigns/{campaign_id}/analytics/geo",
            {"eventType": event_type},
        )

    async def campaign_devices(
        self,
        campaign_id: str,
        *,
        event_type: str | None = None,
    ) -> dict[str, Any]:
        """Get campaign-level device analytics (async)."""
        return await self._http.get(
            f"/v1/campaigns/{campaign_id}/analytics/devices",
            {"eventType": event_type},
        )
