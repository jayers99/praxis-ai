# Documentation Tool Evaluation Spike

**Date:** 2026-01-05  
**Status:** ✅ Completed  
**Priority:** High  
**Size:** Medium  
**Type:** Spike  
**Maturity:** Raw

---

## Executive Summary

This spike evaluates documentation generation tools for Praxis to address growing complexity in the Philosophy and Command Reference sections. Current plain markdown files are limiting navigation, search, versioning, and presentation capabilities.

**Tools evaluated:**
1. **Sphinx** — Python standard, extensive ecosystem
2. **MkDocs** — Simple, markdown-native, Python-friendly
3. **Docusaurus** — Modern, React-based, feature-rich

---

## Problem Statement

The current documentation structure faces several limitations:

- **Navigation:** No sidebar, table of contents, or cross-referencing between documents
- **Search:** No built-in search functionality across documentation
- **Versioning:** Difficult to maintain versioned docs as the CLI evolves
- **Presentation:** Limited styling, no admonitions, callouts, or structured API documentation

---

## Evaluation Criteria

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Python integration | High | Praxis is a Python project; tight integration is essential |
| Markdown compatibility | High | All existing docs are in Markdown; migration path must be smooth |
| CLI reference auto-generation | High | Need to generate CLI docs from Typer commands |
| Search functionality | Medium | Important for usability, but can be added later |
| Versioning support | Medium | Future need as CLI evolves |
| Hosting options | Medium | GitHub Pages is preferred (free, simple) |
| Learning curve | Medium | Should be accessible to contributors |
| Build speed | Low | Documentation build time is not a bottleneck |
| Customization | Low | Default themes are likely sufficient initially |

---

## Tool 1: Sphinx

### Overview

- **Website:** https://www.sphinx-doc.org/
- **Language:** Python
- **Primary format:** reStructuredText (RST), with markdown via MyST extension
- **Ecosystem:** De facto standard for Python documentation (Python docs, Django, Flask, NumPy)

### Features

**Strengths:**
- **Python-native:** Built for Python projects, excellent autodoc capabilities
- **Mature ecosystem:** Extensive extension library (sphinx-autodoc, sphinx-apidoc, sphinx-typer)
- **CLI auto-generation:** `sphinx-typer` or `sphinx-click` for Typer/Click CLIs
- **ReadTheDocs integration:** First-class support, automatic builds on git push
- **Versioning:** Built-in version selector via ReadTheDocs
- **Cross-referencing:** Powerful intersphinx for linking between docs
- **API documentation:** Excellent autodoc from Python docstrings
- **Admonitions:** Rich set of callouts (note, warning, tip, etc.)

**Weaknesses:**
- **Complexity:** Steeper learning curve than MkDocs
- **RST-first:** Markdown support requires MyST parser extension
- **Build time:** Can be slower for large documentation sets
- **Configuration:** More complex `conf.py` setup

**Markdown Compatibility:**
- Supports markdown via `myst-parser` extension
- Existing `.md` files can be used with minimal changes
- Some RST-specific features require conversion

**Hosting Options:**
- ReadTheDocs (free for open source, automatic builds)
- GitHub Pages (requires manual build step or CI)
- Self-hosted

### CLI Reference Auto-Generation

**Option 1: sphinx-typer**
```python
# In docs/conf.py
extensions = ['sphinx_typer']

# In docs/cli-reference.rst or .md
```{typer} praxis.cli:app
```

**Option 2: sphinx-click**
```python
# Similar approach for Click-compatible CLIs
extensions = ['sphinx_click']
```

### Example Setup

```bash
# Install dependencies
pip install sphinx sphinx-typer myst-parser sphinx-rtd-theme

# Initialize
cd docs
sphinx-quickstart

