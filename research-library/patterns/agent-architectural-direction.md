# Architectural Direction for AI Agent Tickets: A Practitioner's Framework

<!--
metadata:
  id: patterns-agent-architectural-direction-2026-01-04
  title: Architectural Direction for AI Agent Tickets
  date: 2026-01-04
  author: researcher
  status: approved
  topic: patterns
  also_relevant: [ai-guards, roles]
  keywords: [ai-agents, architectural-guidance, ddd, hexagonal, tickets, claude-code, instruction-engineering]
  consensus: medium
  epistemic_standard: standard
  sources_count: 17
  timebox: 120 minutes
  supersedes: null
  related: [patterns-ai-code-verification-workflow-2026-01-01, roles-multi-agent-role-specialization-2026-01-02]
  reviewed_by: [software-architect, ai-ml-practitioner, process-engineer]
  review_date: 2026-01-04
  approved_by: human
  approved_date: 2026-01-04
-->

## Executive Summary

- **Explicit architectural guidance is required** — agents generate "architecture by default" that works initially but lacks maintainability; LLMs achieve only ~38.81% accuracy on pattern detection without guidance
- **All codebases need pattern pointers** — even established codebases require explicit references to example files; agents don't automatically discover patterns
- **Code examples outperform prose** — concrete samples are "the most effective strategy" for communicating architectural patterns; include file paths, not just principles
- **Ticket is primary delivery mechanism** — CLAUDE.md supplements tickets but tickets must contain architectural context; agents receive tickets, not configuration files
- **Use a 4-level guidance framework** — match guidance intensity to task complexity and codebase maturity; always include architectural invariants

## Consensus Rating

**Medium**: Core findings (explicit guidance needed, code examples work, codebase maturity matters) are well-supported across 17 sources. Specific thresholds and framework effectiveness lack controlled experiments. Most evidence is practitioner reports rather than rigorous academic studies.

## Body

### First Principles

#### The Implicit Architecture Problem

AI agents don't just generate code — they generate **architectural decisions implicitly**. Without explicit guidance, agents:

- Collapse functionality into route handlers rather than creating layered architectures
- Skip abstraction layers (services, repositories, data transfer objects)
- Follow patterns from training data that may be outdated or suboptimal
- Make local optimizations that break global system behavior

The question isn't whether to provide architectural guidance, but **how much** and **in what form**.

#### The Instruction Budget Constraint

From prior research on AI context windows:

| Constraint | Value | Implication |
|------------|-------|-------------|
| Total instruction capacity | ~150-200 | Can't inline full architecture docs |
| System prompt usage | ~50 | User budget: ~100-150 |
| Architecture allocation | 40-60 | Selective, not comprehensive |
| Order effects | Earlier > Later | Put architectural invariants first |

**Implication:** Use the "pointer pattern" — reference example files rather than inlining documentation.

#### Detection vs. Following

Critical distinction:

- **Detection** (LLMs recognizing patterns): ~38.81% accuracy — unreliable
- **Following** (LLMs replicating explicit instructions): Significantly higher — reliable with good examples

Don't rely on agents to detect architecture from code. Provide explicit guidance.

### Findings

#### Finding 1: Codebase Maturity Changes Requirements (But Never to Zero)

| Maturity | Agent Behavior | Minimum Guidance |
|----------|----------------|------------------|
| **Greenfield** | No patterns to infer; generates from training data | Comprehensive architectural blueprint |
| **Early development** | Some patterns emerging; inconsistent | Explicit rules + example files |
| **Established** | Strong patterns exist | Pattern pointers + invariants |
| **Legacy** | Complex, inconsistent patterns | Heavy guidance + boundary definitions |

**Key revision from CCR:** Even established codebases need explicit pattern pointers. "Follow existing patterns" is insufficient — agents don't automatically read all files.

#### Finding 2: Code Examples Beat Prose

From Martin Fowler's empirical study:

> "Code samples proved more effective than natural language descriptions alone... Agents reliably replicated demonstrated patterns when given concrete examples."

**Pattern Template Format (Recommended):**

```markdown
## Pattern: Service Layer
Location: application/services/
Example: application/services/user_service.py

Services:
- Accept domain entities as input, return domain entities
- Call infrastructure through ports (never directly)
- Contain business logic orchestration, not domain logic
- Raise domain exceptions, not infrastructure exceptions
```

#### Finding 3: Layered Guidance Structure

**Anthropic's "right altitude" principle:**

| Level | Problem | Effect |
|-------|---------|--------|
| Too prescriptive | Hardcoded brittle logic | Fragile, breaks on edge cases |
| Too vague | No concrete signals | Agent guesses, often wrong |
| **Optimal** | Specific heuristics + flexibility | Guides without over-constraining |

**Effective layering:**

1. **Global (CLAUDE.md):** Architectural invariants, layer boundaries, dependency rules
2. **Task-specific (ticket body):** Relevant patterns, example references, constraints
3. **On-demand (doc pointers):** Full architecture docs when agent needs deep context

### The Guidance Framework

