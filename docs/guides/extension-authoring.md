# Extension Authoring Guide

> **Status:** v0.1 (Experimental) — API subject to change before v1.0

This guide explains how to create Praxis extensions that contribute opinions, templates, and audit checks to extend Praxis without modifying core code.

---

## Overview

Praxis extensions enable domain-specific customization:

- **Opinions:** Add guidance for specialized subtypes (e.g., mobile, embedded, ML)
- **Templates:** Provide scaffolding for new project types
- **Audits:** Add domain-specific quality checks (Story 3)

Extensions are discovered from installed extensions in a Praxis workspace and loaded automatically.

---

## Quick Start

### 1. Create Extension Directory

```bash
mkdir praxis-extension-yourname
cd praxis-extension-yourname
```

### 2. Create Manifest

Create `praxis-extension.yaml`:

```yaml
manifest_version: "0.1"
name: yourname
description: Your extension description

contributions:
  opinions:
    - source: opinions/code/subtypes/yourtype.md
      target: code/subtypes/yourtype.md
```

**Critical:** The `name` field MUST match your directory name.

### 3. Add Opinion Files

Create the opinion file referenced in your manifest:

```bash
mkdir -p opinions/code/subtypes
```

Create `opinions/code/subtypes/yourtype.md`:

```markdown
---
domain: code
version: "1.0"
status: active
subtype: yourtype
author: human
last_reviewed: 2026-01-04
---

# Your Subtype Principles

Your guidance content here...
```

### 4. Add Template Files (Optional)

If contributing templates, create the template directory structure:

```bash
mkdir -p templates/domain/code/subtype/yourtype/stage
```

Create `templates/domain/code/subtype/yourtype/stage/formalize.md`:

```markdown
# Formalize Stage - {{subtype}}

**Date:** {{today}}
**Domain:** {{domain}}
**Stage:** {{stage}}

## Your Subtype-Specific Formalization

Your template content here...
```

Update your manifest to include the template contribution:

```yaml
contributions:
  templates:
    - source: templates/domain/code/subtype/yourtype/stage/formalize.md
      target: domain/code/subtype/yourtype/stage/formalize.md
      subtypes: ["yourtype"]
```

### 5. Test Locally

Install your extension in a workspace:

```bash
# Option 1: Clone into workspace
cd $PRAXIS_HOME/extensions
git clone /path/to/your/extension yourname

# Option 2: Symlink for development
ln -s /path/to/your/extension $PRAXIS_HOME/extensions/yourname

# Add to workspace config
# (Or use `praxis extensions add yourname` when available)
```

Verify it loads:

```bash
cd /path/to/any/project
praxis opinions --list
# Should show: code/subtypes/yourtype.md [yourname]

# Test template rendering (if you added templates)
praxis new test-project --domain code --subtype yourtype
cd test-project
praxis templates render --stage formalize
# Should use your extension's template
```

---

## Manifest Schema Reference

### Required Fields

```yaml
manifest_version: "0.1"  # Must be "0.1" (only supported version)
name: extension-name      # Must match directory name exactly
```

### Optional Fields

```yaml
description: "Human-readable description"  # Shown in extension listings
```

### Contributions

Currently supported (v0.1):

```yaml
contributions:
  opinions:
    - source: opinions/path/in/extension.md
      target: path/in/opinions/tree.md
  
  templates:  # NEW in Story 2
    - source: templates/domain/code/subtype/mobile/stage/formalize.md
      target: domain/code/subtype/mobile/stage/formalize.md
      subtypes: ["mobile"]  # Optional: restrict to specific subtypes
```

**Opinion Contribution Fields:**
- `source`: Relative path to opinion file in your extension directory
- `target`: Target path in the global opinions tree (e.g., `code/subtypes/mobile.md`)

**Template Contribution Fields:**
- `source`: Relative path to template file in your extension directory
- `target`: Target path in template tree (for documentation)
- `subtypes`: (Optional) List of subtypes this template applies to. Empty list = all subtypes.

**Coming in Story 3:**
- `audits`: Audit check contributions

---

## Template File Guidelines

### 1. Template Directory Structure

Extensions contribute templates by following the standard template directory structure:

