# Personal Claude Code Instructions

I value directness, minimal changes, and working code over explanations.

## Communication Preferences

- Be direct and concise
- Skip unnecessary preamble
- Provide working code, not explanations of what you could do
- Ask clarifying questions when requirements are ambiguous

## Control Signals

- **"Stop"** = halt immediately, wait for instructions
- **"Pause"** = checkpoint progress, summarize state, wait
- **"Clarify"** = I need to understand before you proceed
- Use Plan Mode for non-trivial implementations

## Workflow

- Read before modifying — understand existing content first
- Make minimal changes to accomplish the task

## Tools & Environment

- macOS environment
- Use project-specified tooling over personal preferences

## Boundaries

- Keep solutions simple and focused on the current problem
- Scope changes to the task at hand
- Mark incomplete or placeholder content clearly

## Domain-Specific Rules

If this project has a praxis.yaml, check its domain field and apply the corresponding rules:
- domain: code → @~/.claude/rules/code.md
- domain: write → @~/.claude/rules/write.md
- domain: create → @~/.claude/rules/create.md
