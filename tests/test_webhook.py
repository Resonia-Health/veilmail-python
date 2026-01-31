"""Tests for webhook signature verification."""

from __future__ import annotations

import hashlib
import hmac

import veilmail


class TestVerifyWebhookSignature:
    def test_valid_signature(self) -> None:
        secret = "whsec_test_secret"
        payload = '{"type": "email.delivered", "data": {}}'
        signature = hmac.new(
            secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        assert veilmail.verify_webhook_signature(payload, signature, secret) is True

    def test_invalid_signature(self) -> None:
        secret = "whsec_test_secret"
        payload = '{"type": "email.delivered", "data": {}}'

        assert veilmail.verify_webhook_signature(payload, "invalid_sig", secret) is False

    def test_wrong_secret(self) -> None:
        secret = "whsec_test_secret"
        wrong_secret = "whsec_wrong_secret"
        payload = '{"type": "email.delivered", "data": {}}'
        signature = hmac.new(
            secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        assert veilmail.verify_webhook_signature(payload, signature, wrong_secret) is False

    def test_bytes_payload(self) -> None:
        secret = "whsec_test_secret"
        payload = b'{"type": "email.delivered", "data": {}}'
        signature = hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        assert veilmail.verify_webhook_signature(payload, signature, secret) is True

    def test_tampered_payload(self) -> None:
        secret = "whsec_test_secret"
        original = '{"type": "email.delivered", "data": {}}'
        tampered = '{"type": "email.delivered", "data": {"tampered": true}}'
        signature = hmac.new(
            secret.encode("utf-8"),
            original.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        assert veilmail.verify_webhook_signature(tampered, signature, secret) is False
