# NivaranX MVP Scope

## MVP user journeys

1. An authorized officer searches for an institution by AICTE Permanent ID.
2. The institution profile shows its complaint history across bureaus/cells.
3. An officer opens a complaint and reviews its status, assignment, SLA, and action timeline.
4. A matching service flags potentially overlapping complaints with human-readable reasons.
5. An authorized reviewer marks a candidate as confirmed overlap, not a duplicate, or needs more information.
6. Supervisors review due-soon/overdue cases and aggregate workload metrics.

## Core entities

- **Institution:** stable internal ID, AICTE Permanent ID, name, location, status.
- **Bureau:** stable ID, name, active status.
- **Complaint:** stable ID, institution ID, bureau ID, category, description, received timestamp, status, SLA deadline.
- **Assignment:** complaint ID, officer ID, assignment timestamp, end timestamp, status.
- **Action:** complaint ID, actor ID, action type, notes, timestamp, evidence reference.
- **DuplicateCandidate:** complaint pair, score, matching signals, reviewer status, reviewer and review timestamp.
- **Notification:** complaint ID, trigger type, created/sent timestamps, delivery status.

## Important rules

- A Permanent ID identifies an institution; it does not identify a complaint.
- Preserve each complaint as its own record. Link possible overlaps rather than silently merging or deleting them.
- Keep complaint actions append-only in the audit history. Corrections should be recorded as new events.
- Calculate SLA status from an explicitly configured policy and timestamps. Do not invent official AICTE deadlines.
- Define reporting periods and numerator/denominator clearly for disposal and resolution metrics.
- Require authorization checks on every API endpoint, not only in the frontend.
- Use synthetic data for the demo until data access and privacy requirements are approved.

## Duplicate candidate scoring (initial design)

Start with explainable signals such as same institution, normalized category match, reference-number match, date-window overlap, and description similarity. Persist the signals used so reviewers can understand why a pair was flagged. Treat thresholds as configurable and validate them on labeled examples. Similarity is a prioritization aid, not a final finding.

## Non-goals for the first demo

- Automatically making regulatory decisions.
- Automatically merging or closing complaints.
- Claiming live integration with AICTE systems without an approved API or data feed.