#### Architectural Invariants (Always Include)

Regardless of guidance level, always include these in CLAUDE.md:

```markdown
## Architectural Invariants

### Layer Structure
src/
├── domain/         # Pure business logic, no external deps
├── application/    # Use cases, orchestrates domain + ports
└── infrastructure/ # External concerns (DB, HTTP, files)

### Dependency Rules (Hexagonal)
- domain/ imports NOTHING from application/ or infrastructure/
- application/ imports from domain/ (entities, ports)
- application/ defines ports; infrastructure/ implements adapters
- infrastructure/ imports from application/ (to implement ports)

### Change Protocol
- New external dependency → Create adapter in infrastructure/
- New business rule → Domain entity or service
- New use case → Application service
```

#### Level 0: Minimal (Established + Simple Bug Fix)

**When to use:**
- Mature codebase with consistent patterns
- Single-file bug fix or minor enhancement
- No new dependencies or architectural decisions

**Ticket guidance:**
```markdown
## Architectural Context
Layer: application
Module: application/services/user_service.py
Pattern: Follow existing error handling in this file
Constraints: No new infrastructure imports
```

**CLAUDE.md:** Architectural invariants only

#### Level 1: Standard (Established + Moderate Feature)

**When to use:**
- Mature codebase with consistent patterns
- New feature that fits existing patterns
- May touch multiple files in same layer

**Ticket guidance:**
```markdown
## Architectural Context
Layer: application
Module: application/services/

### Patterns to Follow
- Service pattern: See application/services/user_service.py
- Repository port: See domain/ports/user_repository.py

### Constraints
- Must NOT import from infrastructure/
- New repository methods → add to existing port interface
- Raise domain exceptions (domain/exceptions.py)
```

**CLAUDE.md:** Invariants + layer descriptions

#### Level 2: Comprehensive (Greenfield or Complex Feature)

**When to use:**
- New project with no established patterns
- Feature requiring new architectural components
- Cross-cutting concerns (new adapter, new aggregate)

**Ticket guidance:**
```markdown
## Architectural Context
Layer: [Primary layer] + [Secondary layers affected]

### New Components Required
- New port: domain/ports/payment_gateway.py
- New adapter: infrastructure/adapters/stripe_adapter.py
- New service: application/services/payment_service.py

### Patterns to Follow
- Port interface: See domain/ports/user_repository.py (lines 1-25)
- Adapter implementation: See infrastructure/adapters/postgres_user_repository.py
- Service orchestration: See application/services/user_service.py

### Dependency Direction
Domain ← Application ← Infrastructure
        ↑               ↑
        └── Ports ──────┘ (Adapters implement ports)

### Constraints
- Payment gateway port: domain/ports/payment_gateway.py
- Stripe adapter: infrastructure/adapters/stripe_adapter.py
- PaymentService calls port, never adapter directly
```

**CLAUDE.md:** Full layer structure + patterns + examples

#### Level 3: Maximal (Critical or Novel Architecture)

**When to use:**
- Foundational architectural decisions
- Novel patterns not yet established in codebase
- High-risk changes to core domain

**Ticket guidance:**
- All of Level 2, plus:
- Pre-implementation architectural review checkpoint
- Human-in-the-loop for each new component
- Post-implementation architectural verification

**Process:**
1. Agent proposes architecture → Human reviews
2. Agent implements incrementally with checkpoints
3. Human verifies each layer before proceeding
4. Post-implementation dependency verification

### Ticket Template

For Level 1+ tickets, include this section:

```markdown
## Architectural Context

### Placement
- Primary Layer: [domain | application | infrastructure]
- Module Path: [path/to/module/]

### Patterns to Follow
| Pattern | Example File | Key Lines |
|---------|--------------|-----------|
| [Pattern name] | [path/to/example.py] | [optional line numbers] |

### Constraints
- Must NOT import from: [forbidden modules]
- New dependencies require: [adapter creation | human approval | etc.]
- If architectural placement unclear: Ask before implementing

### Verification (Post-Implementation)
- [ ] No new imports in domain/ from infrastructure/
- [ ] New ports in domain/ports/, adapters in infrastructure/adapters/
- [ ] Services call ports, not adapters directly
```

### Task Complexity Criteria

Use these criteria to select guidance level:

| Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|-----------|---------|---------|---------|---------|
| Files touched | 1 | 2-5 | 5+ | 10+ or core |
| New components | 0 | 0-1 | 2+ | Novel pattern |
| Layers crossed | 1 | 1-2 | 2-3 | All |
| External deps | 0 | 0 | 1+ | New integration |
| Risk if wrong | Low | Medium | High | Critical |

**Rule:** When in doubt, go one level higher.

### Dissenting Views / Caveats

**Implicit learning claims:** Some sources suggest agents can learn from existing code style. Evidence shows this is unreliable (~38.81% pattern accuracy). Treat implicit learning as supplementary, never primary.

**Instruction budget varies:** The ~150 instruction limit is approximate and model-dependent. Opus may handle more; Haiku may need fewer, more explicit instructions.

