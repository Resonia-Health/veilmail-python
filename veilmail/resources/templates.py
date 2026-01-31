"""Email template management."""

from __future__ import annotations

from typing import Any


class Templates:
    """Email template management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        subject: str,
        html: str,
        text: str | None = None,
        type: str | None = None,
        variables: list[dict[str, Any]] | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a new email template.

        Args:
            name: Template name.
            subject: Email subject (supports variables).
            html: HTML content (supports variables).
            text: Plain text content.
            type: Template type ('transactional' or 'marketing').
            variables: Variable definitions.
            description: Template description.

        Returns:
            Template object.
        """
        body: dict[str, Any] = {"name": name, "subject": subject, "html": html}
        if text is not None:
            body["text"] = text
        if type is not None:
            body["type"] = type
        if variables is not None:
            body["variables"] = variables
        if description is not None:
            body["description"] = description

        response = self._http.post("/v1/templates", body)
        return response["data"]

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all templates.

        Returns:
            Paginated response with template data.
        """
        return self._http.get("/v1/templates", {"limit": limit, "cursor": cursor})

    def get(self, template_id: str) -> dict[str, Any]:
        """Get a single template by ID.

        Args:
            template_id: The template ID.

        Returns:
            Template object.
        """
        response = self._http.get(f"/v1/templates/{template_id}")
        return response["data"]

    def update(
        self,
        template_id: str,
        *,
        name: str | None = None,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        type: str | None = None,
        variables: list[dict[str, Any]] | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Update a template.

        Args:
            template_id: The template ID.
            name: New name.
            subject: New subject.
            html: New HTML content.
            text: New plain text content.
            type: New template type.
            variables: New variable definitions.
            description: New description.

        Returns:
            Updated template object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if subject is not None:
            body["subject"] = subject
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if type is not None:
            body["type"] = type
        if variables is not None:
            body["variables"] = variables
        if description is not None:
            body["description"] = description

        response = self._http.patch(f"/v1/templates/{template_id}", body)
        return response["data"]

    def preview(
        self,
        *,
        html: str,
        subject: str | None = None,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Preview a rendered template with sample data.

        Args:
            html: HTML template content to preview.
            subject: Subject line template to preview.
            variables: Variables to substitute in the template.

        Returns:
            Rendered HTML and optional subject.
        """
        body: dict[str, Any] = {"html": html}
        if subject is not None:
            body["subject"] = subject
        if variables is not None:
            body["variables"] = variables

        return self._http.post("/v1/templates/preview", body)

    def delete(self, template_id: str) -> None:
        """Delete a template.

        Args:
            template_id: The template ID.
        """
        self._http.delete(f"/v1/templates/{template_id}")


class AsyncTemplates:
    """Async email template management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        name: str,
        subject: str,
        html: str,
        text: str | None = None,
        type: str | None = None,
        variables: list[dict[str, Any]] | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a new email template (async)."""
        body: dict[str, Any] = {"name": name, "subject": subject, "html": html}
        if text is not None:
            body["text"] = text
        if type is not None:
            body["type"] = type
        if variables is not None:
            body["variables"] = variables
        if description is not None:
            body["description"] = description

        response = await self._http.post("/v1/templates", body)
        return response["data"]

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all templates (async)."""
        return await self._http.get("/v1/templates", {"limit": limit, "cursor": cursor})

    async def get(self, template_id: str) -> dict[str, Any]:
        """Get a single template by ID (async)."""
        response = await self._http.get(f"/v1/templates/{template_id}")
        return response["data"]

    async def update(
        self,
        template_id: str,
        *,
        name: str | None = None,
        subject: str | None = None,
        html: str | None = None,
        text: str | None = None,
        type: str | None = None,
        variables: list[dict[str, Any]] | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Update a template (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if subject is not None:
            body["subject"] = subject
        if html is not None:
            body["html"] = html
        if text is not None:
            body["text"] = text
        if type is not None:
            body["type"] = type
        if variables is not None:
            body["variables"] = variables
        if description is not None:
            body["description"] = description

        response = await self._http.patch(f"/v1/templates/{template_id}", body)
        return response["data"]

    async def preview(
        self,
        *,
        html: str,
        subject: str | None = None,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Preview a rendered template with sample data (async)."""
        body: dict[str, Any] = {"html": html}
        if subject is not None:
            body["subject"] = subject
        if variables is not None:
            body["variables"] = variables

        return await self._http.post("/v1/templates/preview", body)

    async def delete(self, template_id: str) -> None:
        """Delete a template (async)."""
        await self._http.delete(f"/v1/templates/{template_id}")
