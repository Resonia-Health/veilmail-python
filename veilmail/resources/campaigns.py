"""Campaign management."""

from __future__ import annotations

from typing import Any


class Campaigns:
    """Campaign management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        subject: str,
        from_: str | dict[str, str],
        audience_id: str,
        reply_to: str | dict[str, str] | None = None,
        template_id: str | None = None,
        html: str | None = None,
        text: str | None = None,
        variables: dict[str, Any] | None = None,
        preview_text: str | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new campaign.

        Args:
            name: Campaign name.
            subject: Email subject.
            from_: Sender email address or {email, name} dict.
            audience_id: Target audience ID.
            reply_to: Reply-to address.
            template_id: Template ID.
            html: HTML content.
            text: Plain text content.
            variables: Template variables.
            preview_text: Preview text.
            tags: Tags for categorization.

        Returns:
            Campaign object.
        """
        body: dict[str, Any] = {
            "name": name,
            "subject": subject,
            "from": from_,
            "audienceId": audience_id,
        }
        if reply_to is not None:
            body["replyTo"] = reply_to
        if template_id is not None:
            body["templateId"] = template_id
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if variables is not None:
            body["variables"] = variables
        if preview_text is not None:
            body["previewText"] = preview_text
        if tags is not None:
            body["tags"] = tags

        response = self._http.post("/v1/campaigns", body)
        return response["data"]

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all campaigns.

        Returns:
            Paginated response with campaign data.
        """
        return self._http.get("/v1/campaigns", {"limit": limit, "cursor": cursor})

    def get(self, campaign_id: str) -> dict[str, Any]:
        """Get a single campaign by ID.

        Args:
            campaign_id: The campaign ID.

        Returns:
            Campaign object.
        """
        response = self._http.get(f"/v1/campaigns/{campaign_id}")
        return response["data"]

    def update(
        self,
        campaign_id: str,
        *,
        name: str | None = None,
        subject: str | None = None,
        from_: str | dict[str, str] | None = None,
        audience_id: str | None = None,
        reply_to: str | dict[str, str] | None = None,
        template_id: str | None = None,
        html: str | None = None,
        text: str | None = None,
        variables: dict[str, Any] | None = None,
        preview_text: str | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Update a campaign.

        Args:
            campaign_id: The campaign ID.

        Returns:
            Updated campaign object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if subject is not None:
            body["subject"] = subject
        if from_ is not None:
            body["from"] = from_
        if audience_id is not None:
            body["audienceId"] = audience_id
        if reply_to is not None:
            body["replyTo"] = reply_to
        if template_id is not None:
            body["templateId"] = template_id
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if variables is not None:
            body["variables"] = variables
        if preview_text is not None:
            body["previewText"] = preview_text
        if tags is not None:
            body["tags"] = tags

        response = self._http.patch(f"/v1/campaigns/{campaign_id}", body)
        return response["data"]

    def delete(self, campaign_id: str) -> None:
        """Delete a campaign."""
        self._http.delete(f"/v1/campaigns/{campaign_id}")

    def schedule(self, campaign_id: str, *, scheduled_at: str) -> dict[str, Any]:
        """Schedule a campaign for later delivery.

        Args:
            campaign_id: The campaign ID.
            scheduled_at: Scheduled send time (ISO 8601).

        Returns:
            Updated campaign object.
        """
        response = self._http.post(
            f"/v1/campaigns/{campaign_id}/schedule",
            {"scheduledAt": scheduled_at},
        )
        return response["data"]

    def send(self, campaign_id: str) -> dict[str, Any]:
        """Send a campaign immediately.

        Args:
            campaign_id: The campaign ID.

        Returns:
            Campaign object with updated status.
        """
        response = self._http.post(f"/v1/campaigns/{campaign_id}/send")
        return response["data"]

    def pause(self, campaign_id: str) -> dict[str, Any]:
        """Pause a sending campaign."""
        response = self._http.post(f"/v1/campaigns/{campaign_id}/pause")
        return response["data"]

    def resume(self, campaign_id: str) -> dict[str, Any]:
        """Resume a paused campaign."""
        response = self._http.post(f"/v1/campaigns/{campaign_id}/resume")
        return response["data"]

    def cancel(self, campaign_id: str) -> dict[str, Any]:
        """Cancel a scheduled or sending campaign."""
        response = self._http.post(f"/v1/campaigns/{campaign_id}/cancel")
        return response["data"]


    def send_test(
        self,
        campaign_id: str,
        *,
        to: list[str],
    ) -> dict[str, Any]:
        """Send a test/preview of a campaign to 1-5 email addresses.

        Args:
            campaign_id: The campaign ID.
            to: List of test email addresses (max 5).

        Returns:
            Test send result.
        """
        return self._http.post(f"/v1/campaigns/{campaign_id}/test", {"to": to})

    def clone(
        self,
        campaign_id: str,
        *,
        include_ab_test: bool | None = None,
    ) -> dict[str, Any]:
        """Clone a campaign as a new draft.

        Args:
            campaign_id: The campaign ID.
            include_ab_test: Include A/B test variants.

        Returns:
            Cloned campaign object.
        """
        body: dict[str, Any] = {}
        if include_ab_test is not None:
            body["includeABTest"] = include_ab_test

        return self._http.post(f"/v1/campaigns/{campaign_id}/clone", body)

    def links(
        self,
        campaign_id: str,
        *,
        limit: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Get tracked link analytics for a campaign.

        Args:
            campaign_id: The campaign ID.
            limit: Max links to return.
            sort: Sort field ('uniqueClicks', 'totalClicks').
            order: Sort order ('asc', 'desc').

        Returns:
            Link analytics data.
        """
        return self._http.get(
            f"/v1/campaigns/{campaign_id}/links",
            {"limit": limit, "sort": sort, "order": order},
        )