**Tool-specific behavior:** This framework assumes Claude Code. Other tools (Copilot, Cursor) may have different context handling. Core principles should transfer, but specifics may vary.

### Known Limitations

1. **No controlled experiments:** Framework based on practitioner reports and case studies, not A/B testing of guidance levels
2. **DDD/hexagonal assumed:** Framework optimizes for these patterns; other architectures may need different invariants
3. **Single-agent focus:** Multi-agent systems have additional coordination requirements (see prior research)
4. **Model capability variance:** Opus/Sonnet/Haiku have different reasoning capabilities; guidance needs may vary

## Reusable Artifacts

### Architectural Invariants Template (CLAUDE.md)

```markdown
## Architecture: Hexagonal / Ports-and-Adapters

### Directory Structure
src/
├── domain/         # Entities, value objects, domain services
│   ├── entities/
│   ├── value_objects/
│   ├── services/
│   └── ports/      # Interfaces for external dependencies
├── application/    # Use cases, application services
│   └── services/
└── infrastructure/ # Adapters implementing ports
    └── adapters/

### Dependency Rules (ENFORCED)
- domain/ imports from: standard library only
- application/ imports from: domain/
- infrastructure/ imports from: domain/, application/

### Pattern Examples
- Entity: domain/entities/user.py
- Port: domain/ports/user_repository.py
- Adapter: infrastructure/adapters/postgres_user_repository.py
- Service: application/services/user_service.py
```

### Ticket Architectural Context Section

```markdown
## Architectural Context

**Layer:** [domain | application | infrastructure]
**Module:** [path/to/module/]
**Pattern:** See [path/to/example.py]

**Constraints:**
- [ ] No imports from infrastructure/ in domain/
- [ ] New external dependency → create adapter
- [ ] If unclear → ask before implementing
```

### Level Selection Checklist

```markdown
## Guidance Level Selection

### Task Assessment
- [ ] Files to modify: ___
- [ ] New components needed: ___
- [ ] Layers affected: ___
- [ ] External dependencies: ___
- [ ] Risk level: ___

### Selected Level
- [ ] Level 0: Minimal (established + simple)
- [ ] Level 1: Standard (established + moderate)
- [ ] Level 2: Comprehensive (greenfield/complex)
- [ ] Level 3: Maximal (critical/novel)

Rule: When in doubt, go one level higher.
```

## Sources

### Primary Research
1. [How far can we push AI autonomy in code generation?](https://martinfowler.com/articles/pushing-ai-autonomy.html) — Martin Fowler
2. [CLAUDE.md Best Practices: Prompt Learning](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/) — Arize
3. [Why architecture still matters in the age of AI agents](https://vfunction.com/blog/vibe-coding-architecture-ai-agents/) — vFunction
4. [Coding Guidelines for Your AI Agents](https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/) — JetBrains
5. [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic
6. [Do Code LLMs Understand Design Patterns?](https://arxiv.org/html/2501.04835v1) — arXiv

### Internal Prior Art
7. [Multi-Agent Role Specialization](../roles/multi-agent-role-specialization-context-mitigation.md) — "Well-shaped ticket" criteria
8. [AI Code Verification Workflow](../patterns/ai-code-verification-workflow.md) — Verification bottleneck
9. [AI Memory: First Principles](../ai-guards/first-principles.md) — Instruction limits

### Additional Sources
10. [Best Practices for Context Management](https://docs.digitalocean.com/products/gradient-ai-platform/concepts/context-management/) — DigitalOcean
11. [From Vibe Coding to Spec-Driven Development](https://medium.com/@alonfliess/from-vibe-coding-to-spec-driven-development-bridging-ai-creativity-and-software-discipline-fe17f82cc77c) — Medium
12. [AI Engineering Trends in 2025](https://thenewstack.io/ai-engineering-trends-in-2025-agents-mcp-and-vibe-coding/) — The New Stack

---

## Review Notes

### CCR Review (2026-01-04)

**Verdict**: PASS with revisions

**Issues identified and addressed:**

| Issue | Severity | Resolution |
|-------|----------|------------|
| "Established codebases need less guidance" too optimistic | High | Revised: All levels need explicit pattern pointers |
| Missing hexagonal-specific port/adapter guidance | High | Added architectural invariants section |
| No verification step | Medium | Added post-implementation verification checklist |
| Framework lacks granularity | High | Added task complexity criteria table |
| "Code examples beat prose" but no format | Medium | Added pattern template format |
| Ticket template missing | Medium | Added complete ticket template |

### Synthesis Review (2026-01-04)

**Verdict**: Ready for HVA

**Conflicts resolved:**
- Explicit vs. implicit learning: Explicit primary, implicit supplementary only
- Comprehensive vs. minimal guidance: Match to task complexity via levels
- Static vs. dynamic context: Layer both (CLAUDE.md + ticket)

---

_Generated by researcher_
_Reviewed by software-architect, ai-ml-practitioner, process-engineer_
_Approved: 2026-01-04_
