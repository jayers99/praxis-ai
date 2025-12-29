---
name: "DevSecOps: Security & Trust posture"
about: "Add/clarify security, privacy enforcement, CI gates, release and supply-chain posture"
title: "Feature request: Add DevSecOps Security & Trust posture to docs + release process"
labels: ["documentation", "security", "enhancement"]
---

## Summary

Provide a clear DevSecOps/SRE-facing “Security & Trust” posture starting from the README so adopters can quickly understand what is guaranteed, what is not, and how to operate Praxis safely.

## Problem / Motivation

From the top-level README, it’s easy to understand the framework and CLI usage, but hard to assess:

- Security guarantees (and non-goals)
- Vulnerability reporting path
- Practical privacy enforcement vs conceptual intent
- Supported Python versions/platforms
- CI gates and release process
- Supply-chain posture (locking, provenance/SBOM/signing expectations)
- Secure contribution expectations
- CLA implications for external contributors

## Proposed changes (docs-first, minimal)

### 1) README: add “Security & Trust” section

Include (keep concise; avoid overstating):

- Supported versions/platforms
- High-level threat model boundaries
- Privacy enforcement reality (what CLI enforces today)
- Determinism boundaries (policy resolution vs agent behavior)
- Artifact trust: where official releases live and how to verify

### 2) Add SECURITY.md

Include:

- Supported versions policy
- Vulnerability reporting contact
- Disclosure expectations (what info to include)
- Whether advisories will be published

### 3) Document CI/CD + release posture

Document:

- Required checks before merge (tests, lint, types)
- How releases are built/published (even if manual)
- Dependency locking and update approach

### 4) Supply-chain basics (document current vs target)

Document:

- Poetry + lockfile expectations
- SBOM/provenance/signing: present today vs planned follow-ups
- Recommended CI usage (e.g., `praxis validate --strict`)

### 5) Contribution security expectations

Update contributing guidance to include:

- Local dev commands (`pytest`, `ruff`, `mypy`)
- PR gating expectations
- No-secrets guidance

### 6) CLA clarity (communication)

If the CLA is intentionally owner-favorable, make that explicit in a short, factual note (README “Contributing” section).

## Acceptance criteria

- README contains a concise “Security & Trust” section covering the items above.
- SECURITY.md exists and is linked from README.
- CI gates and release posture are documented.
- Contribution docs include local commands and secure SDLC expectations.
- No new product functionality is required to close this issue.

## Out of scope

- Implementing full artifact signing, SBOM generation, or provenance attestation (may be follow-up issues).
- Adding new CLI features unrelated to documenting posture.
- Rewriting framework docs; keep changes additive and minimal.

## Notes / Context

Link any related discussions or decisions here.
