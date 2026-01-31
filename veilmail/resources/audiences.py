"""Audience and subscriber management."""

from __future__ import annotations

from typing import Any


class Subscribers:
    """Subscriber management within an audience."""

    def __init__(self, http: Any, audience_id: str) -> None:
        self._http = http
        self._audience_id = audience_id

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        status: str | None = None,
        email: str | None = None,
    ) -> dict[str, Any]:
        """List subscribers in the audience.

        Args:
            limit: Number of items per page.
            cursor: Cursor for pagination.
            status: Filter by status.
            email: Search by email.

        Returns:
            Paginated response with subscriber data.
        """
        return self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers",
            {"limit": limit, "cursor": cursor, "status": status, "email": email},
        )

    def add(
        self,
        *,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        double_opt_in: bool | None = None,
        status: str | None = None,
        consent_type: str | None = None,
        consent_source: str | None = None,
        consent_date: str | None = None,
        consent_expires_at: str | None = None,
        consent_proof: str | None = None,
    ) -> dict[str, Any]:
        """Add a subscriber to the audience.

        Args:
            email: Subscriber email address.
            first_name: First name.
            last_name: Last name.
            metadata: Custom metadata.
            double_opt_in: Create with 'pending' status for double opt-in.
            status: Explicit status override.
            consent_type: CASL consent type.
            consent_source: How consent was obtained.
            consent_date: When consent was granted (ISO 8601).
            consent_expires_at: When implied consent expires (ISO 8601).
            consent_proof: Evidence of consent.

        Returns:
            Subscriber object.
        """
        body: dict[str, Any] = {"email": email}
        if first_name is not None:
            body["firstName"] = first_name
        if last_name is not None:
            body["lastName"] = last_name
        if metadata is not None:
            body["metadata"] = metadata
        if double_opt_in is not None:
            body["doubleOptIn"] = double_opt_in
        if status is not None:
            body["status"] = status
        if consent_type is not None:
            body["consentType"] = consent_type
        if consent_source is not None:
            body["consentSource"] = consent_source
        if consent_date is not None:
            body["consentDate"] = consent_date
        if consent_expires_at is not None:
            body["consentExpiresAt"] = consent_expires_at
        if consent_proof is not None:
            body["consentProof"] = consent_proof

        response = self._http.post(
            f"/v1/audiences/{self._audience_id}/subscribers", body
        )
        return response["data"]

    def get(self, subscriber_id: str) -> dict[str, Any]:
        """Get a subscriber by ID.

        Args:
            subscriber_id: The subscriber ID.

        Returns:
            Subscriber object.
        """
        response = self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}"
        )
        return response["data"]

    def update(
        self,
        subscriber_id: str,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        """Update a subscriber.

        Args:
            subscriber_id: The subscriber ID.
            first_name: New first name.
            last_name: New last name.
            metadata: New metadata.
            status: New status.

        Returns:
            Updated subscriber object.
        """
        body: dict[str, Any] = {}
        if first_name is not None:
            body["firstName"] = first_name
        if last_name is not None:
            body["lastName"] = last_name
        if metadata is not None:
            body["metadata"] = metadata
        if status is not None:
            body["status"] = status

        response = self._http.put(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}", body
        )
        return response["data"]

    def remove(self, subscriber_id: str) -> None:
        """Remove a subscriber from the audience.

        Args:
            subscriber_id: The subscriber ID.
        """
        self._http.delete(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}"
        )

    def confirm(self, subscriber_id: str) -> dict[str, Any]:
        """Confirm a pending subscriber (double opt-in flow).

        Args:
            subscriber_id: The subscriber ID.

        Returns:
            Confirmed subscriber object.
        """
        response = self._http.post(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}/confirm",
            {},
        )
        return response["data"]

    def import_subscribers(
        self,
        *,
        subscribers: list[dict[str, Any]] | None = None,
        csv_data: str | None = None,
    ) -> dict[str, Any]:
        """Bulk import subscribers.

        Provide either a list of subscriber dicts or a CSV string.

        Args:
            subscribers: Array of subscriber objects to import.
            csv_data: Raw CSV string with header row.

        Returns:
            Import result with total, created, updated, skipped counts.
        """
        body: dict[str, Any] = {}
        if subscribers is not None:
            body["subscribers"] = subscribers
        if csv_data is not None:
            body["csvData"] = csv_data

        return self._http.post(
            f"/v1/audiences/{self._audience_id}/subscribers/import", body
        )

    def export(self, *, status: str | None = None) -> str:
        """Export subscribers as CSV.

        Args:
            status: Filter by subscriber status.

        Returns:
            CSV string of subscribers.
        """
        return self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers/export",
            {"status": status},
        )

    def activity(
        self,
        subscriber_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        type: str | None = None,
    ) -> dict[str, Any]:
        """Get subscriber activity timeline.

        Args:
            subscriber_id: The subscriber ID.
            limit: Number of items per page.
            cursor: Cursor for pagination.
            type: Filter by event type.

        Returns:
            Paginated response with activity events.
        """
        return self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}/activity",
            {"limit": limit, "cursor": cursor, "type": type},
        )


