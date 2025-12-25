# ai-guards brain dump

**Version:** v0.1

## 1. Research Questions (understand the landscape first)

- How does CLAUDE.md work today? What are best practices?
- What does `/init` actually do? How does it relate to what we're doing here?
- When should Claude be allowed to edit CLAUDE.md? (currently: on /init, or when asked)
- What are experts saying about AI memory/context management?
- How do other AI tools handle this? (Copilot instructions, Gemini context, Cursor rules)
- What's the constraint envelope? What's possible across all AI vendors?

## 2. Constraints / Reality Checks (what we can't change)

- Claude Code reads CLAUDE.md (and ~/.claude/CLAUDE.md) automatically
- Copilot reads .github/copilot-instructions.md
- Cursor reads .cursor/rules/ or .cursorrules
- We can't change how these tools find their instructions
- We CAN control what content those files contain
- Rendering/generation must happen before AI session starts

### Performance / Size Limits

- If guards compose, how big can the rendered output get?
- Do AI tools have token limits for instruction files?
- What's the practical maximum before instructions get ignored or truncated?

### Secrets / Credentials

- Work environment might reference internal URLs, API endpoints
- How to handle sensitive info in guards?
- Should guards ever contain secrets? Or always reference external sources?

## 3. Dimensions (variables that affect the design)

### AI Vendor (priority order)

1. Claude Code (CLAUDE.md, ~/.claude/CLAUDE.md)
2. GitHub Copilot (.github/copilot-instructions.md)
3. Google Antigravity / Gemini (instruction format TBD)
4. Cursor (.cursor/rules/, .cursorrules) — lower priority, don't let it drive design

### Scope

- User-level (applies to all my projects)
- Project-level (applies to this repo)
- Session-level (temporary overrides?)

### Domain (what kind of work)

- code
- create
- write
- observe
- learn

### Privacy Level

- public
- public-trusted
- personal
- confidential
- restricted

### Environment

- home (personal tools, relaxed constraints)
- work (corporate tools, compliance, stricter privacy)

## 4. Dimension Interactions (how dimensions couple)

### Privacy × Environment

- Work environment might *force* certain privacy levels
- Can home environment use "restricted" privacy? Or does restricted imply work?
- Who wins: user's environment setting or project's privacy requirement?

### Domain × Scope

- Non-code domains (write, create) have different concerns than code
- What does a guard look like for `write` domain? `create` domain?
- Are domain guards always project-level, or can user have domain preferences?

## 5. Guard Content & Structure (what goes IN a guard)

### Anatomy of a Guard

- Is it prose instructions? Structured YAML? A mix?
- What sections does a guard have?
- How granular? One big file vs many small focused guards?

### Additive vs Negative Guards

- Everything so far is additive ("do X")
- What about "never do X"?
- What about "ignore this user preference for this project"?
- Can project guards subtract from user guards?

## 6. Inheritance / Composition Model

### How Layers Combine

- Override? Merge? Append?
- Precedence: user > project? project > user? Depends on the property?
- Can a project force constraints the user can't override? (e.g., "this is a restricted project")

### Conflict Resolution

- When user guard says "use tabs" and project guard says "use spaces", who wins?
- Explicit conflict resolution rules vs implicit precedence?
- Should conflicts be errors that block rendering?

## 7. File Structure Options

### Option A: Separate files per AI vendor

```
~/.claude/CLAUDE.md
~/.github/copilot-instructions.md
project/CLAUDE.md
project/.github/copilot-instructions.md
```

Problem: Duplication, drift between vendors

### Option B: Single source, rendered outputs

```
~/.ai-guards/
  core.md           # Shared reasoning, style, preferences
  env/home.md       # Home environment specifics
  env/work.md       # Work environment specifics
  tools.md          # Tool mappings per environment

project/praxis/
  ai-guards/
    domain.md       # Domain-specific guards

# Rendered outputs (generated, maybe .gitignored)
project/CLAUDE.md
project/.github/copilot-instructions.md
```

