# Team Roles for Ticket Refinement and Peer Review: DORA Findings

> A comprehensive analysis of first principles, best practices, prior art, expert consensus, academic research, and anti-patterns for team roles critical to ticket refinement and peer review success according to DORA (DevOps Research and Assessment) findings.

---

## Executive Summary

DORA research establishes that **peer review** and **clear change processes** are foundational to high software delivery performance. This report synthesizes DORA findings with agile best practices and academic research to identify the team roles, responsibilities, and practices that drive success in ticket refinement and peer review workflows.

**Key Finding:** Teams with faster code reviews have **50% better software delivery performance**. Lightweight peer review (pair programming or intra-team code review) produces **superior IT performance** compared to external change approval boards.

---

## 1. First Principles

### 1.1 DORA's Core Finding on Change Approval

> "Change approvals are best implemented through **peer review during the development process**, supplemented by automation to detect, prevent, and correct bad changes early in the software delivery life cycle."
> — DORA 2019 State of DevOps Report

**Key Insight:** Heavyweight formal approval processes (like change advisory boards) have a **negative impact** on software delivery performance. No evidence supports that formal external review processes reduce change fail rates.

### 1.2 The Lean Product Management Connection

DORA identifies four capabilities that together predict both software delivery and organizational performance:

| Capability | Description |
|------------|-------------|
| **Working in Small Batches** | Features sliced to complete in ≤1 week |
| **Team Experimentation** | Ability to try new ideas without external permission |
| **Visibility of Work** | Understanding flow from idea to customer |
| **Customer Feedback** | Incorporating user input into product decisions |

**Refinement and review processes should enable—not hinder—these capabilities.**

### 1.3 Speed and Stability Are Not Trade-offs

DORA's research consistently demonstrates that the four key metrics (Deployment Frequency, Lead Time, Change Failure Rate, MTTR) are **correlated**:
- Top performers excel at all four
- Low performers struggle with all four

**Implication for Review:** Fast reviews do not sacrifice quality—they enable it.

---

## 2. Team Roles in Ticket Refinement

### 2.1 Product Owner

**Accountability:** Maximizing product value and effective Product Backlog management.

**Responsibilities in Refinement:**

| Phase | Activity |
|-------|----------|
| **Before** | Conduct informal refinement with SMEs/stakeholders; write user stories with acceptance criteria; understand team velocity |
| **During** | Share items needing refinement; communicate the "what" and "why" (not the "how"); help developers understand trade-offs |
| **After** | Ensure backlog is transparent, visible, and understood; maintain prioritization |

**Best Practices:**
- Prepare 2 sprints worth of backlog items in advance
- Start with product vision—the "why" before the "what"
- Collaborate rather than dictate; PO is accountable but can delegate work
- Limit preparation beyond 1 month (user stories) / 2 months (features) to avoid waste

**DORA Alignment:** Clear requirements and work visibility directly predict software delivery performance.

### 2.2 Scrum Master / Agile Coach

**Role:** Servant leader who facilitates team processes and removes obstacles.

**Responsibilities in Refinement:**

| Stance | Activity |
|--------|----------|
| **Facilitator** | Create "container" for team ideas; timebox discussions; guide estimation |
| **Coach** | Promote self-organization; foster psychological safety; encourage independence |
| **Observer** | Watch for dysfunction; step back when refinement works well |

**Lyssa Adkins Framework:**
> "The coach creates the container; the team creates the content."

**Best Practices:**
- Ideally, step back when teams are mature—refinement shouldn't require SM presence
- Guide discussions, ensure engagement, foster psychological safety
- Use retrospectives to improve refinement process itself
- Help teams maintain 10% capacity allocation for refinement (per Scrum Guide)

**Anti-Pattern:** Scrum Master dominates discussions or makes decisions that should be the team's.

### 2.3 Development Team Members

**Accountability:** Estimating and executing Product Backlog Items.

**Responsibilities in Refinement:**

