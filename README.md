# NivaranX

**AI-Powered Integrated Institution Complaint Monitoring System**

> One Institution. One View. Smarter Resolution.

NivaranX is a proposed Smart India Hackathon solution for centralized monitoring of institution-related complaints across AICTE bureaus/cells. The platform is designed to consolidate institution complaint histories, track assignments and actions, flag potential duplicate complaints, monitor configurable SLA deadlines, and provide operational analytics.

## Planned capabilities

- **Institution profiles:** consolidate complaint history using the AICTE Permanent ID.
- **Complaint lifecycle:** register, assign, investigate, update, resolve, and audit actions.
- **Potential duplicate detection:** combine rule-based matching with semantic text similarity; flag candidates for human review rather than auto-merging cases.
- **SLA monitoring:** configurable deadlines, due-soon warnings, overdue alerts, and escalation queues.
- **Analytics:** case aging, disposal rates, bureau workload, and resolution-time reporting.
- **Access control:** role-based permissions and auditable status changes.

## Proposed technology stack

- Frontend: React, TypeScript, Tailwind CSS, Recharts
- Backend: Python, FastAPI, SQLAlchemy
- Database: PostgreSQL (SQLite can be used for a lightweight local prototype)
- Background processing: scheduled jobs initially; Celery/Redis if required
- Duplicate analysis: explainable rules first, optionally supplemented with sentence embeddings

These are planned choices, not evidence of integration with existing AICTE systems. Use synthetic/demo records until approved data and integration specifications are provided.

## Initial development plan

1. Build the dashboard shell and navigation.
2. Define institution, complaint, assignment, action-history, and duplicate-candidate models.
3. Implement institution lookup and complaint tracking APIs.
4. Add duplicate candidate review and SLA alerts.
5. Add analytics, tests, documentation, and deployment configuration.

## Development status

Repository initialization. Features listed above are planned and should not be considered implemented until code and tests are added.
