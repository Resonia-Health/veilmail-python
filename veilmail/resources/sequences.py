"""Automation sequence management."""

from __future__ import annotations

from typing import Any


class Sequences:
    """Automation sequence management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        audience_id: str,
        trigger_type: str,
        description: str | None = None,
        trigger_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new automation sequence.

        Args:
            name: Sequence name.
            audience_id: Target audience ID.
            trigger_type: Trigger type ('audience_join', 'segment_match', 'manual').
            description: Sequence description.
            trigger_config: Additional trigger configuration.

        Returns:
            Sequence object.
        """
        body: dict[str, Any] = {
            "name": name,
            "audienceId": audience_id,
            "triggerType": trigger_type,
        }
        if description is not None:
            body["description"] = description
        if trigger_config is not None:
            body["triggerConfig"] = trigger_config

        return self._http.post("/v1/sequences", body)

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all automation sequences.

        Returns:
            Paginated response with sequence data.
        """
        return self._http.get("/v1/sequences", {"limit": limit, "cursor": cursor})

    def get(self, sequence_id: str) -> dict[str, Any]:
        """Get a single sequence by ID.

        Args:
            sequence_id: The sequence ID.

        Returns:
            Sequence object.
        """
        return self._http.get(f"/v1/sequences/{sequence_id}")

    def update(
        self,
        sequence_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        trigger_type: str | None = None,
        trigger_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a sequence (only DRAFT or PAUSED).

        Args:
            sequence_id: The sequence ID.
            name: New name.
            description: New description.
            trigger_type: New trigger type.
            trigger_config: New trigger configuration.

        Returns:
            Updated sequence object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if trigger_type is not None:
            body["triggerType"] = trigger_type
        if trigger_config is not None:
            body["triggerConfig"] = trigger_config

        return self._http.put(f"/v1/sequences/{sequence_id}", body)

    def delete(self, sequence_id: str) -> None:
        """Delete a sequence (only DRAFT)."""
        self._http.delete(f"/v1/sequences/{sequence_id}")

    def activate(self, sequence_id: str) -> dict[str, Any]:
        """Activate a sequence."""
        return self._http.post(f"/v1/sequences/{sequence_id}/activate")

    def pause(self, sequence_id: str) -> dict[str, Any]:
        """Pause an active sequence."""
        return self._http.post(f"/v1/sequences/{sequence_id}/pause")

    def archive(self, sequence_id: str) -> dict[str, Any]:
        """Archive a sequence."""
        return self._http.post(f"/v1/sequences/{sequence_id}/archive")

    def add_step(
        self,
        sequence_id: str,
        *,
        position: int,
        type: str,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        template_id: str | None = None,
        delay_amount: int | None = None,
        delay_unit: str | None = None,
        condition_type: str | None = None,
        condition_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Add a step to a sequence.

        Args:
            sequence_id: The sequence ID.
            position: Step position (0-indexed).
            type: Step type ('email', 'delay', 'condition').
            subject: Email subject (for email steps).
            html: HTML content (for email steps).
            text: Plain text content (for email steps).
            template_id: Template ID (for email steps).
            delay_amount: Delay amount (for delay steps).
            delay_unit: Delay unit ('minutes', 'hours', 'days') (for delay steps).
            condition_type: Condition type (for condition steps).
            condition_config: Condition configuration (for condition steps).

        Returns:
            Step object.
        """
        body: dict[str, Any] = {"position": position, "type": type}
        if subject is not None:
            body["subject"] = subject
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if template_id is not None:
            body["templateId"] = template_id
        if delay_amount is not None:
            body["delayAmount"] = delay_amount
        if delay_unit is not None:
            body["delayUnit"] = delay_unit
        if condition_type is not None:
            body["conditionType"] = condition_type
        if condition_config is not None:
            body["conditionConfig"] = condition_config

        return self._http.post(f"/v1/sequences/{sequence_id}/steps", body)

    def update_step(
        self,
        sequence_id: str,
        step_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a sequence step.

        Args:
            sequence_id: The sequence ID.
            step_id: The step ID.
            **kwargs: Fields to update (subject, html, text, template_id, etc.).

        Returns:
            Updated step object.
        """
        body: dict[str, Any] = {}
        key_map = {
            "subject": "subject",
            "html": "html",
            "text": "text",
            "template_id": "templateId",
            "delay_amount": "delayAmount",
            "delay_unit": "delayUnit",
            "condition_type": "conditionType",
            "condition_config": "conditionConfig",
        }
        for py_key, api_key in key_map.items():
            if py_key in kwargs and kwargs[py_key] is not None:
                body[api_key] = kwargs[py_key]

        return self._http.put(
            f"/v1/sequences/{sequence_id}/steps/{step_id}", body
        )

    def delete_step(self, sequence_id: str, step_id: str) -> None:
        """Delete a sequence step."""
        self._http.delete(f"/v1/sequences/{sequence_id}/steps/{step_id}")

    def reorder_steps(
        self,
        sequence_id: str,
        steps: list[dict[str, Any]],
    ) -> None:
        """Reorder sequence steps.

        Args:
            sequence_id: The sequence ID.
            steps: List of {id, position} dicts.
        """
        self._http.post(
            f"/v1/sequences/{sequence_id}/steps/reorder", {"steps": steps}
        )

    def enroll(
        self,
        sequence_id: str,
        subscriber_ids: list[str],
    ) -> dict[str, Any]:
        """Manually enroll subscribers into a sequence.

        Args:
            sequence_id: The sequence ID.
            subscriber_ids: List of subscriber IDs to enroll.

        Returns:
            Enrollment result with 'enrolled' count.
        """
        return self._http.post(
            f"/v1/sequences/{sequence_id}/enroll",
            {"subscriberIds": subscriber_ids},
        )

    def list_enrollments(
        self,
        sequence_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List enrollments for a sequence.

        Returns:
            Paginated response with enrollment data.
        """
        return self._http.get(
            f"/v1/sequences/{sequence_id}/enrollments",
            {"limit": limit, "cursor": cursor},
        )

    def remove_enrollment(self, sequence_id: str, enrollment_id: str) -> None:
        """Remove an enrollment from a sequence."""
        self._http.delete(
            f"/v1/sequences/{sequence_id}/enrollments/{enrollment_id}"
        )


class AsyncSequences:
    """Async automation sequence management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        name: str,
        audience_id: str,
        trigger_type: str,
        description: str | None = None,
        trigger_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a new automation sequence (async)."""
        body: dict[str, Any] = {
            "name": name,
            "audienceId": audience_id,
            "triggerType": trigger_type,
        }
        if description is not None:
            body["description"] = description
        if trigger_config is not None:
            body["triggerConfig"] = trigger_config

        return await self._http.post("/v1/sequences", body)

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all automation sequences (async)."""
        return await self._http.get("/v1/sequences", {"limit": limit, "cursor": cursor})

    async def get(self, sequence_id: str) -> dict[str, Any]:
        """Get a single sequence by ID (async)."""
        return await self._http.get(f"/v1/sequences/{sequence_id}")

    async def update(
        self,
        sequence_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        trigger_type: str | None = None,
        trigger_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a sequence (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if trigger_type is not None:
            body["triggerType"] = trigger_type
        if trigger_config is not None:
            body["triggerConfig"] = trigger_config

        return await self._http.put(f"/v1/sequences/{sequence_id}", body)

    async def delete(self, sequence_id: str) -> None:
        """Delete a sequence (async)."""
        await self._http.delete(f"/v1/sequences/{sequence_id}")

    async def activate(self, sequence_id: str) -> dict[str, Any]:
        """Activate a sequence (async)."""
        return await self._http.post(f"/v1/sequences/{sequence_id}/activate")

    async def pause(self, sequence_id: str) -> dict[str, Any]:
        """Pause an active sequence (async)."""
        return await self._http.post(f"/v1/sequences/{sequence_id}/pause")

    async def archive(self, sequence_id: str) -> dict[str, Any]:
        """Archive a sequence (async)."""
        return await self._http.post(f"/v1/sequences/{sequence_id}/archive")

    async def add_step(
        self,
        sequence_id: str,
        *,
        position: int,
        type: str,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        template_id: str | None = None,
        delay_amount: int | None = None,
        delay_unit: str | None = None,
        condition_type: str | None = None,
        condition_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Add a step to a sequence (async)."""
        body: dict[str, Any] = {"position": position, "type": type}
        if subject is not None:
            body["subject"] = subject
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if template_id is not None:
            body["templateId"] = template_id
        if delay_amount is not None:
            body["delayAmount"] = delay_amount
        if delay_unit is not None:
            body["delayUnit"] = delay_unit
        if condition_type is not None:
            body["conditionType"] = condition_type
        if condition_config is not None:
            body["conditionConfig"] = condition_config

        return await self._http.post(f"/v1/sequences/{sequence_id}/steps", body)

    async def update_step(
        self,
        sequence_id: str,
        step_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a sequence step (async)."""
        body: dict[str, Any] = {}
        key_map = {
            "subject": "subject",
            "html": "html",
            "text": "text",
            "template_id": "templateId",
            "delay_amount": "delayAmount",
            "delay_unit": "delayUnit",
            "condition_type": "conditionType",
            "condition_config": "conditionConfig",
        }
        for py_key, api_key in key_map.items():
            if py_key in kwargs and kwargs[py_key] is not None:
                body[api_key] = kwargs[py_key]

        return await self._http.put(
            f"/v1/sequences/{sequence_id}/steps/{step_id}", body
        )

    async def delete_step(self, sequence_id: str, step_id: str) -> None:
        """Delete a sequence step (async)."""
        await self._http.delete(f"/v1/sequences/{sequence_id}/steps/{step_id}")

    async def reorder_steps(
        self,
        sequence_id: str,
        steps: list[dict[str, Any]],
    ) -> None:
        """Reorder sequence steps (async)."""
        await self._http.post(
            f"/v1/sequences/{sequence_id}/steps/reorder", {"steps": steps}
        )

    async def enroll(
        self,
        sequence_id: str,
        subscriber_ids: list[str],
    ) -> dict[str, Any]:
        """Enroll subscribers into a sequence (async)."""
        return await self._http.post(
            f"/v1/sequences/{sequence_id}/enroll",
            {"subscriberIds": subscriber_ids},
        )

    async def list_enrollments(
        self,
        sequence_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List enrollments for a sequence (async)."""
        return await self._http.get(
            f"/v1/sequences/{sequence_id}/enrollments",
            {"limit": limit, "cursor": cursor},
        )

    async def remove_enrollment(self, sequence_id: str, enrollment_id: str) -> None:
        """Remove an enrollment (async)."""
        await self._http.delete(
            f"/v1/sequences/{sequence_id}/enrollments/{enrollment_id}"
        )
