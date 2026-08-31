"""Single catalogue of the four stable core experiences."""

from config import (
    EXPERIENCE_CURIOUS,
    EXPERIENCE_PLAYGROUND,
    EXPERIENCE_YEAR8,
    EXPERIENCE_YEAR10,
)


def experience_catalog(*, enabled_only: bool = True):
    """Return experience metadata, optionally including disabled experiences."""
    catalog = [
        {
            "name": EXPERIENCE_CURIOUS,
            "summary": "A guided, facilitator-led workshop built around a small number of purposeful questions.",
            "enabled": True,
        },
        {
            "name": EXPERIENCE_YEAR8,
            "summary": "A scaffolded two-lesson classroom pathway for working with data, variables, graphs and interpretation.",
            "enabled": True,
        },
        {
            "name": EXPERIENCE_YEAR10,
            "summary": "A deeper two-lesson classroom pathway with more independent analysis, comparison or modelling where the dataset supports it.",
            "enabled": True,
        },
        {
            "name": EXPERIENCE_PLAYGROUND,
            "summary": "Open exploration of one, two and three variables, with filtering or fitting when it helps answer a question.",
            "enabled": True,
        },
    ]
    return [item for item in catalog if item["enabled"] or not enabled_only]


def enabled_experience_names() -> list[str]:
    """Return the names of experiences available in normal navigation."""
    return [item["name"] for item in experience_catalog()]
