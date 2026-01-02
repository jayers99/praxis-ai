# Patterns Research Index

_Artifacts: 5_
_Last updated: 2026-01-01_

## Purpose

Reusable patterns and practices. Implementation approaches, best practices, and proven solutions applicable across Praxis.

## Contents

| Title | Consensus | Keywords | Summary |
|-------|-----------|----------|---------|
| [Git + AI First Principles](git-ai-first-principles.md) | Medium | git, ai-assisted, gates, drift, human-oversight | Session gates, review bottleneck inversion, METR counter-evidence |
| [Git + AI Tool Ecosystem](git-ai-tool-ecosystem.md) | Medium | git, mcp, claude-code, heredoc, security | MCP setup, heredoc workarounds, worktrees, security warnings |
| [AI Code Review Optimization](git-ai-review-optimization.md) | Medium | code-review, copilot, severity, uat | Copilot detection, severity classification, UAT gates |
| [AI Code Verification Workflow](ai-code-verification-workflow.md) | Medium | verification, trust-calibration, solo-developer | Three-layer verification model, trust calibration, review bandwidth |
| [TDD and BDD for AI Verification](tdd-bdd-ai-verification.md) | Medium | TDD, BDD, mutation-testing, test-quality | Tests-first for AI, prompting strategies, mutation testing gold standard |

## Git + AI Workflow Series

These three artifacts form a comprehensive guide to Git + AI interactions, produced via full PKDP (Tier 3) with CCR counter-evidence review:

1. **First Principles** — Foundational patterns: gates, drift prevention, human oversight. Includes METR RCT counter-evidence (AI made developers 19% slower).

2. **Tool Ecosystem** — Practical tooling: MCP server setup, heredoc escaping, git worktrees. Includes critical security warnings about MCP prompt injection.

3. **Review Optimization** — Code review patterns: Copilot detection, severity classification, UAT templates. Includes December 2025 "IDEsaster" security disclosure.

### Cross-Cutting Themes

- **Review bandwidth is the new bottleneck** — not code generation
- **Security is primary constraint** — MCP prompt injection, context file attacks, auto-approve CVEs
- **Human approval cannot be bypassed** — GitHub's architectural decision codifies this

### Key Recommendation

**"Write-with-AI, review-with-AI, approve-with-human"**

## AI Code Verification Series

These two artifacts focus on verification strategies for AI-assisted development:

1. **AI Code Verification Workflow** — Three-layer verification model (generation-time, inline, post-hoc). Addresses the human review bottleneck with trust calibration and graduated autonomy.

2. **TDD and BDD for AI Verification** — Extends verification workflow with test-first methodology. Evaluates whether TDD/BDD can strengthen inline verification to reduce review burden.

### Cross-Cutting Themes

- **Tests as guard rails** — TDD provides "user-defined, context-specific guard rails" for AI
- **Context isolation is critical** — Multi-agent architectures achieve 84% TDD compliance vs 20% single-context
- **Mutation testing is the gold standard** — Coverage alone insufficient; mutation score reveals true test effectiveness
- **Human review remains non-negotiable** — Tests improve AI output but don't eliminate oversight

### Key Finding

**AI-generated tests achieve ~79% of human test effectiveness** (0.546 vs 0.690 mutation score). Prompting strategies (role prompting, Explain-Plan-Execute, constraints) significantly improve quality.

## Related Topics

- [Foundations](../foundations/_index.md) — theoretical grounding for patterns
- [Spec](../spec/_index.md) — specifications that use these patterns
- [Knowledge Distillation Pipeline](../foundations/knowledge-distillation-pipeline.md) — PKDP methodology used for this research

---

_Maintained by: cataloger agent_
