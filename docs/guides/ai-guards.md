# AI Guards User Guide

## Overview

AI Guards provide a composable system for managing AI assistant instructions across multiple environments and projects. Guards compose from three levels:

1. **User-level guards** — Your personal preferences and tool mappings
2. **Environment overlays** — Work vs. home constraints
3. **Project-level guards** — Domain-specific workflows and guardrails

The system generates vendor-specific instruction files (CLAUDE.md, .github/copilot-instructions.md, GEMINI.md) from these sources.

## Quick Start

### 1. Set Up Project Guards

Create domain-specific guards for your project:

```bash
mkdir -p praxis/ai-guards
```

Create a guard file for your domain (e.g., `code.md`):

```markdown
# Code Domain Guards

Use TypeScript for all new code.
Write tests for all new functions.
Follow the repository's existing style guide.
```

### 2. Render Guard Files

Generate AI instruction files for all vendors:

```bash
praxis guards render --vendor all
```

Or for a specific vendor:

```bash
praxis guards render --vendor claude
```

### 3. Validate Composition

Check for issues in your guard composition:

```bash
praxis guards validate
```

### 4. List Active Guards

See which guards are being used:

```bash
praxis guards list
```

## File Structure

### Project-Level Guards

Location: `praxis/ai-guards/{domain}.md`

Example for a code project:

```
praxis/
  ai-guards/
    code.md          # Code domain guards
```

Example for a write project:

```
praxis/
  ai-guards/
    write.md         # Write domain guards
```

### User-Level Guards (Coming Soon)

Location: `~/.ai-guards/`

```
~/.ai-guards/
  core.md            # Universal preferences
  tools.md           # Tool mappings
  env.md             # Active environment selector
  env/
    home.md          # Home environment constraints
    work.md          # Work environment constraints
```

## Guard Composition Rules

Guards are composed in this order:

1. User core guards (if exists)
2. Environment overlay (home or work, if exists)
3. User tool mappings (if exists)
4. Project domain guards

Later guards can override earlier ones, but the composition is additive.

## Multi-Vendor Rendering

### Claude

**Output:** `CLAUDE.md`

Used by Claude Code and other Anthropic tools.

```bash
praxis guards render --vendor claude
```

### GitHub Copilot

**Output:** `.github/copilot-instructions.md`

Used by GitHub Copilot in the IDE.

```bash
praxis guards render --vendor copilot
```

### Gemini

**Output:** `GEMINI.md`

Used by Google's Gemini tools.

```bash
praxis guards render --vendor gemini
```

### All Vendors

Render for all vendors at once:

```bash
praxis guards render --vendor all
```

## Validation

The validate command checks for:

- Missing critical guards (warnings)
- Environment leakage (home paths in work environment)
- Empty guard files

```bash
praxis guards validate
```

Example output:

```
ℹ INFO: No user core guards found. Consider creating ~/.ai-guards/core.md

✓ Guard composition is valid
```

## Best Practices

### Keep Guards Focused

Each guard file should focus on its domain:

- **Code guards:** Architecture, testing, patterns
- **Write guards:** Style, tone, structure
- **Create guards:** Design principles, aesthetic goals

### Use Token Budget Wisely

AI models have limited instruction capacity (~150-200 instructions total). Keep guards:

- **Concise:** Short, declarative statements
- **Actionable:** Clear do's and don'ts
- **Prioritized:** Most important rules first

### Avoid Duplication

Don't repeat information across guard levels. Use:

- **User core:** Universal preferences
- **Project guards:** Project-specific requirements

### Environment Separation

Keep environment-specific constraints in environment overlays, not in core guards or project guards.

## Example Guard Files

### Code Domain Guard

```markdown
# Code Domain Guards

## Architecture

Use hexagonal architecture:
- Domain: Pure business logic
- Application: Orchestration
- Infrastructure: External concerns

## Testing

Write tests for all new code:
- Unit tests for domain logic
- Integration tests for services
- BDD tests for user-facing features

## Style

Follow existing conventions:
- Use TypeScript for new code
- Run `poetry run ruff check` before committing
- Run `poetry run mypy` for type checking
```

### Write Domain Guard

```markdown
# Write Domain Guards

## Tone

Technical documentation should be:
- Clear and concise
- Example-driven
- Accessible to intermediate developers

## Structure

Follow this structure for guides:
1. Overview (what and why)
2. Quick Start
3. Detailed Reference
4. Examples

## Style

- Use active voice
- Short paragraphs (2-4 sentences)
- Code examples with explanations
```

## Troubleshooting

### "No guards found at any level"

You haven't created any guard files yet. Start by creating a project-level guard:

```bash
mkdir -p praxis/ai-guards
echo "# My Domain Guards" > praxis/ai-guards/code.md
```

### "Failed to load praxis.yaml"

Make sure you're in a Praxis project directory with a valid `praxis.yaml` file.

### Files not being created

Check file permissions and ensure the output directory is writable.

## Advanced Usage

### Dry Run

Preview what would be rendered without writing files:

```bash
praxis guards render --dry-run
```

### Custom Output Directory

Render guards to a different directory:

```bash
praxis guards render --output /path/to/output
```

## Next Steps

1. Create your first project guard file
2. Run `praxis guards render --vendor all`
3. Commit the generated files to your repository
4. Set up user-level guards for cross-project preferences (coming soon)

## Related Documentation

- [AI Guards Design](/home/runner/work/praxis-ai/praxis-ai/core/ai/ai-guards.md) — Technical design document
- [First Principles](/home/runner/work/praxis-ai/praxis-ai/research-library/ai-guards/first-principles.md) — Research on AI instruction limits
- [CLAUDE.md Guide](/home/runner/work/praxis-ai/praxis-ai/CLAUDE.md) — This repository's AI instructions
