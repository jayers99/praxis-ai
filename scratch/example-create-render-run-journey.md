# Example Journey: Create → Render Run (Draft)

This doc is a cleaned-up version of the brain dump in `scratch/example-create-render-run-journey.txt`.

Goal: capture a plausible end-to-end user journey where a Create-domain artifact (ideas + references) becomes a browsable filesystem run directory containing generated images.

---

## 1) Starting Point: Create Project Generates Ideas

- Source input document (example):
  - `examples/create/xmas-cards-2025/praxis/docs/recipients/darin-card-ideas-opus-4.5.md`
- This document contains a list of Christmas card ideas for a recipient (Darin).

Outcome: we have **human-readable ideas**, but not yet a machine-executable package.

---

## 2) Create Domain Extends the Idea Doc With References

We need to identify all images required to execute the ideas.

### 2.1 Shared (Global) Reference Bundles

Some reference images are reusable across many ideas, so Create should define them once “at the top” as shared assets.

Examples of shared references:

- Likeness references (people):
  - Darin
  - Veronica
  - Milo
  - Izzy
  - Grandkids
  - (etc.)
- Object references (anchors): specific objects that should appear in multiple ideas
- Composition/style references: references for layout / aesthetic / medium

Key governance boundary:

- This work belongs in the **Create domain**, not inside Render Run.
- The Create user does the curation + mapping of references to ideas.

### 2.2 Mapping References to Each Idea

For each idea, the user associates:

- Which likeness references apply
- Which object references apply
- Which composition/style references apply

This is intentional work the user performs to ensure correct execution.

---

## 3) Create Produces a Render Run Input Package

Once the user has created the mapping, the computer can assemble the “package” for Render Run.

### 3.1 What Render Run Needs Per Idea (Minimal Contract)

For the MVP, keep the required contract extremely small:

- `idea_id`: a stable unique identifier
- `prompt`: the exact generated prompt text to execute

Other metadata can exist in the Create doc, but should be treated as optional until formalized.

### 3.2 Image Naming / Disambiguation

Within a single idea, multiple reference images may be provided. To reduce confusion:

- Each reference image should have a clear name/role, e.g.
  - “image 1 = Darin likeness reference”
  - “image 2 = Veronica likeness reference”
  - “image 3 = Milo likeness reference”
  - “image X = composition reference”

The prompt should reference the images using their names/roles so the model (and human reviewer) can keep them straight.

---

## 4) Render Run `prepare`: Produces a Machine-Readable Manifest

Render Run `prepare` should read the Create-produced payload and output a structured manifest suitable for generation.

Render Run `prepare` needs to know:

- Where outputs will be written (run directory)
- Which idea corresponds to which prompt and reference images
- Enough metadata to tie results back to the original Create doc

### 4.1 Input Document Type: Markdown (Create-Owned)

Decision direction:

- The Create domain produces a **Markdown** document with an enforceable structure.
- Create is responsible for validating and enforcing that structure.
- Render Run should rely on that structure (not attempt to interpret arbitrary prose).

Minimal structure example:

```
## darin-001

### prompt
<prompt text>
```

## 5) Config and Output Location Concerns

Render Run needs user-level configuration for:

- API keys / service credentials
- default output root (where runs are written)
- service list to use

Desired behavior:

- A default config file controls:
  - service credentials
  - default output directory
- CLI flags can override:
  - output directory (write somewhere else for a specific run)
  - possibly which API key / profile is used
- Service list to use

render-run prepare should not need service secretes and those should not be stored

---

## 6) What Might Be Missing From the Create → Render Run Contract?

Initial payload proposal (minimal contract) is:

- `idea_id`
- `prompt`

Potential missing dimensions to consider (not decided here):

- Variants (loose/balanced/strict)
- Output controls (aspect ratio / orientation / size)
- Provider selection (gcloud first; others later)
- Number of images per variant/provider
- Traceability links back to:
  - source idea doc path
  - section heading / anchor within that doc

---

## 7) Summary (Contract Direction)

The Create domain should:

- curate and store reference bundles
- map references to ideas
- produce a structured package that Render Run can execute

Render Run should:

- accept the structured package
- write a run folder with a manifest that is machine-readable
- generate artifacts into a browsable directory layout

```

```
