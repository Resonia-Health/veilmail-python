"""Resource classes for the Veil Mail SDK."""

from .analytics import Analytics
from .audiences import Audiences, Subscribers
from .campaigns import Campaigns
from .domains import Domains
from .emails import Emails
from .feeds import Feeds
from .forms import Forms
from .properties import Properties
from .sequences import Sequences
from .templates import Templates
from .topics import Topics
from .webhooks import Webhooks

__all__ = [
    "Analytics",
    "Audiences",
    "Campaigns",
    "Domains",
    "Emails",
    "Feeds",
    "Forms",
    "Properties",
    "Sequences",
    "Subscribers",
    "Templates",
    "Topics",
    "Webhooks",
]
