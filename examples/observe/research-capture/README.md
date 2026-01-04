# Example: Research Capture — "AI Governance Patterns Research"

**Domain:** Observe  
**Subtype:** notes  
**Final Stage:** Close (transitioned to Write domain)

---

## What you'll learn

This example demonstrates the Observe domain lifecycle and domain transition pattern:

- How Observe domain works (raw capture, no formalize artifact required)
- Observe lifecycle stages (Capture → Sense → Explore → Shape → Close)
- **Critical:** Observe has NO Formalize/Commit/Execute stages (pre-formalization by nature)
- How to recognize when Observe transitions to another domain (Observe → Write)
- How domain transition creates new project with proper formalization

---

## Prerequisites

- Basic familiarity with the Praxis lifecycle (see `docs/guides/user-guide.md`)
- Understanding of the Observe domain (see `core/spec/domains.md`)

---

## Project context

This example shows research capture on "AI governance patterns" collected over 2 weeks. The captures started as raw notes, links, and clips. When synthesis and structure emerged, the work transitioned from Observe → Write domain (new project: "AI Governance Synthesis Article").

**Key observation:** Observe is for RAW capture. When you start synthesizing or creating structure, you've crossed into another domain.

---

## Step-by-step walkthrough

### 1. Capture (Raw inputs, no judgment)

**Files in `captures/`:**
- `day-01-hacker-news-thread.md` — HN discussion on AI safety
- `day-03-paper-clip.md` — Research paper bookmark + quote
- `day-05-podcast-notes.md` — Rough notes from AI podcast
- `day-07-twitter-thread.md` — Saved thread on governance frameworks
- `day-10-book-excerpt.md` — Highlighted passage from book
- `day-12-internal-meeting.md` — Notes from work discussion

**Characteristics:**
- Minimal processing (copy/paste, quick notes)
- No organization or tagging yet
- Captures are dated for temporal context
- Mixed formats (links, quotes, thoughts, questions)

### 2. Sense (Patterns emerge)

**File:** `02-sense-themes.md`

Light organization without synthesis:
- **Theme 1:** Technical governance (monitoring, testing, validation)
- **Theme 2:** Organizational governance (roles, decision rights, oversight)
- **Theme 3:** Policy governance (regulation, compliance, ethical frameworks)

Observation: These themes keep recurring across different sources

### 3. Explore (Connections noticed)

**File:** `03-explore-connections.md`

Identified relationships between captures:
- HN thread + research paper both mention "human-in-the-loop" pattern
- Podcast + book excerpt discuss similar risk frameworks
- Multiple sources reference same governance principles (transparency, accountability, reversibility)

**Still Observe:** Noticing patterns, not synthesizing arguments yet

### 4. Shape (Structure forms, but still raw)

**File:** `04-shape-clusters.md`

Grouped captures into potential structure:
- Cluster A: Monitoring & observability patterns (5 captures)
- Cluster B: Decision rights & approval workflows (4 captures)
- Cluster C: Risk assessment frameworks (6 captures)

**Tension point:** Structure is forming, but no thesis or synthesis yet. Still capturing.

### 5. Close (Observe ends)

**File:** `05-close-transition-decision.md`

**Decision:** This has outgrown raw capture. A clear argument is forming: "Organizations need layered AI governance (technical + organizational + policy)."

**Action:** Close Observe project, transition to Write domain

---

## Domain Transition: Observe → Write

**File:** `transition-to-write/new-project-decision.md`

**Transition trigger:** Intent changed from "capture for later" to "synthesize and communicate"

**New project created:**
- **Domain:** Write
- **Project:** "AI Governance Synthesis Article"
- **Formalize artifact:** `docs/brief.md` (Writing Brief)
- **Source material:** All captures from this Observe project

**Key rule:** Observe project closes, Write project begins. They are separate projects with different governance.

---

## Observe Lifecycle (No Formalize!)

```
Capture → Sense → Explore → Shape → Close
   ↓         ↓        ↓        ↓       ↓
  raw     themes  connections clusters transition
```

**Critical observation:** Observe SKIPS Formalize/Commit/Execute/Sustain. It's pre-formalization by design. When you need formalization, you've transitioned to another domain.

---

## Files in this example

```
examples/observe/research-capture/
├── README.md                           # This file
├── praxis.yaml                         # Project configuration (domain: observe)
├── captures/
│   ├── day-01-hacker-news-thread.md    # Raw HN discussion
│   ├── day-03-paper-clip.md            # Research paper bookmark
│   ├── day-05-podcast-notes.md         # Podcast rough notes
│   ├── day-07-twitter-thread.md        # Saved Twitter thread
│   ├── day-10-book-excerpt.md          # Book highlight
│   └── day-12-internal-meeting.md      # Meeting notes
├── 02-sense-themes.md                  # Light organization
├── 03-explore-connections.md           # Noticed relationships
├── 04-shape-clusters.md                # Grouped captures
├── 05-close-transition-decision.md     # Close + transition
└── transition-to-write/
    └── new-project-decision.md         # Write domain project created
```

---

## Key Observations About Observe Domain

### Observe is for RAW capture
- No judgment, no synthesis, no structure (yet)
- Minimal processing (copy/paste, quick notes)
- Goal: Get it out of your head / environment and into a retrievable location

### Observe has NO Formalize artifact
- Formalize requires intent, scope, constraints
- Observe is pre-intent (you don't know what it's for yet)
- When intent emerges → transition to domain that requires formalization

### Observe is temporary
- Projects stay in Observe until patterns emerge (days to weeks, not months)
- Close when: Intent emerges OR Captures go stale OR No longer useful

### Domain transition triggers
| To Domain | Trigger |
|-----------|---------|
| **Write** | Thesis or argument is forming, want to communicate |
| **Learn** | Learning goal identified, want structured practice |
| **Code** | Implementation idea crystallized, need specification |
| **Create** | Creative vision emerged, want to execute |

---

## How to use this example

1. **Read the captures/** files to see raw input format
2. **Notice the progression:** Capture (raw) → Sense (themes) → Explore (connections) → Shape (clusters) → Close (transition)
3. **Pay attention to the transition decision** — This is the critical moment when Observe becomes another domain
4. **Try it yourself:**
   ```bash
   praxis new research-notes --domain observe --privacy personal
   cd research-notes
   # Capture raw inputs without judgment or structure
   # When intent emerges, close and transition to appropriate domain
   ```

---

## Related resources

- **Observe domain specification:** `core/spec/domains.md`
- **Domain transitions:** `core/spec/domains.md` (Transition Triggers section)
- **Lifecycle stages:** `core/spec/lifecycle.md`
- **User guide:** `docs/guides/user-guide.md`
