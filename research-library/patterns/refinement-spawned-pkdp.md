# Refinement-Spawned Knowledge Distillation (PKDP)

<!--
metadata:
  id: patterns-refinement-spawned-pkdp-2026-01-03
  title: Refinement-Spawned Knowledge Distillation Pattern
  date: 2026-01-03
  status: poc
  topic: patterns
  keywords: [refinement, pkdp, knowledge-gaps, spikes, research-spawn, chain-model]
  consensus: low
  depth: poc
  sources_count: 0
  ccr_status: n/a
-->

## Executive Summary

- Knowledge gaps emerge predictably during ticket refinement via a **chain model**: Clarifying Question → Spike → Knowledge Gap
- Gaps discovered in spikes indicate missing conceptual foundations in Praxis specifications or opinions
- **Size-based routing** determines research approach: Small gaps use background agents; Medium/Large gaps use dedicated PKDP sessions
- The pattern separates **gap detection** (during refinement) from **gap resolution** (via PKDP research)
- **POC status:** Templates and runbook integration complete; validation pending first real-world test

## Consensus Rating

**Low (POC)**: Pattern is theoretically grounded but not yet validated in practice. Awaiting at least one successful gap → research → integration cycle.

## Key Caveats

### Untested in Production

This pattern emerged from observing ad-hoc behavior during feature refinement. The formalized process has not yet been tested. Key risks:

- Gap detection signals may be too subtle or too frequent
- Size heuristics may not map to actual research effort
- Background agent routing may not integrate smoothly with refinement flow

### Scope Creep Risk

The pattern intentionally allows spawning research mid-refinement. Guardrails are needed:

- **POC limit:** One gap per refinement session
- **Deferral is valid:** Not every gap requires immediate research
- **Timeboxes:** Research should be bounded (S: 2h, M: 8h, L: explicit)

## The Chain Model

### How Gaps Emerge

During ticket refinement, knowledge gaps follow a predictable chain:

```
Clarifying Question → Spike → Knowledge Gap
```

1. **Clarifying Question:** Agent asks to understand the feature better
2. **Spike:** Question triggers investigation of codebase/specs
3. **Knowledge Gap:** Spike reveals Praxis lacks needed conceptual foundation

### Detection Signals

| Signal | Example | Gap Type |
|--------|---------|----------|
| Missing definition | "The spec doesn't define 'staged validation'" | Terminology gap |
| Conflicting guidance | "lifecycle.md says X but opinions say Y" | Consistency gap |
| Missing pattern | "No established pattern for multi-stage approval" | Architectural gap |
| Undocumented prior art | "This resembles capability maturity models" | Foundation gap |

### What's NOT a Knowledge Gap

- Questions answerable by existing docs
- Implementation decisions specific to the feature
- User preference questions
- Scope decisions

## Size-Based Routing

Gap size determines research approach:

| Size | Characteristics | Research Time | Route |
|------|-----------------|---------------|-------|
| **Small** | Single concept, non-blocking | 1-2 hours | Background agent |
| **Medium** | Pattern/cross-cutting concept | 4-8 hours | Dedicated PKDP session |
| **Large** | Architectural foundation | 12+ hours | Extended PKDP session |

### Sizing Heuristics

**Small (S):**
- Answer exists in external sources
- Single concept or definition
- Refinement can continue with assumption

**Medium (M):**
- Requires synthesis across sources
- May need CCR validation
- May or may not block refinement

**Large (L):**
- Requires prior art research
- Definitely needs CCR + HVA
- Likely blocks refinement

## Process Flow

```
Gap Detected (in spike)
    ↓
Size Estimate (S/M/L)
    ↓
Route Recommendation (agent/session)
    ↓
Present to User
    ↓
User Decision:
  - SPAWN → Initiate research
  - DEFER → Continue with explicit assumption
  - PROCEED → User judges gap not significant
    ↓
[If spawned]
    ↓
Research executes (agent or PKDP)
    ↓
Research completes (HVA for PKDP)
    ↓
Handoff back to feature
    ↓
Integrate findings
```

## Artifacts

### Gap Tracking

`X.XX-knowledge-gap-flags.md` — Created in refinement WIP folder when gaps detected

Contains:
- Gap summary table (ID, description, size, route, status)
- Detection chain (question → spike → gap)
- Size rationale
- Spawn decision and outcome

### Research Handoff

`X.XX-research-handoff-<gap-id>.md` — Created when research completes

Contains:
- Handoff summary (gap ID, artifact link, PKDP run)
- Key findings relevant to feature
- Recommendations for feature spec
- Integration checklist

## Integration Points

### Runbook Integration

Knowledge Gap Detection section added to `ticket-refinement-runbook.md` (Phase 6, after spikes).

Companion doc: `ticket-refinement-runbook-pkdp-companion.md`

### PKDP Integration

Research spawned via standard PKDP process:
- Small gaps: Background researcher agent (lighter weight)
- Medium/Large gaps: `praxis pipeline init` + full PKDP stages

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Chain model (Q → spike → gap) | Spikes are the natural trigger; they're already discovering architectural needs |
| Size routing | Conservative until POC validates; prevents over-investment in small gaps |
| User decides spawn | AI recommends but human controls scope and timing |
| Flagging in all phases | Gaps can emerge in Phase 1, 3-4, or 6 |
| Dedicated flag artifact | Keeps gaps visible and trackable, separate from decisions log |
| One gap limit (POC) | Prevents scope creep during initial validation |

## Open Questions

1. **Gap cascade:** What if researching one gap reveals more gaps? (Proposed: queue additional gaps)
2. **Parallel research:** Can multiple gaps be researched in parallel? (Deferred to post-POC)
3. **Background agent integration:** How does agent output flow back to refinement? (Using `_workshop/1-inbox/`)

## Related Topics

- [Issue Refinement Runbook](../../../extensions/praxis-workshop/runbooks/issue-refinement-runbook.md) — Integration point
- [PKDP Guide](../../docs/guides/pkdp.md) — Research pipeline
- [Knowledge Distillation Pipeline](../foundations/knowledge-distillation-pipeline.md) — PKDP foundations

---

_Status: POC — awaiting first real-world validation_
_Maintained by: research-spawned from issue #126_
