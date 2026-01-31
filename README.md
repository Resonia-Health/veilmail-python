# Veil Mail Python SDK

Official Python SDK for the [Veil Mail](https://veilmail.xyz) API.

## Installation

```bash
pip install veilmail
```

Or install from source:

```bash
pip install git+https://github.com/Resonia-Health/veilmail-python.git
```

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

## Documentation

Full documentation is available at [veilmail.xyz/docs/sdk-python](https://veilmail.xyz/docs/sdk-python).

## License

MIT - see [LICENSE](LICENSE) for details.