```
praxis-extension-yourname/
└── templates/                    # Template root
    ├── stage/                    # Generic stage templates
    │   └── formalize.md
    ├── domain/                   # Domain-specific templates
    │   └── code/
    │       ├── stage/            # Domain stage templates
    │       │   └── formalize.md
    │       ├── artifact/         # Domain artifacts
    │       │   └── sod.md
    │       └── subtype/          # Subtype-specific templates
    │           └── mobile/
    │               ├── stage/
    │               │   └── formalize.md
    │               └── artifact/
    │                   └── sod.md
```

### 2. Template Content

Templates use simple variable substitution:

```markdown
# {{stage}} Stage - {{subtype}}

**Date:** {{today}}
**Domain:** {{domain}}

Your template content here...
```

**Available Variables:**
- `{{today}}`: Current date (ISO format)
- `{{domain}}`: Project domain
- `{{subtype}}`: Project subtype (or empty string)
- `{{stage}}`: Stage name (for stage templates)

### 3. Subtype Filtering

Control which projects can use your templates:

```yaml
contributions:
  templates:
    # Mobile-specific template (only for mobile projects)
    - source: templates/domain/code/subtype/mobile/stage/formalize.md
      target: domain/code/subtype/mobile/stage/formalize.md
      subtypes: ["mobile"]
    
    # Universal template (all projects)
    - source: templates/stage/capture.md
      target: stage/capture.md
      subtypes: []  # Empty list = all subtypes
```

### 4. Template Precedence

Templates are resolved in order of specificity:

1. **Project-local** (`.praxis/templates/`)
2. **Custom** (`--template-root` CLI arg)
3. **Extension** (alphabetically sorted by extension name)
4. **Core** (fallback)

**Example:** For a `mobile` project at `formalize` stage:
1. Check for `domain/code/subtype/mobile/stage/formalize.md` (most specific)
2. Check for `domain/code/stage/formalize.md` (domain-specific)
3. Check for `stage/formalize.md` (generic)

Extensions come before core, so extension templates will be used if available.

### 5. Validation

When loading the manifest, Praxis validates that template source files exist:

```bash
# ✅ Valid - file exists
contributions:
  templates:
    - source: templates/domain/code/subtype/mobile/stage/formalize.md
      target: domain/code/subtype/mobile/stage/formalize.md
      subtypes: ["mobile"]

# ❌ Warning - file missing (contribution skipped)
contributions:
  templates:
    - source: templates/missing.md  # File doesn't exist!
      target: stage/missing.md
      subtypes: []
```

Missing template files generate warnings but don't fail manifest loading.

---

## Audit Check Contributions

### 1. Overview

Extensions can contribute domain-specific audit checks that automatically appear in `praxis audit` output for matching projects.

**Example Use Cases:**
- Mobile-specific checks (e.g., validate mobile.json exists)
- Library-specific checks (e.g., check for CHANGELOG.md)
- Platform-specific checks (e.g., verify deployment configs)

### 2. Basic Structure

Add audit contributions to your manifest:

```yaml
manifest_version: "0.1"
name: mobile-pack
description: Mobile development audit checks

contributions:
  audits:
    - domain: "code"
      subtypes: ["mobile"]
      checks:
        - name: "mobile_manifest_exists"
          category: "structure"
          check_type: "file_exists"
          path: "mobile.json"
          pass_message: "Mobile manifest exists (mobile.json)"
          fail_message: "Mobile manifest missing (create mobile.json)"
          severity: "warning"
```

### 3. Supported Check Types

| Check Type | Parameters | Description |
|------------|------------|-------------|
| `file_exists` | `path` | Checks if a file exists at the specified path |
| `dir_exists` | `path` | Checks if a directory exists at the specified path |
| `file_contains` | `path`, `pattern` | Checks if file contains regex pattern |

**Example - File Exists:**
```yaml
- name: "readme_exists"
  category: "documentation"
  check_type: "file_exists"
  path: "README.md"
  pass_message: "README exists"
  fail_message: "README not found"
  severity: "warning"
```

**Example - Directory Exists:**
```yaml
- name: "tests_directory"
  category: "testing"
  check_type: "dir_exists"
  path: "tests"
  pass_message: "Tests directory exists"
  fail_message: "Tests directory not found"
  severity: "warning"
```