class Audiences:
    """Audience and subscriber management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(self, *, name: str, description: str | None = None) -> dict[str, Any]:
        """Create a new audience.

        Args:
            name: Audience name.
            description: Audience description.

        Returns:
            Audience object.
        """
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description

        response = self._http.post("/v1/audiences", body)
        return response["data"]

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all audiences.

        Returns:
            Paginated response with audience data.
        """
        return self._http.get("/v1/audiences", {"limit": limit, "cursor": cursor})

    def get(self, audience_id: str) -> dict[str, Any]:
        """Get a single audience by ID.

        Args:
            audience_id: The audience ID.

        Returns:
            Audience object.
        """
        response = self._http.get(f"/v1/audiences/{audience_id}")
        return response["data"]

    def update(
        self,
        audience_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Update an audience.

        Args:
            audience_id: The audience ID.
            name: New name.
            description: New description.

        Returns:
            Updated audience object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description

        response = self._http.put(f"/v1/audiences/{audience_id}", body)
        return response["data"]

    def delete(self, audience_id: str) -> None:
        """Delete an audience.

        Args:
            audience_id: The audience ID.
        """
        self._http.delete(f"/v1/audiences/{audience_id}")

    def subscribers(self, audience_id: str) -> Subscribers:
        """Get a subscribers helper for an audience.

        Args:
            audience_id: The audience ID.

        Returns:
            Subscribers instance for the audience.
        """
        return Subscribers(self._http, audience_id)

    def recalculate_engagement(self, audience_id: str) -> dict[str, Any]:
        """Recalculate engagement scores for all subscribers in an audience.

        Args:
            audience_id: The audience ID.

        Returns:
            Result with processed count.
        """
        return self._http.post(
            f"/v1/audiences/{audience_id}/recalculate-engagement", {}
        )

    def get_engagement_stats(self, audience_id: str) -> dict[str, Any]:
        """Get engagement statistics for an audience.

        Args:
            audience_id: The audience ID.

        Returns:
            Engagement stats with distribution and average score.
        """
        return self._http.get(
            f"/v1/audiences/{audience_id}/engagement-stats"
        )


class AsyncSubscribers:
    """Async subscriber management within an audience."""

    def __init__(self, http: Any, audience_id: str) -> None:
        self._http = http
        self._audience_id = audience_id

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        status: str | None = None,
        email: str | None = None,
    ) -> dict[str, Any]:
        """List subscribers in the audience (async)."""
        return await self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers",
            {"limit": limit, "cursor": cursor, "status": status, "email": email},
        )

    async def add(
        self,
        *,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        double_opt_in: bool | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        """Add a subscriber to the audience (async)."""
        body: dict[str, Any] = {"email": email}
        if first_name is not None:
            body["firstName"] = first_name
        if last_name is not None:
            body["lastName"] = last_name
        if metadata is not None:
            body["metadata"] = metadata
        if double_opt_in is not None:
            body["doubleOptIn"] = double_opt_in
        if status is not None:
            body["status"] = status

        response = await self._http.post(
            f"/v1/audiences/{self._audience_id}/subscribers", body
        )
        return response["data"]

    async def get(self, subscriber_id: str) -> dict[str, Any]:
        """Get a subscriber by ID (async)."""
        response = await self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}"
        )
        return response["data"]

    async def update(
        self,
        subscriber_id: str,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        """Update a subscriber (async)."""
        body: dict[str, Any] = {}
        if first_name is not None:
            body["firstName"] = first_name
        if last_name is not None:
            body["lastName"] = last_name
        if metadata is not None:
            body["metadata"] = metadata
        if status is not None:
            body["status"] = status

        response = await self._http.put(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}", body
        )
        return response["data"]

    async def remove(self, subscriber_id: str) -> None:
        """Remove a subscriber from the audience (async)."""
        await self._http.delete(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}"
        )

    async def confirm(self, subscriber_id: str) -> dict[str, Any]:
        """Confirm a pending subscriber (async)."""
        response = await self._http.post(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}/confirm",
            {},
        )
        return response["data"]

    async def import_subscribers(
        self,
        *,
        subscribers: list[dict[str, Any]] | None = None,
        csv_data: str | None = None,
    ) -> dict[str, Any]:
        """Bulk import subscribers (async)."""
        body: dict[str, Any] = {}
        if subscribers is not None:
            body["subscribers"] = subscribers
        if csv_data is not None:
            body["csvData"] = csv_data

        return await self._http.post(
            f"/v1/audiences/{self._audience_id}/subscribers/import", body
        )

    async def export(self, *, status: str | None = None) -> str:
        """Export subscribers as CSV (async)."""
        return await self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers/export",
            {"status": status},
        )

    async def activity(
        self,
        subscriber_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        type: str | None = None,
    ) -> dict[str, Any]:
        """Get subscriber activity timeline (async)."""
        return await self._http.get(
            f"/v1/audiences/{self._audience_id}/subscribers/{subscriber_id}/activity",
            {"limit": limit, "cursor": cursor, "type": type},
        )


