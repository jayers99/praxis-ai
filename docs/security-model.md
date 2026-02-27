# Security Model

This document describes Praxis's security posture, threat model, privacy enforcement reality, and determinism guarantees. For vulnerability reporting, see [SECURITY.md](../SECURITY.md).

## Supported Versions and Platforms

| Component | Support Status |
|-----------|----------------|
| **Python** | >=3.10 (per `pyproject.toml`) |
| **OS** | Linux, macOS (primary), Windows (community-supported) |
| **Supported Release** | Latest commit on `main` branch |
| **Release Cadence** | Early-stage: irregular releases as features stabilize |

**Installation verification:**
```bash
# Verify Python version
python --version  # Should be 3.10 or higher

# Verify installation integrity
poetry install
poetry run praxis --version
poetry run praxis validate --strict  # Validate CLI integrity
```

## Threat Model and Boundaries

**What Praxis protects:**
- **Governance correctness:** Ensures lifecycle stage transitions follow allowed patterns
- **Artifact requirements:** Validates required formalization documents exist before execution
- **Privacy level integrity:** Warns on privacy downgrades and tracks privacy declarations
- **Deterministic policy resolution:** Guarantees consistent behavior from Domain + Stage + Privacy + Environment

**What Praxis does NOT protect against:**
- **Data exfiltration:** Privacy levels are intent declarations, not runtime enforcement barriers
- **Malicious AI behavior:** Praxis does not sandbox or constrain AI tool execution
- **Supply chain attacks:** No artifact signing or provenance attestation (yet—see SECURITY.md roadmap)
- **Secrets in artifacts:** Users are responsible for not committing secrets to project files

**Critical clarification:** Praxis is a **governance framework**, not a security sandbox. It validates structural correctness and provides guidance, but does not prevent all security risks.

## Privacy Enforcement Reality

Privacy levels in Praxis define **intent and constraints**, not runtime enforcement:

| Privacy Level | What IS Enforced | What is NOT Enforced |
|---------------|------------------|----------------------|
| **Public** | Downgrade warnings | AI tool selection |
| **Public–Trusted** | Downgrade warnings | Collaborator verification |
| **Personal** | Downgrade warnings | Local-only AI enforcement |
| **Confidential** | Downgrade warnings | Air-gapped environment enforcement |
| **Restricted** | Downgrade warnings | AI processing prevention |

**Current enforcement:** Privacy levels are validated in `praxis.yaml` and downgrade warnings are displayed during `praxis validate`. Future work may add tool restrictions per privacy level.

**User responsibility:** Choose appropriate privacy levels for your work and select AI tools accordingly. Praxis tracks intent; you enforce boundaries.

## Determinism Claims

**What is deterministic:**
- Policy validation rules (schema validation, artifact checks, regression detection)
- Opinions resolution hierarchy (_shared → domain → stage → subtype)
- Stage transition rules (allowed/disallowed regressions)
- Required artifact mappings (Domain → Formalize stage artifact)

**What is NOT deterministic:**
- AI assistant behavior (opinions are advisory, not enforced)
- Human decision-making during lifecycle progression
- External tool behavior (tests, linters, type checkers)
- Timing of stage transitions (user-driven, not automated)

**Guarantee:** Given the same `praxis.yaml` configuration, `praxis validate` will produce the same validation result. AI-generated content is NOT deterministic.

## Artifact Trust and Verification

**Official releases:**
- **Source of truth:** GitHub repository at https://github.com/jayers99/praxis-ai
- **Future PyPI:** Planned for stable releases (not yet published)
- **Current installation:** Clone repo + `poetry install` (development mode)

**Verifying your installation:**
```bash
# Check git remote points to official repo
cd /path/to/praxis-ai
git remote -v
# Should show: origin  https://github.com/jayers99/praxis-ai.git

# Verify commit integrity (if using a specific commit)
git log --oneline -1
git verify-commit HEAD  # Requires GPG-signed commits (not yet enforced)

# Run integrity checks
poetry run pytest          # All tests should pass
poetry run ruff check .    # Linting should pass
poetry run mypy .          # Type checking should pass
```

**Supply chain hygiene:**
- Dependencies locked in `poetry.lock` (committed to repo)
- Dependency updates follow semver ranges in `pyproject.toml`
- No auto-updates without review

**Future roadmap:**
- [ ] Publish to PyPI with version tags
- [ ] Add SBOM generation (Software Bill of Materials)
- [ ] Implement provenance attestation
- [ ] Sign releases with GPG/Sigstore
