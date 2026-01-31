"""Contact property management."""

from __future__ import annotations

from typing import Any


class Properties:
    """Contact property management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def create(
        self,
        *,
        key: str,
        name: str,
        type: str = "text",
        description: str | None = None,
        required: bool | None = None,
        enum_options: list[str] | None = None,
        sort_order: int | None = None,
    ) -> dict[str, Any]:
        """Create a contact property.

        Args:
            key: Property key (alphanumeric + underscore, must start with letter or underscore).
            name: Display name.
            type: Property type (text, number, date, boolean, enum).
            description: Property description.
            required: Whether the property is required.
            enum_options: Options for ENUM type properties.
            sort_order: Sort order for display.

        Returns:
            Property object.
        """
        body: dict[str, Any] = {"key": key, "name": name, "type": type.upper()}
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        if enum_options is not None:
            body["enumOptions"] = enum_options
        if sort_order is not None:
            body["sortOrder"] = sort_order

        return self._http.post("/v1/properties", body)

    def list(self, *, active: bool | None = None) -> dict[str, Any]:
        """List all contact properties.

        Args:
            active: Filter by active status.

        Returns:
            Response with property data.
        """
        return self._http.get("/v1/properties", {"active": active})

    def get(self, property_id: str) -> dict[str, Any]:
        """Get a single contact property by ID.

        Args:
            property_id: The property ID.

        Returns:
            Property object.
        """
        return self._http.get(f"/v1/properties/{property_id}")

    def update(
        self,
        property_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        required: bool | None = None,
        enum_options: list[str] | None = None,
        sort_order: int | None = None,
        active: bool | None = None,
    ) -> dict[str, Any]:
        """Update a contact property.

        Args:
            property_id: The property ID.
            name: New display name.
            description: New description.
            required: New required state.
            enum_options: New enum options (ENUM type only).
            sort_order: New sort order.
            active: New active state.

        Returns:
            Updated property object.
        """
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        if enum_options is not None:
            body["enumOptions"] = enum_options
        if sort_order is not None:
            body["sortOrder"] = sort_order
        if active is not None:
            body["active"] = active

        return self._http.patch(f"/v1/properties/{property_id}", body)

    def delete(self, property_id: str) -> None:
        """Deactivate a contact property (soft delete).

        Args:
            property_id: The property ID.
        """
        self._http.delete(f"/v1/properties/{property_id}")

    def get_values(
        self,
        audience_id: str,
        subscriber_id: str,
    ) -> dict[str, Any]:
        """Get a subscriber's property values.

        Args:
            audience_id: The audience ID.
            subscriber_id: The subscriber ID.

        Returns:
            Response with property value data.
        """
        return self._http.get(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/properties"
        )

    def set_values(
        self,
        audience_id: str,
        subscriber_id: str,
        values: dict[str, str | int | float | bool | None],
    ) -> dict[str, Any]:
        """Set a subscriber's property values (merge with existing).

        Pass None for a value to delete it.

        Args:
            audience_id: The audience ID.
            subscriber_id: The subscriber ID.
            values: Dictionary of property key-value pairs.

        Returns:
            Success response.
        """
        return self._http.put(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/properties",
            values,
        )


class AsyncProperties:
    """Async contact property management."""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def create(
        self,
        *,
        key: str,
        name: str,
        type: str = "text",
        description: str | None = None,
        required: bool | None = None,
        enum_options: list[str] | None = None,
        sort_order: int | None = None,
    ) -> dict[str, Any]:
        """Create a contact property (async)."""
        body: dict[str, Any] = {"key": key, "name": name, "type": type.upper()}
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        if enum_options is not None:
            body["enumOptions"] = enum_options
        if sort_order is not None:
            body["sortOrder"] = sort_order

        return await self._http.post("/v1/properties", body)

    async def list(self, *, active: bool | None = None) -> dict[str, Any]:
        """List all contact properties (async)."""
        return await self._http.get("/v1/properties", {"active": active})

    async def get(self, property_id: str) -> dict[str, Any]:
        """Get a single contact property by ID (async)."""
        return await self._http.get(f"/v1/properties/{property_id}")

    async def update(
        self,
        property_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        required: bool | None = None,
        enum_options: list[str] | None = None,
        sort_order: int | None = None,
        active: bool | None = None,
    ) -> dict[str, Any]:
        """Update a contact property (async)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        if enum_options is not None:
            body["enumOptions"] = enum_options
        if sort_order is not None:
            body["sortOrder"] = sort_order
        if active is not None:
            body["active"] = active

        return await self._http.patch(f"/v1/properties/{property_id}", body)

    async def delete(self, property_id: str) -> None:
        """Deactivate a contact property (async)."""
        await self._http.delete(f"/v1/properties/{property_id}")

    async def get_values(
        self,
        audience_id: str,
        subscriber_id: str,
    ) -> dict[str, Any]:
        """Get a subscriber's property values (async)."""
        return await self._http.get(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/properties"
        )

    async def set_values(
        self,
        audience_id: str,
        subscriber_id: str,
        values: dict[str, str | int | float | bool | None],
    ) -> dict[str, Any]:
        """Set a subscriber's property values (async)."""
        return await self._http.put(
            f"/v1/audiences/{audience_id}/subscribers/{subscriber_id}/properties",
            values,
        )