class AsyncAudiences:
    """Async audience and subscriber management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(self, *, name: str, description: str | None = None) -> dict[str, Any]:
        """Create a new audience (async)."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description

        response = await self._http.post("/v1/audiences", body)
        return response["data"]

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all audiences (async)."""
        return await self._http.get("/v1/audiences", {"limit": limit, "cursor": cursor})

    async def get(self, audience_id: str) -> dict[str, Any]:
        """Get a single audience by ID (async)."""
        response = await self._http.get(f"/v1/audiences/{audience_id}")
        return response["data"]

    async def update(
        self,
        audience_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Update an audience (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description

        response = await self._http.put(f"/v1/audiences/{audience_id}", body)
        return response["data"]

    async def delete(self, audience_id: str) -> None:
        """Delete an audience (async)."""
        await self._http.delete(f"/v1/audiences/{audience_id}")

    def subscribers(self, audience_id: str) -> AsyncSubscribers:
        """Get an async subscribers helper for an audience."""
        return AsyncSubscribers(self._http, audience_id)

    async def recalculate_engagement(self, audience_id: str) -> dict[str, Any]:
        """Recalculate engagement scores (async)."""
        return await self._http.post(
            f"/v1/audiences/{audience_id}/recalculate-engagement", {}
        )

    async def get_engagement_stats(self, audience_id: str) -> dict[str, Any]:
        """Get engagement statistics (async)."""
        return await self._http.get(
            f"/v1/audiences/{audience_id}/engagement-stats"
        )