# Build
make html
```

**Directory structure:**
```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main entry point
├── guides/              # User guides (markdown)
├── reference/           # CLI reference (auto-generated)
└── _build/html/         # Generated HTML
```

### Pros & Cons Summary

**Pros:**
✅ Python standard with excellent ecosystem  
✅ Powerful autodoc and API documentation  
✅ ReadTheDocs integration for versioning and hosting  
✅ CLI auto-generation via sphinx-typer  
✅ Rich cross-referencing and intersphinx  
✅ Professional output with RTD theme

**Cons:**
❌ Steeper learning curve for contributors  
❌ RST-first (though markdown works)  
❌ More complex configuration  
❌ Slower build times for large projects

---

## Tool 2: MkDocs

### Overview

- **Website:** https://www.mkdocs.org/
- **Language:** Python
- **Primary format:** Markdown (native)
- **Ecosystem:** Simple, focused on markdown documentation

### Features

**Strengths:**
- **Markdown-native:** No conversion needed, works with existing .md files
- **Simple setup:** Minimal configuration via `mkdocs.yml`
- **Fast builds:** Quick iteration during development
- **Material theme:** Modern, feature-rich Material for MkDocs theme
- **GitHub Pages:** One-command deployment (`mkdocs gh-deploy`)
- **Search:** Built-in client-side search
- **Easy learning curve:** Minimal barrier to contribution

**Weaknesses:**
- **Limited API autodoc:** Not designed for Python API documentation
- **CLI auto-generation:** Requires custom scripts or plugins (less mature)
- **Less powerful cross-referencing:** Simpler than Sphinx
- **Fewer extensions:** Smaller ecosystem than Sphinx

**Markdown Compatibility:**
- 100% markdown native
- Existing docs work as-is
- Supports extended markdown (admonitions, tables, code blocks)

**Hosting Options:**
- GitHub Pages (one-command: `mkdocs gh-deploy`)
- ReadTheDocs (supported but not primary)
- Netlify, Vercel, etc.

### CLI Reference Auto-Generation

**Option 1: mkdocs-typer**
- Third-party plugin, less mature than sphinx-typer
- May require manual documentation

**Option 2: mkdocs-click**
- For Click CLIs (Typer is Click-compatible)
- Requires plugin installation

**Option 3: Manual generation**
- Use custom script to extract Typer help text
- Generate markdown files

### Example Setup

```bash
# Install dependencies
pip install mkdocs mkdocs-material

# Initialize
mkdocs new .

# Build
mkdocs serve  # Live preview
mkdocs build  # Build static site
mkdocs gh-deploy  # Deploy to GitHub Pages
```

**Directory structure:**
```
docs/
├── index.md             # Home page
├── guides/              # User guides
├── reference/           # CLI reference
mkdocs.yml               # Configuration
site/                    # Generated HTML
```

**mkdocs.yml example:**
```yaml
site_name: Praxis Documentation
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest

nav:
  - Home: index.md
  - User Guide: guides/user-guide.md
  - CLI Reference: reference/cli.md
  - Philosophy: core/spec/sod.md

plugins:
  - search
  - mkdocstrings  # For Python API docs
```

### Pros & Cons Summary

**Pros:**
✅ Markdown-native, zero conversion needed  
✅ Simple setup and configuration  
✅ Fast builds, live reload during development  
✅ Excellent Material theme with modern UX  
✅ One-command GitHub Pages deployment  
✅ Low learning curve for contributors

**Cons:**
❌ Weaker CLI auto-generation (less mature plugins)  
❌ Limited API autodoc compared to Sphinx  
❌ Smaller extension ecosystem  
❌ Less powerful versioning (manual setup)

---

## Tool 3: Docusaurus

### Overview

- **Website:** https://docusaurus.io/
- **Language:** JavaScript/TypeScript (React)
- **Primary format:** Markdown (MDX with React components)
- **Ecosystem:** Modern, feature-rich, maintained by Meta

### Features

**Strengths:**
- **Modern UX:** React-based, highly interactive
- **Versioning:** First-class version selector built-in
- **Internationalization:** Built-in i18n support
- **MDX:** Embed React components in markdown
- **Search:** Algolia DocSearch integration (free for open source)
- **Blog:** Built-in blog support
- **Customization:** Full control via React components

**Weaknesses:**
- **Not Python-native:** JavaScript/Node.js toolchain required
- **CLI auto-generation:** No Python Typer integration
- **Complexity:** More moving parts than MkDocs
- **Build requirements:** Requires Node.js in CI/CD
- **Overkill:** May be too feature-rich for current needs

**Markdown Compatibility:**
- Supports standard markdown
- MDX allows React components (optional)
- Frontmatter for metadata

**Hosting Options:**
- GitHub Pages
- Netlify, Vercel (recommended)
- Self-hosted

### CLI Reference Auto-Generation

**Challenges:**
- No native Python CLI integration
- Would require custom script to generate markdown
- Not designed for Python tooling

**Workaround:**
```bash
# Generate markdown from Typer CLI
python scripts/generate_cli_docs.py > docs/cli-reference.md
```

### Example Setup

```bash
# Install dependencies (requires Node.js)
npx create-docusaurus@latest docs classic

