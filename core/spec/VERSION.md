# Praxis Specification Version

**Current Version:** v0.3  
**Status:** Under Validation  
**Last Updated:** 2025-12-21

---

## Version History

### v0.3 (2025-12-21)

**Status:** Current — Under validation through worked projects

**Changes:**
- Formalized lifecycle model with 9 canonical stages
- Defined domain-specific formalize artifacts (SOD, briefs, plans)
- Established privacy levels and reclassification rules
- Introduced environment overlay (Home/Work)
- Created deterministic resolution model (Domain + Stage + Privacy + Environment)

**Validation status:**
- Worked examples: uat-praxis-code, examples/learn/python-testing
- ADRs: 001 (Policy Engine), 002 (Validation Model), 003 (Extension Manifest)
- Active issues: #4 (template-python-cli)

**Known gaps:**
- Multi-domain projects not yet addressed
- Template update mechanism not designed
- Collaboration model deferred to post-v1.0

---

### v0.2 (Earlier — Not documented)

**Status:** Superseded

**Changes:** (Historical record incomplete)

---

### v0.1 (Earlier — Not documented)

**Status:** Superseded

**Changes:** (Historical record incomplete)

---

## Version Scheme

Praxis uses **Semantic Versioning (SemVer)** for the specification:

- **MAJOR** (v1.0, v2.0): Breaking changes to lifecycle, domains, or privacy model
- **MINOR** (v0.3, v0.4): Refinements, clarifications, new features (non-breaking)
- **PATCH**: Not used at spec level (reserved for tooling/CLI)

**v0.x status:** Under validation, subject to change based on real-world usage.

**v1.0 criteria:** Spec validated through multiple real projects across domains, no major gaps identified, community feedback incorporated.

---

## Relationship to Other Versions

| Component | Current Version | Relationship to Spec |
|-----------|-----------------|----------------------|
| Praxis Specification | v0.3 | This document |
| CLI Tool (praxis) | v0.1.0 | Implementation of spec; can diverge |
| praxis.yaml schema | (implicit 1.0) | Tied to spec; may version separately in future |
| Extension manifest | v0.1 | Independent API contract (see ADR-003) |
| Stage templates | (tied to spec) | Generated from spec; no separate versioning |

See [ADR-004: Versioning and Naming Schemes](../../adr/004-versioning-and-naming-schemes.md) for full versioning strategy.

---

## Component Spec Versions

Individual specification documents may note their alignment with this version:

- `sod.md` — v0.3 (aligned)
- `lifecycle.md` — v0.3 (aligned)
- `domains.md` — v0.3 (aligned)
- `privacy.md` — v0.3 (aligned)

If a component spec shows a different version, it indicates local updates pending incorporation into the next spec release.

---

## Future Roadmap

### v0.4 (Estimated: TBD)

**Potential changes:**
- Template update mechanism design
- Multi-domain project support (if validated need emerges)
- Refinements from template-python-cli learnings

### v1.0 (Estimated: TBD)

**Criteria for release:**
- Validated through 5+ real projects across 3+ domains
- No major lifecycle or domain gaps identified
- Backward compatibility strategy proven
- Extension API stable (manifest v1.0)
- Community feedback incorporated

**Stability commitment:**
- v1.0 signals conceptual stability
- Breaking changes only in major versions (v2.0+)
- Deprecation warnings before removal

---

## Abandonment Criteria

From [SOD Section 9](sod.md#9-abandonment-criteria), Praxis should be rethought if:

1. **Overhead exceeds value** — Governance slows work without benefit (3+ projects)
2. **Privacy model fails** — Sensitive material exposed due to model gaps
3. **Lifecycle doesn't fit** — >50% of work requires constant regression/stage-skipping
4. **Domain model is wrong** — Significant work falls outside defined domains
5. **Policy enforcement is untenable** — No suitable policy engine can be integrated

If 2+ criteria are met, consider major version bump (v2.0) or project sunset.

---

## References

- [Solution Overview Document (SOD)](sod.md)
- [Lifecycle Specification](lifecycle.md)
- [Domain Definitions](domains.md)
- [Privacy Model](privacy.md)
- [ADR-004: Versioning and Naming Schemes](../../adr/004-versioning-and-naming-schemes.md)
- [Contributing Guide](../../CONTRIBUTING.md)
