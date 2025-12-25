# AI Guards

Design documentation for policy-driven AI assistant configuration.

## Contents

- **models/** — User instruction file templates (CLAUDE.md patterns)
- **research/** — Capture notes, braindumps, and design exploration

## Tips & Tricks

### Reloading CLAUDE.md After /clear

`/clear` resets conversation history but doesn't reload configuration files. To reload your user instructions without restarting the session:

```text
Read ~/.claude/CLAUDE.md and apply it
```

This manually re-injects your preferences into the current conversation.

**When you need a full reload:** Restart Claude Code entirely. This reloads both user-level (`~/.claude/CLAUDE.md`) and project-level (`CLAUDE.md`) instructions.
