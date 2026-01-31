"""Email sending and management."""

from __future__ import annotations

from typing import Any


class Emails:
    """Email sending and management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def send(
        self,
        *,
        from_: str,
        to: str | list[str],
        subject: str,
        html: str | None = None,
        text: str | None = None,
        cc: str | list[str] | None = None,
        bcc: str | list[str] | None = None,
        reply_to: str | None = None,
        headers: dict[str, str] | None = None,
        template_id: str | None = None,
        template_data: dict[str, Any] | None = None,
        scheduled_for: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        unsubscribe_url: str | None = None,
        type: str | None = None,
        attachments: list[dict[str, Any]] | None = None,
        topic_id: str | None = None,
    ) -> dict[str, Any]:
        """Send an email.

        Args:
            from_: Sender email address.
            to: Recipient email address(es).
            subject: Email subject line.
            html: HTML body content.
            text: Plain text body content.
            cc: CC recipients.
            bcc: BCC recipients.
            reply_to: Reply-to address.
            headers: Custom headers.
            template_id: Template ID to use.
            template_data: Data for template variable substitution.
            scheduled_for: Scheduled send time (ISO 8601).
            tags: Tags for categorization.
            metadata: Custom metadata.
            idempotency_key: Key to prevent duplicate sends.
            unsubscribe_url: Unsubscribe URL for marketing emails.
            type: Email type ('transactional' or 'marketing').
            attachments: File attachments.
            topic_id: Subscription topic ID.

        Returns:
            Email object with id, status, and metadata.
        """
        body: dict[str, Any] = {
            "from": from_,
            "to": to,
            "subject": subject,
        }
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if cc is not None:
            body["cc"] = cc
        if bcc is not None:
            body["bcc"] = bcc
        if reply_to is not None:
            body["replyTo"] = reply_to
        if headers is not None:
            body["headers"] = headers
        if template_id is not None:
            body["templateId"] = template_id
        if template_data is not None:
            body["templateData"] = template_data
        if scheduled_for is not None:
            body["scheduledFor"] = scheduled_for
        if tags is not None:
            body["tags"] = tags
        if metadata is not None:
            body["metadata"] = metadata
        if idempotency_key is not None:
            body["idempotencyKey"] = idempotency_key
        if unsubscribe_url is not None:
            body["unsubscribeUrl"] = unsubscribe_url
        if type is not None:
            body["type"] = type
        if attachments is not None:
            body["attachments"] = attachments
        if topic_id is not None:
            body["topicId"] = topic_id

        # Skip camelCase conversion since we built the body with camelCase keys
        return self._http.request("POST", "/v1/emails", body=body)

    def send_batch(self, emails: list[dict[str, Any]]) -> dict[str, Any]:
        """Send multiple emails in a single request (max 100).

        Args:
            emails: List of email parameter dicts (same fields as send()).

        Returns:
            Batch result with total, successful, failed counts, and per-email results.
        """
        return self._http.post("/v1/emails/batch", {"emails": emails})

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> dict[str, Any]:
        """List emails with pagination.

        Args:
            limit: Number of items per page (default: 20, max: 100).
            cursor: Cursor for pagination.
            status: Filter by email status.
            tag: Filter by tag.
            after: Filter emails after this date.
            before: Filter emails before this date.

        Returns:
            Paginated response with data, hasMore, and nextCursor.
        """
        return self._http.get("/v1/emails", {
            "limit": limit,
            "cursor": cursor,
            "status": status,
            "tag": tag,
            "after": after,
            "before": before,
        })

    def get(self, email_id: str) -> dict[str, Any]:
        """Get a single email by ID.

        Args:
            email_id: The email ID.

        Returns:
            Email object.
        """
        return self._http.get(f"/v1/emails/{email_id}")

    def cancel(self, email_id: str) -> dict[str, Any]:
        """Cancel a scheduled email.

        Args:
            email_id: The email ID.

        Returns:
            Cancel result with id, status, and cancelledAt.
        """
        return self._http.post(f"/v1/emails/{email_id}/cancel")

    def update(self, email_id: str, *, scheduled_for: str) -> dict[str, Any]:
        """Update a scheduled email (e.g., reschedule).

        Args:
            email_id: The email ID.
            scheduled_for: New scheduled send time (ISO 8601).

        Returns:
            Updated email object.
        """
        return self._http.patch(f"/v1/emails/{email_id}", {"scheduledFor": scheduled_for})


    def links(
        self,
        email_id: str,
        *,
        limit: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Get tracked link analytics for a specific email.

        Args:
            email_id: The email ID.
            limit: Max links to return.
            sort: Sort field ('uniqueClicks', 'totalClicks').
            order: Sort order ('asc', 'desc').

        Returns:
            Link analytics data.
        """
        return self._http.get(
            f"/v1/emails/{email_id}/links",
            {"limit": limit, "sort": sort, "order": order},
        )


