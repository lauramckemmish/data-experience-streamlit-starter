# Learner-facing UI grammar

**Status:** Established working decision
**Scope:** Educational data-science resources built from this starter
**Review:** Revisit when evidence from learners, facilitators, teachers, accessibility review, or multiple new resources shows this grammar is inadequate.

## Design problem

Data Science Streamlits need a consistent semantic interaction grammar so learners can infer what a treatment means. The aim is **shared grammar + reusable components + separate experiences + local pedagogy**.

This grammar describes UI meaning, not a rigid screen template, fixed visual style, or mandatory vocabulary. A mature resource is evidence and reference, not automatically the universal template. Apply the pattern: **shared playbook → local resource design → explicit deviations**.

## Current decision

Use the following grammar when the same intellectual job occurs.

| Intellectual action | Standard learner-facing treatment | When to use it | When not to use it | Progression/state rule | Local-pedagogy boundary |
| --- | --- | --- | --- | --- | --- |
| Form a judgement | A short reasoning cue: spoken estimate, Think, discussion prompt, prediction, interpretation, or trust judgement. | Learners benefit from forming a judgement before later evidence or explanation. | Written submission would merely simulate engagement; verbal/group reasoning has no educational reason to become a form. | Usually non-blocking; require commitment only when it genuinely matters before evidence. | Word, widget, individual/group mode, and prompt are local. Do not impose fixed vocabulary. |
| Explore or compare evidence | A control changes displayed data, evidence, a model/view, a comparison, or makes a genuinely necessary commitment before evidence. | Search, filtering, selection, and view changes do intellectual work. | The control merely makes a page appear interactive. Free text must not be a progression gate by itself. | State belongs to what it changes; an essential commitment may gate the next reveal. | Open search, constrained selection, and the scientific comparison remain local. |
| Protect consequential evidence | A hard reveal with a locally clear prerequisite/reason. | Seeing evidence or conclusion early would undermine the intended reasoning sequence. | Ordinary continuation, routine page staging, or optional depth. | Evidence/conclusion starts hidden; revealed state persists; Continue remains unavailable when completing the reveal is essential. | The experience owns whether the prerequisite is prediction, comparison, interpretation, trust, or another action, and owns its wording. |
| Offer optional depth | A soft reveal/optional expander. | Provenance, source detail, optional scientific explanation, or facilitator-independent extension adds value without being required. | Evidence or explanation is necessary for the core reasoning journey. | Never blocks progression. | Label and content are local. |
| State a scientific conclusion | A named conclusion treatment, such as Key idea, Big idea, or scientific conclusion. | A conclusion must be distinguished from learner prediction or ordinary explanatory text. | The statement is learner-response validation or generic encouragement. | No gate is implied unless deliberately protected by a hard reveal. | Local wording may vary. Meaning comes from the named treatment/context, not colour alone; green or `st.success` is not itself “scientific conclusion.” |
| Validate a narrow response | Success-style validation only for a genuinely checkable response where that judgement is pedagogically appropriate. | A bounded check helps learners test a precise claim. | Generic praise, celebration for clicking, universal conclusion styling, or nuanced scientific interpretation. | Validation must not reduce interpretive science to simplistic right/wrong assessment. | Misconception work may need explanatory feedback rather than positive/negative marking. |
| Support, qualify, and limit evidence | Clearly labelled neutral support near the evidence/model: scope, range, missingness, instructions, guardrails, or limitations. Captions/sample notes suit lower-priority detail. | Learners need to know what is available, missing, in range, or unsupported by evidence. | Ordinary uncertainty should look like an application error, or qualification is hidden away. | No gate is implied. Warnings/errors are for actual unavailable, invalid, or exceptional conditions. | This is a semantic contract, not one universal widget. `st.info`-style presentation is broad neutral support, not a tightly defined category. |
| Read a graph | A concise nearby cue that says how to inspect evidence without giving away the conclusion. | A graph's variables, representation, or intended comparison needs decoding. | The graph is self-evident to the audience or the cue supplies the conclusion. | No gate is implied. | Complexity and audience determine the exact treatment. |
| Support delivery | Conditional, visually subordinate **Facilitator notes**, separate from learner content. | Facilitation, curriculum, or classroom guidance helps the person delivering the experience. | Learners need the material to complete the core journey. | Learner progress must not depend on opening Facilitator notes. | Their depth and content remain local. **Facilitator notes** is the canonical UI/component label; do not introduce Teacher notes or Teacher guidance as parallel names for this pattern. |
| Move between stages | Established staged steps with Back and Continue. | Learners are moving through a guided sequence. | Continue would be mistaken for evidence reveal, meaningful commitment, or a data/model action. | Back remains available; Continue is ordinary navigation and reflects any essential gates. | Step labels should name the real intellectual action: Think, Estimate, Explore, Compare, Discuss, Predict, Interpret, Test, or another appropriate local term. |

## Why this decision exists

Learner-facing interaction should make the intellectual job visible. Shared mechanics can remain understandable while resources preserve different scientific questions, evidence structures, classroom conditions, and reasoning journeys. Optional support, consequential action, response validation, and scientific claims should not become visually interchangeable.

## Boundaries and failure modes

Do not:

- add interaction for its own sake;
- require free text that does not affect reasoning or evidence;
- use colour alone to encode semantic meaning;
- treat `st.success` as both scientific conclusion and generic praise;
- hide essential material in optional expanders;
- use hard reveals for ordinary page staging;
- mechanically copy one mature application into another;
- proliferate callout variants where clear wording and context already carry the distinction.

Shared grammar must not standardise away spoken versus typed reasoning, open search versus constrained selection, graph-led versus question-led discussion, different amounts of Facilitator notes, or different reveal sequences where the evidence structure genuinely differs. The naming decision is terminology consolidation, not a claim that every facilitator is a teacher; genuine references to teachers as an audience or role remain appropriate.

## Reconsideration triggers

Revisit this decision when learners cannot infer interaction meaning, shared treatments create recurrent confusion, local exceptions proliferate, accessibility requires a different semantic treatment, or a recurring local pattern becomes mature enough to deserve shared status.