| Activity | Purpose |
|----------|---------|
| **Sizing/Estimating** | Developers doing the work are responsible for estimates |
| **Clarifying** | Ask questions; surface assumptions; identify risks |
| **Breaking Down** | Split large items into smaller, INVEST-compliant stories |
| **Defining Done** | Ensure shared understanding of acceptance criteria |

**Best Practices:**
- All developers participate—not just leads or seniors
- Demand 20% slack time to support teammates and maintain shared understanding
- Engage deeply with requirements to provide accurate estimates
- Surface concerns about technical feasibility early

**DORA Alignment:** Team experimentation requires developers to write and change specifications during development without external permission.

### 2.4 Subject Matter Experts (SMEs) / Stakeholders

**Role:** Provide domain knowledge and business context.

**Responsibilities:**
- Clarify business rules and edge cases
- Validate acceptance criteria
- Provide feedback on proposed solutions
- Participate in refinement when domain expertise is needed

**Best Practice:** Include in informal pre-refinement discussions to affirm business value before team sessions.

---

## 3. Team Roles in Peer Review

### 3.1 Code Author

**Accountability:** Producing high-quality, reviewable code.

**Responsibilities:**

| Practice | Purpose |
|----------|---------|
| **Small PRs** | Keep changes small for faster, higher-quality reviews |
| **Clear Context** | Provide description, related tickets, testing approach |
| **Self-Review** | Review own code before submitting |
| **Responsive** | Address feedback promptly; engage in discussion |

**Best Practices:**
- Trunk-based development: Merge to trunk at least daily
- Dark launching for incomplete features
- Use draft PRs for early feedback
- Include estimated review time to help reviewers schedule

**DORA Finding:** "The more files in a change, the lower the proportion of valuable review comments."

### 3.2 Code Reviewer

**Accountability:** Ensuring code quality, correctness, security, and maintainability.

**Responsibilities:**

| Area | What to Review |
|------|----------------|
| **Functionality** | Does code behave as intended? As users expect? |
| **Design** | Well-architected? Fits surrounding system? |
| **Complexity** | Can another developer easily understand and use it? |
| **Security** | Follows secure coding standards? No hardcoded secrets? |
| **Tests** | Correct and well-designed automated tests? |

**Feedback Quality:**
- Specific and actionable
- Focus on code, not the person
- Offer alternatives rather than just criticism
- Complete review in single pass—don't nitpick iteratively

**Microsoft Research Finding:** "Proportion of useful comments increases dramatically in the first year but tends to plateau afterwards."

### 3.3 Review Lead / Senior Reviewer

**Role:** Oversee review quality and mentor junior reviewers.

**Responsibilities:**
- Ensure review coverage across codebase areas
- Assign reviewers based on expertise
- Mentor on effective feedback techniques
- Break bottlenecks when reviews pile up

**Anti-Pattern:** Restricting reviews to senior members only creates significant bottlenecks.

**DORA Recommendation:** Distribute review responsibility; avoid single points of failure.

### 3.4 Team Lead / Engineering Manager

**Role:** Create conditions for effective review culture.

**Responsibilities:**
- Set expectations for review turnaround time (ideally <24 hours)
- Remove systemic blockers to review speed
- Monitor metrics (PR pickup time, cycle time)
- Ensure psychological safety for honest feedback

**DORA Finding:** "Find ways to discover problems like regressions, performance issues, and security issues automatically as soon as possible after changes are committed."

---

## 4. The Definition of Ready

### 4.1 INVEST Criteria

The Definition of Ready (DoR) ensures backlog items are actionable before sprint planning:

| Criterion | Meaning |
|-----------|---------|
| **I**ndependent | Self-contained; no blocking dependencies |
| **N**egotiable | Room for discussion on implementation |
| **V**aluable | Clear value to stakeholders |
| **E**stimable | Team can estimate relative size |
| **S**mall | Completable within a sprint |
| **T**estable | Clear acceptance criteria |

### 4.2 Acceptance Criteria