**Example - File Contains (with regex):**
```yaml
- name: "version_in_pyproject"
  category: "configuration"
  check_type: "file_contains"
  path: "pyproject.toml"
  pattern: 'version\s*=\s*"[0-9]+\.[0-9]+"'
  pass_message: "Version specified in pyproject.toml"
  fail_message: "Version not specified"
  severity: "warning"
```

### 4. Filtering

**Domain Filtering:**
```yaml
audits:
  - domain: "code"  # Only applies to code domain projects
    checks: [...]
  
  - domain: "create"  # Only applies to create domain projects
    checks: [...]
```

**Subtype Filtering:**
```yaml
audits:
  - domain: "code"
    subtypes: ["mobile"]  # Only for mobile projects
    checks: [...]
  
  - domain: "code"
    subtypes: []  # All code projects (empty = no filter)
    checks: [...]
```

**Stage Filtering:**
```yaml
checks:
  - name: "docs_site_exists"
    check_type: "dir_exists"
    path: "docs"
    min_stage: "formalize"  # Only at formalize stage or later
    pass_message: "Documentation site exists"
    fail_message: "Documentation site not found"
    severity: "warning"
```

### 5. Check Fields Reference

**Required Fields:**
- `name` (string): Unique check name within the extension
- `category` (string): Check category (e.g., "structure", "tooling", "documentation")
- `check_type` (string): Type of check (`file_exists`, `dir_exists`, `file_contains`)
- `path` (string): File or directory path (relative to project root)
- `pass_message` (string): Message when check passes
- `fail_message` (string): Message when check fails

**Optional Fields:**
- `pattern` (string): Regex pattern (required for `file_contains` checks)
- `severity` (string): `"warning"` or `"failed"` (default: `"warning"`)
- `min_stage` (string): Minimum lifecycle stage (e.g., `"formalize"`, `"commit"`)

### 6. Provenance and Naming

Extension checks are automatically prefixed with the extension name for provenance:

```yaml
# In manifest:
name: "mobile_manifest_exists"

# In audit output:
# Check is registered as: "mobile-pack:mobile_manifest_exists"
```

This prevents naming conflicts between extensions.

### 7. Best Practices

**✅ Do:**
- Use descriptive check names that explain what's being validated
- Provide helpful pass/fail messages that guide users
- Use appropriate severity levels (`warning` for best practices, `failed` for requirements)
- Use `min_stage` to avoid noise in early stages
- Group related checks by category

**❌ Don't:**
- Create checks that require external tools or network access
- Use overly complex regex patterns that are hard to maintain
- Duplicate core checks (check what exists first)
- Create checks that only apply to your organization (keep extensions general)

### 8. Example: Complete Audit Contribution

```yaml
manifest_version: "0.1"
name: mobile-pack
description: Mobile development best practices

contributions:
  audits:
    - domain: "code"
      subtypes: ["mobile"]
      checks:
        # Structure checks (all stages)
        - name: "mobile_manifest_exists"
          category: "structure"
          check_type: "file_exists"
          path: "mobile.json"
          pass_message: "Mobile manifest exists (mobile.json)"
          fail_message: "Mobile manifest missing (create mobile.json)"
          severity: "warning"
        
        - name: "mobile_source_directory"
          category: "structure"
          check_type: "dir_exists"
          path: "src/mobile"
          pass_message: "Mobile source directory exists (src/mobile/)"
          fail_message: "Mobile source directory missing"
          severity: "warning"
        
        # Documentation checks (formalize+)
        - name: "native_bridge_documented"
          category: "documentation"
          check_type: "file_exists"
          path: "docs/native-bridge.md"
          pass_message: "Native bridge documented"
          fail_message: "Native bridge not documented"
          severity: "warning"
          min_stage: "formalize"
        
        # Configuration checks (formalize+)
        - name: "platform_target_specified"
          category: "configuration"
          check_type: "file_contains"
          path: "mobile.json"
          pattern: '"platforms"\s*:\s*\['
          pass_message: "Platform targets specified"
          fail_message: "Platform targets not specified"
          severity: "warning"
          min_stage: "formalize"
```

### 9. Testing Your Checks

**Local Testing:**
1. Install your extension in a workspace
2. Create a test project with matching domain/subtype
3. Run `praxis audit` to see your checks

