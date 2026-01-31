"""Veil Mail Python SDK — secure email with built-in PII protection.

Example::

    import veilmail

    client = veilmail.VeilMail("veil_live_xxxxx")

    email = client.emails.send(
        from_="hello@yourdomain.com",
        to="user@example.com",
        subject="Hello!",
        html="<h1>Welcome!</h1>",
    )

    print(email["id"])
"""

from .client import AsyncVeilMail, VeilMail
from .errors import (
    AuthenticationError,
    ForbiddenError,
    NetworkError,
    NotFoundError,
    PiiDetectedError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
    VeilMailError,
)
from .webhook import verify_signature as verify_webhook_signature

__version__ = "0.1.0"

__all__ = [
    # Clients
    "VeilMail",
    "AsyncVeilMail",
    # Errors
    "VeilMailError",
    "AuthenticationError",
    "ForbiddenError",
    "NetworkError",
    "NotFoundError",
    "PiiDetectedError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "ValidationError",
    # Utilities
    "verify_webhook_signature",
]
