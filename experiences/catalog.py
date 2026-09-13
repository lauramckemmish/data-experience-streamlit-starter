"""Single catalogue of the starter's three reference surfaces."""

from config import (
    EXPERIENCE_PATTERN_REFERENCE,
    EXPERIENCE_PLAYGROUND,
    EXPERIENCE_TEMPLATE,
)


def experience_catalog(*, enabled_only: bool = True):
    """Return experience metadata, optionally including disabled experiences."""
    catalog = [
        {
            "name": EXPERIENCE_TEMPLATE,
            "summary": "A small guided investigation that moves from a question and prediction to evidence and a learner response.",
            "audience_badge": "Guided investigation",
            "enabled": True,
        },
        {
            "name": EXPERIENCE_PLAYGROUND,
            "summary": "Open exploration of variables, distributions, relationships, missingness and evidence.",
            "audience_badge": "Open data exploration",
            "enabled": True,
        },
        {
            "name": EXPERIENCE_PATTERN_REFERENCE,
            "summary": "Canonical examples of selected shared interface and interaction patterns.",
            "audience_badge": "Authoring reference",
            "enabled": True,
        },
    ]
    return [item for item in catalog if item["enabled"] or not enabled_only]


def enabled_experience_names() -> list[str]:
    """Return the names of experiences available in normal navigation."""
    return [item["name"] for item in experience_catalog()]