**Best Practice:** 3-5 acceptance criteria per story.

**Anti-Pattern:** Too many acceptance criteria indicate the story is too large.

### 4.3 Cautions

> "An exhaustive list of pre-work will complicate the team's ability to start work items."

**Balance:** DoR should facilitate collaboration, not create barriers. It should evolve as the team matures.

---

## 5. Best Practices from DORA Research

### 5.1 Streamlining Change Approval

| Practice | Impact |
|----------|--------|
| Peer review at code check-in | Superior IT performance vs. CABs |
| Automated testing | Catches issues without human bottleneck |
| Pair programming | Code already reviewed by second person |
| Synchronous review | Avoids merge conflicts from delays |

**Heavyweight Approval Anti-Pattern:**
> "When code review is laborious and takes hours or days, developers avoid working in small batches and instead batch up many changes. This leads to a downward spiral where reviewers procrastinate with large code reviews due to their complexity."

### 5.2 Working in Small Batches

| Metric | Best Practice |
|--------|---------------|
| **Commit frequency** | Multiple small changes per day |
| **Feature slicing** | Complete work in ≤1 week |
| **Branch lifetime** | Hours, not days or weeks |
| **Active branches** | ≤3 active branches |

**Benefits:**
- Faster feedback loops
- Easier triage and remediation
- Reduced risk per change
- Avoids sunk-cost fallacy

### 5.3 Team Experimentation

DORA research shows high-performing teams can:
- Work on new ideas without external permission
- Write and change specifications during development
- Make changes to stories without external approval

**Enabler:** Lightweight refinement and review processes that trust teams.

### 5.4 Continuous Integration

| Practice | Purpose |
|----------|---------|
| Trunk-based development | Merge to trunk ≥1x daily |
| Fast automated tests | Run after each commit |
| No code freezes | Continuous flow |
| No integration phases | Small batches eliminate need |

---

## 6. Anti-Patterns

### 6.1 Refinement Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Rare refinement** | No visibility on upcoming work; poor estimates | Regular sessions; 10% capacity allocation |
| **Too much refinement** | Impacts focus on current sprint; waste | Just-in-time; 2 sprints ahead max |
| **Unprepared PO** | Wasted team time; poor outcomes | PO pre-work with SMEs |
| **Surface-level understanding** | Wrong estimates; rework | Deep discussion; all devs participate |
| **Only seniors estimate** | Knowledge gaps; lack of commitment | Full team estimation |
| **Oversized backlog** | Wasted refinement effort; clutter | 3-6 sprints of items max |
| **Horizontal slicing** | No end-to-end value delivery | Vertical slicing by user value |
| **No slack time** | 100% utilization kills collaboration | 20% slack for support/pairing |
| **Unrefined items in planning** | Blindsides team; poor breakdown | Enforce DoR before planning |
| **Waterfall planning backdoor** | Fixed annual roadmap defeats agility | Emergent, adaptive planning |

### 6.2 Code Review Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Slow reviews** | 4+ day wait destroys cycle time | Prioritize reviews; <24hr turnaround |
| **Excessive reviewers** | Bottlenecks and delays | 1-2 reviewers max |
| **Only senior reviewers** | Single point of failure | Distribute review responsibility |
| **Iterative nitpicking** | Stop-read-comment-repeat wastes time | Complete review in single pass |
| **Style wars** | Debates over preferences | Automated linting; agreed style guides |
| **No automated checks** | Reviewers catch trivial issues | CI/CD with quality gates |
| **Large PRs** | Exponentially longer review time | Small, frequent PRs |
| **Infrequent reviews** | Isolated development; missed errors | Continuous, daily reviews |
| **Blame culture** | Defensive reactions; hidden problems | Blameless, learning-focused feedback |
| **Context switching** | Reviewers too busy to engage | Protect review time; minimize WIP |

