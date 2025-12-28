# MULTI_AGENT_PLAYBOOK.md

_Last updated: 2025-12-28_

## Goal
Run multiple AI-assisted workstreams in parallel with minimal collisions, predictable integration, and a clear audit trail.

## Principles
- **Isolation by default**: one worktree + branch per agent.
- **Single source of truth**: one authoritative spec (issue/ADR/SOD) per effort.
- **Explicit ownership**: define file/area boundaries up front.
- **One integration gate**: merges are centralized and deliberate.
- **Reproducibility**: every agent provides “how to run” and “what changed”.

---

## Recommended Topology

### Worktrees
Use Git worktrees (preferred) so each agent has:
- its own working directory
- its own branch
- shared object store for speed

### Branch naming
Use a consistent prefix:
- `agent/<name>/<topic>`
- examples: `agent/tester/authz`, `agent/feature/api-client`, `agent/docs/readme`

### Directory naming
Mirror branch intent:
- `../<repo>-agent-<name>-<topic>` (or similar)

---

## Operating Procedure

### 0) Prepare
1. Create/confirm the authoritative spec:
   - problem statement
   - acceptance criteria
   - non-goals
   - constraints (security/compliance/ops)
2. Define ownership boundaries (example):
   - Agent A: `src/api/**`
   - Agent B: `tests/**`
   - Agent C: `docs/**`
   - Lockfiles: single owner only
3. Identify shared resources to isolate:
   - ports, containers, DBs, caches, venvs

---

### 1) Create worktrees
Create one worktree per agent/branch.

Example:
```bash
git fetch --all --prune
git worktree add ../repo-agent-a -b agent/a/my-topic
git worktree add ../repo-agent-b -b agent/b/my-topic
```

---

### 2) Assign roles (recommended defaults)
- **Feature Agent**: implements code changes (bounded to defined paths).
- **Test Agent**: adds/updates unit/integration tests; improves coverage.
- **Docs/UX Agent**: updates README, runbooks, examples; confirms developer ergonomics.

Optional specialist roles:
- **Refactor Agent**: reduces complexity post-feature, minimal behavior change.
- **Security Agent**: threat modeling, validation, policy checks, SAST configs.

---

### 3) Agent execution rules
Each agent must:
- Work only within its ownership boundary.
- Avoid modifying shared lockfiles unless explicitly assigned.
- Run the project’s standard checks within its worktree:
  - formatter / linter
  - unit tests
  - any relevant integration tests
- Produce a handoff using `AGENT_HANDOFF_TEMPLATE.md`.

---

### 4) Integration & merge policy
- Integration is performed by a human (or a dedicated integration agent).
- Merge order should minimize conflicts:
  1. shared interfaces first
  2. feature changes next
  3. tests
  4. docs
- Prefer rebase/merge strategies consistent with your repo norms.

---

## Collision Avoidance Checklist
- [ ] Branch/worktree per agent
- [ ] Ownership boundaries published
- [ ] Lockfile owner assigned
- [ ] Ports isolated (e.g., `PORT=51xx`)
- [ ] Compose project names isolated (`COMPOSE_PROJECT_NAME=agent_x`)
- [ ] Per-worktree virtualenv
- [ ] Clear acceptance criteria
- [ ] Standard handoff produced

---

## “Definition of Done” for an agent branch
- [ ] Meets acceptance criteria within scope
- [ ] Tests updated/added and passing
- [ ] Lint/format checks passing
- [ ] Handoff completed (summary, files, run instructions, risks)
- [ ] No undocumented behavior changes