```bash
# In your workspace
export PRAXIS_HOME=$HOME/praxis-workspace

# Install extension
cp -r praxis-extension-yourname $PRAXIS_HOME/extensions/

# Update workspace-config.yaml
# Add 'yourname' to installed_extensions list

# Create test project
mkdir test-project
cd test-project
cat > praxis.yaml << EOF
domain: code
stage: capture
subtype: mobile
privacy_level: personal
environment: Home
EOF

# Run audit
praxis audit
```

**Expected Output:**
- Your extension checks should appear in the output
- Check names prefixed with extension name
- Checks respect domain, subtype, and stage filters

### 10. Error Handling

Praxis gracefully handles malformed audit contributions:

**Invalid check type:**
```yaml
checks:
  - name: "bad_check"
    check_type: "custom_eval"  # Not supported
    # ⚠️ Warning: Unsupported check_type, check skipped
```

**Invalid regex:**
```yaml
checks:
  - name: "regex_check"
    check_type: "file_contains"
    pattern: "[unclosed"  # Invalid regex
    # ⚠️ Warning: Invalid regex pattern, check skipped
```

**Missing required fields:**
```yaml
checks:
  - name: "incomplete_check"
    check_type: "file_contains"
    # Missing 'pattern' field
    # ⚠️ Warning: Missing required field, check skipped
```

Malformed checks generate warnings but don't prevent other checks from running.

---

## Opinion File Guidelines

### 1. Frontmatter Requirements

All opinion files MUST include valid YAML frontmatter:

```yaml
---
domain: code             # REQUIRED: code, create, write, learn, observe
version: "1.0"           # REQUIRED: Semver string (quoted)
status: active           # REQUIRED: draft, active, deprecated

# Optional but recommended:
subtype: yourtype        # Restrict to specific subtype
stage: execute           # Restrict to specific stage
author: human            # human, ai, hybrid
last_reviewed: 2026-01-04  # ISO date
---
```

### 2. Content Structure

Follow the same structure as core opinions:

```markdown
# Title

## Section 1
Content...

## Section 2
Content...

## Quality Gates
- [ ] Gate 1
- [ ] Gate 2
```

See `opinions/_templates/` in the praxis-ai repository for templates.

### 3. Best Practices

- **Be specific:** Focus on concrete, actionable guidance
- **Provide rationale:** Explain WHY, not just WHAT
- **Include quality gates:** Define clear readiness criteria
- **Keep it current:** Update `last_reviewed` when revising
- **Mark deprecated:** Set `status: deprecated` for obsolete guidance

---

## Conflict Resolution

### Precedence Rules

When multiple sources contribute the same opinion file:

1. **Core wins** over all extensions
2. **Alphabetically later extension name** wins (Z > A)

**Example:**
```
Core:     code/principles.md → Core version used
aaa-pack: code/principles.md → Ignored (core wins)
zzz-pack: code/principles.md → Ignored (core wins)

No core version:
aaa-pack: code/subtypes/mobile.md → Ignored
zzz-pack: code/subtypes/mobile.md → Used (zzz > aaa)
```

### Provenance Tracking

The source of each opinion is tracked and displayed:

```bash
praxis opinions --list
# Output shows source in brackets:
code/principles.md             # Core (no bracket)
code/subtypes/mobile.md [mobile-pack]  # Extension
```

### Handling Conflicts

**If you want to override another extension:**
- Name your extension alphabetically after it (e.g., `zzz-override-pack`)

**If your extension is being overridden:**
- Check `praxis opinions --list` to see which extension won
- Consider renaming or coordinating with the other extension author

---

## Validation and Errors

### Valid Manifest Checklist

- [ ] `manifest_version` is "0.1"
- [ ] `name` matches directory name exactly
- [ ] YAML syntax is valid
- [ ] Opinion source paths exist in extension directory
- [ ] Opinion files have valid frontmatter
- [ ] Template source paths exist in extension directory (if contributing templates)
- [ ] Template files use valid variable substitution (if contributing templates)

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Unsupported manifest version '99.0'" | Wrong version number | Use "0.1" |
| "Manifest name 'foo' does not match extension directory name 'bar'" | Name mismatch | Rename directory or update manifest |
| "Invalid YAML in manifest" | Syntax error | Fix YAML syntax |
| "Contribution source not found" | Missing opinion file | Create the file at the specified path |
| "Template source not found: ..." | Missing template file | Create the template file or remove from manifest |
| "Missing required field: name" | No name field | Add `name: yourname` |