# Build
cd docs
npm run start  # Development server
npm run build  # Production build
```

**Directory structure:**
```
docs/
├── docs/                # Documentation markdown
│   ├── guides/
│   └── reference/
├── blog/                # Optional blog
├── src/                 # Custom React components
├── static/              # Static assets
├── docusaurus.config.js # Configuration
└── package.json         # Node dependencies
```

### Pros & Cons Summary

**Pros:**
✅ Modern, feature-rich UX  
✅ First-class versioning support  
✅ Excellent search (Algolia)  
✅ Internationalization built-in  
✅ Highly customizable

**Cons:**
❌ Not Python-native (requires Node.js)  
❌ No Typer/Python CLI integration  
❌ More complex setup and build process  
❌ Overkill for current Praxis needs  
❌ Higher learning curve for contributors

---

## Comparison Matrix

| Feature | Sphinx | MkDocs | Docusaurus |
|---------|--------|--------|------------|
| **Python Integration** | ✅ Excellent | ✅ Good | ❌ Poor (Node.js) |
| **Markdown Native** | ⚠️ Via extension | ✅ Yes | ✅ Yes |
| **CLI Auto-gen** | ✅ sphinx-typer | ⚠️ Less mature | ❌ Manual |
| **API Autodoc** | ✅ Excellent | ⚠️ Basic | ❌ None |
| **Search** | ✅ Yes | ✅ Yes | ✅ Yes (Algolia) |
| **Versioning** | ✅ Via ReadTheDocs | ⚠️ Manual | ✅ Built-in |
| **GitHub Pages** | ⚠️ Manual setup | ✅ One command | ✅ Supported |
| **Learning Curve** | ⚠️ Moderate | ✅ Low | ⚠️ Moderate-High |
| **Build Speed** | ⚠️ Slower | ✅ Fast | ⚠️ Moderate |
| **Ecosystem** | ✅ Large | ⚠️ Medium | ✅ Large |

**Legend:** ✅ Strong | ⚠️ Adequate | ❌ Weak

---

## Recommendation

### Primary Recommendation: **MkDocs with Material Theme**

**Rationale:**

1. **Minimal Migration Effort:** All existing markdown works as-is, no conversion needed
2. **Low Barrier to Entry:** Simple configuration, easy for contributors to understand
3. **Fast Iteration:** Quick builds, live reload for rapid development
4. **GitHub Pages:** One-command deployment fits existing workflow
5. **Good Enough:** Covers 90% of needs without the complexity of Sphinx

**When to choose MkDocs:**
- ✅ You prioritize markdown compatibility
- ✅ You want simple, fast setup
- ✅ You don't need extensive API autodoc
- ✅ You want low contributor friction

**Trade-offs:**
- CLI auto-generation is less mature (may need custom script)
- Versioning requires manual setup (vs ReadTheDocs automation)
- Less powerful than Sphinx for complex API documentation

### Alternative Recommendation: **Sphinx with MyST Parser**

**When to choose Sphinx:**

- ✅ You need robust CLI auto-generation via sphinx-typer
- ✅ You want first-class ReadTheDocs integration with versioning
- ✅ You plan extensive API documentation from Python docstrings
- ✅ You value the mature ecosystem and extensions

**Trade-offs:**
- Steeper learning curve for contributors
- More complex configuration
- Slower iteration during development

### Not Recommended: **Docusaurus**

**Why not:**
- ❌ Requires Node.js toolchain (not Python-native)
- ❌ No Python CLI integration
- ❌ Overkill for current needs
- ❌ Higher complexity without proportional benefit

Docusaurus is excellent for large-scale, multi-lingual documentation sites with heavy customization needs. Praxis doesn't need this level of sophistication yet.

---

## Implementation Roadmap

### Phase 1: Initial Setup (MkDocs)

**Goal:** Get basic documentation site live with existing content

**Tasks:**
1. Install MkDocs and Material theme
2. Create `mkdocs.yml` configuration
3. Organize existing docs into site structure
4. Set up GitHub Pages deployment
5. Add search functionality

**Estimated effort:** 2-4 hours

**Example `mkdocs.yml`:**
```yaml
site_name: Praxis Documentation
site_url: https://jayers99.github.io/praxis-ai/
repo_url: https://github.com/jayers99/praxis-ai
repo_name: jayers99/praxis-ai

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - toc.integrate
    - search.suggest
    - search.highlight
    - content.code.copy

