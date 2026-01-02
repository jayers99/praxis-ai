# Patterns Research Index

_Artifacts: 3_
_Last updated: 2026-01-01_

## Purpose

Reusable patterns and practices. Implementation approaches, best practices, and proven solutions applicable across Praxis.

## Contents

| Title | Consensus | Keywords | Summary |
|-------|-----------|----------|---------|
| [Git + AI First Principles](git-ai-first-principles.md) | Medium | git, ai-assisted, gates, drift, human-oversight | Session gates, review bottleneck inversion, METR counter-evidence |
| [Git + AI Tool Ecosystem](git-ai-tool-ecosystem.md) | Medium | git, mcp, claude-code, heredoc, security | MCP setup, heredoc workarounds, worktrees, security warnings |
| [AI Code Review Optimization](git-ai-review-optimization.md) | Medium | code-review, copilot, severity, uat | Copilot detection, severity classification, UAT gates |

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

## Related Topics

- [Foundations](../foundations/_index.md) — theoretical grounding for patterns
- [Spec](../spec/_index.md) — specifications that use these patterns
- [Knowledge Distillation Pipeline](../foundations/knowledge-distillation-pipeline.md) — PKDP methodology used for this research

---

_Maintained by: cataloger agent_
