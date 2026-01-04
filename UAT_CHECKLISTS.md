# UAT Instructions: Lifecycle Checklists as First-Class Artifacts

## Overview

This PR implements lifecycle checklists as first-class artifacts in the Praxis framework. Users can now see exactly what's required to complete their current stage and understand why validation gates are failing, with direct links to relevant checklists.

## What Changed

### 1. Checklist Artifacts Created

**9 Base Checklists** (one per lifecycle stage):
- `core/checklists/capture.md`
- `core/checklists/sense.md`
- `core/checklists/explore.md`
- `core/checklists/shape.md`
- `core/checklists/formalize.md`
- `core/checklists/commit.md`
- `core/checklists/execute.md`
- `core/checklists/sustain.md`
- `core/checklists/close.md`

**2 Domain Addenda** (domain-specific guidance):
- `core/checklists/formalize-code.md` — Code domain formalization (SOD creation)
- `core/checklists/sustain-code.md` — Code domain sustainment (maintenance, monitoring)

### 2. CLI Output Changes

**`praxis status` now includes checklist references:**

```
Checklist: core/checklists/formalize.md
           core/checklists/formalize-code.md
```

**`praxis validate` error messages now include checklist references:**

```
✗ [ERROR] Stage 'commit' requires formalization artifact at 'docs/sod.md', 
  but file not found. See checklist: core/checklists/formalize.md
```

### 3. Data Model Changes

**ProjectStatus model** now includes:
- `checklist_path: str | None` — Path to base checklist
- `checklist_addendum_path: str | None` — Path to domain-specific addendum (if exists)

## UAT Test Cases

### Test 1: Status Shows Base Checklist for Any Stage

```bash
cd /tmp && mkdir -p uat-checklist-1 && cd uat-checklist-1
cat > praxis.yaml << 'EOF'
domain: code
stage: formalize
privacy_level: personal
environment: Home
EOF

praxis status
```

**Expected:** Output includes `core/checklists/formalize.md` and `core/checklists/formalize-code.md`

### Test 2: Validate References Checklist on Gate Failure

```bash
cd /tmp && mkdir -p uat-checklist-2 && cd uat-checklist-2
cat > praxis.yaml << 'EOF'
domain: code
stage: commit
privacy_level: personal
environment: Home
EOF

praxis validate
```

**Expected:** Error message includes "See checklist: core/checklists/formalize.md"

### Test 3: All 9 Base Checklists Exist

```bash
ls -1 core/checklists/*.md
```

**Expected:** 11 total files (9 base + 2 domain addenda)

### Test 4: Automated Tests Pass

```bash
poetry run pytest tests/step_defs/test_checklists.py -v
```

**Expected:** All 6 checklist tests pass

## Success Criteria

- [x] All 9 lifecycle stages have base checklist files
- [x] Domain addenda exist for formalize-code and sustain-code
- [x] `praxis status` displays checklist references
- [x] `praxis validate` includes checklist references in error messages
- [x] All 6 new BDD tests passing
- [x] All 281 existing tests still passing
- [x] Documentation updated (CLAUDE.md, user-guide.md)
