"""Small, editable project configuration.

Change this file when adapting the starter to a new dataset or topic.
Lesson wording belongs in the relevant module under ``experiences/``.
"""

from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
# Shared-shell local dependencies. Copy only assets required by adopted helpers.
SIDEBAR_INSTITUTIONAL_LOGO = ASSETS_DIR / "unsw-sydney-logo-landscape.png"
# Landscape is the compact horizontal identity treatment for both identity rows.
ABOUT_INSTITUTIONAL_LOGO = ASSETS_DIR / "unsw-sydney-logo-landscape.png"
SIDEBAR_LANDSCAPE_LOGO = ASSETS_DIR / "unsw-sydney-logo-landscape.png"

# Resource content contract: these roles have different information jobs.
# short_name is the compact persistent identity used in the shell; keep it brief.
SHORT_NAME = "Data Experiences"
# descriptive_name is the formal identity shown in About; it may be longer.
DESCRIPTIVE_NAME = "Data Experiences: a starter for scientific data learning"
# hero_hook is the learner-facing main idea, not a navigation or formal title.
HERO_HOOK = "Turn data into questions, investigations and discoveries"
RESOURCE_DESCRIPTION = "A reusable educational resource for exploring real datasets through guided and open-ended data experiences."
# Kept as a compatibility alias for existing Streamlit page configuration.
APP_TITLE = SHORT_NAME
APP_ICON = "📊"
APP_SUBTITLE = "Explore a real scientific dataset through guided and open-ended experiences"
LANDING_ORIENTATION = "This example uses a small demonstration dataset. Replace this sentence with the scientific question, dataset and context for your resource."

EXPERIENCE_CURIOUS = "CURIOUS"
EXPERIENCE_YEAR8 = "Year 8"
EXPERIENCE_YEAR10 = "Year 10"
EXPERIENCE_PLAYGROUND = "Data Exploration Playground"

# Dataset metadata shown prominently on the introduction page and in the sidebar.
# Update these when adapting the starter to a real dataset.
DATASET_NAME = "Taylor Swift demo dataset"
DATASET_SHORT_DESCRIPTION = (
    "A deliberately playful, non-scientific dataset using familiar song and album labels "
    "to demonstrate Starter functionality."
)
DATASET_SCOPE_NOTE = (
    "The song and album fields are ordinary labels. Every demo_* metric is synthetic "
    "demonstration data, not real Taylor Swift analytics or scientific evidence."
)
DATASET_SOURCE_LABEL = "Starter playful demo data"
DATASET_SOURCE_URL = None
DATASET_CITATION = None
DATASET_SOURCE_NOTE = (
    "This deliberately synthetic dataset exists to exercise Starter exploration, "
    "variable, graph and missing-data patterns. Identifying labels are used for familiarity; "
    "demo_* duration, energy, danceability, streams and mood values must not be read as real analytics."
)
# Resource-context authoring guidance: replace the hero/orientation and About
# content with claims verified for each derived resource. Institutional identity
# permission and resource stewardship are separate claims, and neither implies
# scientific/domain review. Credit distinctive perspectives that materially
# shaped the resource; use the vocabulary in
# playbook/decisions/contributor-credit.md. Keep review, feedback, support and
# partnership fields optional and resource-specific.
RESOURCE_STEWARD = {
    "name": "Dr Laura McKemmish",
    "affiliation": "UNSW Chemistry",
    "role": "Computational astrochemist",
    "descriptor": "10+ years creating research-connected science experiences and data-rich investigations for school students",
}

RESOURCE_ABOUT = {
    "title": DESCRIPTIVE_NAME,
    "description": RESOURCE_DESCRIPTION,
    "unsw_stewardship": (
        "**UNSW identity and stewardship**  \n"
        "This Starter uses UNSW Sydney branding under the stewardship of Dr Laura McKemmish, UNSW Chemistry. "
        "Use of the UNSW name and visual identity in a derived resource is not automatically granted by use of this template. "
        "If you are adapting this Starter for a new resource, confirm the appropriate UNSW ownership, approval and branding arrangements with Laura before retaining the UNSW identity."
    ),
    "stewardship": (
        f"**Resource stewardship · {RESOURCE_STEWARD['name']}, {RESOURCE_STEWARD['affiliation']}**  \n"
        f"*{RESOURCE_STEWARD['role']} · {RESOURCE_STEWARD['descriptor']}*  \n\n"
        "Resource stewardship means owning the resource's coherence, development and maintenance. "
        "Scientific/domain review is an additional local claim: add it only when the named reviewer has relevant disciplinary expertise to stand behind this resource's scientific content. "
        "Do not infer it from institutional affiliation, professional title, ownership or computational/data-science expertise."
    ),
    "why": "The shared shell helps new resources present their purpose, context and accountability clearly while keeping local teaching content in its own experience modules. For your resource, use this section to explain the development choices and context that matter to trust and future improvement.",
    "development": "This Starter is intended to improve through use, testing and feedback. For your resource, describe the important development or iteration context, then replace this guidance with the status and evidence that readers should understand.",
    "feedback": "State how feedback can improve the resource and provide an appropriate route where one exists. Replace this guidance with your resource-specific feedback mechanism; do not imply that a feedback route exists if it does not.",
    "contributors": {},
    "contributors_intro": "Contributor credits are separate from resource stewardship. Identify people whose distinctive perspectives or intellectual contributions materially shaped the resource or the approach behind it. Credit the contribution rather than job title, seniority, amount of labour, attendance or delivery alone. Replace this guidance with resource-specific provenance.",
    "contribution_vocabulary": {
        "Research translation": "Turning authentic research practices, questions, data, computational methods or ways of reasoning into learning experiences.",
        "Data-science perspective": "A specifically data-science way of understanding, structuring or reasoning with data.",
        "Pedagogical expertise": "Learning design, evaluation, scaffolding or expertise in how learning experiences work.",
        "Teacher perspective": "Judgment grounded in substantial direct secondary-school classroom teaching.",
        "Near-peer perspective": "Insight arising from relative proximity to the learner journey and transition towards independent or facilitating practice.",
    },
    "support": "Use this optional subsection to acknowledge meaningful institutional, funding or partnership support where relevant. Replace this guidance with verified acknowledgements, or leave it empty when there is nothing to state.",
}
