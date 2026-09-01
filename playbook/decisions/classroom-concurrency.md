# Classroom concurrency release readiness

## Decision

For a facilitated Streamlit classroom resource, use a lightweight browser smoke
test before release: **1 session → expected class size → safety margin**. The
usual default is **1 → 20 → 30** sessions. At each level, keep independent
Streamlit sessions open, reach one representative learner stage, run several
synchronized interactions and confirm that sessions remain usable.

## Why

Learners often act in synchronized bursts immediately after a facilitator's
instruction. A single-user visual check does not expose that release risk.
This small check captures the practical question—"does the application remain
usable when a class behaves like a class?"—without turning ordinary educational
app work into a load-testing programme.

## Reusable pattern

`tools/classroom_concurrency.py` owns the generic process lifecycle,
independent browser contexts, synchronized rounds, timeout/error detection and
clean shutdown. Each repository owns a short `classroom_smoke_adapter.py` that
defines:

- how its local Streamlit app starts;
- a representative learner route or stage;
- a real synchronized interaction; and
- a lightweight assertion that the stage remains usable.

The generic runner detects, where practical, server exits, page/browser errors,
failed navigation, interaction timeouts and clearly slow rounds. It does not
claim to diagnose memory leaks: Python allocator high-water behaviour alone is
not evidence of a leak.

## Stopping and escalation

If the test passes comfortably at the safety-margin level, record the result
and stop. Do not profile, optimise or refactor merely because extra measurement
is possible.

Escalate only for a failed or marginal smoke test. First reproduce the smallest
failing level and preserve the failing route/interaction. Deeper investigation
may then examine application logs, resource limits, memory over multiple
rounds, caching or deployment-specific constraints.

## Propagation

Copy the generic runner, its tests, this decision record and the Playwright
dependency to a mature resource. Write a new local adapter; do not copy the
Starter adapter's route. Exoplanets should supply Planet Shopping → Combine and
the representative Combine action. Any other resource supplies its own stable
learner stage and interaction.
