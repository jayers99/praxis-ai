# Spike Report: Sustain for Non-Code Domains

**Project:** opinions-framework
**Spike:** #77 - Sustain for Non-Code Domains
**Date:** 2025-12-28
**Status:** Complete

---

## Executive Summary

Researched what "sustain" means for non-Code domains (Create, Write, Learn, Observe). Found distinct patterns for each domain, with the common thread being: **maintenance activities that preserve value over time without fundamentally changing the work.**

---

## Domain-Specific Sustain Definitions

### Create Domain (Art, Music, Video)

**Definition:** Sustain = keeping creative work accessible, attributed, and (optionally) commercially viable.

**Key Activities:**
1. **Portfolio maintenance** - Curating which works represent current skill level
2. **Format preservation** - Ensuring files remain playable/viewable (codec updates, format migrations)
3. **Rights management** - Maintaining copyright, licensing, attribution
4. **Distribution health** - Keeping links alive, platforms updated

**Sources:**
- [Managing the Life Cycle of Art - Hippo Reads](https://hipporeads.com/from-inspiration-to-preservation-managing-the-life-cycle-of-art/)
- [Professional Self-Structuration in the Arts - MDPI](https://www.mdpi.com/2071-1050/9/6/1035)

**Key Insight:** Creative work has a "decay" problem—file formats become obsolete, platforms disappear, portfolios become stale. Sustain is about fighting entropy.

---

### Write Domain (Docs, Essays, Specs)

**Definition:** Sustain = keeping written content accurate, discoverable, and versioned.

**Key Activities:**
1. **Version control** - Tracking changes, maintaining history
2. **Accuracy reviews** - Periodic checks for outdated information
3. **Link maintenance** - Fixing broken references
4. **Discoverability** - Ensuring proper indexing and navigation

**Sources:**
- [Revising and Maintaining Documentation - Digital Preservation Coalition](https://www.dpconline.org/digipres/implement-digipres/digital-preservation-documentation-guide/digital-preservation-documentation-revising)
- [Document Lifecycle Management - Technical Writer HQ](https://technicalwriterhq.com/documentation/document-lifecycle-management/)

**Best Practices from Research:**
- Use version numbering (major.minor.patch)
- Schedule regular review cycles (quarterly/annually)
- Track document owners and expiration dates
- Maintain audit trails for compliance

**Key Insight:** Documents without scheduled reviews become "write-only"—created but never maintained. Sustain requires explicit review triggers.

---

### Learn Domain (Skills, Knowledge)

**Definition:** Sustain = preventing skill decay through spaced repetition and deliberate practice.

**Key Activities:**
1. **Spaced repetition** - Reviewing knowledge at optimal intervals
2. **Deliberate practice** - Targeted exercises to maintain proficiency
3. **Skill inventory** - Tracking what needs maintenance vs. what can decay
4. **Refresh cycles** - Re-engaging with material before forgetting

**Sources:**
- [Spaced Repetition for Efficient Learning - Gwern.net](https://gwern.net/spaced-repetition)
- [Cognitive Science of Learning - Justin Skycak](https://www.justinmath.com/cognitive-science-of-learning-spaced-repetition/)

**Key Research Findings:**
- Memory follows a forgetting curve—without review, knowledge decays exponentially
- Spaced repetition is for *maintenance*, not improvement: "If one is a gifted amateur when one starts reviewing, one remains a gifted amateur"
- Rule of thumb: "If you'll spend more than 5 minutes looking something up over your lifetime, it's worth memorizing with spaced repetition"
- Deliberate practice (not just repetition) is required for skill *improvement*

**Key Insight:** Learn domain has the most mature science behind Sustain—spaced repetition systems (Anki, etc.) are explicitly designed for this. Praxis could integrate with SRS tools.

---

### Observe Domain (Notes, Bookmarks)

**Definition:** Sustain = curating and pruning captured information to maintain signal-to-noise ratio.

**Key Activities:**
1. **Curation** - Deciding what's still valuable vs. noise
2. **Organization** - Maintaining structure and findability
3. **Link checking** - Ensuring bookmarked resources still exist
4. **Archival decisions** - Moving to cold storage vs. deletion

**Sources:**
- [Personal Knowledge Management practices](https://gwern.net/spaced-repetition) (PKM literature)
- Creative portfolio maintenance patterns apply here too

**Key Insight:** Observe is the lowest-commitment domain for Sustain. Captured observations may intentionally be allowed to decay if they're not worth maintaining. The Sustain decision is: "Is this still worth keeping?"

---

## Sustain Pattern Comparison

| Domain | Decay Type | Sustain Trigger | Primary Tool |
|--------|------------|-----------------|--------------|
| Code | Bit rot, dependencies | CI failures, security alerts | Automated tests |
| Create | Format obsolescence, platform death | Scheduled review | Portfolio audit |
| Write | Accuracy decay, link rot | Calendar trigger | Review cycle |
| Learn | Forgetting curve | SRS algorithm | Spaced repetition |
| Observe | Signal decay | Manual curation | Archive/delete review |

---

## Common Principles Across Domains

1. **Scheduled triggers beat ad-hoc reviews.** Without explicit triggers, Sustain doesn't happen.

2. **Sustain ≠ Improvement.** Sustain maintains current state; improvement requires returning to earlier stages (Formalize or Execute).

3. **Not everything deserves Sustain.** Some work is intentionally allowed to Close after Execute. Sustain is a choice, not a default.

4. **Automation varies by domain.** Code has the best automation (tests, CI). Learn has good tooling (SRS). Create/Write/Observe are more manual.

---

## Proposed Sustain Definitions for Praxis

```yaml
sustain_definitions:
  code:
    description: "Keeping software running, secure, and maintainable"
    triggers: ["test failures", "security alerts", "dependency updates"]

  create:
    description: "Keeping creative work accessible and properly attributed"
    triggers: ["scheduled portfolio review", "format obsolescence", "platform changes"]

  write:
    description: "Keeping content accurate, discoverable, and versioned"
    triggers: ["scheduled review cycle", "broken links", "accuracy complaints"]

  learn:
    description: "Preventing skill/knowledge decay through deliberate review"
    triggers: ["spaced repetition schedule", "skill not used recently"]

  observe:
    description: "Curating captured information to maintain value"
    triggers: ["scheduled curation", "storage limits", "explicit review request"]
```

---

## Sources

- [Spaced Repetition for Efficient Learning - Gwern.net](https://gwern.net/spaced-repetition)
- [Managing the Life Cycle of Art - Hippo Reads](https://hipporeads.com/from-inspiration-to-preservation-managing-the-life-cycle-of-art/)
- [Revising and Maintaining Documentation - DPC](https://www.dpconline.org/digipres/implement-digipres/digital-preservation-documentation-guide/digital-preservation-documentation-revising)
- [Document Lifecycle Management - Technical Writer HQ](https://technicalwriterhq.com/documentation/document-lifecycle-management/)
- [Professional Self-Structuration in the Arts - MDPI](https://www.mdpi.com/2071-1050/9/6/1035)
- [Cognitive Science of Learning - Justin Skycak](https://www.justinmath.com/cognitive-science-of-learning-spaced-repetition/)

---

## Follow-Up Recommendations

1. **Add domain-specific sustain guidance** to `docs/domains.md`
2. **Consider SRS integration** for Learn domain (Anki, RemNote, etc.)
3. **Define sustain triggers** as part of `praxis.yaml` schema
4. **Add `praxis sustain` command** to show what needs review per domain
