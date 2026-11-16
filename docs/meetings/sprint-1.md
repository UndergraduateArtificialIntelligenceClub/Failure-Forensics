# Sprint 1 Meeting Minutes

2 Nov 2026 → 13 Nov 2026 · Definition & Architecture

## Sprint planning

**Date:** 2 Nov 2026 · **Attendees:** Pranav, Mohib, Eziokwu, Sehajvir (Absent: Sashreek, Aarsh, Vaishnavi, Kinjal) · **Note taker:** Mohib

**Agenda**

1. Project requirements and tools (Jira and Confluence)
2. Requirements summary
3. Sprint 1 discussion and role allocation

**Decisions**

- Reviewed project requirements, Jira/Confluence workflows, and Sprint 1 backlog items.
- Allocated initial Sprint 1 roles: Pranav (T1), Mohib (T3), Eziokwu (T3; updated post-meeting to T8), and Sehajvir (T4).

**Action items**

| Action | Owner | Due |
|---|---|---|
| Complete KAN-15, KAN-16, KAN-17, KAN-18 (T1) | Pranav | 6 Nov 2026 |
| Complete KAN-21, KAN-22, KAN-23, KAN-25 (T3) | Mohib | 6 Nov 2026 |
| Complete KAN-24 (T8, updated post-meeting from T3) | Eziokwu | 6 Nov 2026 |
| Complete KAN-26, KAN-27 (T4) | Sehajvir | 6 Nov 2026 |

## Mid-sprint check-in

**Date:** 6 Nov 2026 · **Attendees:** Pranav (Team Lead), Kinjal, Sashreek, Vaishnavi, Aarsh, Eziokwu, Mohib (Absent: Sehajvir) · **Note taker:** Aarsh

**Agenda**

1. Team progress, roles, sprints, and pairings
2. Definition of Done (DoD) and code review standards
3. Core observability concepts
4. Project purpose and 7 architecture layers
5. 7 planned deliverables and cost optimization

**Decisions**

- Acknowledged Mohib and Eziokwu for starting Sprint 1 tasks and updating the Jira dashboard.
- Confirmed workload point allocations: Pranav (54 pts), Vaishnavi (63 pts), Mohib (61 pts), Sehajvir (61 pts), Sashreek (64 pts), Kinjal (65 pts), Aarsh (63 pts), and Eziokwu (62 pts).
- Confirmed project schedule across 8 sprints (2 Nov – 26 Feb) covering milestones M0 through M4, final demo in mid-March, and **M0 Architecture Freeze on 13 Nov 2026**.
- Proposed Sprint 1 & 2 pairings: Pranav & Eziokwu, Kinjal & Aarsh, Sashreek & Vaishnavi, and Mohib & Sehajvir.
- Adopted 10 mandatory Definition of Done (DoD) criteria: acceptance tests passing, paired review + separate non-paired PR approval, green CI pipeline, no exposed secrets/credentials, mandatory local reviewer testing, type contracts updated, UI state handling (loading/empty/error), backend logging/metrics, and linking PRs to Jira.
- Enforced branching policy: all development must target the `sprint-1` branch and never merge directly to `main`.
- Reviewed 5 core observability concepts (Traces, Spans, Span Links, Quality Signals vs. Verdicts, Root Cause vs. Propagation, and Grounding), recommending 10–15 mins for trace/span material and ~60 mins total for a conceptual overview.
- Confirmed 7-layer AI failure diagnosis architecture (Python SDK, FastAPI, PostgreSQL, MinIO/S3, Redis, Celery, Next.js) and major ownership: Vaishnavi (Layer 1 – Ingestion SDK/API), Mohib (Backend/Infra/Data Layer; shares trace layer with Vaishnavi), Sashreek (Forensics & RCA Engine), and Kinjal (Layer 7 – UI/UX & DevX).
- Confirmed 7 planned deliverables (Python SDK, Storage Backend, Data Detectors, Forensic RCA Engine, Evidence/Grounding Gate, Human Review/Regression Gate, Next.js Dashboard) and a PostgreSQL/S3 caching strategy to reuse prior failure diagnoses and reduce repeated LLM API costs.

**Action items**

| Action | Owner | Due |
|---|---|---|
| Share AI-assisted presentations, OneNote PDF, and YouTube links on Discord and Confluence | Pranav | Next meeting |
| Share documented branch naming and PR approval rules on Confluence | Pranav | Next meeting |
| Perform CI/CD and `main`-branch checks after sprint completion | Pranav | 13 Nov 2026 |
| Continue/begin working on Sprint 1 tasks and pair programming assignments | All Team Members | 13 Nov 2026 |
| Review shared documentation/presentations on Discord and Confluence | All Team Members | Next meeting |
| Propose any architecture feedback, features, or changes before the M0 freeze | All Team Members | 13 Nov 2026 |
| Follow all 10 Definition of Done (DoD) criteria for sprint tasks | All Team Members | Ongoing |

## Sprint review

**Date:** 13 Nov 2026 · **Attendees:** · **Note taker:**

**Agenda**

1. 

**Decisions**

- 

**Action items**

| Action | Owner | Due |
|---|---|---|
| | | |

## Retrospective

**Date:** 13 Nov 2026 · **Attendees:** · **Note taker:**

**Agenda**

1. 

**Decisions**

- 

**Action items**

| Action | Owner | Due |
|---|---|---|
| | | |
