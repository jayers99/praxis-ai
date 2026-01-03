# Handoff: Refactor Praxis Roles Structure — COMPLETED

> **Status:** This refactoring was completed. Retained for historical reference.

## Objective
Refactor the praxis-ai repository to adopt the new Praxis Roles structure.

## Target structure
- praxis-ai/core/roles/
- praxis-ai/handoff/
- praxis-ai/research/

## Steps
1. Create directories if missing
2. Move existing role markdown into core/roles/definitions
3. Create anchor READMEs
4. Update references and links
5. Validate no semantic changes

## Acceptance criteria
- No broken links
- Core definitions unchanged
- Research separated from core