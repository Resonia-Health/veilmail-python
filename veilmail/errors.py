"""Error classes for the Veil Mail SDK."""

from __future__ import annotations

from typing import Any


class VeilMailError(Exception):
    """Base error class for all Veil Mail SDK errors."""

    def __init__(
        self,
        message: str,
        code: str = "unknown_error",
        status: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.details = details


class AuthenticationError(VeilMailError):
    """Raised when authentication fails (401)."""

    def __init__(self, message: str = "Invalid API key") -> None:
        super().__init__(message, code="authentication_error", status=401)


class ForbiddenError(VeilMailError):
    """Raised when the request is forbidden (403)."""

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message, code="forbidden", status=403)


class NotFoundError(VeilMailError):
    """Raised when a resource is not found (404)."""

    def __init__(self, resource: str = "Resource", resource_id: str | None = None) -> None:
        if resource_id:
            message = f"{resource} with ID '{resource_id}' not found"
        else:
            message = f"{resource} not found"
        super().__init__(message, code="not_found", status=404)


class ValidationError(VeilMailError):
    """Raised when request validation fails (400/422)."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, code="validation_error", status=400, details=details)


class PiiDetectedError(VeilMailError):
    """Raised when PII is detected in email content (422)."""

    def __init__(self, message: str, pii_types: list[str]) -> None:
        super().__init__(
            message,
            code="pii_detected",
            status=422,
            details={"pii_types": pii_types},
        )
        self.pii_types = pii_types


class RateLimitError(VeilMailError):
    """Raised when the rate limit is exceeded (429)."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None) -> None:
        details = {"retry_after": retry_after} if retry_after else None
        super().__init__(message, code="rate_limit", status=429, details=details)
        self.retry_after = retry_after


class ServerError(VeilMailError):
    """Raised when the API returns a server error (5xx)."""

    def __init__(self, message: str = "Internal server error", status: int = 500) -> None:
        super().__init__(message, code="server_error", status=status)


class TimeoutError(VeilMailError):
    """Raised when a request times out."""

    def __init__(self, timeout: float) -> None:
        super().__init__(f"Request timed out after {timeout}s", code="timeout")


class NetworkError(VeilMailError):
    """Raised for network-related issues."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="network_error")


def _parse_error_response(status_code: int, body: dict[str, Any] | None, headers: dict[str, str] | None = None) -> VeilMailError:
    """Parse an API error response and return the appropriate error."""
    error_data = (body or {}).get("error", {})
    message = error_data.get("message", "Unknown error")
    code = error_data.get("code", "unknown_error")
    details = error_data.get("details")

    if status_code == 400:
        return ValidationError(message, details)
    if status_code == 401:
        return AuthenticationError(message)
    if status_code == 403:
        return ForbiddenError(message)
    if status_code == 404:
        return NotFoundError("Resource")
    if status_code == 422:
        if code == "pii_detected" and details and "pii_types" in details:
            return PiiDetectedError(message, details["pii_types"])
        return ValidationError(message, details)
    if status_code == 429:
        retry_after = None
        if headers:
            raw = headers.get("retry-after")
            if raw:
                try:
                    retry_after = int(raw)
                except ValueError:
                    pass
        return RateLimitError(message, retry_after)
    if status_code >= 500:
        return ServerError(message, status_code)
    return VeilMailError(message, code, status_code, details)