class AsyncCampaigns:
    """Async campaign management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        name: str,
        subject: str,
        from_: str | dict[str, str],
        audience_id: str,
        reply_to: str | dict[str, str] | None = None,
        template_id: str | None = None,
        html: str | None = None,
        text: str | None = None,
        variables: dict[str, Any] | None = None,
        preview_text: str | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new campaign (async)."""
        body: dict[str, Any] = {
            "name": name,
            "subject": subject,
            "from": from_,
            "audienceId": audience_id,
        }
        if reply_to is not None:
            body["replyTo"] = reply_to
        if template_id is not None:
            body["templateId"] = template_id
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if variables is not None:
            body["variables"] = variables
        if preview_text is not None:
            body["previewText"] = preview_text
        if tags is not None:
            body["tags"] = tags

        response = await self._http.post("/v1/campaigns", body)
        return response["data"]

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all campaigns (async)."""
        return await self._http.get("/v1/campaigns", {"limit": limit, "cursor": cursor})

    async def get(self, campaign_id: str) -> dict[str, Any]:
        """Get a single campaign by ID (async)."""
        response = await self._http.get(f"/v1/campaigns/{campaign_id}")
        return response["data"]

    async def update(
        self,
        campaign_id: str,
        *,
        name: str | None = None,
        subject: str | None = None,
        from_: str | dict[str, str] | None = None,
        audience_id: str | None = None,
        reply_to: str | dict[str, str] | None = None,
        template_id: str | None = None,
        html: str | None = None,
        text: str | None = None,
        variables: dict[str, Any] | None = None,
        preview_text: str | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Update a campaign (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if subject is not None:
            body["subject"] = subject
        if from_ is not None:
            body["from"] = from_
        if audience_id is not None:
            body["audienceId"] = audience_id
        if reply_to is not None:
            body["replyTo"] = reply_to
        if template_id is not None:
            body["templateId"] = template_id
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if variables is not None:
            body["variables"] = variables
        if preview_text is not None:
            body["previewText"] = preview_text
        if tags is not None:
            body["tags"] = tags

        response = await self._http.patch(f"/v1/campaigns/{campaign_id}", body)
        return response["data"]

    async def delete(self, campaign_id: str) -> None:
        """Delete a campaign (async)."""
        await self._http.delete(f"/v1/campaigns/{campaign_id}")

    async def schedule(self, campaign_id: str, *, scheduled_at: str) -> dict[str, Any]:
        """Schedule a campaign (async)."""
        response = await self._http.post(
            f"/v1/campaigns/{campaign_id}/schedule",
            {"scheduledAt": scheduled_at},
        )
        return response["data"]

    async def send(self, campaign_id: str) -> dict[str, Any]:
        """Send a campaign immediately (async)."""
        response = await self._http.post(f"/v1/campaigns/{campaign_id}/send")
        return response["data"]

    async def pause(self, campaign_id: str) -> dict[str, Any]:
        """Pause a sending campaign (async)."""
        response = await self._http.post(f"/v1/campaigns/{campaign_id}/pause")
        return response["data"]

    async def resume(self, campaign_id: str) -> dict[str, Any]:
        """Resume a paused campaign (async)."""
        response = await self._http.post(f"/v1/campaigns/{campaign_id}/resume")
        return response["data"]

    async def cancel(self, campaign_id: str) -> dict[str, Any]:
        """Cancel a campaign (async)."""
        response = await self._http.post(f"/v1/campaigns/{campaign_id}/cancel")
        return response["data"]

    async def send_test(
        self,
        campaign_id: str,
        *,
        to: list[str],
    ) -> dict[str, Any]:
        """Send a test/preview of a campaign (async)."""
        return await self._http.post(f"/v1/campaigns/{campaign_id}/test", {"to": to})

    async def clone(
        self,
        campaign_id: str,
        *,
        include_ab_test: bool | None = None,
    ) -> dict[str, Any]:
        """Clone a campaign as a new draft (async)."""
        body: dict[str, Any] = {}
        if include_ab_test is not None:
            body["includeABTest"] = include_ab_test

        return await self._http.post(f"/v1/campaigns/{campaign_id}/clone", body)

    async def links(
        self,
        campaign_id: str,
        *,
        limit: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Get tracked link analytics for a campaign (async)."""
        return await self._http.get(
            f"/v1/campaigns/{campaign_id}/links",
            {"limit": limit, "sort": sort, "order": order},
        )
