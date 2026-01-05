# Documentation Tool Spike — Summary

**Date:** 2026-01-05  
**Status:** ✅ Completed  
**Related Issue:** (Documentation tool investigation)

---

## Executive Summary

This spike evaluated documentation generation tools for Praxis to address limitations in the current plain markdown structure. After researching Sphinx, MkDocs, and Docusaurus, **MkDocs with Material theme is recommended** for its simplicity, markdown compatibility, and low barrier to entry.

---

## Recommendation

### Primary: MkDocs with Material Theme

**Why MkDocs:**
✅ Markdown-native (zero conversion needed)  
✅ Simple setup and configuration  
✅ Fast builds with live reload  
✅ Excellent Material theme  
✅ One-command GitHub Pages deployment  
✅ Low learning curve for contributors

**Trade-offs:**
⚠️ CLI auto-generation less mature (custom script needed)  
⚠️ Versioning requires manual setup (vs ReadTheDocs automation)  
⚠️ Less powerful for extensive API documentation

### Alternative: Sphinx with MyST Parser

**When to consider Sphinx:**
- Need robust CLI auto-generation via sphinx-typer
- Want first-class ReadTheDocs integration
- Plan extensive API documentation from Python docstrings

**Why not now:**
- Steeper learning curve
- More complex configuration
- Slower iteration

### Not Recommended: Docusaurus

**Why not:**
- Requires Node.js (not Python-native)
- No Python CLI integration
- Overkill for current needs

---

## Prototype Validation

A working MkDocs prototype was created and tested:

✅ Successfully builds documentation site  
✅ Material theme renders correctly  
✅ Search functionality works  
✅ Navigation and structure validated  
✅ Build time: ~1 second

**Prototype files:**
- `mkdocs.yml` — Configuration
- `docs/index.md` — Home page
- `docs/reference/cli.md` — CLI reference placeholder
- `adr/index.md` — ADR index

---

## Next Steps

### Immediate (Separate Implementation Issue)

1. **Copy core documentation into docs/**
   - Copy `core/spec/*.md` to `docs/philosophy/`
   - Copy `core/governance/*.md` to `docs/governance/`
   - Copy `adr/*.md` to `docs/adr/`
   - Copy `CONTRIBUTING.md` to `docs/`

2. **Set up GitHub Pages deployment**
   - Create `.github/workflows/docs.yml`
   - Configure automatic build on push to main
   - Enable GitHub Pages on repository

3. **Create CLI reference auto-generation**
   - Write script to extract Typer help text
   - Generate markdown from CLI structure
   - Integrate into build process

### Short-term

1. Add versioning support (mike plugin or ReadTheDocs)
2. Improve navigation and cross-references
3. Add code blocks with syntax highlighting
4. Create contribution guide for documentation

### Long-term

1. Consider switching to Sphinx if API documentation needs grow
2. Explore ReadTheDocs for automated versioning
3. Add search analytics to understand user needs

---

## Comparison Matrix

| Feature | Sphinx | MkDocs | Docusaurus |
|---------|--------|--------|------------|
| Python Integration | ✅ Excellent | ✅ Good | ❌ Poor |
| Markdown Native | ⚠️ Via extension | ✅ Yes | ✅ Yes |
| CLI Auto-gen | ✅ sphinx-typer | ⚠️ Custom script | ❌ Manual |
| Learning Curve | ⚠️ Moderate | ✅ Low | ⚠️ High |
| Build Speed | ⚠️ Slower | ✅ Fast | ⚠️ Moderate |
| GitHub Pages | ⚠️ Manual setup | ✅ One command | ✅ Supported |

---

## Key Findings

1. **MkDocs covers 90% of needs** without Sphinx complexity
2. **Typer's own docs use MkDocs** — strong validation for CLI projects
3. **CLI auto-generation** is the main gap; custom script is acceptable
4. **Versioning** not critical until v1.0; can add later
5. **Migration effort** is minimal due to markdown compatibility

---

## References

- **Full evaluation:** [docs/spikes/documentation-tool-evaluation.md](documentation-tool-evaluation.md)
- **MkDocs:** https://www.mkdocs.org/
- **Material for MkDocs:** https://squidfunk.github.io/mkdocs-material/
- **Typer docs (MkDocs example):** https://typer.tiangolo.com/

---

**Status:** ✅ Ready for implementation  
**Next Action:** Create implementation issue: "Set up MkDocs documentation site"
