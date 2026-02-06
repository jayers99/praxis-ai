# Agentic Performance Tracking System — Design Document

**Project:** Praxis AI
**Status:** Proposed (Explore/Shape)
**Date:** 2026-02-06
**ADR:** [005-agentic-performance-tracking](../../adr/005-agentic-performance-tracking.md)

---

## 1. The Problem

Praxis tells agents *what to do* (opinions, guardrails, lifecycle rules) but never learns whether its guidance was effective. This creates several failures:

1. **Opinions are untested hypotheses.** The opinions framework contains principles like "prefer composition over inheritance" but there's no data on whether projects that follow this principle have fewer regressions or higher audit pass rates.

2. **Bottlenecks are invisible.** If 80% of projects stall at the Shape→Formalize transition, there's no mechanism to detect this, let alone diagnose why.

3. **Quality is binary.** Validation says "valid" or "invalid" — it doesn't say "this project is trending toward problems" or "this project is unusually healthy."

4. **The system can't learn.** Without a feedback loop, every project starts with the same guidance regardless of accumulated experience.

---

## 2. The Self-Improving Loop

The core insight: Praxis already has the *plan* layer (opinions, governance) and the *execution* layer (validation, CLI). What's missing is the *observation* layer that closes the loop.

```
                     ┌──────────────────────┐
                     │    OPINIONS LAYER     │
                     │  principles, guidance │
                     │  guardrails, checks   │
                     └──────────┬───────────┘
                                │ guides
                                ▼
                     ┌──────────────────────┐
                     │   EXECUTION LAYER    │
                     │  stage transitions   │
                     │  validation, audit   │
                     │  artifact creation   │
                     └──────────┬───────────┘
                                │ produces
                                ▼
                     ┌──────────────────────┐
                     │  OBSERVATION LAYER   │  ◄── NEW
                     │  event telemetry     │
                     │  quality evaluation  │
                     │  pattern analysis    │
                     └──────────┬───────────┘
                                │ informs
                                ▼
                     ┌──────────────────────┐
                     │   REFINEMENT LAYER   │  ◄── NEW
                     │  opinion scoring     │
                     │  guardrail proposals │
                     │  checklist tuning    │
                     └──────────┬───────────┘
                                │ updates
                                ▼
                     ┌──────────────────────┐
                     │    OPINIONS LAYER    │  (cycle repeats)
                     └──────────────────────┘
```

This is the fundamental architecture of self-improvement: **act, observe, evaluate, adapt.**

---

## 3. Layer 1: Execution Telemetry

### What Gets Recorded

Every meaningful action in Praxis already passes through a service. Telemetry means persisting the *result* of these service calls as immutable events.

| Service | Event Type | What It Captures |
|---|---|---|
| `stage_service.transition()` | `stage.transition` | from_stage, to_stage, is_regression, reason, duration_since_last |
| `validate_service.validate()` | `validation.run` | total_issues, errors, warnings, rules_triggered, valid |
| `audit_service.audit()` | `audit.run` | checks_run, passed, warned, failed, check_names |
| `opinions_service.resolve()` | `opinions.resolved` | files_resolved, domain, stage, subtype |
| `init_service.init()` | `project.created` | domain, subtype, privacy_level, lifecycle_mode |
| `next_steps_service.get()` | `guidance.requested` | steps_returned, priorities |

### Event Format

```python
class MetricEvent(BaseModel):
    """A single immutable fact about what happened."""

    event_id: str           # UUID
    timestamp: str          # ISO8601
    event_type: str         # Dotted namespace: "stage.transition"
    project_slug: str       # Project identifier
    domain: str             # Domain at time of event
    stage: str              # Stage at time of event
    payload: dict[str, Any] # Event-type-specific data

    class Config:
        frozen = True       # Events are immutable
```

### Storage

Append-only JSONL file at `.praxis/metrics.jsonl` within each project:

```jsonl
{"event_id":"a1b2","timestamp":"2026-02-06T10:00:00Z","event_type":"stage.transition","project_slug":"my-cli","domain":"code","stage":"shape","payload":{"from":"explore","to":"shape","regression":false}}
{"event_id":"c3d4","timestamp":"2026-02-06T10:05:00Z","event_type":"validation.run","project_slug":"my-cli","domain":"code","stage":"shape","payload":{"valid":true,"errors":0,"warnings":1,"rules":["privacy_downgrade"]}}
```

