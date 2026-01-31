"""Main Veil Mail client classes."""

from __future__ import annotations

from typing import Any

from ._http import AsyncHttpClient, HttpClient
from .resources.analytics import Analytics, AsyncAnalytics
from .resources.audiences import AsyncAudiences, Audiences
from .resources.campaigns import AsyncCampaigns, Campaigns
from .resources.domains import AsyncDomains, Domains
from .resources.emails import AsyncEmails, Emails
from .resources.feeds import AsyncFeeds, Feeds
from .resources.forms import AsyncForms, Forms
from .resources.properties import AsyncProperties, Properties
from .resources.sequences import AsyncSequences, Sequences
from .resources.templates import AsyncTemplates, Templates
from .resources.topics import AsyncTopics, Topics
from .resources.webhooks import AsyncWebhooks, Webhooks


class VeilMail:
    """The official Veil Mail Python SDK client (synchronous).

    Example::

        import veilmail

        client = veilmail.VeilMail("veil_live_xxxxx")

        # Send an email
        email = client.emails.send(
            from_="hello@yourdomain.com",
            to="user@example.com",
            subject="Hello!",
            html="<h1>Welcome!</h1>",
        )

        # Use as context manager
        with veilmail.VeilMail("veil_live_xxxxx") as client:
            client.emails.send(...)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.veilmail.xyz",
        timeout: float = 30.0,
    ) -> None:
        """Create a new Veil Mail client.

        Args:
            api_key: API key (starts with veil_live_ or veil_test_).
            base_url: Base URL for API requests.
            timeout: Request timeout in seconds (default: 30).
        """
        self._http = HttpClient(api_key, base_url=base_url, timeout=timeout)

        self.emails = Emails(self._http)
        self.domains = Domains(self._http)
        self.templates = Templates(self._http)
        self.audiences = Audiences(self._http)
        self.campaigns = Campaigns(self._http)
        self.webhooks = Webhooks(self._http)
        self.topics = Topics(self._http)
        self.properties = Properties(self._http)
        self.sequences = Sequences(self._http)
        self.feeds = Feeds(self._http)
        self.forms = Forms(self._http)
        self.analytics = Analytics(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> VeilMail:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncVeilMail:
    """The official Veil Mail Python SDK client (asynchronous).

    Example::

        import veilmail

        client = veilmail.AsyncVeilMail("veil_live_xxxxx")

        # Send an email
        email = await client.emails.send(
            from_="hello@yourdomain.com",
            to="user@example.com",
            subject="Hello!",
            html="<h1>Welcome!</h1>",
        )

        # Use as async context manager
        async with veilmail.AsyncVeilMail("veil_live_xxxxx") as client:
            await client.emails.send(...)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.veilmail.xyz",
        timeout: float = 30.0,
    ) -> None:
        """Create a new async Veil Mail client.

        Args:
            api_key: API key (starts with veil_live_ or veil_test_).
            base_url: Base URL for API requests.
            timeout: Request timeout in seconds (default: 30).
        """
        self._http = AsyncHttpClient(api_key, base_url=base_url, timeout=timeout)

        self.emails = AsyncEmails(self._http)
        self.domains = AsyncDomains(self._http)
        self.templates = AsyncTemplates(self._http)
        self.audiences = AsyncAudiences(self._http)
        self.campaigns = AsyncCampaigns(self._http)
        self.webhooks = AsyncWebhooks(self._http)
        self.topics = AsyncTopics(self._http)
        self.properties = AsyncProperties(self._http)
        self.sequences = AsyncSequences(self._http)
        self.feeds = AsyncFeeds(self._http)
        self.forms = AsyncForms(self._http)
        self.analytics = AsyncAnalytics(self._http)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncVeilMail:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
