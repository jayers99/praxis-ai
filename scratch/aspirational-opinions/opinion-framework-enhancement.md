# Opinion Framework Enhancement

> Organized from voice dictation brain dump (2025-12-28)

---

## Core Problem

Create a framework for **domain × stage** quality guidance that:
- Defines aspirational goals per cell (domain + stage combination)
- Integrates with `praxis validate` and `praxis audit`
- Limits downstream defects between lifecycle stages

---

## Proposed Architecture

### 1. Sub-Agent Research Approach

- Spawn sub-agents for each domain × stage cell
- Each agent works in its own directory
- Output: markdown files
- Research based on academic sources and key influencers

### 2. Execution Phases

1. First pass: identify key influencers for each cell
2. Review/validate the influencer list
3. Deep research on each influencer
4. Consolidate into first principles (consensus model from code domain)

### 3. File Structure Concept

```
docs/opinions/{domain}/
  README.md           # Domain overview
  {stage}.md          # Stage-specific aspirational goals
```

Each file contains:
- Aspirational goals (what quality looks like)
- "What's done" notes/checklist
- Suggestions for next phase transition

### 4. CLI Integration

- `praxis audit`: Compare current state against aspirational goals
- Output: requirements (must-have) + suggestions (nice-to-have)
- Stage-aware: "To advance from Shape → Formalize, consider X"

---

## Clarifications Needed

| Unclear Area | Question |
|--------------|----------|
| **Scope** | All 5 domains × 9 stages = 45 cells. Start with Code domain only? |
| **Influencers** | Academic papers? Industry practitioners? Frameworks (DDD, TDD)? |
| **Consensus model** | Reference to prior work—where is this documented? |
| **Requirements vs suggestions** | Hard gates (block progression) or advisory only? |

---

## Suggested Enhancements

### 1. Prioritize Cells

Not all domain × stage combinations need equal depth. Code + Formalize/Execute are highest value.

### 2. Schema for Opinion Files

```yaml
# docs/opinions/code/execute.md frontmatter
domain: code
stage: execute
sources:
  - "Clean Code (Martin)"
  - "Accelerate (Forsgren)"
```

### 3. Audit Output Levels

- `passed`: Meets aspirational goal
- `warning`: Advisory suggestion
- `blocked`: Cannot advance stage without this

### 4. Downstream Defect Tracking

Define what "defect" means per stage:
- Shape defect = ambiguous scope leaking into Formalize
- Formalize defect = incomplete contract leaking into Execute
- Execute defect = implementation bug leaking into Sustain

### 5. Template for Sub-Agent Instructions

```markdown
## Research Task: {domain} × {stage}

### Questions to Answer
- What does quality look like at this stage?
- What are common failure modes?
- What artifacts should exist?

### Sources to Consult
- Academic: [specific journals/conferences]
- Practitioner: [specific authors/frameworks]

### Output Format
- Key principles (3-5)
- Checklist items
- Anti-patterns to avoid
```

---

## Next Steps

- [ ] Decide: Start with Code domain only, or multiple domains?
- [ ] Document the "consensus model" referenced from prior work
- [ ] Create issue for implementation
