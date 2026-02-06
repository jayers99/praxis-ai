# ADR-005: Agentic Performance Tracking System

**Status:** Proposed
**Date:** 2026-02-06
**Authors:** @jayers99, Claude

## Context

Praxis governs *how* work should proceed (lifecycle, validation, opinions) but has no mechanism to observe *how well* work actually proceeds. The system cannot answer:

- Did following opinion X lead to better outcomes?
- Which stages are bottlenecks across projects?
- Is agent-generated work improving over time?
- Which validation failures recur, and what causes them?
- Are guardrails effective or just friction?

The role metrics framework (`core/roles/metrics-framework.md`) defines theoretical metrics but has no automation. Stage history in `praxis.yaml` captures transitions but not quality signals. Validation and audit results are ephemeral — computed, displayed, then discarded.

Without observability, Praxis cannot self-improve. Opinions remain static guesses. Guardrails are added reactively. There is no evidence-based path from "this seems like good guidance" to "this guidance measurably improves outcomes."

## Decision

Introduce an **Agentic Performance Tracking System (APTS)** built on three layers:

1. **Execution Telemetry** — Persist what happens (events)
2. **Quality Evaluation** — Assess how good it was (scores)
3. **Guidance Refinement** — Feed learnings back (adaptation)

### Design Principles

- **Append-only event log** — Events are immutable facts, not mutable state
- **Opt-in, low-friction** — Tracking adds no mandatory steps to existing workflows
- **Local-first** — All data stays in the project (no external services)
- **Evaluation is separate from collection** — Collect raw events; evaluate lazily
- **The system tracks itself** — APTS follows the Praxis lifecycle (this ADR is its Formalize artifact)

### Architecture

Follows the existing hexagonal pattern:

```
Domain:         src/praxis/domain/metrics/
                  models.py       — MetricEvent, QualityScore, PerformanceReport
                  evaluators.py   — Pure evaluation functions
                  patterns.py     — Pattern detection (stateless)

Application:    src/praxis/application/
                  metrics_service.py     — Record events, query history
                  evaluation_service.py  — Run evaluations on collected data
                  improvement_service.py — Generate refinement suggestions

Infrastructure: src/praxis/infrastructure/
                  metrics_store.py       — Append-only JSON log (.praxis/metrics.jsonl)
```

### Event Model

```python
class MetricEvent(BaseModel):
    timestamp: str          # ISO8601
    event_type: str         # stage_transition, validation_run, audit_check, etc.
    project_slug: str       # Which project
    domain: str             # Domain at time of event
    stage: str              # Stage at time of event
    payload: dict           # Event-specific data
```

### Integration Points

Events are emitted from existing services with no behavioral changes:

| Existing Service | Event Type | Payload |
|---|---|---|
| `stage_service` | `stage_transition` | from, to, duration_since_last, regression |
| `validate_service` | `validation_run` | issues, errors, warnings, valid |
| `audit_service` | `audit_run` | checks_passed, checks_failed, checks_warned |
| `opinions_service` | `opinions_resolved` | opinions_applied, domain, stage, subtype |
| `init_service` | `project_created` | domain, subtype, privacy_level |

### Quality Evaluation

Evaluations are computed from accumulated events, not collected in real-time:

| Signal | Source | Formula |
|---|---|---|
| Stage velocity | `stage_transition` events | Time between transitions |
| Validation health | `validation_run` events | Error rate over time, error categories |
| Rework rate | `stage_transition` events | Regression count / forward transition count |
| Audit trend | `audit_run` events | Pass rate change over time |
| Lifecycle completion | `stage_transition` events | Did project reach Execute? Sustain? Close? |
| Opinion coverage | `opinions_resolved` events | % of available opinions actually applied |

### Self-Improvement Loop

```
  ┌─────────────────────────────────────────────────────┐
  │                                                     │
  ▼                                                     │
Opinions ──► Guide Agent ──► Agent Works ──► Emit Events │
  ▲                                                     │
  │                                                     │
  └── Refinement ◄── Pattern Analysis ◄── Evaluate ◄───┘
```

1. **Opinions** guide agent behavior during work
2. **Agent** produces artifacts, transitions stages, runs validation
3. **Events** are emitted at each integration point
4. **Evaluation** computes quality scores from accumulated events
5. **Pattern Analysis** identifies what correlates with success/failure
6. **Refinement** suggests opinion updates, new guardrails, adjusted severity

The loop closes when evaluation data influences guidance. This can be:
- **Manual**: Human reviews metrics report and updates opinions
- **Semi-automated**: System generates suggested opinion edits for human review
- **Automated** (future): System updates advisory guidance directly (with audit trail)

## Consequences

### Positive

- Praxis can measure its own effectiveness for the first time
- Opinion quality becomes evidence-based rather than assumed
- Bottleneck stages become visible across projects
- The role metrics framework gets its automation backbone
- Project health is observable at a glance via `praxis metrics`

### Negative

- Adds `.praxis/metrics.jsonl` to each project (disk usage)
- Event emission adds minor overhead to existing commands
- Risk of "metrics theater" — tracking for its own sake
- Pattern analysis quality depends on sufficient project volume

### Mitigations

- Metrics file is append-only JSONL — minimal write overhead
- All tracking is opt-in; existing behavior unchanged
- Anti-pattern guidance in metrics framework already warns against gaming
- Start with simple aggregation; defer ML-based analysis until data volume justifies it

## Alternatives Considered

### Alternative 1: External Observability Platform

Ship events to Prometheus/Grafana/Datadog.

**Pros:** Rich visualization, alerting, dashboards
**Cons:** Violates local-first principle, adds infrastructure dependency, overkill for solo/small use
**Why rejected:** Praxis is designed for local-first workflows; external dependencies contradict the philosophy

### Alternative 2: Git-Only Tracking

Use git commit metadata and branch patterns to infer metrics.

**Pros:** No new storage, leverages existing infrastructure
**Cons:** Limited event granularity, expensive to query, can't capture ephemeral events like validation runs
**Why rejected:** Git captures transitions but not the quality signals between transitions

### Alternative 3: Database-Backed Metrics

Use SQLite for structured queries.

**Pros:** Richer query capabilities, aggregation support
**Cons:** Adds dependency, schema migrations, more complex infrastructure
**Why rejected:** Premature — JSONL provides sufficient capability for v1; migrate to SQLite if query complexity demands it

## Implementation Phases

### Phase 1: Event Foundation (Starting Point)
- `MetricEvent` model
- `MetricsStore` (append-only JSONL)
- Emit events from `stage_service` and `validate_service`
- `praxis metrics` CLI command (basic event listing)

### Phase 2: Quality Evaluation
- Evaluation functions (velocity, rework, health)
- `praxis metrics report` command
- Per-project quality scores

### Phase 3: Cross-Project Analysis
- Workspace-level metrics aggregation
- Pattern detection across projects
- Opinion effectiveness correlation

### Phase 4: Guidance Refinement
- Suggested opinion updates based on patterns
- Guardrail proposals from recurring failures
- Checklist adjustments from stage bottleneck data

## References

- [Role Metrics Framework](../core/roles/metrics-framework.md) — Theoretical metrics this system automates
- [ADR-001: Policy Engine](001-policy-engine.md) — Architecture decisions for validation
- [ADR-002: Validation Model](002-validation-model.md) — Validation rules that generate events
- [Guardrails](../core/governance/guardrails.md) — Execution-level rules refined by this system
