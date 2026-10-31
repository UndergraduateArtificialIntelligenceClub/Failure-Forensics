# Story Map

Epics across the top, sprints down the side. Each cell lists story keys; open the [User Stories](../requirements/user-stories.md) page for details.

| Sprint | Project setup & architecture | Python SDK | Ingestion & trace platform | Data model, product APIs & jobs | Security, DevOps & platform observability | Detection & DecisionGate | Root-cause forensics | Evidence, explanation & grounding | Human review & eval cases | Benchmarks & fault injection | Evaluation, regression & experiments | Developer console | Analytics, compare & export | Hardening, documentation & final demo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S1** | KAN-15<br>KAN-16<br>KAN-17<br>KAN-18 | KAN-19<br>KAN-20 |  | KAN-23<br>KAN-25 | KAN-21<br>KAN-22<br>KAN-24 | KAN-26<br>KAN-27 | KAN-28 | KAN-29 |  | KAN-32<br>KAN-34 | KAN-33 | KAN-30<br>KAN-31 |  |  |
| **S2** | KAN-35<br>KAN-36 | KAN-37<br>KAN-38 | KAN-39 | KAN-40 | KAN-41 | KAN-42<br>KAN-43 | KAN-44<br>KAN-45 |  |  | KAN-48<br>KAN-49 |  | KAN-46<br>KAN-47 |  |  |
| **S3** | KAN-50<br>KAN-51 | KAN-53<br>KAN-54 | KAN-52 | KAN-55<br>KAN-56<br>KAN-57 |  | KAN-58 | KAN-59 |  |  | KAN-62 |  | KAN-60<br>KAN-61 |  |  |
| **S4** | KAN-63 |  | KAN-64<br>KAN-65 | KAN-66 |  | KAN-67 |  | KAN-68 |  | KAN-71 | KAN-72 | KAN-69<br>KAN-70 |  |  |
| **S5** | KAN-73 | KAN-75<br>KAN-76 |  |  | KAN-78<br>KAN-102 | KAN-79<br>KAN-80 | KAN-74<br>KAN-81 |  | KAN-77 | KAN-84 |  | KAN-82<br>KAN-83 |  |  |
| **S6** |  | KAN-87 | KAN-88 | KAN-89 | KAN-90 | KAN-91 | KAN-86<br>KAN-92 | KAN-93 | KAN-101 | KAN-95 | KAN-96 | KAN-94 |  | KAN-85 |
| **S7** | KAN-109 |  |  |  | KAN-97<br>KAN-99<br>KAN-113 | KAN-103<br>KAN-104 | KAN-116 | KAN-105 | KAN-100 | KAN-108 | KAN-119 | KAN-106<br>KAN-118 | KAN-98<br>KAN-111 |  |
| **S8** | KAN-120 |  |  |  | KAN-112 | KAN-126 | KAN-117 |  |  |  | KAN-127<br>KAN-131<br>KAN-140 | KAN-129 | KAN-110 | KAN-121<br>KAN-132<br>KAN-133<br>KAN-134<br>KAN-135<br>KAN-136<br>KAN-137<br>KAN-138<br>KAN-139 |
| **Stretch** |  |  |  | KAN-124 |  | KAN-114<br>KAN-115 |  |  |  |  | KAN-130 | KAN-107<br>KAN-128 | KAN-122<br>KAN-123 | KAN-125 |

## Release slices

| Slice | Ends | What a user can do |
|---|---|---|
| Walking skeleton (M1) | 11 Dec 2026 | Run a benchmark app and see its trace as a graph and timeline. |
| MVP (M2) | 29 Jan 2027 | Flag a bad answer and get a grounded root-cause diagnosis on document and RAG pipelines. |
| Feature freeze (M3) | 12 Feb 2027 | Review a diagnosis, turn it into an eval case, agent benchmark, ranked causes, DecisionGate. |
| Code complete (M4) | 26 Feb 2027 | Regression runs, compare and analytics screens, staging release, evaluation report. |