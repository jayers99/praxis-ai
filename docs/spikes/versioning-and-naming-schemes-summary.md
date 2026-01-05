# Versioning and Naming Schemes Spike — Summary

**Date:** 2026-01-05  
**Status:** Completed  
**Related:** Issue #4 (template-python-cli), ADR-004

---

## Executive Summary

This spike explored versioning and naming conventions across the Praxis ecosystem. The research identified 7 distinct components requiring versioning strategies, analyzed similar template systems (Cookiecutter, Copier, Yeoman, Cargo Generate), and produced comprehensive recommendations.

**Key deliverables:**
1. ADR-004 — Comprehensive versioning and naming strategy
2. core/spec/VERSION.md — Praxis specification version tracking
3. docs/guides/versioning.md — User-facing quick reference

---

## Key Findings

### 1. Multiple Versioning Concerns

Praxis has 7 distinct components with different versioning needs:

| Component | Current State | Recommendation |
|-----------|---------------|----------------|
| Praxis Spec | v0.3 in SOD/lifecycle | SemVer in VERSION.md |
| praxis.yaml Schema | Implicit v1.0 | Optional `schema_version` field |
| Extension Manifests | v0.1 (ADR-003) | Continue existing approach |
| Stage Templates | No versioning | Tie to spec version |
| Project Templates | No formal versioning | SemVer via git tags |
| CLI Tool | v0.1.0 in pyproject.toml | Continue SemVer |
| User Projects | Domain-specific | User choice |

### 2. SemVer is Dominant

Research of similar systems (Cookiecutter, Copier, Yeoman, Cargo Generate) showed:
- SemVer is the de facto standard for templates and tools
- Git tags are dominant for template versioning
- Manifest files track metadata beyond just version
- Template vs project versioning are separate concerns

### 3. Naming Conventions Matter

Established clear naming patterns:
- **Templates:** `praxis-template-{domain}-{type}` (e.g., praxis-template-code-cli)
- **Extensions:** `praxis-extension-{name}` (e.g., praxis-extension-mobile-pack)
- **Stage files:** `{STAGE}.md` (no version suffix)

### 4. Backward Compatibility Strategy

- **Optional schema_version** in praxis.yaml (defaults to latest)
- **N and N-1 version support** for schemas and manifests
- **Migration tooling** via `praxis migrate` (future)
- **Deprecation warnings** before breaking changes

---

## Recommendations

### Immediate (Issue #4)

1. **Apply template naming** to template-python-cli design
2. **Document template versioning** in extension authoring guide
3. **Consider adding schema_version** to PraxisConfig (optional, not required)

### Short-term (Post-Issue #4)

1. **Create VERSION.md** ✅ DONE
2. **Update spec files** ✅ DONE
3. **Add schema_version field** to praxis.yaml schema (optional)
4. **Implement schema version warnings** in `praxis validate`
5. **Define .praxis-template.yaml schema** for template metadata

### Long-term (v1.0 Readiness)

1. **Implement `praxis migrate`** command for schema migrations
2. **Design template update mechanism** (Copier-like)
3. **Stabilize Praxis spec to v1.0** (after multiple real projects)
4. **Stabilize extension manifest to v1.0** (after 2 first-party packs)

---

## Success Criteria Met

✅ **Research similar systems** — Analyzed Cookiecutter, Copier, Yeoman, Cargo Generate  
✅ **Document recommendations** — Created ADR-004 with comprehensive strategy  
✅ **Define versioning scheme** — SemVer for all components, git tags for templates  
✅ **Define naming scheme** — Template and extension naming conventions established  
✅ **Address backward compatibility** — Optional schema_version with migration path  
✅ **Update relevant specs** — VERSION.md created, all spec files updated

---

## Next Steps

### For Issue #4 (template-python-cli)

1. Apply template naming: `praxis-template-code-cli`
2. Add git tag for initial version: v0.1.0 or v1.0.0
3. Consider adding `.praxis-template.yaml` metadata
4. Reference ADR-004 in template documentation

### For Praxis Core

1. Add `schema_version: str | None = None` to PraxisConfig model
2. Update validation service to warn on outdated schema
3. Document schema_version in user guide
4. Plan `praxis migrate` command for future milestone

---

## References

- **Primary:** [ADR-004: Versioning and Naming Schemes](../../adr/004-versioning-and-naming-schemes.md)
- **Spec Version:** [core/spec/VERSION.md](../../core/spec/VERSION.md)
- **User Guide:** [docs/guides/versioning.md](../../docs/guides/versioning.md)
- **Related ADRs:** ADR-001 (Policy Engine), ADR-002 (Validation Model), ADR-003 (Extension Manifest)
- **Related Issues:** #4 (template-python-cli)
