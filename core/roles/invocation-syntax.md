# Role Invocation Syntax
**Canonical Reference (v1.0)**

Purpose: Provide a minimal, explicit grammar for activating roles in prompts.

## Syntax

```
[ROLE: Research Librarian]
[PHASE: Explore]
[PRIMARY]
```

Optional modifiers:
- `[CONSULTED]`
- `[FORBIDDEN]`
- `[TIMEBOX: 30 minutes]`
- `[VERBOSITY: low|medium|high]`

## Rules
- Multiple PRIMARY roles are allowed per phase (see lifecycle-matrix.md for details).
- Forbidden roles may not be implicitly invoked.
- Phase must always be declared.

## Example

```
[ROLE: Red Team]
[PHASE: Shape]
[CONSULTED]
Challenge the proposed backlog ordering.
```

## Shorthand

For quick invocation, the following shorthand is acceptable:

```
You are the Product Owner role. Phase: Decide.
```

The formal syntax is preferred for agent-to-agent communication.