### 6.3 Organizational Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Change Advisory Boards** | Negative impact on all DORA metrics | Peer review + automation |
| **External approvals** | Slows delivery; no quality benefit | Team-level authority |
| **Treating all changes equally** | Inefficient; can't focus on high-risk | Risk-based review intensity |
| **Silos between roles** | Handoffs; delays; finger-pointing | Cross-functional teams |
| **Pipeline ownership bottleneck** | Only DevOps understands CI/CD | Democratize pipeline knowledge |

---

## 7. Academic Research

### 7.1 Microsoft Research on Code Reviews

**Study:** "Characteristics of Useful Code Reviews" (Bosu, Greiler, Bird, 2015)

**Method:** Analyzed 1.5 million review comments across five Microsoft projects.

**Key Findings:**
- Useful comment proportion increases dramatically in reviewer's first year, then plateaus
- More files per change → lower proportion of valuable comments
- Primary purpose: improve quality by identifying defects, better approaches, maintainability
- Secondary benefits: knowledge dissemination, team awareness

### 7.2 Google Research on Code Reviews

**Study:** Modern Code Review at Google (Sadowski et al., 2018)

**Key Findings:**
- Primary reason for code review: improve code understandability and maintainability
- Mandatory reviews with readability certification
- Google's engineering practices prioritize review speed: "optimize for the speed at which a team of developers can produce a product together"

### 7.3 General Findings

| Finding | Source |
|---------|--------|
| Tool-assisted reviews yield ~2x more accepted comments than over-the-shoulder | Academic literature |
| Review turnaround should be <24 hours | Google Engineering Practices |
| Small PR size has exponential relationship with review time | LinearB research (4M review cycles, 25K developers) |
| PRs wait average 4+ days before pickup | LinearB study (~1M PRs) |
| Three dimensions of developer friction: feedback loops, cognitive load, flow state | Developer experience research |

---

## 8. Metrics to Track

### 8.1 Refinement Metrics

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Backlog depth** | 3-6 sprints | Avoids waste; ensures readiness |
| **Refinement time** | ≤10% capacity | Scrum Guide recommendation |
| **Story readiness** | 100% meet DoR | Prevents sprint disruption |
| **Rework rate** | Decreasing | Indicates refinement quality |

### 8.2 Review Metrics

| Metric | Elite Target | Why It Matters |
|--------|--------------|----------------|
| **PR pickup time** | <4 hours | Prevents bottleneck |
| **Review cycle time** | <24 hours | Maintains flow |
| **PR size** | <200 lines | Enables quality review |
| **Change failure rate** | <1% | Quality gate validation |

### 8.3 DORA Metrics

| Metric | Elite Benchmark |
|--------|-----------------|
| Deployment Frequency | Multiple per day |
| Lead Time for Changes | <1 hour |
| Change Failure Rate | <1% |
| Mean Time to Recovery | <1 hour |

---

## 9. Implementation Recommendations

### 9.1 For Refinement

1. **Establish rhythm**: Regular sessions at consistent times
2. **Prepare ahead**: PO conducts pre-refinement with SMEs
3. **Full team participation**: All developers, not just leads
4. **Define DoR**: Collaboratively; keep it lightweight
5. **Vertical slicing**: End-to-end user value, not horizontal layers
6. **Limit WIP**: 2 sprints ahead; 3-6 sprints backlog max
7. **Measure and improve**: Use retrospectives to refine the refinement process

### 9.2 For Peer Review

1. **Small PRs**: <200 lines; complete in single session
2. **Fast turnaround**: <24 hour target; prioritize reviews
3. **Automate the automatable**: Linting, security scanning, test coverage
4. **Distribute responsibility**: Avoid senior-only bottleneck
5. **Complete reviews**: Single-pass; no iterative nitpicking
6. **Provide context**: Clear PR descriptions; estimated review time
7. **Trunk-based development**: Merge daily; no long-lived branches

### 9.3 Organizational Enablers

1. **Eliminate CABs for routine changes**: Peer review + automation
2. **Trust teams**: Authority to make changes without external approval
3. **Protect review time**: Minimize context switching
4. **Foster psychological safety**: Blameless culture
5. **Measure outcomes, not output**: DORA metrics over activity metrics

