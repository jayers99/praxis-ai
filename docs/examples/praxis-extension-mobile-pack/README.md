# Mobile Pack - Reference Extension for Praxis

This extension demonstrates the Plugin/Contribution API for Praxis.

## Overview

This extension adds mobile development opinions and audit checks to the Code domain, showing how third-party extensions can contribute domain-specific guidance and quality checks without modifying Praxis core.

## Structure

```
praxis-extension-mobile-pack/
├── README.md                        # This file
├── praxis-extension.yaml            # Extension manifest
└── opinions/                        # Opinion contributions
    └── code/
        └── subtypes/
            └── mobile/
                └── principles.md    # Mobile subtype principles
```

## Installation

If you have a Praxis workspace:

```bash
# Clone this repo into your workspace extensions directory
cd $PRAXIS_HOME/extensions
git clone https://github.com/your-org/praxis-extension-mobile-pack.git mobile-pack

# Add to workspace config
# (This would normally be done via `praxis extensions add mobile-pack`)
```

## Features

### 1. Opinion Contributions

The mobile opinions will automatically appear when:

**Listing opinions:**
```bash
praxis opinions --list
# Will show: subtypes/mobile/principles.md [mobile-pack]
```

**Resolving opinions for mobile projects:**
```bash
# In a project with subtype: mobile in praxis.yaml
praxis opinions
# Will include mobile/principles.md in the resolution chain
```

**AI context generation:**
```bash
praxis opinions --prompt
# Mobile opinions will be included in AI-ready context
```

### 2. Audit Contributions

The extension contributes mobile-specific audit checks that automatically run for code projects with `subtype: mobile`:

**Run audit checks:**
```bash
# In a mobile project
praxis audit
```

**Contributed checks:**
- `mobile_manifest_exists` - Validates mobile.json exists
- `mobile_source_directory` - Checks for src/mobile/ directory
- `native_bridge_documented` - Ensures native bridge is documented (formalize+)
- `platform_target_specified` - Validates platform targets in mobile.json (formalize+)

**Check details:**
- All checks apply to `domain: code` with `subtype: mobile`
- Some checks only apply at specific stages (e.g., formalize or later)
- Checks are prefixed with extension name for provenance (e.g., `mobile-pack:mobile_manifest_exists`)

## Manifest Structure

See `praxis-extension.yaml` for the manifest schema. Key sections:

### Opinion Contributions
```yaml
contributions:
  opinions:
    - source: opinions/code/subtypes/mobile/principles.md
      target: code/subtypes/mobile/principles.md
```

### Audit Contributions
```yaml
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

**Supported check types:**
- `file_exists` - Check if a file exists
- `dir_exists` - Check if a directory exists
- `file_contains` - Check if a file contains a regex pattern

**Optional fields:**
- `min_stage` - Minimum lifecycle stage for the check to apply
- `subtypes` - Filter by project subtypes (empty = all subtypes)

## Conflict Resolution

If multiple extensions (or core) contribute the same opinion file:

1. **Core takes precedence** over all extensions
2. **Alphabetically later extension names** take precedence over earlier ones
3. Provenance is tracked and displayed in `--list` output

For audit checks:
- Extensions are processed in alphabetical order
- Each extension's checks appear in the order defined in the manifest
- Check names are prefixed with extension name to avoid conflicts

## Contributing

This is a minimal reference extension. For real mobile development guidance, consider:

- Adding stage-specific mobile opinions (e.g., mobile/formalize.md)
- Adding more platform-specific audit checks (iOS, Android, React Native)
- Contributing mobile project templates (Story 2)

