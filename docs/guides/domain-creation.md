# Domain Creation Guide

This guide explains how to create custom domains in Praxis to extend the framework beyond the built-in domains (Code, Create, Write, Observe, Learn).

## Overview

Praxis allows you to define custom domains that fit your specific workflow patterns. Custom domains are stored in your workspace and can be used in any project just like built-in domains.

## Quick Start

### Creating a Domain

Use the interactive domain creation command:

```bash
praxis domain create
```

This will guide you through:
1. **Template Selection** - Choose from predefined templates or create custom
2. **Domain Configuration** - Define characteristics and behavior
3. **AI Permissions** - Set AI operation constraints
4. **Subtypes** - Define domain-specific subtypes

### Predefined Templates

Praxis provides several opinionated domain templates:

#### Research Domain
- **Purpose:** Academic and exploratory investigation
- **Formalize Artifact:** Research Brief (`docs/research-brief.md`)
- **Default Privacy:** Personal
- **Subtypes:** academic, market, user, technical, competitive
- **AI Permissions:** Suggest ✓, Complete ✓, Generate (ask), Transform (ask)

#### Design Domain
- **Purpose:** Product and system design work
- **Formalize Artifact:** Design Brief (`docs/design-brief.md`)
- **Default Privacy:** Personal
- **Subtypes:** ux, ui, system, service, product
- **AI Permissions:** Suggest ✓, Complete ✓, Generate ✓, Transform ✓

#### Data Domain
- **Purpose:** Data analysis and modeling work
- **Formalize Artifact:** Data Analysis Plan (`docs/analysis-plan.md`)
- **Default Privacy:** Confidential
- **Subtypes:** analysis, modeling, visualization, pipeline, quality
- **AI Permissions:** Suggest ✓, Complete (ask), Generate (ask), Transform (ask), Execute (ask)

#### Custom Domain
- **Purpose:** Define your own domain from scratch
- Fully customizable through guided Q&A

## Domain Specification

Custom domains are defined in YAML format with the following structure:

```yaml
# Domain identity
name: research                    # Lowercase, alphanumeric, dashes
display_name: Research            # Human-readable name
description: Academic and exploratory investigation

# Lifecycle configuration
formalize_artifact_name: Research Brief
formalize_artifact_path: docs/research-brief.md
allowed_stages:
  - capture
  - sense
  - explore
  - shape
  - formalize
  - commit
  - execute
  - sustain
  - close

# Privacy and security
default_privacy: personal

# AI permissions
ai_permissions:
  suggest: allowed
  complete: allowed
  generate: ask
  transform: ask
  execute: blocked

# Subtypes
subtypes:
  - academic
  - market
  - user
  - technical
  - competitive

# Metadata
author: username
version: "1.0"
created_at: "2026-01-05T12:00:00Z"
```

## Managing Domains

### List Domains

View all available domains (built-in and custom):

```bash
praxis domain list
```

Output:
```
Built-in Domains:
  • code
  • create
  • write
  • observe
  • learn

Custom Domains:
  • research - Academic and exploratory investigation
```

### Show Domain Details

View detailed information about a custom domain:

```bash
praxis domain show research
```

Output:
```
Domain: Research (research)
  Description: Academic and exploratory investigation
  Version: 1.0
  Author: username
  Created: 2026-01-05T12:00:00Z

Formalize Artifact: Research Brief
  Path: docs/research-brief.md

Default Privacy: personal

AI Permissions:
  suggest      → allowed
  complete     → allowed
  generate     → ask
  transform    → ask
  execute      → blocked

Subtypes: academic, market, user, technical, competitive
```

### JSON Output

All commands support `--json` for machine-readable output:

```bash
praxis domain list --json
praxis domain show research --json
```

## Using Custom Domains

Once created, custom domains can be used in projects:

```bash
# Create a new project with custom domain
praxis new my-research-project --domain research --privacy personal
```

