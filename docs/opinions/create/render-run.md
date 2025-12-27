# Create ↔ Render Run Integration

This doc defines the **Create-domain contract** for using Render Run (Code domain) to execute image generation runs.

The intent is to keep ownership clean:

- Create projects own **prompt intent** (prompt slots, reference bundles, variants, desired outputs).
- Render Run owns **execution + traceability** (manifests, provider fan-out, artifact layout, reproducibility).

---

## What Create Provides

### MVP Input (Today): Markdown Idea Doc (Create-Owned)

Create provides a **Markdown document** that Render Run can later parse.

Key governance boundary:

- The **Create domain** owns this document type and is responsible for keeping it valid.
- Render Run should not “guess” structure from arbitrary prose.

#### Required fields (minimal contract)

Only two fields are required per idea:

- `idea_id`
- `prompt`

#### Minimal Markdown structure (recommended)

Each idea is a section with an ID in the heading and a fenced prompt block:

````md
## darin-001

```prompt
A detailed prompt for the image generator...
```
````

```

Recommended location inside a Create project:

- `praxis/docs/prompting/ideas.md`

### Future Input (Provider-Agnostic Payload)

Create should evolve toward a structured YAML/JSON payload using the prompt taxonomy:

- [prompt-taxonomy.md](prompt-taxonomy.md)

Render Run treats this payload as **data** (record, expand, execute, and archive), not as “opinions”.

---

## How Create Calls Render Run

Two common setups:

- **Local checkout / submodule** (good for experimentation)
- **Dependency** (good once versioning is stable)

### Recommended Invocation (Derived Output Path)

Create project calls `prepare` using `--domain create` and `--project <project-slug>`.

Render Run then writes into:

`<generated_root>/create/<project>/runs/<run_id>/`

Example (xmas-cards-2025):

`~/icloud/praxis-generated-content/create/xmas-cards-2025/runs/<timestamp>`

Example command (Create project repo, using Render Run as a local checkout/submodule):

- `poetry -C ../../code/render-run run render-run prepare --in praxis/docs/prompting/ideas.md --domain create --project xmas-cards-2025`

### Output Root Configuration

Render Run resolves `<generated_root>` by:

1. `PRAXIS_GENERATED_CONTENT_ROOT`
2. `~/.config/praxis/config.json` with `{ "generated_content_root": "..." }`
3. Default: `~/icloud/praxis-generated-content`

---

## What Render Run Produces

Inside a run folder, Create can expect (MVP):

- `manifest.json` (run metadata + items)
- `expanded_prompts.txt` (expanded prompts, one per line)

Future (when providers are active):

- `images/` (or provider-specific subfolders)
- Logs and provider job records (for retries + traceability)

---

## Feedback Loop Back Into Create

Create projects should record decisions **in the project repo** (not in the generated-content folder):

- Which variants are “winners”
- What prompt slot changes improved outcomes
- Which reference bundles worked best

A simple pattern is to keep a short “run review” note next to the prompting assets (project-local), and treat the generated run folder as a reproducible build artifact.
```
