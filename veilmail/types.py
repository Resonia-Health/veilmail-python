"""Type definitions for the Veil Mail SDK.

Uses TypedDict for request/response types to provide type checking
without requiring instantiation of model classes.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union


# ============================================================================
# Common Types
# ============================================================================


class PaginatedResponse(TypedDict):
    data: List[Dict[str, Any]]
    hasMore: bool
    nextCursor: Optional[str]


# ============================================================================
# Email Types
# ============================================================================

EmailStatus = Literal[
    "pending", "queued", "sending", "sent", "delivered",
    "bounced", "failed", "cancelled", "scheduled", "complained",
]


class EmailAttachment(TypedDict, total=False):
    filename: str  # required
    content: str
    url: str
    contentType: str  # required
    contentId: str


class SendEmailParams(TypedDict, total=False):
    # Required fields
    from_: str  # mapped to "from" in JSON
    to: Union[str, List[str]]
    subject: str
    # Optional fields
    html: str
    text: str
    cc: Union[str, List[str]]
    bcc: Union[str, List[str]]
    reply_to: str
    headers: Dict[str, str]
    template_id: str
    template_data: Dict[str, Any]
    scheduled_for: str
    tags: List[str]
    metadata: Dict[str, Any]
    idempotency_key: str
    unsubscribe_url: str
    type: Literal["transactional", "marketing"]
    attachments: List[EmailAttachment]
    topic_id: str


class Email(TypedDict, total=False):
    id: str
    from_: str
    to: List[str]
    subject: str
    status: EmailStatus
    createdAt: str
    security: Dict[str, Any]
    sentAt: Optional[str]
    deliveredAt: Optional[str]
    openedAt: Optional[str]
    openCount: int
    clickCount: int
    events: List[Dict[str, Any]]


class ListEmailsParams(TypedDict, total=False):
    limit: int
    cursor: str
    status: EmailStatus
    tag: str
    after: str
    before: str


class BatchSendResult(TypedDict):
    total: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]


class CancelEmailResult(TypedDict):
    id: str
    status: Literal["cancelled"]
    cancelledAt: str


# ============================================================================
# Domain Types
# ============================================================================

DomainStatus = Literal["pending", "verified", "failed"]


class DnsRecord(TypedDict, total=False):
    type: Literal["TXT", "CNAME", "MX"]
    host: str
    value: str
    priority: int
    status: Literal["pending", "verified", "failed"]


class Domain(TypedDict, total=False):
    id: str
    domain: str
    status: DomainStatus
    dnsRecords: List[DnsRecord]
    verifiedAt: Optional[str]
    createdAt: str
    updatedAt: str


# ============================================================================
# Template Types
# ============================================================================

TemplateType = Literal["transactional", "marketing"]


class TemplateVariable(TypedDict, total=False):
    name: str
    type: Literal["string", "number", "boolean", "array", "object"]
    required: bool
    defaultValue: Any
    description: str


class Template(TypedDict, total=False):
    id: str
    name: str
    subject: str
    html: str
    text: Optional[str]
    type: TemplateType
    variables: List[TemplateVariable]
    description: Optional[str]
    createdAt: str
    updatedAt: str


# ============================================================================
# Audience Types
# ============================================================================


class Audience(TypedDict, total=False):
    id: str
    name: str
    description: Optional[str]
    subscriberCount: int
    createdAt: str
    updatedAt: str


# ============================================================================
# Subscriber Types
# ============================================================================

SubscriberStatus = Literal["pending", "active", "unsubscribed", "bounced", "complained"]
ConsentType = Literal["express", "implied", "not_set"]


class Subscriber(TypedDict, total=False):
    id: str
    email: str
    firstName: Optional[str]
    lastName: Optional[str]
    status: SubscriberStatus
    metadata: Any
    source: Optional[str]
    subscribedAt: Optional[str]
    confirmedAt: Optional[str]
    unsubscribedAt: Optional[str]
    consentType: Optional[ConsentType]
    consentSource: Optional[str]
    consentDate: Optional[str]
    consentExpiresAt: Optional[str]
    createdAt: str
    updatedAt: str


class ImportSubscribersResult(TypedDict):
    total: int
    created: int
    updated: int
    skipped: int
    errors: List[Dict[str, Any]]


# ============================================================================
# Activity Types
# ============================================================================

ActivityEventType = Literal[
    "queued", "processing", "sent", "delivered", "opened",
    "clicked", "bounced", "complained", "unsubscribed", "failed", "cancelled",
]


class ActivityEvent(TypedDict, total=False):
    id: str
    type: str
    timestamp: str
    data: Any
    email: Dict[str, Any]


# ============================================================================
# Campaign Types
# ============================================================================

CampaignStatus = Literal["draft", "scheduled", "sending", "sent", "paused", "cancelled"]


class CampaignStats(TypedDict):
    total: int
    sent: int
    delivered: int
    opened: int
    clicked: int
    bounced: int
    complained: int
    unsubscribed: int


class Campaign(TypedDict, total=False):
    id: str
    name: str
    subject: str
    from_: Dict[str, str]
    replyTo: Optional[Dict[str, str]]
    audienceId: str
    templateId: Optional[str]
    html: Optional[str]
    text: Optional[str]
    previewText: Optional[str]
    status: CampaignStatus
    tags: List[str]
    stats: CampaignStats
    scheduledAt: Optional[str]
    sentAt: Optional[str]
    createdAt: str
    updatedAt: str


# ============================================================================
# Webhook Types
# ============================================================================

WebhookEventType = Literal[
    "email.sent", "email.delivered", "email.opened", "email.clicked",
    "email.bounced", "email.complained", "email.failed",
    "subscriber.added", "subscriber.removed", "subscriber.unsubscribed",
    "campaign.sent", "campaign.completed",
]


class Webhook(TypedDict, total=False):
    id: str
    url: str
    events: List[WebhookEventType]
    description: Optional[str]
    enabled: bool
    secret: str
    lastTriggeredAt: Optional[str]
    createdAt: str
    updatedAt: str


class WebhookTestResult(TypedDict):
    success: bool
    statusCode: int
    responseTime: int
    error: Optional[str]


# ============================================================================
# Topic Types
# ============================================================================


class Topic(TypedDict, total=False):
    id: str
    name: str
    slug: str
    description: Optional[str]
    isDefault: bool
    sortOrder: int
    active: bool
    subscriberCount: int
    emailCount: int
    createdAt: str
    updatedAt: str


class TopicPreference(TypedDict):
    topicId: str
    topicName: str
    topicSlug: str
    topicDescription: Optional[str]
    subscribed: bool