Why JSONL:
- Append-only (no read-modify-write)
- Human-readable
- Greppable
- No schema migrations
- Each line is self-contained

### Emission Pattern

Events are emitted at the *end* of service calls, after the action completes. This ensures events reflect actual outcomes, not intentions.

```python
# In stage_service.py (conceptual)
def transition(self, project_path: Path, target_stage: Stage) -> StageResult:
    result = self._do_transition(project_path, target_stage)

    # Emit telemetry (fire-and-forget, never blocks the action)
    self.metrics.emit(MetricEvent(
        event_type="stage.transition",
        project_slug=self._get_slug(project_path),
        domain=config.domain,
        stage=target_stage,
        payload={
            "from": str(config.stage),
            "to": str(target_stage),
            "regression": target_stage < config.stage,
            "success": result.success,
        }
    ))

    return result
```

---

## 4. Layer 2: Quality Evaluation

Evaluation is **lazy** — computed from stored events when requested, not at event emission time. This keeps collection fast and allows evaluation logic to evolve independently.

### Quality Signals

#### Stage Velocity
How long does each stage take?

```
Input:   stage.transition events for a project
Output:  median time per stage, slowest stage, total lifecycle time
Value:   Identifies bottleneck stages across projects
```

#### Validation Health
Is the project getting cleaner or dirtier over time?

```
Input:   validation.run events for a project
Output:  error trend (improving/degrading/stable), most common rules triggered
Value:   Predicts problems before they block progression
```

#### Rework Rate
How often does work regress?

```
Input:   stage.transition events with regression=true
Output:  regressions / total transitions, regression sources and targets
Value:   Measures process stability; high rework → unclear formalization
```

#### Lifecycle Completion Rate
Do projects reach their destination?

```
Input:   stage.transition events across all projects
Output:  % reaching Execute, % reaching Sustain, % reaching Close, abandonment stage
Value:   The ultimate outcome metric — are projects finishing?
```

#### Opinion Coverage
How much available guidance was actually used?

```
Input:   opinions.resolved events for a project
Output:  opinions applied / opinions available, which opinions were skipped
Value:   Measures whether guidance is being surfaced and consumed
```

### Quality Score Model

```python
class QualityScore(BaseModel):
    """Composite quality assessment for a project."""

    project_slug: str
    evaluated_at: str           # ISO8601
    event_count: int            # How many events inform this score

    stage_velocity: StageVelocity | None
    validation_health: ValidationHealth | None
    rework_rate: float | None   # 0.0 (no rework) to 1.0 (all rework)
    lifecycle_progress: float   # 0.0 (capture) to 1.0 (close)
    opinion_coverage: float     # 0.0 (none applied) to 1.0 (all applied)

    # Derived
    overall_health: Literal["healthy", "at_risk", "troubled"]
```

### Evaluation Triggers

- `praxis metrics report` — On-demand evaluation
- `praxis status` — Could include a lightweight health indicator
- After stage transitions — Optional post-transition evaluation

---

## 5. Layer 3: Pattern Analysis

Cross-project analysis reveals systemic patterns that single-project metrics cannot.

### Pattern Types

#### Bottleneck Stages
```
Pattern:   Stage X consistently takes >2x the median across projects
Signal:    Checklists for stage X may be unclear, or the transition requires
           capabilities that guidance doesn't address
Action:    Review and improve opinions for stage X, or add a guardrail
```

#### Validation Failure Clusters
```
Pattern:   Rule Y fails in >40% of validation runs across projects
Signal:    The requirement may be unclear, or the default project setup
           doesn't satisfy it
Action:    Improve error messages, add to project templates, or adjust
           severity if the rule is too strict
```

#### Regression Patterns
```
Pattern:   Projects in domain Z regress from Execute→Formalize at 3x the rate
           of other domains
Signal:    Formalization standards for domain Z may be insufficient
Action:    Strengthen Formalize checklist for domain Z, review domain-specific
           opinions
```

