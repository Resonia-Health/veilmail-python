"""Tests for the Veil Mail Python SDK client."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

import veilmail

BASE_URL = "https://api.veilmail.xyz"


class TestClientInit:
    def test_requires_api_key(self) -> None:
        with pytest.raises(ValueError, match="API key is required"):
            veilmail.VeilMail("")

    def test_validates_api_key_format(self) -> None:
        with pytest.raises(ValueError, match="Invalid API key format"):
            veilmail.VeilMail("invalid_key")

    def test_accepts_live_key(self) -> None:
        client = veilmail.VeilMail("veil_live_test123")
        assert client is not None
        client.close()

    def test_accepts_test_key(self) -> None:
        client = veilmail.VeilMail("veil_test_test123")
        assert client is not None
        client.close()

    def test_context_manager(self) -> None:
        with veilmail.VeilMail("veil_live_test123") as client:
            assert client.emails is not None
            assert client.domains is not None
            assert client.templates is not None
            assert client.audiences is not None
            assert client.campaigns is not None
            assert client.webhooks is not None
            assert client.topics is not None


class TestAsyncClientInit:
    def test_requires_api_key(self) -> None:
        with pytest.raises(ValueError, match="API key is required"):
            veilmail.AsyncVeilMail("")

    def test_validates_api_key_format(self) -> None:
        with pytest.raises(ValueError, match="Invalid API key format"):
            veilmail.AsyncVeilMail("invalid_key")

    def test_accepts_live_key(self) -> None:
        client = veilmail.AsyncVeilMail("veil_live_test123")
        assert client is not None


class TestEmails:
    def test_send_email(self) -> None:
        with respx.mock:
            email_response = {
                "id": "email_123",
                "from": "hello@example.com",
                "to": ["user@example.com"],
                "subject": "Hello!",
                "status": "queued",
                "createdAt": "2025-01-01T00:00:00Z",
            }
            respx.post(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(200, json=email_response)
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.emails.send(
                    from_="hello@example.com",
                    to="user@example.com",
                    subject="Hello!",
                    html="<h1>Hello!</h1>",
                )

            assert result["id"] == "email_123"
            assert result["status"] == "queued"

            request = respx.calls.last.request
            body = json.loads(request.content)
            assert body["from"] == "hello@example.com"
            assert body["to"] == "user@example.com"
            assert body["subject"] == "Hello!"
            assert body["html"] == "<h1>Hello!</h1>"

    def test_send_email_with_options(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(200, json={"id": "email_123", "status": "queued"})
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                client.emails.send(
                    from_="hello@example.com",
                    to=["user1@example.com", "user2@example.com"],
                    subject="Hello!",
                    html="<p>Hi</p>",
                    cc="cc@example.com",
                    reply_to="reply@example.com",
                    tags=["welcome"],
                    metadata={"source": "test"},
                )

            request = respx.calls.last.request
            body = json.loads(request.content)
            assert body["to"] == ["user1@example.com", "user2@example.com"]
            assert body["cc"] == "cc@example.com"
            assert body["replyTo"] == "reply@example.com"
            assert body["tags"] == ["welcome"]
            assert body["metadata"] == {"source": "test"}

    def test_list_emails(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(200, json={
                    "data": [{"id": "email_1"}, {"id": "email_2"}],
                    "hasMore": False,
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.emails.list(limit=10, status="delivered")

            assert len(result["data"]) == 2
            request = respx.calls.last.request
            assert "limit=10" in str(request.url)
            assert "status=delivered" in str(request.url)

    def test_get_email(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/emails/email_123").mock(
                return_value=httpx.Response(200, json={"id": "email_123", "status": "delivered"})
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.emails.get("email_123")

            assert result["id"] == "email_123"

    def test_cancel_email(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/emails/email_123/cancel").mock(
                return_value=httpx.Response(200, json={
                    "id": "email_123",
                    "status": "cancelled",
                    "cancelledAt": "2025-01-01T00:00:00Z",
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.emails.cancel("email_123")

            assert result["status"] == "cancelled"


class TestDomains:
    def test_create_domain(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/domains").mock(
                return_value=httpx.Response(200, json={
                    "data": {"id": "dom_123", "domain": "mail.example.com", "status": "pending"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.domains.create(domain="mail.example.com")

            assert result["id"] == "dom_123"

    def test_list_domains(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/domains").mock(
                return_value=httpx.Response(200, json={
                    "data": [{"id": "dom_1"}],
                    "hasMore": False,
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.domains.list()

            assert len(result["data"]) == 1

    def test_verify_domain(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/domains/dom_123/verify").mock(
                return_value=httpx.Response(200, json={
                    "data": {"id": "dom_123", "status": "verified"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.domains.verify("dom_123")

            assert result["status"] == "verified"

    def test_delete_domain(self) -> None:
        with respx.mock:
            respx.delete(f"{BASE_URL}/v1/domains/dom_123").mock(
                return_value=httpx.Response(204)
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                client.domains.delete("dom_123")


class TestAudiences:
    def test_create_audience(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/audiences").mock(
                return_value=httpx.Response(200, json={
                    "data": {"id": "aud_123", "name": "Newsletter"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                result = client.audiences.create(name="Newsletter")

            assert result["id"] == "aud_123"

    def test_subscribers_add(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/audiences/aud_123/subscribers").mock(
                return_value=httpx.Response(200, json={
                    "data": {"id": "sub_123", "email": "user@example.com"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                subs = client.audiences.subscribers("aud_123")
                result = subs.add(email="user@example.com", first_name="Alice")

            assert result["id"] == "sub_123"

            request = respx.calls.last.request
            body = json.loads(request.content)
            assert body["email"] == "user@example.com"
            assert body["firstName"] == "Alice"

    def test_subscribers_export(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/audiences/aud_123/subscribers/export").mock(
                return_value=httpx.Response(
                    200,
                    content=b"email,firstName\nuser@example.com,Alice",
                    headers={"content-type": "text/csv"},
                )
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                subs = client.audiences.subscribers("aud_123")
                result = subs.export()

            assert "user@example.com" in result

    def test_subscribers_import(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/audiences/aud_123/subscribers/import").mock(
                return_value=httpx.Response(200, json={
                    "total": 2,
                    "created": 2,
                    "updated": 0,
                    "skipped": 0,
                    "errors": [],
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                subs = client.audiences.subscribers("aud_123")
                result = subs.import_subscribers(
                    subscribers=[
                        {"email": "user1@example.com"},
                        {"email": "user2@example.com"},
                    ]
                )

            assert result["created"] == 2


class TestErrorHandling:
    def test_authentication_error(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(401, json={
                    "error": {"code": "authentication_error", "message": "Invalid API key"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                with pytest.raises(veilmail.AuthenticationError):
                    client.emails.list()

    def test_forbidden_error(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(403, json={
                    "error": {"code": "forbidden", "message": "Insufficient scope"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                with pytest.raises(veilmail.ForbiddenError):
                    client.emails.list()

    def test_not_found_error(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/emails/email_999").mock(
                return_value=httpx.Response(404, json={
                    "error": {"code": "not_found", "message": "Email not found"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                with pytest.raises(veilmail.NotFoundError):
                    client.emails.get("email_999")

    def test_validation_error(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(400, json={
                    "error": {"code": "validation_error", "message": "Subject is required"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                with pytest.raises(veilmail.ValidationError, match="Subject is required"):
                    client.emails.send(
                        from_="hello@example.com",
                        to="user@example.com",
                        subject="",
                    )

    def test_rate_limit_error(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(
                    429,
                    json={"error": {"code": "rate_limit", "message": "Rate limit exceeded"}},
                    headers={"retry-after": "60"},
                )
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                with pytest.raises(veilmail.RateLimitError) as exc_info:
                    client.emails.send(
                        from_="hello@example.com",
                        to="user@example.com",
                        subject="Hello",
                        html="<p>Hi</p>",
                    )

            assert exc_info.value.retry_after == 60

    def test_pii_detected_error(self) -> None:
        with respx.mock:
            respx.post(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(422, json={
                    "error": {
                        "code": "pii_detected",
                        "message": "PII detected in email body",
                        "details": {"pii_types": ["PHONE_NUMBER", "EMAIL_ADDRESS"]},
                    },
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                with pytest.raises(veilmail.PiiDetectedError) as exc_info:
                    client.emails.send(
                        from_="hello@example.com",
                        to="user@example.com",
                        subject="Hello",
                        html="<p>Call 555-0123</p>",
                    )

            assert "PHONE_NUMBER" in exc_info.value.pii_types

    def test_server_error(self) -> None:
        with respx.mock:
            respx.get(f"{BASE_URL}/v1/emails").mock(
                return_value=httpx.Response(500, json={
                    "error": {"code": "server_error", "message": "Internal server error"},
                })
            )

            with veilmail.VeilMail("veil_live_test123") as client:
                with pytest.raises(veilmail.ServerError):
                    client.emails.list()
