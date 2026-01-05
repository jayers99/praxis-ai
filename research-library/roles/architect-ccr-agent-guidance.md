# Architect CCR Enhancement for AI Agent Tickets

<!--
metadata:
  id: roles-architect-ccr-agent-guidance-2026-01-04
  title: Architect CCR Enhancement for AI Agent Tickets
  date: 2026-01-04
  author: researcher
  status: approved
  approved_by: human
  approved_date: 2026-01-04
  topic: roles
  also_relevant: [patterns]
  keywords: [architect, CCR, agent-readiness, architectural-guidance, tickets, kickback-triggers, issue-refinement]
  consensus: medium
  epistemic_standard: standard
  sources_count: 11
  timebox: 60 minutes
  supersedes: null
  related: [patterns-agent-architectural-direction-2026-01-04]
  reviewed_by: [process-engineer, software-architect]
  review_date: 2026-01-04
-->

## Executive Summary

- The Architect CCR review should verify that tickets contain adequate architectural guidance for AI coding agents
- Add one new checklist item: **Guidance level classified and architectural context adequate**
- Add five new kickback triggers mapped to guidance levels (0-3)
- Map guidance levels to existing ticket size indicators (XS/S → 0, M → 1, L → 2, XL → 3)
- Add "Architectural Context" section to the ticket template with level-appropriate content

## Consensus Rating

**Medium**: Core findings (guidance required, level-based approach) are well-supported by prior research. Implementation details validated by specialist review but need real-world testing.

## Body

### First Principles

**Why this matters:**

1. **Tickets are the primary delivery mechanism.** CLAUDE.md provides baseline context, but implementation details live in tickets. No architectural guidance in ticket = no architectural guidance for agent.

2. **Detection is unreliable; following is reliable.** LLMs achieve ~38.81% accuracy detecting patterns from code, but reliably follow explicit instructions with examples. The Architect's job is to ensure tickets contain guidance to follow.

3. **The reviewer gap.** Current Architect CCR checks enforce human-understandable constraints (boundaries, NFRs, ADRs). An agent-understandable check must be added.

### Findings

#### Finding 1: Add One Checklist Item

Add to the existing 8-item Architect review checklist:

```markdown
9. [ ] **Guidance level and architectural context**
   - Level: [0/1/2/3] (based on size/complexity)
   - [ ] Architectural Context section present
   - [ ] Content adequate for classified level
```

**Rationale:** Combines level determination and verification into a single actionable check.

#### Finding 2: Map Levels to Size Indicators

Use existing IRR size signals to determine guidance level:

| Ticket Size | Guidance Level | Architectural Context Required |
|-------------|----------------|-------------------------------|
| XS / S | Level 0 (Minimal) | Layer + module + pattern pointer |
| M | Level 1 (Standard) | Level 0 + example files + constraints |
| L | Level 2 (Comprehensive) | Level 1 + new components + dependency direction |
| XL or "high complexity" | Level 3 (Maximal) | Level 2 + human review checkpoints |

**Default:** Level 1 for all non-trivial work. Only escalate when complexity signals are clear.

#### Finding 3: Five New Kickback Triggers

Add to the existing Issue Review triggers in `architect.md`:

| Trigger | Level | When to Kick Back |
|---------|-------|-------------------|
| Missing architectural context | All | Implementation ticket without Architectural Context section |
| Missing layer/module | 0+ | No placement specified for where code goes |
| Missing pattern examples | 1+ | Multi-file feature without example file references |
| Missing component specification | 2+ | New ports/adapters created without interface definition |
| Missing dependency direction | 2+ | Cross-layer work without dependency arrows/diagram |

**Enforcement:** KICKBACK (not SUGGEST) when trigger conditions are met.

#### Finding 4: Ticket Template Section

Add to `github-issue-feature.md` after "Proposed approach":

```markdown
## Architectural Context

**Level:** [0/1/2/3] (determined by Architect during CCR)

### Placement
- **Layer:** [domain | application | infrastructure]
- **Module:** [path/to/module/]

### Patterns to Follow
| Pattern | Example File | Notes |
|---------|--------------|-------|
| [Pattern name] | [path/to/example.py] | [optional guidance] |

### Constraints
- Must NOT import from: [forbidden modules]
- New dependencies require: [adapter creation | human approval]
- If architectural placement unclear: **Ask before implementing**

<!-- For Level 2+ only: -->
### New Components (Level 2+)
- New port: [domain/ports/X.py]
- New adapter: [infrastructure/adapters/X.py]
- New service: [application/services/X.py]

### Dependency Direction (Level 2+)
```
Domain ← Application ← Infrastructure
        ↑               ↑
        └── Ports ──────┘ (Adapters implement ports)
```

<!-- For Level 3 only: -->
### Human Review Checkpoints (Level 3)
- [ ] Pre-implementation: Architect approves design sketch
- [ ] Mid-implementation: Review after core logic complete
- [ ] Post-implementation: Verify dependency rules followed
```

#### Finding 5: Quick-Check for Level 0

For trivial tickets (XS/S), allow abbreviated context:

```markdown
## Architectural Context

**Level:** 0

Layer: application | Module: services/user_service.py | Pattern: existing

Constraints: None beyond standard rules. If unclear, ask before implementing.
```

### Dissenting Views / Caveats

**Pattern reference freshness:** This enhancement verifies that pattern examples are referenced, but not that the referenced files are current or accurate. Stale references can mislead agents.

