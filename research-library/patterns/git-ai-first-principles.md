# Git + AI Workflow: First Principles and Patterns

<!--
metadata:
  id: patterns-git-ai-first-principles-2026-01-01
  title: Git + AI Workflow First Principles and Patterns
  date: 2026-01-01
  status: validated
  topic: patterns
  keywords: [git, ai-assisted, workflow, gates, drift, human-oversight, review-bandwidth]
  consensus: medium
  depth: comprehensive
  sources_count: 21
  ccr_status: mitigations-applied
-->

## Executive Summary

- Git remains the single source of truth; all AI-generated code must flow through version control for review, testing, and rollback
- Explicit stop points (gates) reduce AI drift, though the optimal frequency is a practitioner heuristic, not empirically validated
- Structured context artifacts (CLAUDE.md, copilot-instructions.md) improve consistency, but carry security risks if sourced from untrusted repos
- **Counter-evidence:** A rigorous RCT found AI tools made experienced developers 19% slower on average, despite perceiving themselves faster
- The emerging pattern: **"Write-with-AI, review-with-AI, approve-with-human"**
- Review bandwidth—not code generation—is the new bottleneck

## Consensus Rating

**Medium**: Core patterns validated across 8+ sources, but key productivity claims contradicted by rigorous research. Vendor-sponsored studies should be weighted accordingly.

## Key Caveats (CCR-Verified)

### Counter-Evidence: METR RCT (July 2025)

A randomized controlled trial with 16 experienced open-source developers across 246 tasks found:

> **AI tools made developers 19% SLOWER on average**
> Developers predicted 24% speedup, perceived 20% speedup after.

The "perception gap" is real: developers believe AI helps even when objective measures show otherwise.

**Source:** [METR Study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)

### Security Warning: Context File Attacks

"Rules File Backdoor" attacks via CLAUDE.md/AGENTS.md files are documented:
- Malicious hidden instructions via Unicode characters
- Content injected directly into system prompts
- Risk when cloning repos you don't control

**Mitigation:** Review context files from untrusted sources before allowing AI to read them.

## First Principles

### The Bottleneck Inversion

The fundamental tension in AI-assisted development is between speed and oversight:

- **Old constraint:** "How fast can we write code?"
- **New constraint:** "How fast can we verify code?"

This explains why the most successful patterns focus on **review bandwidth preservation**, not generation acceleration.

### Git as Safety Net

Git's role transforms from collaboration tool to architectural necessity:

> "In an AI-assisted workflow, Git is not optional—it's the safety net that lets you experiment with AI contributions while preserving history and accountability."

Every AI-generated change must be:
- Committable
- Reviewable
- Testable
- Reversible

### Human as Navigator

The traditional pair programming model (driver-navigator) adapts to human-AI collaboration:
- AI can type faster
- Human provides intent, constraints, quality judgment
- Explicit handoff points (gates) where human reasserts control

## Key Findings

### Finding 1: Structured Context Artifacts Improve Consistency

**Consensus: Strong (5 sources)**

AI coding assistants perform better with structured context documents:
1. **Repository-wide**: `.github/copilot-instructions.md`
2. **Path-specific**: `.github/instructions/*.instructions.md`
3. **Claude-specific**: `CLAUDE.md`

**Evidence:** Teams using structured instructions report fewer style mismatches (44% of quality complaints cite context issues).

### Finding 2: Explicit Gates Reduce Drift

**Consensus: Strong on concept, weak on specifics**

Context drift in extended AI sessions is documented:

> "The model does still see earlier turns, but attention favors recent tokens. Constraints you asserted an hour ago get quietly deprioritized."

Effective gate patterns:
- **Forced resets:** Split large tasks into multiple sessions
- **Checkpoint rollbacks:** Claude Code saves state before changes
- **Human-in-the-loop:** Mandatory review for security/financial changes

**Practitioner heuristic:** "If the session goes beyond 5 turns or touches multiple subsystems, stop and validate."

### Finding 3: AI Review Requires Human Supplement

**Consensus: Strong (4 sources)**

GitHub's architectural decision: Copilot can only leave "Comment" reviews, never "Approve" or "Request changes."

**The pattern:** Write-with-AI, review-with-AI, approve-with-human.

## Reusable Artifacts

### Session Gate Checklist

| Gate | Trigger | Action |
|------|---------|--------|
| Context reset | >5 turns OR multiple subsystems | Start new session, restate constraints |
| Test validation | Any code generation | Run unit tests before proceeding |
| Security review | Auth, secrets, permissions code | Mandatory human review |
| Architecture decision | New patterns or dependencies | Exit AI session, document decision |
| Pre-merge | PR ready | Human approval required |

### Context File Template

```markdown
# CLAUDE.md

## Project Overview
[One sentence describing this codebase]

## Code Style
- [Naming conventions]
- [Error handling patterns]
- [Import organization]

## Testing Requirements
- [Coverage expectations]
- [Test file locations]

## Security Rules
- [Secrets handling]
- [Input validation]

## Examples
[Code blocks showing preferred patterns]
```

## Sources

1. Simon Willison: Using LLMs for Code (2025) — primary
2. Simon Willison: Parallel Coding Agents (2025) — primary
3. GitHub Blog: Copilot Code Review Instructions (2025) — primary
4. GitHub Docs: Copilot Code Review Architecture — primary
5. METR: AI Productivity RCT (July 2025) — counter-evidence
6. Nicole Forsgren/InfoQ: DORA Metrics for AI Workflows (2025) — primary

---
_PKDP Status: CCR mitigations applied, HVA validated_
_Ingested: 2026-01-01_
