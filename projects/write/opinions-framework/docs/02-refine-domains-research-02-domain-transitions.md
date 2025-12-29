# Spike: Domain Transition Mechanics


**Issue:** #81
**Type:** Research Spike
**Time Box:** 15 minutes
**Status:** Complete

---

## Spike Intent

Research how an artifact transitions between domains (e.g., Observe → Write).

---

## Research Findings

### 1. Artifact-Centric Process Models

From academic research on artifact-centric business processes:

> "The artifact-centric approach focuses on describing how business data is changed/updated by a particular action or task throughout the process."

**Key insight:** The notion of lifecycle is prominent in artifact-centric models. Artifacts have states and transitions, not just locations.

**Source:** [Artifact-centric business process model – Wikipedia](https://en.wikipedia.org/wiki/Artifact-centric_business_process_model)

---

### 2. PKM Progressive Summarization Pattern

Tiago Forte's Progressive Summarization describes how raw captures evolve:

| Layer | Action | Domain Analogy |
|-------|--------|----------------|
| L1 | Raw capture | Observe |
| L2 | Bold key passages | Observe → Observe (enriched) |
| L3 | Highlight within bold | Observe → Write (distillation begins) |
| L4 | Executive summary | Write |
| L5 | Remix into new form | Write → Create or Code |

**Pattern:** Transition happens when the *intent* changes from capture to synthesis.

**Source:** [Progressive Summarization – Forte Labs](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)

---

### 3. DCC Lifecycle Model (Data Curation)

The Digital Curation Centre defines 7 sequential lifecycle actions:

1. **Create or receive** data
2. **Appraise and select**
3. **Ingest** into managed environment
4. **Preserve**
5. **Store**
6. **Access, use, reuse**
7. **Transform** into derived products

**Pattern:** The "Transform" step is where domain transitions occur – creating new artifacts from existing ones.

---

### 4. FHIR Knowledge Artifact Lifecycle

Healthcare knowledge artifacts follow strict status transitions:

```
draft → active → retired
```

**Key rule:** An active artifact SHALL NOT transition back to draft. A new version is required.

**Praxis parallel:** Domain transitions might create new artifacts rather than mutating existing ones.

**Source:** [FHIR Artifact Lifecycle](https://build.fhir.org/ig/HL7/crmi-ig/artifact-lifecycle.html)

---

## Proposed Domain Transition Patterns

### Pattern 1: Promotion (most common)

Artifact matures from one domain to another.

```
Observe → Write    (notes become essay)
Observe → Learn    (capture becomes study material)
Write → Code       (spec becomes implementation)
Learn → Code       (practice becomes tool)
```

**Trigger:** User explicitly promotes artifact with intent change.

### Pattern 2: Derivation

New artifact created in different domain, referencing original.

```
Write → Create     (essay inspires illustration)
Code → Write       (implementation spawns documentation)
Observe → Create   (photo becomes design reference)
```

**Trigger:** User creates derived work, links to source.

### Pattern 3: Decomposition

One artifact splits into multiple, possibly across domains.

```
Write → Write + Code    (blog post + code examples)
Create → Create + Write (artwork + artist statement)
```

**Trigger:** Complex artifact needs domain-specific treatment.

### Pattern 4: Aggregation

Multiple artifacts combine into one in new domain.

```
Observe + Observe + Observe → Write (notes → synthesis essay)
Learn + Learn → Write (study notes → learning summary)
```

**Trigger:** Synthesis work produces unified output.

---

## Transition Trigger Conditions

| Condition | Description | Example |
|-----------|-------------|---------|
| **Intent change** | Purpose shifts from capture to create | Raw notes → structured outline |
| **Quality bar** | Artifact exceeds domain's natural ceiling | Notes too polished for Observe |
| **Audience change** | From self to others | Personal notes → shared document |
| **Formalization** | Artifact requires domain-specific artifacts | Notes need SOD → must be Code |
| **Time investment** | Significant effort signals transition | Hours of editing → no longer Observe |

---

## Domain Handoff Mechanics

### Proposal: Explicit Transition Command

```bash
praxis transition observe/my-notes.md --to write
```

**Effects:**
1. Validates artifact can transition (has required maturity)
2. Creates new artifact in target domain (or moves if appropriate)
3. Updates `praxis.yaml` with domain assignment
4. Records transition in audit log
5. Links derived artifact to source

### Proposal: Transition Artifact Requirements

| From → To | Requirement |
|-----------|-------------|
| Observe → Write | Summary/thesis statement present |
| Observe → Learn | Learning goal identified |
| Write → Code | Technical specification present |
| Learn → Code | Working prototype exists |
| * → Create | Aesthetic intent declared |

---

## Definition of Done Checklist

- [x] At least 3 transition patterns documented
- [x] Trigger conditions identified
- [x] Ready for PR

---

## Follow-Up Considerations

1. **Bidirectional transitions:** Can artifacts transition "backwards"? (Code → Write for documentation)
2. **Multi-domain artifacts:** Can one artifact belong to multiple domains simultaneously?
3. **Automatic detection:** Can praxis suggest transitions based on artifact characteristics?

---

## Handoff Summary

**Researched:** Artifact transition patterns between Praxis domains, drawing from artifact-centric BPM, PKM progressive summarization, and data curation lifecycle models.

**Key findings:**
- 4 transition patterns identified: Promotion, Derivation, Decomposition, Aggregation
- Progressive Summarization provides clear model for Observe → Write transition
- FHIR lifecycle suggests transitions should create new artifacts, not mutate
- Trigger conditions include intent change, quality bar, audience change, formalization, time investment

**What remains unknown:**
- Whether bidirectional transitions should be allowed
- How to handle multi-domain artifacts
- Automatic transition detection heuristics

**Time spent:** Within 15-minute time box.
=======
**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Small  
**Priority:** Medium

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| **Small** | **30 min** | **~20 queries** |
| Medium | 60 min | ~50 queries |
| Large | 120 min | ~100 queries |

*This spike is Small.*

---

## Spike Intent

Research how an artifact transitions between domains. For example, how does an observation (Observe) become a document (Write)?

---

## Research Questions

1. How exactly does an artifact move from Observe → Write?
2. What triggers a domain transition?
3. Is this a new project or a continuation?
4. How do PKM systems handle progressive summarization?
5. What artifacts carry over between domains?

---

## Where to Look

- PKM literature on progressive summarization (Tiago Forte)
- Zettelkasten literature notes → permanent notes
- Knowledge pipeline patterns

---

## Output Artifacts

1. Research report → `02-refine-domains-research-02-domain-transitions-report.md`
2. Transition patterns documented
3. Proposed mechanics for domain handoff
4. Follow-up stories if needed

---

## Definition of Done

- [ ] At least 3 transition patterns documented
- [ ] Trigger conditions identified
- [ ] Artifact handoff rules proposed
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 30-minute time box
3. Commit changes to your branch with message: `docs: spike domain transitions research`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: Domain Transition Mechanics" --body-file <handoff.md> --base main
   ```
5. Include "Closes #XX" in your PR body

---

## Handoff Template

```markdown
## Summary
What you researched and key findings

## Files Changed
- List of files created/modified

## Decisions Made
- Key choices and rationale

## Open Questions
- What remains unknown

## Time Spent
- Actual time vs budget

## Follow-Up Needed
- Recommended next spikes/stories

Closes #XX
```