### Silent Skips

Extensions are silently skipped (no error) if:
- No `praxis-extension.yaml` found (backward compatibility)
- Extension not in `installed_extensions` list

---

## Testing Your Extension

### 1. Unit Testing

Create opinion files and verify frontmatter:

```bash
# Check YAML frontmatter is valid
python3 -c "import yaml; yaml.safe_load(open('opinions/code/subtypes/yourtype.md').read().split('---')[1])"
```

### 2. Integration Testing

Install in a test workspace:

```bash
# Create test workspace
export PRAXIS_HOME=/tmp/test-workspace
praxis workspace init

# Install your extension
ln -s /path/to/your/extension $PRAXIS_HOME/extensions/yourname

# Manually add to config (until CLI command available)
# Edit $PRAXIS_HOME/workspace-config.yaml and add 'yourname' to installed_extensions

# Test listing
praxis opinions --list

# Test resolution
cd /tmp/test-project
echo "domain: code\nstage: capture\nsubtype: yourtype\nprivacy_level: personal\nenvironment: Home" > praxis.yaml
praxis opinions
```

### 3. End-to-End Testing

Create a project using your subtype and verify opinions appear:

```bash
praxis new my-test-project --domain code --subtype yourtype
cd my-test-project
praxis opinions --prompt
# Should include your opinion content
```

---

## Distribution

### Repository Structure

Recommended structure for your extension repository:

```
praxis-extension-yourname/
├── README.md                     # Installation and usage instructions
├── praxis-extension.yaml         # Extension manifest
├── LICENSE                       # License for your extension
├── .gitignore
├── opinions/                     # Opinion contributions
│   └── code/
│       └── subtypes/
│           └── yourtype.md
└── templates/                    # Template contributions (optional)
    └── domain/
        └── code/
            └── subtype/
                └── yourtype/
                    ├── stage/
                    │   └── formalize.md
                    └── artifact/
                        └── sod.md
```

### Installation Instructions

Provide clear installation instructions in your README:

```markdown
## Installation

```bash
cd $PRAXIS_HOME/extensions
git clone https://github.com/your-org/praxis-extension-yourname.git yourname

# Add to workspace config
# (Manual until `praxis extensions add` supports custom repos)
```
```

### Versioning

- Use Git tags for releases: `v0.1.0`, `v0.2.0`, etc.
- Increment when manifest schema changes or opinions update
- Document breaking changes in CHANGELOG.md

---

## Security Considerations

### What Extensions CAN Do

- Provide opinion files (markdown with frontmatter)
- Contribute templates (Story 2)
- Contribute file-based audit checks (Story 3)

### What Extensions CANNOT Do

- Execute arbitrary code during discovery/loading
- Modify core Praxis behavior
- Access user credentials or sensitive data
- Perform network requests during loading

**Safety:** v0.1 only supports file-based contributions. No code execution.

### Trusted Sources

Only install extensions from trusted sources:
- Official Praxis extension registry (when available)
- Well-known GitHub organizations
- Extensions you've audited yourself

Never install extensions from untrusted sources or random repositories.

---

## Reference Extension

See `praxis-extension-mobile-pack` for a complete working example:

- Minimal manifest demonstrating schema
- Single opinion file with proper frontmatter
- README with installation and usage instructions

---

## Getting Help

- **Issues:** File issues on the praxis-ai repository
- **Discussions:** Use GitHub Discussions for questions
- **Examples:** Browse official extensions for patterns

---

## Roadmap

### Current (v0.1)

- ✅ Opinion contributions
- ✅ Template contributions (Story 2)
- ❌ Audit contributions (Story 3)

### Coming Soon

- Audit contributions (Story 3)
- `praxis extensions verify` command
- Extension dependency resolution (if needed)

### v1.0 Criteria

- 2 first-party extension packs shipped using API
- Schema stabilized based on real-world usage
- Breaking changes documented and migrated
