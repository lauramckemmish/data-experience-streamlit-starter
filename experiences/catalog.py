"""Single catalogue of available experiences."""

from config import (
    EXPERIENCE_CURIOUS,
    EXPERIENCE_PLAYGROUND,
    EXPERIENCE_YEAR8,
    EXPERIENCE_YEAR10,
)


def experience_catalog():
    return [
        (EXPERIENCE_CURIOUS, "A guided, facilitator-led experience. Replace the neutral steps with the CURIOUS workshop sequence for your dataset."),
        (EXPERIENCE_YEAR8, "A two-lesson Year 8 classroom pathway. The route and shell exist; add subject-specific pedagogy when ready."),
        (EXPERIENCE_YEAR10, "A two-lesson Year 10 classroom pathway. The route and shell exist; add subject-specific pedagogy when ready."),
        (EXPERIENCE_PLAYGROUND, "An open exploration space kept deliberately separate from the guided CURIOUS sequence."),
    ]
