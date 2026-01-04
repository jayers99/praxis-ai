# Example: Technical Article — "Testing in Production: A Pragmatic Approach"

**Domain:** Write  
**Subtype:** technical  
**Final Stage:** Sustain

---

## What you'll learn

This example demonstrates a complete lifecycle for a technical article project:

- How to use a **Writing Brief** (`docs/brief.md`) to formalize your thesis, audience, and scope before drafting
- How to progress through stages: Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain
- How stage artifacts evolve from raw notes to polished output
- How to use Praxis governance to maintain intent while writing

---

## Prerequisites

- Basic familiarity with the Praxis lifecycle (see `docs/guides/user-guide.md`)
- Understanding of the Write domain (see `core/spec/domains.md`)

---

## Project context

This example shows the development of a technical article arguing that "testing in production" is a pragmatic necessity for modern systems, not a reckless anti-pattern. The article targets engineering managers and technical leads evaluating quality practices.

---

## Step-by-step walkthrough

### 1. Capture (Raw inputs)

**File:** `01-capture-notes.md`

Initial brainstorming and collected thoughts. No structure yet—just capturing the raw idea:
- Core thesis roughed out
- Links to supporting articles
- Personal experiences noted

### 2. Sense (Understanding emerges)

**File:** `02-sense-synthesis.md`

Synthesized the raw captures into a coherent problem statement:
- Identified the audience (engineering managers)
- Clarified the core argument (TiP is pragmatic, not reckless)
- Tagged key themes (observability, risk management, progressive delivery)

### 3. Explore (Generate possibilities)

**File:** `03-explore-angles.md`

Explored different angles for the article:
- Historical perspective (how we got here)
- Technical deep-dive (techniques and tools)
- **Selected:** Pragmatic argument for managers (risk vs. value tradeoff)

### 4. Shape (Converge on structure)

**File:** `04-shape-outline.md`

Roughed out article structure:
- Hook: "If you're not testing in prod, you're not testing what users experience"
- 3 main sections: Why TiP is necessary, How to do it safely, When to avoid it
- Conclusion: Maturity model for adopting TiP practices

### 5. Formalize (Lock scope and intent)

**File:** `docs/brief.md` ✅ **Required artifact**

Created the Writing Brief, which locks:
- Thesis: TiP is a pragmatic necessity when done with proper guardrails
- Audience: Engineering managers and tech leads
- Scope: 1500-2000 words, authoritative but accessible tone
- Success criteria: Published on company blog, no factual corrections needed

**This is the hard boundary.** After this point, iteration is refinement, not discovery.

### 6. Commit (Decide to proceed)

**File:** `06-commit-decision.md`

Explicit commitment to write the article:
- Reviewed the brief for completeness
- Allocated 6 hours over 2 weeks
- Confirmed sources are available
- Greenlit for drafting

### 7. Execute (Write the article)

**Files:**
- `drafts/v1-first-draft.md` — Initial full draft following the outline
- `drafts/v2-revised.md` — Incorporated feedback, tightened argument
- `drafts/v3-final.md` — Final edits, polish, fact-checking complete

**Output:** `article-final.md` — The finished article ready for publication

### 8. Sustain (Maintain and update)

**File:** `08-sustain-updates.md`

Post-publication activities:
- Fixed typo in code example (no contract change → stays in Sustain)
- Added clarification based on reader feedback
- Tracked engagement metrics
- Considered follow-up article (new project → Close this, Capture the next)

---

## Lifecycle progression

```
Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain
   ↓         ↓        ↓        ↓         ↓          ↓         ↓         ↓
  notes   synthesis angles  outline   brief     commit    drafts   updates
```

**Key observation:** Formalize (the Writing Brief) is where the article's identity is locked. Before that, we're discovering what to write. After that, we're refining how well we write it.

---

## Files in this example

```
examples/write/technical-article/
├── README.md                      # This file
├── praxis.yaml                    # Project configuration
├── 01-capture-notes.md            # Raw brainstorming
├── 02-sense-synthesis.md          # Synthesized understanding
├── 03-explore-angles.md           # Explored alternatives
├── 04-shape-outline.md            # Converged structure
├── docs/
│   └── brief.md                   # Writing Brief (formalize artifact)
├── 06-commit-decision.md          # Commitment decision
├── drafts/
│   ├── v1-first-draft.md          # Initial draft
│   ├── v2-revised.md              # Revised draft
│   └── v3-final.md                # Final draft
├── article-final.md               # Published article
└── 08-sustain-updates.md          # Post-publication updates
```

---

## How to use this example

1. **Read through the files in order** (01 → 02 → 03 → ... → 08)
2. **Pay special attention to `docs/brief.md`** — This is the required formalize artifact for Write domain
3. **Notice the shift at Formalize** — Before: discovering what to write. After: refining the writing
4. **Try it yourself:**
   ```bash
   praxis new my-article --domain write --privacy public
   cd my-article
   # Follow the pattern demonstrated in this example
   praxis templates render --stage formalize  # Generates docs/brief.md
   ```

---

## Related resources

- **Write domain specification:** `core/spec/domains.md`
- **Lifecycle stages:** `core/spec/lifecycle.md`
- **Writing Brief template:** `src/praxis/templates/domain/write/artifact/brief.md`
- **User guide:** `docs/guides/user-guide.md`
