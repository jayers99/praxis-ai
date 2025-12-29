# Spike Report: Shape Up Deep Dive

**Project:** opinions-framework
**Spike:** #79 - Shape Up Deep Dive
**Date:** 2025-12-28
**Status:** Complete

---

## Executive Summary

Mapped Shape Up methodology to Praxis stages. Found strong alignment with Shape/Formalize stages. Key divergences: Praxis supports multiple domains (not just software), has more granular stages, and allows explicit regression.

---

## Shape Up Overview

Shape Up is Basecamp's product development methodology with three phases:

1. **Shaping** - Senior people define problems and sketch solutions
2. **Betting** - Leadership decides what to build in the next cycle
3. **Building** - Teams execute with full autonomy for 6 weeks

Key principles:
- Fixed time, variable scope
- No backlogs (pitches that aren't bet on are discarded)
- Appetite-based scoping (how much is this worth?)
- Circuit breaker (6 weeks max, then kill or re-pitch)

---

## Alignment Matrix

| Shape Up Concept | Praxis Stage/Concept | Alignment |
|------------------|---------------------|-----------|
| **Shaping** | Shape | Strong |
| **Pitch** | SOD (Formalize artifact) | Strong |
| **Betting Table** | Formalize → Commit transition | Strong |
| **Building** | Execute | Strong |
| **Cooldown** | Sustain or Close | Partial |
| **Appetite** | SOD constraints | Strong |
| **Six-week cycle** | (no equivalent) | Diverge |
| **No backlog** | (no equivalent) | Diverge |

---

## What Praxis Can Borrow

### 1. Appetite-Based Scoping
Shape Up uses "appetite" (how much time this is worth) rather than estimates (how long will this take). This inverts the typical planning question.

**Recommendation:** Add "Appetite" as a required SOD section. Frame it as "How much effort is appropriate?" not "How long will this take?"

### 2. Pitch Structure
The Shape Up pitch has five ingredients:
- Problem
- Appetite
- Solution
- Rabbit holes
- No-gos

**Recommendation:** The SOD template should mirror this structure. Already proposed in Spike #76.

### 3. Fixed Boundaries, Not Fixed Scope
Shape Up teams cut scope to fit the time box, not extend time to fit scope. This is a mindset, not just a process.

**Recommendation:** Add "scope cutting" as an explicit Execute activity in lifecycle.md. "If time runs out, cut features, don't extend deadlines."

### 4. Circuit Breaker Pattern
If work isn't done in 6 weeks, it's killed—no extensions by default. This prevents runaway projects.

**Recommendation:** Consider optional "circuit breaker" setting in praxis.yaml that triggers automatic regression to Formalize if Execute exceeds threshold.

---

## Where Praxis Diverges (and Why)

### 1. Multiple Domains
Shape Up is designed for software product development. Praxis covers Code, Create, Write, Learn, and Observe.

**Implication:** Shape Up's "Building" phase maps to Execute, but the definition of Execute varies by domain.

### 2. More Granular Stages
Shape Up has 3 phases. Praxis has 9 stages.

**Implication:** Praxis captures early-stage work (Capture → Sense → Explore) that Shape Up skips. Shape Up assumes ideas arrive already somewhat shaped.

### 3. Explicit Regression
Shape Up kills projects that don't finish. Praxis allows regression to earlier stages.

**Implication:** Praxis is more forgiving but requires regression detection (Spike #78) to prevent abuse.

### 4. Backlogs Allowed
Shape Up discards unbetted pitches. Praxis doesn't mandate backlog policy.

**Implication:** Teams can choose Shape Up's "no backlog" approach or maintain traditional backlogs. Praxis is agnostic.

### 5. Individual vs. Team Focus
Shape Up assumes team-based work. Praxis works for solo projects too.

**Implication:** "Betting table" concept doesn't translate to solo work. Praxis Formalize is the decision point.

---

## Appetite vs. Constraints

| Shape Up | Praxis Equivalent |
|----------|-------------------|
| Small Batch (2 weeks) | size: small |
| Big Batch (6 weeks) | size: medium or large |
| Specific appetite ("2 weeks of one designer") | SOD constraints section |

**Key insight:** Shape Up's appetite is about *commitment level*, not just time. "How much are we willing to lose if this fails?"

**Recommendation:** Frame SOD "Appetite" as risk tolerance, not just duration.

---

## Relationship to Formalize Boundary

Shape Up's "Betting Table" is equivalent to Praxis's Formalize → Commit transition:

| Aspect | Shape Up | Praxis |
|--------|----------|--------|
| Decision point | Betting Table | Formalize stage exit |
| Artifact required | Pitch | SOD |
| Who decides | Senior leadership | (varies by project) |
| Outcome if approved | Goes to Building | Advances to Commit |
| Outcome if rejected | Discarded (by default) | Stays in Formalize or regresses |

**Key insight:** The Formalize boundary is Praxis's version of the betting table, but without mandating who makes the decision.

---

## Borrowed Terms

Consider adopting these Shape Up terms in Praxis:

| Term | Meaning | Use In Praxis |
|------|---------|---------------|
| **Appetite** | How much we're willing to spend | SOD section |
| **Rabbit holes** | Traps to avoid | SOD section (already adopted) |
| **No-gos** | Explicitly excluded | SOD "Out of Scope" section |
| **Circuit breaker** | Automatic kill if over time | Optional regression trigger |

---

## Sources

- [Shape Up - Basecamp (full book PDF)](https://basecamp.com/shapeup/shape-up.pdf)
- [The Betting Table - Shape Up Ch. 8](https://basecamp.com/shapeup/2.2-chapter-08)
- [Write the Pitch - Shape Up Ch. 6](https://basecamp.com/shapeup/1.5-chapter-06)
- [Bets, Not Backlogs - Shape Up Ch. 7](https://basecamp.com/shapeup/2.1-chapter-07)
- [Shape Up Complete Guide 2024 - AgileFirst](https://agilefirst.io/what-is-shape-up/)

---

## Follow-Up Recommendations

1. **Add "Appetite" to SOD template** (already in Spike #76)
2. **Add scope cutting guidance** to lifecycle.md Execute section
3. **Consider circuit breaker config** in praxis.yaml schema
4. **Document Shape Up alignment** for teams familiar with that methodology
