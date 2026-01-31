"""Webhook signature verification utility."""

from __future__ import annotations

import hashlib
import hmac


def verify_signature(payload: str | bytes, signature: str, secret: str) -> bool:
    """Verify a webhook signature.

    Uses constant-time comparison to prevent timing attacks.

    Args:
        payload: The raw request body (string or bytes).
        signature: The X-VeilMail-Signature header value.
        secret: Your webhook signing secret.

    Returns:
        True if the signature is valid, False otherwise.

    Example::

        import veilmail

        @app.post("/webhooks/veilmail")
        def handle_webhook(request):
            payload = request.body
            signature = request.headers["X-VeilMail-Signature"]

            if not veilmail.verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
                return Response(status_code=401)

            event = json.loads(payload)
            # ... handle event
    """
    if isinstance(payload, str):
        payload = payload.encode("utf-8")

    expected = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