Benefit: Single source of truth, vendor-specific translation

### Option C: Hybrid

User-level is rendered, project-level is manual but inherits user context

### What should be fast/targeted?

- Different CLAUDE.md per domain? (code vs write vs create)
- Load only relevant opinions based on praxis.yaml domain?
- Keep base instructions minimal, load extensions on demand?

## 8. User Stories (how people use this)

### New user setup (bootstrap problem)

1. User installs praxis CLI (or just creates ~/.ai-guards/)
2. Runs `praxis guards init` or manually creates core.md
3. Sets environment (home/work) — maybe auto-detected?
4. Guards are ready for any project

Questions:
- How does a brand new user get started?
- Empty guards? Sensible defaults? Interactive setup?
- Starter templates?

### New project setup

1. User runs `praxis init` in project
2. Creates praxis.yaml with domain, privacy
3. Domain-specific guards loaded from opinions
4. CLAUDE.md rendered from user + project guards

### Switching environments

1. User changes from home to work (how? env var? explicit command?)
2. Tool mappings change (personal AWS → corporate AWS)
3. Privacy constraints tighten
4. CLAUDE.md re-rendered with work overlay

### Learning something new (back-propagation)

1. While working on project, discover a pattern that should be universal
2. Elevate it: "this guard should be in my user profile, not just this project"
3. Move guard from project to user level
4. Other projects automatically benefit

Questions:
- Is this a CLI feature (`praxis guards elevate`)?
- Or a manual process?

### Multi-AI workflow

1. User has Claude Code and Copilot both active
2. Both read from same source guards
3. Each gets vendor-appropriate rendered file
4. Behavior is consistent despite different instruction formats

### Migration from existing setup

- People have existing CLAUDE.md files
- How do they adopt this system without starting over?
- Import existing? Diff and merge? Start fresh?

## 9. Validation & Debugging

### Validation / Linting

- What would `praxis guards validate` check?
- Syntax errors? Missing required sections?
- Circular dependencies between guards?
- Size limits exceeded?

### Testing Guards

- How do you know guards work?
- Can you test a guard before deploying it?
- Example-based testing? "Given this guard, expect this behavior"?

### Debugging

- When AI behaves unexpectedly, how to trace which guard caused it?
- Rendered output should show provenance? (this section came from user/core.md)
- Diff between expected and actual behavior?

## 10. Open Threads (unresolved questions)

- Is "guards" the right term? Alternatives: rules, directives, context, persona
- How does this relate to MCP servers? (Claude's tool/context extension mechanism)
- Should guards be versioned? (guard v1 vs v2)

---

## Appendix: Original raw notes (preserved)

- understand how claude.md works and best practices
- understand what /init does
- understand if and when i should allow claude to edit claude.md
- collect the best ideas of experts in the field on how to use AI memory
- i want things to be fast and targeted to each domain
  -- should i have a different project claude.md file for each domain. i think so
- the best possible base user profile claude.md (~/.claude/CLAUDE.md)
- how should user and project claude.md related and function
- document our constraints of what is possible to have what we come up with work across all these AI if possible
  -- claude
  -- copilot
  -- gemini
- capture all the dimensions that would affect the design
  -- my current dimensions i can think of
  --- AI vendor
  ---- claude
  ---- copilot
  ---- gemini
  --- project vs user
  --- domain
  ---- code
  ---- create
  ---- write
  ---- observe
  ---- learn
  --- privacy level
  ---- public
  ---- public-trusted
  ---- personal
  ---- confidential
  ---- restricted
  --- environment
  ---- home
  ---- work
- what should be shared across each of these dimension variables
- how to logically structure and store commonalities across dimension variables
- think about how to structure the files on disk to make this work best
- what would user stories look like of how to use the system at these stages
  -- brand new user profile creation
  -- new project creation
  -- back propagating new guards that should logically exist at another dimension or place
- can work through example user scenarios to hone thinking
