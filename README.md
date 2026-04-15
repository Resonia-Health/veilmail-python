# Veil Mail Python SDK

[![PyPI version](https://img.shields.io/pypi/v/veilmail.svg)](https://pypi.org/project/veilmail/)
[![Python Version](https://img.shields.io/pypi/pyversions/veilmail.svg)](https://pypi.org/project/veilmail/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

The official Python SDK for [Veil Mail](https://veilmail.xyz) — secure transactional and marketing email with automatic PII protection, CASL compliance, and a developer-first API.

> **Veil Mail is a drop-in alternative to [Resend](https://veilmail.xyz/vs/resend), [SendGrid](https://veilmail.xyz/vs/sendgrid), [Mailgun](https://veilmail.xyz/vs/mailgun), and [Postmark](https://veilmail.xyz/vs/postmark).** If you're already using one of these, migration is typically a package swap and a few renamed arguments.

```python
# Before — Resend
import resend
resend.api_key = "re_xxxxx"
resend.Emails.send({
    "from": "hello@yourdomain.com",
    "to": "user@example.com",
    "subject": "Welcome!",
    "html": "<h1>Welcome</h1>",
})

# After — Veil Mail
from veilmail import VeilMail
client = VeilMail("veil_live_xxxxx")
client.emails.send(
    from_email="hello@yourdomain.com",
    to="user@example.com",
    subject="Welcome!",
    html="<h1>Welcome</h1>",
)
```

**Migration guides:** [from Resend](https://veilmail.xyz/docs/guides/migrate-resend) · [from SendGrid](https://veilmail.xyz/docs/guides/migrate-sendgrid) · [from Mailgun](https://veilmail.xyz/docs/guides/migrate-mailgun) · [from Postmark](https://veilmail.xyz/docs/guides/migrate-postmark)

## Installation

```bash
pip install veilmail
```

Or install from source:

```bash
pip install git+https://github.com/Resonia-Health/veilmail-python.git
```

Requires Python 3.9+.

## Quick Start

```python
from veilmail import VeilMail

client = VeilMail("veil_live_xxxxx")

email = client.emails.send(
    from_email="hello@yourdomain.com",
    to="user@example.com",
    subject="Hello!",
    html="<h1>Welcome!</h1>",
)

print(f"Sent: {email['id']}")
```

> **Note on `from_email`:** Python reserves `from` as a keyword, so the SDK uses `from_email` as the parameter name. This is the only significant field rename versus the Resend / SendGrid Python SDKs.

## Features

- **Automatic PII protection** — every email is scanned for SSNs, credit cards, medical records, and other sensitive data via Google Cloud DLP before delivery
- **CASL & GDPR compliance** — built-in consent tracking, subscription topics, and compliant unsubscribe handling
- **Drop-in alternative** to Resend, SendGrid, Mailgun, and Postmark Python SDKs
- **Transactional + marketing** — one API for both, classified via the `type` field
- **Typed with mypy** — full type hints across the public surface
- **Built on `httpx`** — modern HTTP client with connection pooling

## Sending Marketing Emails

Set `type="marketing"` to automatically add unsubscribe headers, footer, and suppression checks:

```python
client.emails.send(
    from_email="news@yourdomain.com",
    to="subscriber@example.com",
    subject="Monthly Newsletter",
    html="<h1>Updates</h1>",
    type="marketing",  # Adds List-Unsubscribe headers, footer, physical address
)
```

## Error Handling

```python
from veilmail import (
    VeilMail,
    VeilMailError,
    AuthenticationError,
    ValidationError,
    PiiDetectedError,
    RateLimitError,
)

try:
    client.emails.send(...)
except PiiDetectedError as e:
    print(f"PII detected: {e.pii_types}")
except RateLimitError as e:
    print(f"Rate limited, retry after: {e.retry_after}")
except AuthenticationError:
    print("Invalid API key")
except VeilMailError as e:
    print(f"API error: {e.code} - {e}")
```

## Configuration

```python
client = VeilMail(
    api_key="veil_live_xxxxx",
    base_url="https://api.veilmail.xyz",  # Optional
    timeout=30.0,  # Optional, in seconds
)
```

## Resources

- [Full documentation](https://veilmail.xyz/docs)
- [Python SDK reference](https://veilmail.xyz/docs/sdk-python)
- [Email API reference](https://veilmail.xyz/docs/emails)
- [Authentication](https://veilmail.xyz/docs/authentication)
- [Webhooks](https://veilmail.xyz/docs/webhooks)
- [MCP server for Claude/Cursor](https://veilmail.xyz/docs/mcp)
- Framework guides: [FastAPI](https://veilmail.xyz/docs/guides/fastapi) · [Django](https://veilmail.xyz/docs)

## License

MIT — see [LICENSE](./LICENSE) for details.
