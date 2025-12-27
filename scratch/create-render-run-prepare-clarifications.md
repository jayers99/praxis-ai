# Clarifications Needed: Create → Render Run `prepare` (Markdown Input)

This document captures the open questions that need to be decided to implement a deterministic, low-churn `create → render-run prepare` workflow.

Scope: **Create-domain Markdown input** → `render-run prepare` parses → writes a run folder + manifest.

---

## 1) Markdown Structure (Parsing Rules)

- **Idea boundary**: What denotes a single idea block?
  - Is it always a `## <idea_id>` heading?
  - Are other heading levels allowed for other content?
- **ID format**: What characters are allowed in `idea_id`?
  - Examples: `darin-001`, `darin_001`, `DARIN-001`, UUID
  - Do we enforce a regex? If yes, which?
- **Uniqueness**: Must `idea_id` be unique within the document?
- **Ordering**: Does ordering matter (e.g., stable order becomes `item.id`)?

---

## 2) Prompt Extraction (Canonical Format)

You’ll want one canonical prompt format to avoid ambiguity.

- **Canonical format choice**:

  - Option A: a `### prompt` section whose body is the prompt text
  - Option B: a fenced block, e.g.:

    ````md
    ## darin-001

    ```prompt
    <prompt text>
    ```
    ````

    ```

    ```

- **Multi-paragraph prompts**: are blank lines allowed inside a prompt?
- **Whitespace preservation**: does the prompt need exact whitespace preserved?
- **Edge cases**:
  - What if the prompt contains lines that look like headings?
  - What if the prompt contains fenced code blocks?

---

## 3) Minimal Contract vs References

The current MVP intent is **minimal**:

- Required per idea: `idea_id` + `prompt`

But the story also relies on reference images and “image 1 = Darin…” disambiguation.

Decide MVP behavior:

- Should `prepare` **ignore references entirely** for now?
- Or should `prepare` **record references** in the manifest (without using them yet)?

If references are recorded later:

- What is the Markdown format?
  - e.g., `### references` with a bullet list of relative paths
- What reference types exist?
  - likeness / objects / style / composition
- Are paths absolute or relative? Relative to what root?

---

## 4) Output Path Defaults (Run Directory Convention)

We have a run directory convention; implementation needs exact rules:

- Default convention:
  - `<generated_root>/create/<project>/runs/<run_id>/`
- How is `<project>` determined?
  - passed via `--project`?
  - derived from repo folder name?
  - read from Create `praxis.yaml`?
- How is `run_id` determined?
  - always timestamp?
  - allow user-provided semantic run names?

---

## 5) Manifest Contract (What `prepare` Emits)

Even with minimal inputs, define required vs optional manifest fields.

- Required fields?
  - `schema_version`, `created_at`, `out_dir`, `items[{idea_id,prompt}]` (or equivalent)
- Should it record traceability back to Create?
  - `source_doc_path` (absolute vs relative?)
  - `idea_heading` anchor (e.g., `## darin-001`) or just `idea_id`
- Stable ordering rules?

---

## 6) Providers / Services (What `prepare` Is Allowed To Know)

Your doc notes: `prepare` should not need secrets.

Decide how much provider info `prepare` can/should handle:

- `prepare` records **no providers** (providers selected only at `generate` time)
- OR `prepare` can record a **provider list** (strings only), but never touches credentials

---

## 7) Validation Ownership (Create Enforces Structure)

You want the Markdown document type to be Create-owned and Create-validated.

Clarify what that means operationally:

- Manual validation (template + checklist), or automated validation tooling?
- Minimum validation rules (suggested):
  - every idea has a valid `idea_id`
  - every idea has a non-empty prompt
  - idea IDs are unique
  - prompt length limits (optional)

---

## 8) Doc Consistency (Resolve Current Conflict)

Right now, different places show different formats:

- Some docs show fenced ```prompt blocks
- Some show a `### prompt` section

Pick one canonical format and update the docs to match.

---

## The 3 Decisions That Unblock Implementation Fastest

1. Prompt format: **fenced ```prompt blocks** or **`### prompt` section**?
2. References: recorded in `prepare` manifest now, or ignored for MVP?
3. Default derivation: how to determine `<project>` and `run_id`?
