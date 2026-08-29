"""Small, editable project configuration.

Change this file when adapting the starter to a new dataset or topic.
Lesson wording belongs in the relevant module under ``experiences/``.
"""

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
DATASET_NAME = "Sample scientific dataset"
DATASET_SHORT_DESCRIPTION = (
    "A small example dataset included only to demonstrate the app structure. "
    "Replace it with the scientific dataset for your project."
)
DATASET_SCOPE_NOTE = (
    "Every scientific dataset has a scope. Replace this sentence with a short, "
    "student-friendly explanation of what this dataset includes and excludes."
)
DATASET_SOURCE_LABEL = "Starter-generated example data"
DATASET_SOURCE_URL = None
DATASET_CITATION = None
DATASET_SOURCE_NOTE = (
    "Replace this note with the original dataset provider, publication, repository, "
    "DOI, licence, or other provenance information."
)
# Resource-context authoring guidance: replace the hero/orientation and About
# content with claims verified for each derived resource. Stewardship names the
# UNSW identity permission is separate from resource scientific/educational
# stewardship; both must be reviewed locally. Credit distinctive perspectives
# that materially shaped the resource; use the vocabulary in
# playbook/decisions/contributor-credit.md. Keep review, feedback, support and
# partnership fields optional and resource-specific.
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
        "**Resource-specific scientific and educational stewardship**  \n"
        "Identify the person or people who take appropriate intellectual responsibility for the scientific and/or educational content of this resource. "
        "State the relevant expertise or role that makes that stewardship meaningful. Replace this guidance with the actual arrangement for your resource."
    ),
    "why": "The shared shell helps new resources present their purpose, context and accountability clearly while keeping local teaching content in its own experience modules. For your resource, use this section to explain the development choices and context that matter to trust and future improvement.",
    "development": "This Starter is intended to improve through use, testing and feedback. For your resource, describe the important development or iteration context, then replace this guidance with the status and evidence that readers should understand.",
    "feedback": "State how feedback can improve the resource and provide an appropriate route where one exists. Replace this guidance with your resource-specific feedback mechanism; do not imply that a feedback route exists if it does not.",
    "contributors": {"Laura McKemmish": "Pedagogical expertise"},
    "contributors_intro": "For your resource, identify people whose distinctive perspectives or intellectual contributions materially shaped the resource or the approach behind it. Credit the contribution rather than job title, seniority, amount of labour, attendance or delivery alone. Replace this guidance and the worked attribution below with resource-specific provenance.",
    "contribution_vocabulary": {
        "Research translation": "Turning authentic research practices, questions, data, computational methods or ways of reasoning into learning experiences.",
        "Data-science perspective": "A specifically data-science way of understanding, structuring or reasoning with data.",
        "Pedagogical expertise": "Learning design, evaluation, scaffolding or expertise in how learning experiences work.",
        "Teacher perspective": "Judgment grounded in substantial direct secondary-school classroom teaching.",
        "Near-peer perspective": "Insight arising from relative proximity to the learner journey and transition towards independent or facilitating practice.",
    },
    "support": "Use this optional subsection to acknowledge meaningful institutional, funding or partnership support where relevant. Replace this guidance with verified acknowledgements, or leave it empty when there is nothing to state.",
}
