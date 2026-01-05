# Praxis Versioning Quick Reference

> **Full details:** See [ADR-004: Versioning and Naming Schemes](../../adr/004-versioning-and-naming-schemes.md)

This guide provides a quick reference for understanding Praxis versioning across different components.

---

## What Gets Versioned?

| Component | Current Version | Scheme | Location |
|-----------|-----------------|--------|----------|
| **Praxis Specification** | v0.3 | SemVer | [core/spec/VERSION.md](../../core/spec/VERSION.md) |
| **CLI Tool** | v0.1.0 | SemVer | `pyproject.toml` |
| **praxis.yaml Schema** | (implicit 1.0) | SemVer MAJOR.MINOR | Future: `schema_version` field |
| **Extension Manifests** | v0.1 | SemVer MAJOR.MINOR | `manifest_version` in extension |
| **Project Templates** | varies | SemVer | Git tags + template metadata |
| **Stage Templates** | tied to spec | (none) | Evolves with spec version |
| **Your Projects** | your choice | domain-specific | pyproject.toml, package.json, etc. |

---

## Checking Versions

### Praxis Specification Version
```bash
cat core/spec/VERSION.md
```
Current: **v0.3** (under validation, subject to change)

### CLI Tool Version
```bash
praxis --version
```
Current: **v0.1.0** (implementation maturity)

### Your Project Schema Version
```yaml
# praxis.yaml (future, currently optional)
schema_version: "1.0"
domain: code
stage: execute
# ...
```

---

## Version Independence

Different components can have different versions:

- **Spec v0.3, CLI v0.1.0** — Normal! Spec = conceptual model, CLI = implementation
- **Template v1.2.0, Praxis v0.3** — Normal! Templates evolve independently
- **Extension v0.2, Praxis v0.3** — Normal! Extensions have their own lifecycle

**Why?** Each component evolves at its own pace. The spec stabilizes slowly (conceptual validation), while CLI and templates iterate quickly.

---

## Naming Conventions

### Templates

**Pattern:** `praxis-template-{domain}-{type}`

**Examples:**
```
praxis-template-code-cli        # Python CLI project
praxis-template-code-api        # REST API service
praxis-template-write-article   # Technical article
praxis-template-learn-course    # Learning curriculum
```

### Extensions

**Pattern:** `praxis-extension-{name}`

**Examples:**
```
praxis-extension-mobile-pack
praxis-extension-devops-opinions
```

### Stage Files

**Pattern:** `{STAGE}.md` (no version suffix)

**Examples:**
```
CAPTURE.md
FORMALIZE.md
EXECUTE.md
```

**Why no version?** Stage files are living documents. Git history provides versioning.

---

## Version Compatibility

### praxis.yaml Schema

**Current:** No schema version required (backward compatible)

**Future:** Optional `schema_version` field
```yaml
schema_version: "1.0"  # Optional, defaults to latest
```

**What happens if schema changes?**
1. `praxis validate` warns about outdated schema
2. `praxis migrate --to-schema X.Y` provides automated migration
3. Core supports N and N-1 schema versions

### Extension Manifests

**Current:** `manifest_version: "0.1"` required

**Support policy:**
- Praxis supports N and N-1 manifest versions
- Deprecation warnings before removing version support
- Extensions without manifests are silently skipped

### Templates

**Current:** Git tags for version history

**Usage:**
```bash
# Use specific template version
praxis new myproject --template praxis-template-code-cli@v1.0.0

# Use latest (default)
praxis new myproject --template praxis-template-code-cli
```

---

## When Does Version Matter?

### For Praxis Users

**You care about:**
- CLI tool version (features available)
- Template version (when bootstrapping projects)
- Spec version (conceptual model stability)

**You don't care about:**
- praxis.yaml schema version (managed automatically)
- Extension manifest version (managed by extension authors)

### For Extension Authors

**You care about:**
- Extension manifest version (API contract)
- Praxis spec version (compatibility)
- CLI version (feature requirements)

**See:** [Extension Authoring Guide](extension-authoring.md)

### For Template Authors

**You care about:**
- Template version (evolution tracking)
- Praxis CLI version (generator features)
- praxis.yaml schema (what fields to include)

---

## Version Roadmap

### v0.x (Current)

**Status:** Under validation, subject to change

**What this means:**
- Core concepts are stable (lifecycle, domains, privacy)
- Details may evolve based on real projects
- No backward compatibility guarantees yet

### v1.0 (Future)

**Criteria:**
- Validated through 5+ real projects across 3+ domains
- No major lifecycle or domain gaps
- Extension API stable
- Backward compatibility strategy proven

**Stability commitment:**
- Breaking changes only in major versions (v2.0+)
- Deprecation warnings before removal
- Migration tooling available

---

## FAQ

### Q: Why is the spec v0.3 but the CLI v0.1.0?

**A:** They track different things. The spec (v0.3) tracks conceptual model stability. The CLI (v0.1.0) tracks implementation maturity. They evolve at different rates.

### Q: Do I need to add schema_version to my praxis.yaml?

**A:** Not yet. It's optional and will default to latest. Add it when you want explicit control over schema migration.

### Q: How do I know which template version to use?

**A:** Use the latest unless you have a specific reason to pin. Template versions are tracked via git tags.

### Q: Will old projects break when Praxis updates?

**A:** No. Backward compatibility is a core principle. When breaking changes are necessary:
1. You'll get warnings
2. Migration tooling will be provided
3. Old schema versions will be supported during transition

### Q: Can I use my own versioning scheme for my project?

**A:** Yes! Praxis doesn't dictate project versioning. Use whatever your domain/ecosystem expects (SemVer for Python, CalVer if you prefer, etc.).

---

## Next Steps

- **Full details:** [ADR-004: Versioning and Naming Schemes](../../adr/004-versioning-and-naming-schemes.md)
- **Spec version history:** [core/spec/VERSION.md](../../core/spec/VERSION.md)
- **Extension authoring:** [extension-authoring.md](extension-authoring.md)
- **User guide:** [user-guide.md](user-guide.md)
