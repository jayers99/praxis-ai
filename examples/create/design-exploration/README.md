# Example: Design Exploration — "Louie's New Year's Eve Party Poster"

**Domain:** Create  
**Subtype:** design  
**Final Stage:** Sustain

---

## What you'll learn

This example demonstrates a complete lifecycle for a creative design project:

- How to use a **Creative Brief** (`docs/brief.md`) to formalize your vision, constraints, and deliverables
- How to progress through stages with creative work: Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain
- How exploration artifacts (mood boards, sketches, iterations) evolve into final deliverables
- How to balance creative freedom with client requirements and deadlines

---

## Prerequisites

- Basic familiarity with the Praxis lifecycle (see `docs/guides/user-guide.md`)
- Understanding of the Create domain (see `core/spec/domains.md`)

---

## Project context

This example shows the design process for a New Year's Eve party poster for Louie's speakeasy-themed event. The poster must capture the vintage aesthetic, drive ticket sales, and be print-ready within a tight timeline.

**Deliverables:** 11x17 print poster + Instagram story variant

---

## Step-by-step walkthrough

### 1. Capture (Initial inputs)

**File:** `01-capture-inspiration.md`

Collected raw creative inputs:
- Client brief (venue = speakeasy, occasion = NYE party)
- Visual references (art deco posters, 1920s typography)
- Venue photos and existing brand assets
- Required copy (date, time, venue, ticket link)

### 2. Sense (Visual direction emerges)

**File:** `02-sense-moodboard.md`

Created mood board synthesizing inspirations:
- Color palette: Gold, black, deep burgundy
- Typography style: Art deco, geometric sans-serif
- Visual motifs: Champagne glasses, city skyline, geometric patterns
- Tone: Elegant, celebratory, mysterious

### 3. Explore (Generate visual options)

**Files in `explorations/`:**
- `exploration-01-classic-deco.md` — Traditional art deco approach
- `exploration-02-modern-minimal.md` — Minimalist geometric NYE
- `exploration-03-vintage-speakeasy.md` ✓ **SELECTED** — Vintage poster aesthetic

Explored three distinct visual directions, client selected vintage speakeasy approach.

### 4. Shape (Refine chosen direction)

**File:** `04-shape-composition.md`

Refined the selected direction:
- Layout: Centered composition with champagne toast focal point
- Typography hierarchy: Event name dominant, details secondary
- Visual elements: Venue skyline silhouette, art deco border
- Color application: Gold foil effect for headline, black background

### 5. Formalize (Lock creative vision)

**File:** `docs/brief.md` ✅ **Required artifact**

Created the Creative Brief, which locks:
- Creative Intent: Vintage speakeasy NYE poster that drives ticket sales
- Brand & Voice: Art deco aesthetic, elegant and celebratory
- Required Elements: Venue logo, event details, ticket URL
- Technical Constraints: 11x17 portrait for print, Instagram 9:16 variant
- Deliverables: Print-ready PDF + social media asset

**This is the hard boundary.** After this point, iteration is refinement, not discovering what to design.

### 6. Commit (Decide to proceed)

**File:** `06-commit-approval.md`

Client approved the creative brief:
- Direction confirmed (vintage speakeasy)
- Timeline locked (1 week for finals)
- Deliverables agreed (print + Instagram)
- Budget allocated (design time + print costs)

### 7. Execute (Create the deliverables)

**Files in `iterations/`:**
- `iteration-v1-draft.md` — Initial composition and typography
- `iteration-v2-refinement.md` — Client feedback incorporated (adjust gold tone, enlarge ticket URL)
- `iteration-v3-final.md` — Final polish, print-ready files exported

**Output:**
- `poster-final-print.pdf` — 11x17 print-ready file (300 DPI, CMYK)
- `poster-final-instagram.pdf` — 9:16 Instagram story variant (RGB)

### 8. Sustain (Post-publication)

**File:** `08-sustain-usage.md`

Post-delivery activities:
- Poster printed and displayed at venue
- Instagram story posted and performing well (high engagement)
- Client requested minor color adjustment for future print run (stays in Sustain)
- Considered creating matching ticket design (new project → Close this, Capture next)

---

## Lifecycle progression

```
Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain
   ↓         ↓        ↓        ↓         ↓          ↓         ↓         ↓
  inspo   moodboard options  refined    brief    approval iterations  usage
```

**Key observation:** Formalize (the Creative Brief) is where the design's identity is locked. Before that, we're discovering what to create. After that, we're refining how well we execute it.

---

## Files in this example

```
examples/create/design-exploration/
├── README.md                           # This file
├── praxis.yaml                         # Project configuration
├── 01-capture-inspiration.md           # Raw creative inputs
├── 02-sense-moodboard.md               # Synthesized visual direction
├── explorations/
│   ├── exploration-01-classic-deco.md  # Option 1: Traditional art deco
│   ├── exploration-02-modern-minimal.md # Option 2: Minimal geometric
│   └── exploration-03-vintage-speakeasy.md # Option 3: SELECTED
├── 04-shape-composition.md             # Refined layout and composition
├── docs/
│   └── brief.md                        # Creative Brief (formalize artifact)
├── 06-commit-approval.md               # Client approval decision
├── iterations/
│   ├── iteration-v1-draft.md           # Initial design
│   ├── iteration-v2-refinement.md      # Client feedback round
│   └── iteration-v3-final.md           # Final polish
├── poster-final-print.pdf              # Print-ready deliverable (11x17)
├── poster-final-instagram.pdf          # Social media variant (9:16)
└── 08-sustain-usage.md                 # Post-delivery updates
```

---

## How to use this example

1. **Read through the files in order** (01 → 02 → explorations → 04 → ... → 08)
2. **Pay special attention to `docs/brief.md`** — This is the required formalize artifact for Create domain
3. **Notice the shift at Formalize** — Before: discovering what to design. After: refining the execution
4. **Try it yourself:**
   ```bash
   praxis new my-design --domain create --privacy public
   cd my-design
   # Follow the pattern demonstrated in this example
   praxis templates render --stage formalize  # Generates docs/brief.md
   ```

---

## Related resources

- **Create domain specification:** `core/spec/domains.md`
- **Lifecycle stages:** `core/spec/lifecycle.md`
- **Creative Brief template:** `src/praxis/templates/domain/create/artifact/brief.md`
- **User guide:** `docs/guides/user-guide.md`