**Note:** Integration with `praxis new` and `praxis init` requires workspace setup. See [Integration](#integration) section below.

## Storage Location

Custom domain specifications are stored in:

```
$PRAXIS_HOME/domains/
  ├── research.yaml
  ├── design.yaml
  └── data.yaml
```

Each domain is stored as a YAML file named `{domain-name}.yaml`.

## Domain Characteristics

### Formalize Artifact

Domains can optionally require a formalize artifact (equivalent to SOD for Code domain):

- **Name:** Human-readable artifact name (e.g., "Research Brief")
- **Path:** Must be in `docs/` directory and use `.md` extension
- **Purpose:** Locks intent and boundaries before execution stage

If a domain doesn't require formalization (like Observe), leave these fields empty.

### AI Permissions

Control AI behavior per operation:

| Operation | Description | Values |
|-----------|-------------|--------|
| suggest | AI can suggest code/content | allowed, ask, blocked |
| complete | AI can complete partial work | allowed, ask, blocked |
| generate | AI can generate new content | allowed, ask, blocked |
| transform | AI can transform existing content | allowed, ask, blocked |
| execute | AI can execute code/commands | allowed, ask, blocked |

**Permission Values:**
- `allowed` - AI can proceed without asking
- `ask` - AI must ask for permission first
- `blocked` - AI cannot perform this operation

### Subtypes

Subtypes provide domain-specific categorization:

- Must be lowercase, alphanumeric, with dashes/underscores
- Used for opinion resolution and template selection
- Enable fine-grained workflow customization

### Privacy Defaults

Set a sensible default privacy level for new projects in this domain:

- `public` - Open source, publicly accessible
- `public-trusted` - Public but with collaborator access control
- `personal` - Private, personal use
- `confidential` - Sensitive information
- `restricted` - Highly restricted access

## Integration

### Workspace Setup

Custom domains require a Praxis workspace:

```bash
# Set workspace location
export PRAXIS_HOME="$HOME/praxis-workspace"

# Initialize workspace
praxis workspace init
```

### Validation

Domain specifications are validated on creation:

- Name format (lowercase, alphanumeric, dashes)
- Artifact path format (`docs/*.md`)
- AI permission values
- Privacy level values

### Extension Model

Custom domains complement the extension system:

- **Extensions:** Add opinions, templates, audits for existing domains
- **Custom Domains:** Create entirely new domain categories

Both can be combined: create a custom domain, then add extensions for it.

## Best Practices

### Choosing Between Extension and Custom Domain

**Use an Extension when:**
- Adding specialized guidance to an existing domain
- Contributing subtype-specific templates
- Sharing domain-specific audit checks

**Use a Custom Domain when:**
- Defining a fundamentally different work category
- Need different lifecycle artifact requirements
- Require unique AI permission constraints

### Domain Naming

- Keep names short and descriptive (e.g., `research`, `design`, `data`)
- Use domain-specific terminology familiar to practitioners
- Avoid generic terms that overlap with built-in domains

### AI Permissions

Consider your domain's characteristics:

- **Creative domains:** Allow generate/transform for exploration
- **Analytical domains:** Require asks for generation (citation, accuracy)
- **Production domains:** Block execution unless explicitly safe

### Privacy Defaults

Choose defaults based on typical work in the domain:

- **Research:** Personal (working notes, drafts)
- **Design:** Personal (explorations before sharing)
- **Data:** Confidential (often contains sensitive information)

## Limitations

### Current Limitations

1. **No validation integration** - Custom domains don't yet participate in `praxis validate`
2. **No init integration** - `praxis new` doesn't yet support custom domains
3. **No opinion resolution** - Custom domains don't yet trigger opinion loading

These integrations are planned for future releases.

### Workarounds

Until full integration is available:

1. Create domain specification for documentation
2. Use extension system for opinions/templates
3. Manually reference domain characteristics in project docs

## Examples

### Example 1: Product Management Domain

```yaml
name: product
display_name: Product Management
description: Product strategy and roadmap planning
formalize_artifact_name: Product Requirements Document
formalize_artifact_path: docs/prd.md
default_privacy: confidential
ai_permissions:
  suggest: allowed
  complete: ask
  generate: ask
  transform: ask
  execute: blocked
subtypes:
  - strategy
  - roadmap
  - feature
  - metric
  - experiment
```

### Example 2: Infrastructure Domain

```yaml
name: infra
display_name: Infrastructure
description: Cloud and systems infrastructure
formalize_artifact_name: Infrastructure Design
formalize_artifact_path: docs/infrastructure-design.md
default_privacy: confidential
ai_permissions:
  suggest: allowed
  complete: ask
  generate: ask
  transform: ask
  execute: ask
subtypes:
  - cloud
  - network
  - security
  - monitoring
  - automation
```

### Example 3: Education Domain

```yaml
name: education
display_name: Education
description: Course and training material development
formalize_artifact_name: Course Outline
formalize_artifact_path: docs/course-outline.md
default_privacy: personal
ai_permissions:
  suggest: allowed
  complete: allowed
  generate: allowed
  transform: allowed
  execute: blocked
subtypes:
  - course
  - tutorial
  - workshop
  - assessment
  - curriculum
```

## Troubleshooting

### Domain Creation Fails

**Error:** `PRAXIS_HOME not set and --workspace not provided`

**Solution:** Set up workspace first:
```bash
export PRAXIS_HOME="$HOME/praxis-workspace"
praxis workspace init
```

### Invalid Domain Name

**Error:** Domain name validation failed

**Solution:** Ensure name is:
- Lowercase only
- Starts with a letter
- Contains only letters, numbers, and dashes

### Domain Already Exists

When creating a domain that already exists, you'll be prompted to overwrite. Choose:
- **Yes:** Replace existing specification
- **No:** Cancel creation (keeps existing spec)

## References

- [Extension Authoring Guide](extension-authoring.md) - Create extensions for domains
- [Workspace Guide](user-guide.md#workspace) - Workspace setup and management
- [Domain Specifications](../core/spec/domains.md) - Built-in domain definitions
