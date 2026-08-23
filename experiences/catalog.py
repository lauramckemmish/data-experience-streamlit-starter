"""Single catalogue of the four stable core experiences."""

from config import (
    EXPERIENCE_CURIOUS,
    EXPERIENCE_PLAYGROUND,
    EXPERIENCE_YEAR8,
    EXPERIENCE_YEAR10,
)


def experience_catalog():
    return [
        (
            EXPERIENCE_CURIOUS,
            "A guided, facilitator-led workshop that introduces the dataset slowly through a small number of purposeful questions.",
        ),
        (
            EXPERIENCE_YEAR8,
            "A scaffolded two-lesson classroom pathway for building confidence with data, variables, graphs and interpretation.",
        ),
        (
            EXPERIENCE_YEAR10,
            "A deeper two-lesson classroom pathway with more independent analysis and dataset-appropriate modelling or comparison.",
        ),
        (
            EXPERIENCE_PLAYGROUND,
            "Open exploration of one, two and three variables, with dataset-specific tools such as filtering or fitting where appropriate.",
        ),
    ]