---

## 10. Key Takeaways

1. **Peer review > External approval**: DORA research proves lightweight peer review outperforms heavyweight formal processes
2. **Speed enables quality**: Fast reviews (50% better delivery performance) don't sacrifice quality—they enable it
3. **Small batches are essential**: Smaller changes = faster reviews = lower risk = faster recovery
4. **Full team refinement**: All developers participate; not just leads or seniors
5. **Prepare but don't over-prepare**: 2 sprints ahead; DoR should enable, not block
6. **Distribute review responsibility**: Avoid bottlenecks; senior-only review is an anti-pattern
7. **Automate the automatable**: Let humans focus on logic, design, and architecture
8. **Measure to improve, not to blame**: Use metrics for continuous improvement
9. **Trunk-based development**: Merge daily; eliminate long integration phases
10. **Trust teams**: High performers can change specs during development without external permission

---

## Sources

### Official DORA Resources
- [DORA Streamlining Change Approval](https://dora.dev/capabilities/streamlining-change-approval/)
- [DORA Working in Small Batches](https://dora.dev/capabilities/working-in-small-batches/)
- [DORA Team Experimentation](https://dora.dev/capabilities/team-experimentation/)
- [DORA Visibility of Work in Value Stream](https://dora.dev/capabilities/work-visibility-in-value-stream/)
- [DORA Trunk-Based Development](https://dora.dev/capabilities/trunk-based-development/)
- [DORA Four Keys](https://dora.dev/guides/dora-metrics-four-keys/)

### Agile & Scrum Resources
- [Scrum.org - Product Backlog Refinement](https://www.scrum.org/resources/blog/scrum-trenches-product-backlog-refinement-scrum-team-responsibility)
- [Scrum.org - 27 Backlog Anti-Patterns](https://www.scrum.org/resources/blog/27-product-backlog-and-refinement-anti-patterns)
- [Scrum.org - Scrum Master Facilitation](https://www.scrum.org/resources/blog/scrum-master-master-art-facilitation)
- [Atlassian - Backlog Refinement](https://www.atlassian.com/agile/scrum/backlog-refinement)
- [Atlassian - Definition of Ready](https://www.atlassian.com/agile/project-management/definition-of-ready)
- [Scrum Inc - Definition of Ready](https://www.scruminc.com/definition-of-ready/)

### Code Review Research
- [Microsoft Research - Characteristics of Useful Code Reviews](https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/)
- [AWS DevOps Guidance - Code Review Anti-Patterns](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-code-review.html)
- [Yelp Engineering - Code Review Guidelines](https://engineeringblog.yelp.com/2017/11/code-review-guidelines.html)
- [Graphite - Understanding Code Review](https://graphite.dev/guides/understanding-code-review-software-engineering)

### Industry Analysis
- [LinearB - DORA Metrics](https://linearb.io/blog/dora-metrics)
- [LinearB - PR Pickup Time](https://linearb.io/blog/pull-request-pickup-time)
- [Stack Overflow - Engineering's Hidden Bottleneck: Pull Requests](https://stackoverflow.blog/2023/02/08/engineerings-hidden-bottleneck-pull-requests/)
- [Software.com - Code Reviews Bottleneck](https://www.software.com/src/code-reviews-bottleneck-in-your-delivery-pipeline)
- [GetDX - Pull Requests](https://getdx.com/blog/pull-request/)

### Community Resources
- [DORA Community - Code Reviews](https://dora.community/blog/Code%20Reviews)
- [Dojo Consortium - 24 DORA Capabilities](https://dojoconsortium.org/docs/dora-recommendations/)
- [Age of Product - Backlog Anti-Patterns](https://age-of-product.com/28-product-backlog-anti-patterns/)

---

*Report generated: 2026-01-02*
*Research methodology: Web search synthesis of DORA official publications, Scrum.org resources, academic research from Microsoft and Google, and industry analysis.*
