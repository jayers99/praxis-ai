# Mobile Pack - Reference Extension for Praxis

This extension demonstrates the Plugin/Contribution API for Praxis.

## Overview

This extension adds mobile development opinions to the Code domain, showing how third-party extensions can contribute domain-specific guidance without modifying Praxis core.

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

## Usage

Once installed, the mobile opinions will automatically appear when:

1. **Listing opinions:**
   ```bash
   praxis opinions --list
   # Will show: subtypes/mobile/principles.md [mobile-pack]
   ```

2. **Resolving opinions for mobile projects:**
   ```bash
   # In a project with subtype: mobile in praxis.yaml
   praxis opinions
   # Will include mobile/principles.md in the resolution chain
   ```

3. **AI context generation:**
   ```bash
   praxis opinions --prompt
   # Mobile opinions will be included in AI-ready context
   ```

## Manifest Structure

See `praxis-extension.yaml` for the manifest schema. Key points:

- `manifest_version`: Must be a supported version (currently "0.1")
- `name`: Must match the directory name
- `contributions.opinions`: List of opinion files to contribute
  - `source`: Path in extension directory
  - `target`: Path in opinions tree

## Conflict Resolution

If multiple extensions (or core) contribute the same opinion file:

1. **Core takes precedence** over all extensions
2. **Alphabetically later extension names** take precedence over earlier ones
3. Provenance is tracked and displayed in `--list` output

## Contributing

This is a minimal reference extension. For real mobile development guidance, consider:

- Adding stage-specific mobile opinions (e.g., mobile/formalize.md)
- Contributing mobile-specific audit checks (Story 3)
- Adding mobile project templates (Story 2)
