"""Subscription topic management."""

from __future__ import annotations

from typing import Any


class Topics:
    """Subscription topic management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        is_default: bool | None = None,
        sort_order: int | None = None,
    ) -> dict[str, Any]:
        """Create a subscription topic.

        Args:
            name: Topic name.
            description: Topic description.
            is_default: Whether new subscribers are subscribed by default.
            sort_order: Sort order for display.

        Returns:
            Topic object.
        """
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if is_default is not None:
            body["isDefault"] = is_default
        if sort_order is not None:
            body["sortOrder"] = sort_order

        return self._http.post("/v1/topics", body)

    def list(self, *, active: bool | None = None) -> dict[str, Any]:
        """List all subscription topics.

        Args:
            active: Filter by active status.

        Returns:
            Response with topic data.
        """
        return self._http.get("/v1/topics", {"active": active})

    def get(self, topic_id: str) -> dict[str, Any]:
        """Get a single topic by ID.

        Args:
            topic_id: The topic ID.

        Returns:
            Topic object.
        """
        return self._http.get(f"/v1/topics/{topic_id}")

    def update(
        self,
        topic_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        is_default: bool | None = None,
        sort_order: int | None = None,
        active: bool | None = None,
    ) -> dict[str, Any]:
        """Update a subscription topic.

        Args:
            topic_id: The topic ID.
            name: New name.
            description: New description.
            is_default: New default state.
            sort_order: New sort order.
            active: New active state.

        Returns:
            Updated topic object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if is_default is not None:
            body["isDefault"] = is_default
        if sort_order is not None:
            body["sortOrder"] = sort_order
        if active is not None:
            body["active"] = active

        return self._http.patch(f"/v1/topics/{topic_id}", body)

    def delete(self, topic_id: str) -> None:
        """Deactivate a subscription topic (soft delete).

        Args:
            topic_id: The topic ID.
        """
        self._http.delete(f"/v1/topics/{topic_id}")

    def get_preferences(
        self,
        audience_id: str,
        subscriber_id: str,
    ) -> dict[str, Any]:
        """Get a subscriber's topic preferences.

        Args:
            audience_id: The audience ID.
            subscriber_id: The subscriber ID.

        Returns:
            Response with topic preference data.
        """
        return self._http.get(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/topics"
        )

    def set_preferences(
        self,
        audience_id: str,
        subscriber_id: str,
        *,
        topics: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set a subscriber's topic preferences.

        Args:
            audience_id: The audience ID.
            subscriber_id: The subscriber ID.
            topics: List of {topicId, subscribed} dicts.

        Returns:
            Response with updated topic preferences.
        """
        return self._http.put(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/topics",
            {"topics": topics},
        )


class AsyncTopics:
    """Async subscription topic management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        is_default: bool | None = None,
        sort_order: int | None = None,
    ) -> dict[str, Any]:
        """Create a subscription topic (async)."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if is_default is not None:
            body["isDefault"] = is_default
        if sort_order is not None:
            body["sortOrder"] = sort_order

        return await self._http.post("/v1/topics", body)

    async def list(self, *, active: bool | None = None) -> dict[str, Any]:
        """List all subscription topics (async)."""
        return await self._http.get("/v1/topics", {"active": active})

    async def get(self, topic_id: str) -> dict[str, Any]:
        """Get a single topic by ID (async)."""
        return await self._http.get(f"/v1/topics/{topic_id}")

    async def update(
        self,
        topic_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        is_default: bool | None = None,
        sort_order: int | None = None,
        active: bool | None = None,
    ) -> dict[str, Any]:
        """Update a subscription topic (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if is_default is not None:
            body["isDefault"] = is_default
        if sort_order is not None:
            body["sortOrder"] = sort_order
        if active is not None:
            body["active"] = active

        return await self._http.patch(f"/v1/topics/{topic_id}", body)

    async def delete(self, topic_id: str) -> None:
        """Deactivate a subscription topic (async)."""
        await self._http.delete(f"/v1/topics/{topic_id}")

    async def get_preferences(
        self,
        audience_id: str,
        subscriber_id: str,
    ) -> dict[str, Any]:
        """Get a subscriber's topic preferences (async)."""
        return await self._http.get(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/topics"
        )

    async def set_preferences(
        self,
        audience_id: str,
        subscriber_id: str,
        *,
        topics: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Set a subscriber's topic preferences (async)."""
        return await self._http.put(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/topics",
            {"topics": topics},
        )