**Mitigation:** Developer role can flag stale pattern references during their review. Future enhancement: automated pattern reference validation.

**Layer name flexibility:** Template assumes domain/application/infrastructure. For projects using different conventions, adapt layer names to match actual structure.

### Known Limitations

1. **No automated enforcement:** Checklist verification is manual (Architect review)
2. **Pattern freshness not verified:** Referenced example files may drift from stated patterns
3. **Hexagonal assumed:** Template optimized for ports-and-adapters; other architectures need adaptation
4. **Single-agent focus:** Multi-agent coordination requires additional patterns (see prior research)

## Reusable Artifacts

### Enhanced Architect Checklist (for architect.md)

```markdown
### Review Checklist

1. [ ] **Architectural fit** — change aligns with existing system structure
2. [ ] **Boundaries** — affected components/interfaces are identified
3. [ ] **NFRs** — performance, scalability, reliability requirements stated
4. [ ] **Dependencies** — external systems, libraries, services identified
5. [ ] **Impact analysis** — downstream effects on other components noted
6. [ ] **ADR needed** — significant decisions flagged for documentation
7. [ ] **Migration path** — breaking changes have upgrade strategy
8. [ ] **Technical debt** — new debt acknowledged or existing debt addressed
9. [ ] **Guidance level and architectural context**
   - Level: [0/1/2/3] (XS/S=0, M=1, L=2, XL=3)
   - [ ] Architectural Context section present
   - [ ] Content adequate for classified level
```

### Enhanced Kickback Triggers (for architect.md)

```markdown
### Kickback Triggers (Issue Review)

<!-- Existing triggers -->
- No consideration of existing architecture (greenfield assumptions)
- Boundary violations or unclear ownership
- Missing NFRs for user-facing features
- New dependency without justification
- Breaking change without migration path
- Over-engineering for the problem size
- Under-specification of integration points
- Technical debt created without acknowledgment

<!-- New agent-readiness triggers -->
- Missing Architectural Context section for implementation ticket
- Missing layer/module placement (Level 0+)
- Missing pattern examples for multi-file feature (Level 1+)
- Missing component specification for new ports/adapters (Level 2+)
- Missing dependency direction for cross-layer work (Level 2+)
```

### Level Selection Quick Reference

```markdown
| Size | Files | New Components | Layers | Level |
|------|-------|----------------|--------|-------|
| XS/S | 1-2 | 0 | 1 | 0 |
| M | 2-5 | 0-1 | 1-2 | 1 |
| L | 5+ | 2+ | 2-3 | 2 |
| XL | 10+ | Novel | All | 3 |

**Rule:** When in doubt, go one level higher.
**Default:** Level 1 for all non-trivial work.
```

### Before/After Examples

**Before (Inadequate):**
```markdown
## Proposed approach

Add a new endpoint for user preferences.
```

**After (Level 1 — Adequate):**
```markdown
## Architectural Context

**Level:** 1

### Placement
- **Layer:** application
- **Module:** application/services/

### Patterns to Follow
| Pattern | Example File | Notes |
|---------|--------------|-------|
| Service pattern | application/services/user_service.py | Follow validation approach |
| API endpoint | infrastructure/api/users.py | Follow response format |

### Constraints
- Must NOT import from infrastructure/ in service layer
- New validation rules go in domain/validators/
- If unclear, ask before implementing
```

## Sources

### Primary Research
1. [Architectural Direction for AI Agent Tickets](../patterns/agent-architectural-direction.md) — Praxis research-library

### Internal Sources
2. [Architect Role Definition](../../core/roles/definitions/architect.md) — Praxis core roles
3. [Issue Refinement Runbook](../../../extensions/praxis-workshop/runbooks/issue-refinement-runbook.md) — CCR process
4. [DORA Refinement and Peer Review Roles](dora-refinement-peer-review-roles.md) — DORA findings
5. [GitHub Issue Feature Template](../../../extensions/praxis-workshop/templates/github-issue-feature.md) — Current template

### Web Sources
6. [Emergent Code Review Patterns for AI-Generated Code](https://www.propelcode.ai/blog/emergent-code-review-patterns-ai-generated-code) — Propel
7. [My LLM Coding Workflow Going into 2026](https://medium.com/@addyosmani/my-llm-coding-workflow-going-into-2026-52fe1681325e) — Addy Osmani
8. [Coding Guidelines for Your AI Agents](https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/) — JetBrains
9. [2026 Demands Agentic Engineering](https://medium.com/generative-ai-revolution-ai-native-transformation/2025-overpromised-ai-agents-2026-demands-agentic-engineering-5fbf914a9106) — Yi Zhou
10. [Code Review Guidelines - Vibe Coding Framework](https://docs.vibe-coding-framework.com/best-practices/code-review-guidelines) — Vibe Framework

---

## Review Notes

### Specialist Review (2026-01-04)

**Process Engineer Verdict:** APPROVE with refinements
- Combined checklist items 9 and 10 into single item
- Mapped levels to existing size indicators
- Added quick-check shortcut for Level 0

**Software Architect Verdict:** APPROVE with refinements
- Default to Level 1 for non-trivial work
- Added "if unclear, ask" footer
- Noted pattern freshness limitation
- Added layer name flexibility note

### Synthesis Review (2026-01-04)

**Conflicts resolved:**
- Checklist structure: Combined into single item with sub-checks
- Level selection: Use size indicators + default to Level 1

---

_Generated by researcher_
_Reviewed by process-engineer, software-architect_