#### Opinion Effectiveness
```
Pattern:   Projects that apply opinion set A have 30% lower rework rates than
           those that don't
Signal:    Opinion set A contains effective guidance
Action:    Promote these opinions, consider making key principles part of
           checklists
```

### Cross-Project Aggregation

At the workspace level (`$PRAXIS_HOME/.praxis/workspace-metrics.jsonl`), aggregate events from all managed projects. This enables:

- Portfolio-level health dashboards
- Domain-specific pattern detection
- Global trend analysis

---

## 6. Layer 4: Guidance Refinement

The ultimate goal: the system improves its own guidance based on evidence.

### Refinement Types

#### Opinion Effectiveness Scoring

Each opinion file gets an effectiveness score based on correlation with outcomes:

```yaml
# Generated annotation (not in opinion file itself)
opinions/code/principles.md:
  projects_exposed: 12        # Projects where this opinion was resolved
  avg_rework_rate: 0.15       # Among exposed projects
  baseline_rework_rate: 0.28  # Among all code projects
  effectiveness_delta: +0.13  # Positive = opinion correlates with improvement
  confidence: medium          # Based on sample size
```

#### Guardrail Proposals

When a validation failure recurs across projects, the system can propose a new guardrail:

```markdown
## Proposed Guardrail: G2 (Auto-Generated)

**Pattern Detected:** `missing_formalize_artifact` error occurs in 67% of
projects attempting stage transition to Commit.

**Proposed Rule:** Warn users at Shape stage that Formalize artifact will be
required, with a template generation prompt.

**Evidence:** 8/12 projects in last 90 days hit this error. Average delay
after error: 2.3 days.

**Confidence:** High (sufficient sample, consistent pattern)
```

#### Checklist Tuning

Stage checklists can be adjusted based on which items correlate with successful transitions:

```
Checklist item "Review SOD with stakeholder" is marked as completed
in 90% of projects that successfully reach Execute without regression,
but only 30% of projects that regress.

Recommendation: Elevate this item's priority in the Formalize checklist.
```

### Refinement Modes

1. **Report mode** (Phase 3): System generates a report with suggestions. Human decides.
2. **Propose mode** (Phase 4): System creates draft opinion/guardrail files for review.
3. **Auto-advisory mode** (future): System updates advisory-layer files directly, with git-tracked changes and audit trail.

Note: The system should **never** auto-modify governance or execution layer files. Only the opinions layer (which is explicitly advisory) is eligible for automated refinement, and even then only with full audit trail.

---

## 7. Starting Point: Phase 1 Implementation

### Why Start Here

Phase 1 (Event Foundation) is the right starting point because:

1. **It's the dependency for everything else.** Evaluation, patterns, and refinement all need events.
2. **It's low-risk.** Emitting events doesn't change any existing behavior.
3. **It provides immediate value.** Even raw event data answers questions like "when did I last transition?" and "how many validation errors have I had?"
4. **It's small.** ~4 new files, ~200 lines of code, modifications to 2-3 existing services.

### Phase 1 Scope

```
New files:
  src/praxis/domain/metrics/__init__.py
  src/praxis/domain/metrics/models.py          # MetricEvent model
  src/praxis/application/metrics_service.py    # Emit and query events
  src/praxis/infrastructure/metrics_store.py   # JSONL read/write

Modified files:
  src/praxis/application/stage_service.py      # Emit stage.transition events
  src/praxis/application/validate_service.py   # Emit validation.run events
  src/praxis/cli.py                            # Add `praxis metrics` command

New tests:
  tests/features/metrics.feature               # BDD scenarios
  tests/step_defs/test_metrics.py              # Step definitions
```

### Phase 1 CLI

```bash
# Show recent events
praxis metrics

# Show events for specific type
praxis metrics --type stage.transition

# Show event count summary
praxis metrics --summary

# Export events as JSON (for external analysis)
praxis metrics --export
```

### Phase 1 Acceptance Criteria

