# Agent Prompt: Migrate Praxis Roles to praxis-ai
**Handoff Artifact (v1.1)**

## Use
Copy/paste this entire prompt into your agentic coding tool.

---

You are an execution agent. Your task is to migrate the Praxis Roles subsystem from `bench/inbox/praxis-roles/` to `praxis-ai/`.

### Source Structure (current)
```
bench/inbox/praxis-roles/
├── README.md
├── core-roles-index.md
├── core-roles-README.md
├── authority-and-change-control.md
├── lifecycle-matrix.md
├── invocation-syntax.md
├── kickback-rubrics.md
├── system-prompt-bundle.md
├── roles/
│   └── [00-11 role definitions]
├── research-README.md
├── research-rationale-roles-core-research-handoff.md
├── decision-roles-vs-hats.md
├── example-role-flow.md
├── handoff-README.md
├── handoff-refactor-praxis-roles.md
└── handoff-agent-refactor-prompt.md
```

### Target Structure
```
praxis-ai/
├── core/
│   └── roles/
│       ├── index.md                    # from core-roles-index.md
│       ├── README.md                   # from core-roles-README.md
│       ├── lifecycle-matrix.md
│       ├── invocation-syntax.md
│       ├── kickback-rubrics.md
│       ├── system-prompt-bundle.md
│       └── definitions/
│           └── [all role .md files]
├── research/
│   ├── README.md                       # from research-README.md
│   ├── rationale-roles-core-research-handoff.md
│   ├── decision-roles-vs-hats.md
│   └── example-role-flow.md
├── handoff/
│   ├── README.md                       # from handoff-README.md
│   ├── refactor-praxis-roles.md
│   └── agent-refactor-prompt.md
└── authority-and-change-control.md
```

### Constraints
- Preserve semantics: role content must not change meaning during moves.
- Update internal links to new paths.
- Use git mv where possible to preserve history.
- If any file name collisions occur, propose deterministic renames.

### Implementation Steps
1. Create target directories if missing.
2. Move governance docs to `core/roles/`.
3. Move role definitions to `core/roles/definitions/`.
4. Move research docs to `research/`.
5. Move handoff docs to `handoff/`.
6. Move top-level `authority-and-change-control.md` to `praxis-ai/`.
7. Update all internal links (grep for old paths).
8. Validate no broken links.

### Acceptance Criteria
- `git status` clean after changes (except intended edits)
- No broken markdown links (validate by grep-based verification)
- All role definitions discoverable under `core/roles/definitions/`
- README files clearly state authority boundaries
- No semantic changes to role definitions

### Deliverables
- A PR (or commit set) implementing the migration.
- A summary table: old path → new path.
- A verification log (commands run + results).

---
