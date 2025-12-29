# Spike: Research Domain Definitions

**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Medium  
**Priority:** High (foundational for all opinions work)

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 30 min | ~20 queries |
| **Medium** | **60 min** | **~50 queries** |
| Large | 120 min | ~100 queries |

*This spike is Medium.*

---

## Spike Intent

Research and document best practices, prior art, and academic foundations for the 5 Praxis domains (Code, Create, Write, Observe, Learn). Explore boundary definitions, subtype taxonomies, and how similar frameworks categorize work.

**This is NOT an implementation story.** The output is research, not code or final documentation.

---

## Why a Spike?

- We need to understand how others categorize creative/technical work
- Domain boundaries (Write vs. Create, Observe vs. Learn) need grounding in prior art
- Subtype taxonomies should be informed by industry patterns
- Better to research now than discover gaps during execution

---

## Research Questions per Domain

### Code

- What taxonomies exist for software project types?
- How do others categorize: CLI, Library, API, Web App, Infrastructure?
- What's the industry standard for "project archetypes"?
- Key influencers/sources?

### Create

- How do creative fields categorize work? (Visual, Audio, Interactive)
- What distinguishes "aesthetic" from "functional" output?
- How do design schools/frameworks categorize creative work?
- Key influencers/sources?

### Write

- How is "writing" categorized in professional/academic contexts?
- Technical writing vs. business writing vs. narrative — standard taxonomy?
- Where does documentation fit?
- Key influencers/sources?

### Observe

- What prior art exists on passive capture? (Note-taking, journaling, bookmarking)
- How do knowledge management systems categorize raw capture?
- When does observation become something else?
- Key influencers/sources?

### Learn

- How is learning categorized? (Skill vs. concept vs. practice)
- What frameworks exist for learning goals? (Bloom's taxonomy, etc.)
- When does learning produce an artifact vs. internal capability?
- Key influencers/sources?

### Boundary Questions

- **Write vs. Create:** Is a blog post Write or Create? Is fiction Write or Create?
- **Observe vs. Learn:** When does observation become learning?
- **Code vs. Create:** Is generative AI art tooling Code or Create?
- **Hybrid work:** How do other frameworks handle multi-domain projects?

---

## Output Artifacts

### 1. Research Report

**File:** `projects/write/opinions-framework/docs/spike-02-domains-research.md`

For each domain:
- Summary of prior art found
- How others categorize this type of work
- Subtype taxonomies from industry/academia
- Boundary criteria (what's in, what's out)
- Confidence level in our current definition

### 2. Follow-Up Spikes Needed

Areas where more research is needed. Each should specify:
- What question remains unanswered
- Where to look for answers

### 3. Implementation Stories Ready

Refinements that are well-understood enough to become concrete stories.

### 4. Proposed Next Steps

What to do after this spike.

---

## Time Box Structure

| Phase | Time | Activity |
|-------|------|----------|
| Setup | 3 min | Read current domain definitions |
| Research: Code + Create | 10 min | Web search, synthesis |
| Research: Write + Learn + Observe | 10 min | Web search, synthesis |
| Boundary resolution | 5 min | Research hybrid/edge cases |
| Synthesis | 5 min | Compile report, identify gaps |
| **Total** | **30 min** | |

---

## Definition of Done

- [ ] Research report produced for all 5 domains
- [ ] Each domain has at least 2-3 sources identified
- [ ] Boundary questions addressed with research-backed proposals
- [ ] Follow-up spikes listed if needed
- [ ] Time box respected (stop at 30 min even if incomplete)
- [ ] Handoff summary produced

---

## Non-Goals

- Not updating `docs/domains.md` (that's implementation)
- Not defining complete subtype taxonomies (may need more research)
- Not exceeding time box

---

## Dependencies

- Can run in parallel with Spike 01 (Lifecycle)

## Enables

- Concrete domain refinement stories
- Story 03 (Praxis contract)
- All downstream opinion work

---

## Agent Instructions

**To execute this spike, copy the following to the agent:**

```
Read and execute this spike file completely.

This is a RESEARCH spike, not an implementation story. Your job is to explore, not to change docs/domains.md.

Time box: 30 minutes (stop when time is up, even if incomplete)

Your task:
1. For EACH of the 5 domains (Code, Create, Write, Observe, Learn):
   - Search for prior art on how this type of work is categorized
   - Find industry/academic taxonomies for subtypes
   - Identify boundary criteria (what's in, what's out)
   - Note key influencers/sources
   - Rate confidence in our current definition (high/medium/low)

2. Address the boundary questions:
   - Write vs. Create (blog post? fiction?)
   - Observe vs. Learn (when does observation become learning?)
   - Code vs. Create (AI art tooling?)
   - Hybrid work handling

3. Produce the research report:
   - Save to: projects/write/opinions-framework/docs/spike-02-domains-research.md

4. List follow-up spikes needed (questions that remain unanswered)

5. List implementation-ready stories (changes we're confident about)

6. Produce handoff summary with:
   - What you researched
   - Key findings
   - What remains unknown
   - Time spent

If you hit the time box before finishing, STOP and document your partial findings.
```