nav:
  - Home: index.md
  - User Guide:
    - Getting Started: guides/user-guide.md
    - Installation: guides/installation.md
    - AI Setup: guides/ai-setup.md
    - Stage Templates: guides/stage-templates.md
  - Philosophy:
    - Overview: core/spec/sod.md
    - Lifecycle: core/spec/lifecycle.md
    - Domains: core/spec/domains.md
    - Privacy: core/spec/privacy.md
  - CLI Reference: reference/cli.md
  - ADRs: adr/

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - toc:
      permalink: true
```

### Phase 2: CLI Reference Auto-Generation

**Goal:** Generate CLI documentation from Typer commands

**Options:**

**Option A: Custom script**
```python
# scripts/generate_cli_docs.py
import typer
from praxis.cli import app

def extract_help(app: typer.Typer) -> str:
    # Extract command structure and help text
    # Generate markdown
    pass

if __name__ == "__main__":
    docs = extract_help(app)
    with open("docs/reference/cli.md", "w") as f:
        f.write(docs)
```

**Option B: Use mkdocs-click plugin**
- Test if it works with Typer (Typer is Click-compatible)
- May require adjustments

**Estimated effort:** 4-8 hours

### Phase 3: Versioning Support

**Goal:** Add version selector for documentation

**Approach 1: Manual versioning**
- Use `mike` plugin for MkDocs
- Deploy multiple versions to gh-pages branch
- Version selector in UI

**Approach 2: ReadTheDocs**
- Switch hosting to ReadTheDocs
- Automatic version builds on git tags
- Built-in version selector

**Estimated effort:** 2-4 hours

### Phase 4: Migration & Cleanup

**Goal:** Reorganize existing docs for optimal site structure

**Tasks:**
1. Review all existing markdown files
2. Consolidate redundant content
3. Add cross-references between pages
4. Improve navigation hierarchy
5. Add admonitions and callouts where appropriate

**Estimated effort:** 8-16 hours

---

## Migration Path

### Current Structure
```
praxis-ai/
├── README.md
├── docs/
│   ├── guides/
│   │   ├── user-guide.md
│   │   ├── installation.md
│   │   └── ...
│   └── spikes/
├── core/
│   ├── spec/
│   │   ├── sod.md
│   │   ├── lifecycle.md
│   │   └── ...
│   └── governance/
└── adr/
```

### Target Structure (MkDocs)
```
praxis-ai/
├── README.md (simplified, points to docs site)
├── docs/
│   ├── index.md (home page)
│   ├── guides/
│   │   ├── user-guide.md
│   │   ├── installation.md
│   │   └── ...
│   ├── philosophy/
│   │   ├── overview.md (from core/spec/sod.md)
│   │   ├── lifecycle.md (symlink or copy)
│   │   └── ...
│   ├── reference/
│   │   ├── cli.md (auto-generated)
│   │   └── api.md (future)
│   └── adr/
├── mkdocs.yml
├── core/ (unchanged, source of truth)
└── site/ (generated, gitignored)
```

### Migration Steps

1. **No breaking changes:** Keep existing files in place
2. **Symlink approach:** Link from `docs/` to `core/spec/` to avoid duplication
3. **Generate site:** Build documentation site from existing content
4. **Update README:** Add link to documentation site
5. **CI/CD:** Add GitHub Actions workflow for automatic deployment

**Example GitHub Actions workflow:**
```yaml
# .github/workflows/docs.yml
name: Deploy Documentation

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: 3.12
      - name: Install dependencies
        run: pip install mkdocs mkdocs-material
      - name: Build and deploy
        run: mkdocs gh-deploy --force