```gherkin
Feature: Agentic Performance Tracking

  Scenario: Stage transitions emit telemetry events
    Given a Praxis project at stage "capture"
    When I transition to stage "sense"
    Then a metric event of type "stage.transition" is recorded
    And the event payload contains from_stage "capture" and to_stage "sense"

  Scenario: Validation runs emit telemetry events
    Given a Praxis project with an invalid configuration
    When I run validation
    Then a metric event of type "validation.run" is recorded
    And the event payload contains the validation errors

  Scenario: Metrics command shows recent events
    Given a Praxis project with recorded metric events
    When I run "praxis metrics"
    Then I see a summary of recent events

  Scenario: Metrics are append-only
    Given a Praxis project with existing metric events
    When a new event is recorded
    Then the existing events are unchanged
    And the new event is appended to the end
```

---

## 8. Data Flow Diagram

```
                        ┌─────────────────────────────────┐
                        │         CLI Commands             │
                        │  praxis stage, validate, audit   │
                        └──────────────┬──────────────────┘
                                       │ calls
                                       ▼
                        ┌─────────────────────────────────┐
                        │      Application Services        │
                        │  stage_service, validate_service │
                        │  audit_service, opinions_service │
                        └──────┬──────────────┬───────────┘
                               │              │
                    does work   │              │  emits event
                               ▼              ▼
                  ┌──────────────┐   ┌─────────────────────┐
                  │  praxis.yaml │   │   metrics_service    │
                  │  artifacts   │   │                      │
                  └──────────────┘   └──────────┬──────────┘
                                                │ persists
                                                ▼
                                    ┌──────────────────────┐
                                    │   metrics_store      │
                                    │ .praxis/metrics.jsonl│
                                    └──────────┬──────────┘
                                               │ reads
                                               ▼
                                    ┌──────────────────────┐
                                    │  evaluation_service   │  (Phase 2)
                                    │  quality scores       │
                                    └──────────┬──────────┘
                                               │ analyzes
                                               ▼
                                    ┌──────────────────────┐
                                    │  improvement_service  │  (Phase 3-4)
                                    │  pattern detection    │
                                    │  refinement proposals │
                                    └──────────────────────┘
```

---

## 9. Relationship to Existing Systems

### Stage History (praxis.yaml)

Stage history in `praxis.yaml` is the *committed record* of transitions — it's part of the project's governed state. Metric events are the *observational record* — they capture more detail (timing, context, ephemeral data) but are not governance artifacts. They complement each other:

- `praxis.yaml` history: authoritative, minimal, versioned in git
- `metrics.jsonl`: detailed, append-only, local observation data

### Role Metrics Framework

The role metrics framework defines *what to measure*. APTS provides *how to measure it*. Specifically:

| Framework Metric | APTS Event Source |
|---|---|
| Kickback Rate | `stage.transition` with regression=true |
| Time-to-Resolution | Duration between regression and next forward transition |
| Review Cycle Count | Count of regressions for same stage pair |
| First-pass Acceptance | `validation.run` with valid=true on first attempt |

### Pipeline System (PKDP)

The pipeline already tracks stage execution with timestamps and agent outputs. APTS can consume pipeline events as another event source, giving unified metrics across both project lifecycle and knowledge distillation.

---

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Metrics become noise, not signal | Start with 3-5 event types max; add only when there's a question to answer |
| Storage growth | JSONL compresses well; add rotation after N events or N days |
| Privacy concerns (tracking AI behavior) | All data is local; no external transmission; follows project privacy level |
| Gaming metrics | Metrics are for learning, not performance review; follow anti-patterns from metrics framework |
| Analysis paralysis | Phase 1 is just collection; don't build analysis until there's data to analyze |
| Correlation ≠ causation in opinion effectiveness | Always frame findings as correlations; require human judgment for causal claims |

---

## 11. Future Considerations

- **SQLite migration**: If query complexity outgrows JSONL grep-ability, migrate to SQLite with the same event schema
- **Visualization**: Export to CSV/JSON for external visualization tools
- **Multi-user**: If Praxis gains collaboration features, metrics need attribution
- **AI-native evaluation**: Use LLM to evaluate artifact quality (SOD completeness, test scenario coverage) as a richer quality signal than pass/fail checks
- **Comparative benchmarking**: Compare agent performance across different model versions or prompt strategies
