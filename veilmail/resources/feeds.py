"""RSS feed management."""

from __future__ import annotations

from typing import Any


class Feeds:
    """RSS feed management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        url: str,
        audience_id: str,
        poll_interval: str = "daily",
        mode: str = "single",
        subject_template: str | None = None,
        html_template: str | None = None,
    ) -> dict[str, Any]:
        """Create a new RSS feed.

        Args:
            name: Feed name.
            url: RSS feed URL.
            audience_id: Target audience ID.
            poll_interval: Poll interval ('hourly', 'daily', 'weekly').
            mode: Feed mode ('single' or 'digest').
            subject_template: Subject line template with variables.
            html_template: HTML template with feed variables.

        Returns:
            Feed object.
        """
        body: dict[str, Any] = {
            "name": name,
            "url": url,
            "audienceId": audience_id,
            "pollInterval": poll_interval,
            "mode": mode,
        }
        if subject_template is not None:
            body["subjectTemplate"] = subject_template
        if html_template is not None:
            body["htmlTemplate"] = html_template

        return self._http.post("/v1/feeds", body)

    def list(self) -> dict[str, Any]:
        """List all RSS feeds.

        Returns:
            Response with feed data.
        """
        return self._http.get("/v1/feeds")

    def get(self, feed_id: str) -> dict[str, Any]:
        """Get a single feed by ID (includes recent items).

        Args:
            feed_id: The feed ID.

        Returns:
            Feed object with recentItems.
        """
        return self._http.get(f"/v1/feeds/{feed_id}")

    def update(
        self,
        feed_id: str,
        *,
        name: str | None = None,
        url: str | None = None,
        poll_interval: str | None = None,
        mode: str | None = None,
        subject_template: str | None = None,
        html_template: str | None = None,
    ) -> dict[str, Any]:
        """Update a feed.

        Args:
            feed_id: The feed ID.

        Returns:
            Updated feed object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if url is not None:
            body["url"] = url
        if poll_interval is not None:
            body["pollInterval"] = poll_interval
        if mode is not None:
            body["mode"] = mode
        if subject_template is not None:
            body["subjectTemplate"] = subject_template
        if html_template is not None:
            body["htmlTemplate"] = html_template

        return self._http.put(f"/v1/feeds/{feed_id}", body)

    def delete(self, feed_id: str) -> dict[str, Any]:
        """Delete a feed and all its items."""
        return self._http.delete(f"/v1/feeds/{feed_id}")

    def poll(self, feed_id: str) -> dict[str, Any]:
        """Manually trigger a feed poll.

        Returns:
            Result with success and newItems count.
        """
        return self._http.post(f"/v1/feeds/{feed_id}/poll")

    def pause(self, feed_id: str) -> dict[str, Any]:
        """Pause an active feed."""
        return self._http.post(f"/v1/feeds/{feed_id}/pause")

    def resume(self, feed_id: str) -> dict[str, Any]:
        """Resume a paused or errored feed."""
        return self._http.post(f"/v1/feeds/{feed_id}/resume")

    def list_items(
        self,
        feed_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        processed: bool | None = None,
    ) -> dict[str, Any]:
        """List feed items with pagination.

        Args:
            feed_id: The feed ID.
            limit: Number of items per page.
            cursor: Cursor for pagination.
            processed: Filter by processed status.

        Returns:
            Paginated response with feed item data.
        """
        params: dict[str, Any] = {"limit": limit, "cursor": cursor}
        if processed is not None:
            params["processed"] = str(processed).lower()

        return self._http.get(f"/v1/feeds/{feed_id}/items", params)


class AsyncFeeds:
    """Async RSS feed management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        name: str,
        url: str,
        audience_id: str,
        poll_interval: str = "daily",
        mode: str = "single",
        subject_template: str | None = None,
        html_template: str | None = None,
    ) -> dict[str, Any]:
        """Create a new RSS feed (async)."""
        body: dict[str, Any] = {
            "name": name,
            "url": url,
            "audienceId": audience_id,
            "pollInterval": poll_interval,
            "mode": mode,
        }
        if subject_template is not None:
            body["subjectTemplate"] = subject_template
        if html_template is not None:
            body["htmlTemplate"] = html_template

        return await self._http.post("/v1/feeds", body)

    async def list(self) -> dict[str, Any]:
        """List all RSS feeds (async)."""
        return await self._http.get("/v1/feeds")

    async def get(self, feed_id: str) -> dict[str, Any]:
        """Get a single feed by ID (async)."""
        return await self._http.get(f"/v1/feeds/{feed_id}")

    async def update(
        self,
        feed_id: str,
        *,
        name: str | None = None,
        url: str | None = None,
        poll_interval: str | None = None,
        mode: str | None = None,
        subject_template: str | None = None,
        html_template: str | None = None,
    ) -> dict[str, Any]:
        """Update a feed (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if url is not None:
            body["url"] = url
        if poll_interval is not None:
            body["pollInterval"] = poll_interval
        if mode is not None:
            body["mode"] = mode
        if subject_template is not None:
            body["subjectTemplate"] = subject_template
        if html_template is not None:
            body["htmlTemplate"] = html_template

        return await self._http.put(f"/v1/feeds/{feed_id}", body)

    async def delete(self, feed_id: str) -> dict[str, Any]:
        """Delete a feed (async)."""
        return await self._http.delete(f"/v1/feeds/{feed_id}")

    async def poll(self, feed_id: str) -> dict[str, Any]:
        """Manually trigger a feed poll (async)."""
        return await self._http.post(f"/v1/feeds/{feed_id}/poll")

    async def pause(self, feed_id: str) -> dict[str, Any]:
        """Pause an active feed (async)."""
        return await self._http.post(f"/v1/feeds/{feed_id}/pause")

    async def resume(self, feed_id: str) -> dict[str, Any]:
        """Resume a paused or errored feed (async)."""
        return await self._http.post(f"/v1/feeds/{feed_id}/resume")

    async def list_items(
        self,
        feed_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        processed: bool | None = None,
    ) -> dict[str, Any]:
        """List feed items with pagination (async)."""
        params: dict[str, Any] = {"limit": limit, "cursor": cursor}
        if processed is not None:
            params["processed"] = str(processed).lower()

        return await self._http.get(f"/v1/feeds/{feed_id}/items", params)
