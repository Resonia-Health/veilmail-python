"""Signup form management."""

from __future__ import annotations

from typing import Any


class Forms:
    """Signup form management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        audience_id: str,
        fields: list[dict[str, Any]] | None = None,
        double_opt_in: bool | None = None,
        redirect_url: str | None = None,
        honeypot: bool | None = None,
        casl_consent: bool | None = None,
    ) -> dict[str, Any]:
        """Create a new signup form.

        Args:
            name: Form name.
            audience_id: Target audience ID.
            fields: Form field configuration.
            double_opt_in: Enable double opt-in.
            redirect_url: URL to redirect after submission.
            honeypot: Enable honeypot spam protection.
            casl_consent: Require CASL consent checkbox.

        Returns:
            Form object.
        """
        body: dict[str, Any] = {
            "name": name,
            "audienceId": audience_id,
        }
        if fields is not None:
            body["fields"] = fields
        if double_opt_in is not None:
            body["doubleOptIn"] = double_opt_in
        if redirect_url is not None:
            body["redirectUrl"] = redirect_url
        if honeypot is not None:
            body["honeypot"] = honeypot
        if casl_consent is not None:
            body["caslConsent"] = casl_consent

        return self._http.post("/v1/forms", body)

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all signup forms.

        Returns:
            Paginated response with form data.
        """
        return self._http.get("/v1/forms", {"limit": limit, "cursor": cursor})

    def get(self, form_id: str) -> dict[str, Any]:
        """Get a single form by ID.

        Args:
            form_id: The form ID.

        Returns:
            Form object.
        """
        return self._http.get(f"/v1/forms/{form_id}")

    def update(
        self,
        form_id: str,
        *,
        name: str | None = None,
        fields: list[dict[str, Any]] | None = None,
        double_opt_in: bool | None = None,
        redirect_url: str | None = None,
        honeypot: bool | None = None,
        casl_consent: bool | None = None,
    ) -> dict[str, Any]:
        """Update a form.

        Args:
            form_id: The form ID.

        Returns:
            Updated form object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if fields is not None:
            body["fields"] = fields
        if double_opt_in is not None:
            body["doubleOptIn"] = double_opt_in
        if redirect_url is not None:
            body["redirectUrl"] = redirect_url
        if honeypot is not None:
            body["honeypot"] = honeypot
        if casl_consent is not None:
            body["caslConsent"] = casl_consent

        return self._http.put(f"/v1/forms/{form_id}", body)

    def delete(self, form_id: str) -> None:
        """Delete a form."""
        self._http.delete(f"/v1/forms/{form_id}")


class AsyncForms:
    """Async signup form management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        name: str,
        audience_id: str,
        fields: list[dict[str, Any]] | None = None,
        double_opt_in: bool | None = None,
        redirect_url: str | None = None,
        honeypot: bool | None = None,
        casl_consent: bool | None = None,
    ) -> dict[str, Any]:
        """Create a new signup form (async)."""
        body: dict[str, Any] = {
            "name": name,
            "audienceId": audience_id,
        }
        if fields is not None:
            body["fields"] = fields
        if double_opt_in is not None:
            body["doubleOptIn"] = double_opt_in
        if redirect_url is not None:
            body["redirectUrl"] = redirect_url
        if honeypot is not None:
            body["honeypot"] = honeypot
        if casl_consent is not None:
            body["caslConsent"] = casl_consent

        return await self._http.post("/v1/forms", body)

    async def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """List all signup forms (async)."""
        return await self._http.get("/v1/forms", {"limit": limit, "cursor": cursor})

    async def get(self, form_id: str) -> dict[str, Any]:
        """Get a single form by ID (async)."""
        return await self._http.get(f"/v1/forms/{form_id}")

    async def update(
        self,
        form_id: str,
        *,
        name: str | None = None,
        fields: list[dict[str, Any]] | None = None,
        double_opt_in: bool | None = None,
        redirect_url: str | None = None,
        honeypot: bool | None = None,
        casl_consent: bool | None = None,
    ) -> dict[str, Any]:
        """Update a form (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if fields is not None:
            body["fields"] = fields
        if double_opt_in is not None:
            body["doubleOptIn"] = double_opt_in
        if redirect_url is not None:
            body["redirectUrl"] = redirect_url
        if honeypot is not None:
            body["honeypot"] = honeypot
        if casl_consent is not None:
            body["caslConsent"] = casl_consent

        return await self._http.put(f"/v1/forms/{form_id}", body)

    async def delete(self, form_id: str) -> None:
        """Delete a form (async)."""
        await self._http.delete(f"/v1/forms/{form_id}")