class AsyncEmails:
    """Async email sending and management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def send(
        self,
        *,
        from_: str,
        to: str | list[str],
        subject: str,
        html: str | None = None,
        text: str | None = None,
        cc: str | list[str] | None = None,
        bcc: str | list[str] | None = None,
        reply_to: str | None = None,
        headers: dict[str, str] | None = None,
        template_id: str | None = None,
        template_data: dict[str, Any] | None = None,
        scheduled_for: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        unsubscribe_url: str | None = None,
        type: str | None = None,
        attachments: list[dict[str, Any]] | None = None,
        topic_id: str | None = None,
    ) -> dict[str, Any]:
        """Send an email (async)."""
        body: dict[str, Any] = {
            "from": from_,
            "to": to,
            "subject": subject,
        }
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if cc is not None:
            body["cc"] = cc
        if bcc is not None:
            body["bcc"] = bcc
        if reply_to is not None:
            body["replyTo"] = reply_to
        if headers is not None:
            body["headers"] = headers
        if template_id is not None:
            body["templateId"] = template_id
        if template_data is not None:
            body["templateData"] = template_data
        if scheduled_for is not None:
            body["scheduledFor"] = scheduled_for
        if tags is not None:
            body["tags"] = tags
        if metadata is not None:
            body["metadata"] = metadata
        if idempotency_key is not None:
            body["idempotencyKey"] = idempotency_key
        if unsubscribe_url is not None:
            body["unsubscribeUrl"] = unsubscribe_url
        if type is not None:
            body["type"] = type
        if attachments is not None:
            body["attachments"] = attachments
        if topic_id is not None:
            body["topicId"] = topic_id

        return await self._http.request("POST", "/v1/emails", body=body)

    async def send_batch(self, emails: list[dict[str, Any]]) -> dict[str, Any]:
        """Send multiple emails in a single request (async, max 100)."""
        return await self._http.post("/v1/emails/batch", {"emails": emails})

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> dict[str, Any]:
        """List emails with pagination (async)."""
        return await self._http.get("/v1/emails", {
            "limit": limit,
            "cursor": cursor,
            "status": status,
            "tag": tag,
            "after": after,
            "before": before,
        })

    async def get(self, email_id: str) -> dict[str, Any]:
        """Get a single email by ID (async)."""
        return await self._http.get(f"/v1/emails/{email_id}")

    async def cancel(self, email_id: str) -> dict[str, Any]:
        """Cancel a scheduled email (async)."""
        return await self._http.post(f"/v1/emails/{email_id}/cancel")

    async def update(self, email_id: str, *, scheduled_for: str) -> dict[str, Any]:
        """Update a scheduled email (async)."""
        return await self._http.patch(f"/v1/emails/{email_id}", {"scheduledFor": scheduled_for})

    async def links(
        self,
        email_id: str,
        *,
        limit: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Get tracked link analytics for a specific email (async)."""
        return await self._http.get(
            f"/v1/emails/{email_id}/links",
            {"limit": limit, "sort": sort, "order": order},
        )