```

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Contributor friction** | Contributors unfamiliar with doc tooling | Choose MkDocs (simple), provide clear setup guide |
| **Maintenance burden** | Another system to maintain | Minimize config, use GitHub Actions for automation |
| **Content duplication** | Docs out of sync with specs | Use symlinks or includes, single source of truth |
| **Build failures** | CI failures block deployment | Thorough testing, fail gracefully with warnings |
| **Version management** | Multiple versions to maintain | Start simple, add versioning only when needed |

---

## Open Questions

1. **CLI auto-generation:** Should we write a custom script or try mkdocs-click plugin first?
2. **Versioning timing:** When do we need versioned docs? (Probably not until v1.0)
3. **Hosting:** GitHub Pages vs ReadTheDocs?
4. **Migration timing:** Big-bang or incremental?
5. **API docs:** Do we need Python API documentation now or later?

---

## Success Criteria

This spike is successful if:

✅ **Evaluated 3+ tools** — Sphinx, MkDocs, Docusaurus analyzed  
✅ **Documented pros/cons** — Comparison matrix created  
✅ **Provided recommendation** — MkDocs recommended with rationale  
✅ **Identified migration path** — Phased approach defined  
✅ **Prototype feasibility** — Basic setup validated (Phase 1)

---

## Prototype Results

A working MkDocs prototype was created and validated:

**Files created:**
- `mkdocs.yml` — Configuration with Material theme
- `docs/index.md` — Home page with quick links and overview
- `docs/reference/cli.md` — CLI reference placeholder (manual for now)
- `adr/index.md` — ADR index page

**Build results:**
- ✅ Successfully builds with `mkdocs build`
- ✅ Material theme renders correctly
- ✅ Search functionality works
- ✅ Navigation tabs and sections display properly
- ✅ Markdown extensions work (admonitions, code blocks, tables)
- ✅ Live reload works with `mkdocs serve`

**Build time:** ~1 second for clean build

**Warnings resolved:**
- Simplified navigation to only include files in `docs/` directory
- Links to `core/`, `adr/`, and `CONTRIBUTING.md` need to be copied/symlinked or navigation updated

**Next steps for full implementation:**
1. Copy or symlink files from `core/`, `adr/`, and root into `docs/`
2. Update internal links to work within `docs/` structure
3. Set up GitHub Actions for automated deployment
4. Create custom script for CLI reference auto-generation

---

## Next Steps

### For Immediate Implementation (Separate Issue)

1. Create issue: "Implement MkDocs documentation site"
   - Label: `type: feature`, `maturity: formalized`, `size: medium`
   - Implement Phase 1 (basic setup)
   - Set up GitHub Pages deployment
   
2. Create issue: "Generate CLI reference documentation"
   - Label: `type: feature`, `maturity: shaped`, `size: small`
   - Implement custom script or test mkdocs-click
   - Automate regeneration on CLI changes

3. Create issue: "Add versioning support to documentation"
   - Label: `type: feature`, `maturity: raw`, `size: small`
   - Defer until closer to v1.0
   - Research `mike` plugin for MkDocs

### For Long-term Consideration

- **Search analytics:** Track what users search for to improve docs
- **Contribution guide:** Add docs contribution section
- **API documentation:** Add when Python API stabilizes
- **Internationalization:** Consider if community grows

---

## Appendix: Research Notes

### Similar Python Projects

**Projects using Sphinx:**
- Python official docs
- Django
- Flask
- NumPy
- Pandas
- Requests

**Projects using MkDocs:**
- FastAPI
- Material for MkDocs (self-documenting)
- Typer (ironically, Typer's docs use MkDocs!)
- mkdocstrings

**Projects using Docusaurus:**
- React (Meta)
- Jest
- Babel
- Prettier

### Typer Documentation Example

Interestingly, **Typer itself uses MkDocs with Material theme**:
- Source: https://github.com/tiangolo/typer
- Docs: https://typer.tiangolo.com/

This is a strong signal that MkDocs works well for Python CLI documentation.

### ReadTheDocs vs GitHub Pages

**ReadTheDocs:**
- ✅ Automatic builds on push
- ✅ Built-in version selector
- ✅ Free for open source
- ✅ No CI/CD setup needed
- ⚠️ Slightly slower builds
- ⚠️ Less control over deployment

**GitHub Pages:**
- ✅ Simple, integrated with GitHub
- ✅ Fast, CDN-backed
- ✅ Full control via GitHub Actions
- ⚠️ Requires CI/CD setup
- ⚠️ Manual version management

**Recommendation:** Start with GitHub Pages for simplicity, switch to ReadTheDocs if versioning becomes critical.

---

## References

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Docusaurus Documentation](https://docusaurus.io/)
- [sphinx-typer](https://github.com/tiangolo/sphinx-typer)
- [mkdocstrings](https://mkdocstrings.github.io/)
- [Typer Documentation Source](https://github.com/tiangolo/typer)
- [ADR-004: Versioning and Naming Schemes](../../adr/004-versioning-and-naming-schemes.md)

---

**Status:** ✅ Completed  
**Next Action:** Create implementation issue for MkDocs setup
