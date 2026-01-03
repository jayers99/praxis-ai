# Critical Scrum Team Roles: Backlog Refinement, Ticket Refinement, and Peer Review

<!--
metadata:
  id: roles-scrum-team-comprehensive-2026-01-02
  title: Critical Scrum Team Roles for Success
  date: 2026-01-02
  status: draft
  topic: roles
  keywords: [scrum, product owner, scrum master, developers, backlog refinement, ticket refinement, peer review, cross-functional, self-organizing, agile, sprint planning]
  consensus: strong
  depth: deep
  sources_count: 40+
-->

## Executive Summary

- The Scrum Guide (2020) defines exactly **three accountabilities**: Product Owner, Scrum Master, and Developers. No other roles exist in official Scrum.
- **Product Owner** is accountable for the Product Backlog, represents stakeholders, and defines "what" to build—but refinement is a team responsibility.
- **Scrum Master** serves as a facilitator and coach, removing impediments and ensuring Scrum is understood—but should not become a bottleneck or project manager.
- **Developers** are collectively responsible for delivering increments, self-organizing their work, estimation, and code quality—including peer review.
- Academic research (Verwijs & Russo, 2021) on 2,000+ Scrum teams identifies **five factors** for effectiveness: responsiveness, stakeholder concern, continuous improvement, team autonomy, and management support.
- **Psychological safety** (Google Project Aristotle) is the #1 predictor of team success—more important than individual talent or specific role expertise.
- Cross-functional teams should include all skills necessary to deliver value: development, testing, UX, and any other required expertise—all under "Developers."
- Backlog refinement should consume **no more than 10%** of the Developers' capacity, with the goal of achieving shared understanding of items before Sprint Planning.
- Peer code review is **not mentioned in the Scrum Guide** but is a widespread best practice, typically included in the Definition of Done.
- Common anti-patterns: absent Product Owner, Scrum Master as bottleneck, Developers waiting for assignments, hero culture, and treating velocity as a performance metric.

## Consensus Rating

**Strong**: The three Scrum roles are well-defined in the official Scrum Guide and widely accepted. There is strong consensus on:
1. Role boundaries and accountabilities
2. Backlog refinement as a team activity
3. Self-organization of Developers
4. Facilitation (not management) role of Scrum Master

Debate continues on: specific team compositions, how to integrate specialized skills (UX, QA), and whether additional roles (Tech Lead, Architect) are compatible with Scrum.

---

## The Three Official Scrum Roles

The [2020 Scrum Guide](https://scrumguides.org/scrum-guide.html) defines three, and only three, accountabilities within a Scrum Team:

| Role | Core Accountability | Relationship to Backlog |
|------|---------------------|------------------------|
| **Product Owner** | Maximizing value of the product | Owns and orders the Product Backlog |
| **Scrum Master** | Scrum Team effectiveness | Facilitates refinement, removes impediments |
| **Developers** | Creating Done Increments | Refine, estimate, and implement backlog items |

**Critical principle**: These are **accountabilities**, not job titles. One person may hold multiple accountabilities in some contexts, though the Product Owner and Scrum Master should typically be different people to avoid conflicts of interest.

---

## Product Owner

### Purpose and Accountability

The Product Owner is the **single person** accountable for maximizing the value of the product resulting from the work of the Scrum Team. They are the voice of the customer and stakeholders, responsible for:

- Developing and communicating the **Product Goal**
- Creating and clearly expressing **Product Backlog items**
- **Ordering** the Product Backlog to maximize value
- Ensuring the Product Backlog is **transparent, visible, and understood**

> "The Product Owner is one person, not a committee." — [Scrum Guide](https://scrumguides.org/scrum-guide.html)

### Role in Backlog Refinement

The Product Owner [owns the backlog refinement process](https://www.scrum.org/resources/blog/scrum-trenches-product-backlog-refinement-scrum-team-responsibility), but it is a **collaborative team effort**:

| Responsibility | Description |
|----------------|-------------|
| Vision communication | Start with the "Why" before anything else |
| Pre-refinement preparation | Work with stakeholders and SMEs to validate business value |
| Acceptance criteria | Collaborate with team to define clear, measurable criteria |
| Prioritization | Order items based on value, risk, and dependencies |
| Clarification | Answer team questions during refinement sessions |
| Backlog maintenance | Remove irrelevant items, keep backlog appropriately sized |

**Best practice**: [Limit the Product Backlog to about 100 items](https://age-of-product.com/28-product-backlog-anti-patterns/). An oversized backlog creates waste and cognitive overload.

**Time investment**: [1.5 hours per week is recommended](https://ancaonuta.medium.com/product-owners-checklist-for-product-backlog-refinement-d60364c960a7), with fixed time and frequency established at the beginning of the project.

### Role in Ticket/Story Refinement

During individual story refinement, the Product Owner:

1. **Explains the "Why"**: Business context and value proposition
2. **Defines acceptance criteria**: 3-5 criteria are typically sufficient
3. **Answers questions**: Available to clarify requirements
4. **Negotiates scope**: Works with Developers to right-size stories
5. **Validates understanding**: Confirms the team understands what's needed

**Anti-pattern**: Providing solutions ("the how") instead of problems ("the what"). The Product Owner [should not dictate implementation](https://big-agile.com/blog/anti-patterns-of-the-product-owner).

### Role in Peer Review

The Product Owner typically does **not participate directly** in code peer review. Their involvement is at the acceptance level:

- Verifying that completed work meets acceptance criteria
- Accepting or rejecting the Increment during Sprint Review
- Providing feedback on user-facing aspects of completed work

### Product Owner Anti-Patterns

| Anti-Pattern | Description | Impact |
|--------------|-------------|--------|
| [Absent Product Owner](https://www.scrum.org/resources/blog/anti-patterns-product-owner) | Not available to answer team questions | Team works in the dark, risking Sprint Goal |
| [Proxy Product Owner](https://www.scrum.org/resources/blog/anti-patterns-product-owner) | Lacks decision-making authority | Becomes a bottleneck, delays decisions |
| [The "Yes Man"](https://geniusee.com/single-blog/product-owner-anti-patterns) | Can't say no to stakeholders | Overloaded backlog, unrealistic expectations |
| [Part-time PO](https://medium.com/hackernoon/product-owner-anti-patterns-22ed1f989867) | Not working daily on the backlog | Backlog becomes stale, team lacks direction |
| [Copy & Paste PO](https://age-of-product.com/28-product-backlog-anti-patterns/) | Breaks requirements into tickets without understanding | "Ticket monkey" behavior, no value optimization |
| [Clinging to tasks](https://www.scrum.org/resources/blog/anti-patterns-product-owner) | Changes scope mid-Sprint | Disrupts team focus, risks Sprint Goal |
| [Dominant PO](https://geniusee.com/single-blog/product-owner-anti-patterns) | Makes all decisions without team input | Kills collaboration, ignores technical insights |
| [Technical overreach](https://www.scrum.org/resources/blog/anti-patterns-product-owner) | Dictates architecture and implementation | Undermines Developer autonomy |

---

## Scrum Master

### Purpose and Accountability

The Scrum Master is accountable for the **effectiveness of the Scrum Team**. They serve the team as a **servant-leader**, not as a manager or project lead:

- Ensuring Scrum is understood and enacted
- Helping the team focus on creating high-value Increments
- Removing impediments to progress
- Facilitating Scrum events as requested or needed
- Coaching the organization in Scrum adoption

> "The Scrum Master serves the Scrum Team in several ways, including coaching, facilitating, and helping establish empirical product planning." — [Scrum Guide](https://scrumguides.org/scrum-guide.html)

### Role in Backlog Refinement

The Scrum Master's role in refinement is [primarily facilitative](https://www.growingscrummasters.com/blog/how-does-a-scrum-master-facilitate-backlog-refinement/):

| Before Refinement | During Refinement | After Refinement |
|-------------------|-------------------|------------------|
| Help PO understand healthy backlog | Guide attention back to topics | Ensure action items are captured |
| Coach PO on articulating value | Notice conversation lulls | Track estimation accuracy over time |
| Ensure stories are prepared | Ensure engagement from all | Identify improvement opportunities |
| Set up tools and space | Implement time-boxes | Remove identified impediments |

**Key facilitation behaviors**:
- Ensure [everyone has opportunity to speak](https://age-of-product.com/scrum-master-anti-patterns/)
- Maintain psychological safety
- Ask probing questions
- Keep discussions focused and time-boxed
- [Observe for team members seeking eye contact before speaking](https://age-of-product.com/scrum-master-anti-patterns/)—a sign the SM has slipped into supervisor mode

**Ultimate goal**: [If the team is independent in refinement, "you've done a great job."](https://www.growingscrummasters.com/blog/what-is-the-role-of-the-scrum-master-in-backlog-refinement/)

### Role in Ticket/Story Refinement

During story-level refinement:

1. **Facilitates INVEST criteria**: Guides team to create Independent, Negotiable, Valuable, Estimable, Small, and Testable stories
2. **Supports estimation**: Ensures all voices are heard, discussions stay focused
3. **Identifies impediments**: Notes dependencies or blockers for resolution
4. **Tracks patterns**: Analyzes estimation accuracy to help team improve

**Anti-pattern**: [Providing technical inputs or influencing estimates](https://agilemania.com/scrum-master-antipatterns)—especially if the Scrum Master has a technical background.

### Role in Peer Review

The Scrum Master does **not directly participate** in code peer review, but may:

- Facilitate discussions about code review practices
- Help establish team agreements on review turnaround times
- Identify if code review is becoming an impediment (bottleneck)
- Coach team on making code review a learning opportunity

### Scrum Master Anti-Patterns

| Anti-Pattern | Description | Impact |
|--------------|-------------|--------|
| [Tech Lead Masquerading](https://www.scrum.org/resources/blog/anti-patterns-scrum-master) | Makes technical decisions, influences estimates | Undermines self-organization |
| [The Bottleneck](https://www.scrum.org/resources/blog/anti-patterns-scrum-master) | All communication runs through SM | Slows team, creates dependency |
| [Laissez-faire](https://www.scrum.org/resources/blog/anti-patterns-scrum-master) | No boundaries, anything goes | Team becomes undisciplined |
| [Conflict Avoidance](https://age-of-product.com/scrum-master-anti-patterns/) | Sweeps problems under the rug | Issues fester, team health degrades |
| [Allowing Micro-management](https://age-of-product.com/scrum-master-anti-patterns/) | Lets others assign tasks to engineers | Destroys self-organization |
| [The Messenger](https://agilemania.com/scrum-master-antipatterns) | Relays information instead of enabling direct communication | Becomes bottleneck |
| [Solving all impediments](https://worldofagile.com/blog/anti-pattern-scrum-master-solver-of-all-impediments/) | Takes on every impediment personally | Team doesn't learn to solve problems |
| [Status Report Daily Scrum](https://www.scrum.org/resources/blog/27-sprint-anti-patterns) | Turns Daily Scrum into reporting meeting | Misses purpose of team coordination |

---

## Developers

### Purpose and Accountability

Developers are the people in the Scrum Team committed to creating any aspect of a usable Increment each Sprint. They are accountable for:

- Creating a plan for the Sprint (Sprint Backlog)
- Instilling quality by adhering to a Definition of Done
- Adapting their plan each day toward the Sprint Goal
- Holding each other accountable as professionals

> "Scrum Teams are cross-functional, meaning the members have all the skills necessary to create value each Sprint." — [Scrum Guide](https://scrumguides.org/scrum-guide.html)

**Note on terminology**: "Developers" in Scrum includes **anyone** who does work to create the Increment—programmers, testers, designers, analysts, etc. There is [no division between dev, operations, and QA in Scrum](https://www.qamadness.com/software-testing-in-scrum/).

### Role in Backlog Refinement

Developers [actively participate in refinement](https://www.scrum.org/resources/blog/product-backlog-refinement-explained-23), contributing:

| Activity | Developer Responsibility |
|----------|-------------------------|
| Technical feasibility | Identify risks, dependencies, and constraints |
| Estimation | Provide size estimates (story points, t-shirt sizes) |
| Decomposition | Break large items into implementable pieces |
| Spike identification | Recommend spikes for high-uncertainty items |
| Technical debt | Advocate for debt reduction work |
| Creative solutions | Propose approaches to meet Sprint Goals |

**Time investment**: [Up to 10% of Developers' capacity](https://www.scrum.org/resources/blog/product-backlog-refinement-explained-13) should be reserved for refinement.

**Key principle**: [How work is decomposed is at the sole discretion of the Developers](https://www.simpliaxis.com/resources/scrum-developer-roles-and-responsibilities). No one else tells them how to turn Product Backlog items into Increments.

### Role in Ticket/Story Refinement

During story-level refinement:

1. **Ask clarifying questions**: Ensure understanding of requirements
2. **Identify edge cases**: Surface scenarios the PO may not have considered
3. **Estimate collaboratively**: Use Planning Poker with simultaneous reveal
4. **Define technical approach**: Discuss "how" after understanding "what"
5. **Identify dependencies**: Note cross-team or technical dependencies
6. **Challenge assumptions**: Question scope if effort seems disproportionate

**Estimation guidance**:
- [Use simultaneous reveal to prevent anchoring](https://www.mountaingoatsoftware.com/agile/planning-poker)
- Discrepancies point to differences in understanding
- [Timeboxing to 2-3 minutes per item prevents over-analysis](https://planningpoker.live/knowledge-base/planning-poker-guide-agile-estimation-techniques)

### Role in Peer Review

Code review is [not mentioned in the Scrum Guide](https://www.scrum.org/forum/scrum-forum/40055/pull-requests-reviews-team) but is a widespread best practice. Developers are responsible for:

| Practice | Description |
|----------|-------------|
| Reviewing each other's code | All Developers share responsibility |
| Timely turnaround | First review within 4 hours, completion within 24 hours |
| Quality standards | Adherence to team coding standards and Definition of Done |
| Mentoring through review | Teaching, not gatekeeping |
| Distributed reviews | No single person should review all code |

**Best practice**: [Consider having pairs of developers work together](https://www.scrum.org/forum/scrum-forum/40055/pull-requests-reviews-team), where one develops a feature and the other is the primary reviewer. This ensures context and commitment.

**Anti-pattern**: [Cherry-picking work while PRs queue up](https://www.scrum.org/resources/blog/27-sprint-anti-patterns)—a sign the team views work individually rather than collectively.

### Developer Anti-Patterns

| Anti-Pattern | Description | Impact |
|--------------|-------------|--------|
| [Overcommitment](https://www.scrum.org/resources/blog/development-team-anti-patterns) | Taking on too many tasks | Rushed work, missed Sprint Goals |
| [Insufficient refinement](https://www.scrum.org/resources/blog/development-team-anti-patterns) | Not reserving 10% for refinement | Low-quality backlog, unclear stories |
| [Cherry-picking](https://www.scrum.org/resources/blog/27-sprint-anti-patterns) | Grabbing preferred tasks, ignoring reviews | Code review bottleneck, unbalanced work |
| [No WiP limit](https://age-of-product.com/scrum-sprint-planning-anti-patterns/) | Too much work in progress | Flow problems, context switching |
| [Waiting for assignments](https://age-of-product.com/development-team-anti-patterns/) | Not self-organizing | Dependency on "team lead," slow response |
| [Excluding the PO](https://www.scrum.org/resources/blog/development-team-anti-patterns) | Not inviting PO to retrospectives | Team silos, missed alignment |
| [Velocity as performance](https://www.easyagile.com/blog/agile-scrum-sprint-anti-patterns-team-collaboration) | Gaming velocity numbers | Inflated estimates, focus on output not value |
| [Technical debt ignored](https://age-of-product.com/scrum-sprint-planning-anti-patterns/) | Not allocating time for refactoring | Growing debt, slowing velocity |

---

## Cross-Functional Team Composition

### What Cross-Functional Means

[A cross-functional team has all skills necessary to deliver value](https://www.scrum.org/resources/blog/unraveling-significance-cross-functional-scrum) each Sprint. This does **not** mean each member has all skills—it means the **team collectively** has them.

### Common Specializations Within "Developers"

All of these are considered "Developers" in Scrum terminology:

| Specialization | Role in Refinement | Role in Peer Review |
|----------------|-------------------|---------------------|
| **Programmers** | Technical feasibility, estimation, decomposition | Primary code reviewers |
| **QA/Testers** | Testability assessment, acceptance criteria validation | Review test coverage, test quality |
| **UX Designers** | Design input, interaction questions, usability concerns | Review UI implementation fidelity |
| **DevOps/SRE** | Infrastructure dependencies, deployment considerations | Review operational concerns |
| **DBAs** | Data model implications, performance considerations | Review data access patterns |

### QA/Tester Integration

[There is no separate "tester" role in Scrum](https://www.scrum.org/resources/blog/role-professional-tester-agile-world)—testers are Developers. The professional tester's role is:

- **Quality coach**: Helping team understand testing practices
- **Acceptance criteria collaboration**: Working with PO to define criteria
- **Test strategy**: Defining how stories will be tested
- **Whole-team quality**: [The entire team is responsible for QA](https://www.qamadness.com/software-testing-in-scrum/)

### UX Designer Integration

[UX designers should be full Scrum Team members](https://www.scrum.org/resources/blog/integrating-ux-design-scrum-framework-stop-rework), not a separate team:

- Participate in refinement for design input
- Pair with Developers during implementation
- Attend Sprint Reviews for feedback
- Join retrospectives for process improvement

**Anti-pattern**: [Splitting UX into a separate team with different timelines](https://www.scrum.org/resources/blog/integrating-ux-design-scrum-framework-stop-rework)—a recipe for waste, rework, and frustration.

### T-Shaped Skills

Scrum teams benefit from ["T-shaped" team members](https://www.scrum.org/resources/blog/unraveling-significance-cross-functional-scrum)—deep expertise in one area with broader skills in related areas. This promotes:
- Flexibility and adaptability
- Reduced bottlenecks
- Shared responsibility
- Collective ownership

---

## Academic Research on Team Effectiveness

### "A Theory of Scrum Team Effectiveness" (Verwijs & Russo, 2021)

[This peer-reviewed study](https://dl.acm.org/doi/10.1145/3571849) analyzed data from approximately 5,000 developers and 2,000 Scrum teams.

**Five high-level factors for effectiveness:**

| Factor | Description |
|--------|-------------|
| **Responsiveness** | Ability to respond to changing needs quickly |
| **Stakeholder Concern** | Focus on delivering value to stakeholders |
| **Continuous Improvement** | Regular reflection and adaptation |
| **Team Autonomy** | Self-organization and decision-making authority |
| **Management Support** | Active backing from organizational leadership |

**Key findings**:
- Adoption of Agile practices is a critical success factor
- Project size did not matter
- Scrum Master leadership significantly contributes to success
- Shared understanding of value (value congruence) is important

### Team Maturity Research

[A study of 182 Scrum team members](https://www.sciencedirect.com/science/article/pii/S0950584922001884) found that success depends on team maturity:

| Factor | Impact |
|--------|--------|
| Fully allocated team members | Positive |
| Low turnover rates | Positive |
| Required skills and expertise | Positive |
| Self-management capability | Positive |
| Working in accordance with Scrum values (openness, courage) | Positive |

### Personality and Team Traits

Effective Scrum team members typically show traits of:
- Altruism
- Compliance
- Tender-mindedness
- Dutifulness
- Openness to values

### Google Project Aristotle Findings

[Google's research on 180+ teams](https://rework.withgoogle.com/intl/en/guides/understanding-team-effectiveness) found **psychological safety** is the #1 predictor of team success:

- 43% of variance in team performance
- 19% higher productivity
- 31% more innovation
- High-performing teams showed equality in conversational turn-taking

---

## Definition of Ready vs. Definition of Done

### Definition of Done (DoD)

The Definition of Done is [required in Scrum](https://www.scrum.org/resources/blog/what-difference-between-definition-done-dod-and-definition-ready-dor) and creates transparency by providing a shared understanding of what "complete" means:

- Owned by the Developers
- Applies to all Increments
- Must be met before work is considered Done
- Typically includes: code review, tests passing, documentation updated, deployed to staging

### Definition of Ready (DoR)

The Definition of Ready is [NOT part of the Scrum Guide](https://www.scrum.org/resources/blog/why-isnt-definition-ready-described-scrum-guide) and can lead to problems:

**Potential benefits**:
- Ensures stories are actionable
- Reduces mid-sprint clarification needs

**Potential problems**:
- Can become a gatekeeping mechanism
- May shift responsibility inappropriately
- Creates phase-gate thinking contrary to Agile principles

**Recommendation**: Use [Backlog Refinement as an activity](https://www.scrum.org/resources/blog/why-isnt-definition-ready-described-scrum-guide) rather than DoR as a sequential checklist.

---

## Stakeholder Engagement

### Who Are Stakeholders?

[Stakeholders](https://www.scrum.org/resources/blog/scrum-who-are-key-stakeholders-should-be-attending-every-sprint-review) are people external to the Scrum Team with specific interest in and knowledge of the product:
- Customers and users
- Executives and sponsors
- Subject matter experts
- Other teams with dependencies

### Stakeholder Involvement in Scrum Events

| Event | Stakeholder Role |
|-------|------------------|
| Sprint Planning | Generally not present |
| Daily Scrum | Not present (Developers only) |
| Backlog Refinement | Invited when relevant knowledge needed |
| Sprint Review | **Required**—primary feedback opportunity |
| Retrospective | Not present (Scrum Team only) |

### Best Practices for Sprint Review

- [Schedule mid-week, not Friday](https://www.eficode.com/blog/revitalize-scrum-sprint-reviews-overcome-stakeholder-apathy)
- Include agenda with calendar invitation
- [Hand stakeholders the keyboard](https://www.mountaingoatsoftware.com/blog/top-7-ways-to-get-stakeholders-to-attend-sprint-reviews)—let them experiment
- Plan conversation breaks after demonstrations
- Use less technical language
- [Focus on what needs feedback, not exhaustive demos](https://www.mountaingoatsoftware.com/blog/top-7-ways-to-get-stakeholders-to-attend-sprint-reviews)

---

## Best Practices Summary

### For Product Owners

1. **Be available**—answer team questions daily
2. **Focus on "what" and "why"**, let team determine "how"
3. **Keep backlog appropriately sized** (~100 items max)
4. **Define clear acceptance criteria** (3-5 per story)
5. **Participate in refinement** but don't dominate
6. **Protect the Sprint**—avoid scope changes mid-Sprint
7. **Validate understanding** before Sprint Planning

### For Scrum Masters

1. **Facilitate, don't manage**—enable team self-organization
2. **Ensure equal speaking time** in all discussions
3. **Cause impediments to be removed**—don't solve everything yourself
4. **Protect psychological safety**—address bullying and dominance
5. **Coach toward independence**—work yourself out of a job
6. **Observe without supervising**—notice when team seeks your approval
7. **Track patterns**—help team improve estimation accuracy

### For Developers

1. **Self-organize**—don't wait for task assignments
2. **Reserve 10% for refinement**—invest in backlog quality
3. **Estimate collaboratively**—use simultaneous reveal
4. **Review code promptly**—<4 hours first response, <24 hours completion
5. **Mentor through reviews**—teach, don't gatekeep
6. **Limit work in progress**—focus on flow, not individual output
7. **Allocate 15-20% for technical debt**—maintain code health
8. **Own quality collectively**—testing is everyone's job

### For Cross-Functional Teams

1. **Include all necessary skills**—don't create dependencies on external teams
2. **Develop T-shaped skills**—reduce bottlenecks
3. **Integrate UX and QA**—don't treat as separate teams
4. **Share responsibility**—the team wins or fails together
5. **Communicate directly**—don't route through Scrum Master

---

## Role Interaction Matrix

How each role relates to key activities:

| Activity | Product Owner | Scrum Master | Developers |
|----------|---------------|--------------|------------|
| **Backlog Refinement** | Owns, clarifies, prioritizes | Facilitates, time-boxes | Estimates, decomposes, questions |
| **Story Writing** | Defines "what" and "why" | Coaches on INVEST criteria | Contributes technical perspective |
| **Acceptance Criteria** | Owns, defines with team | Ensures clarity | Validates testability |
| **Estimation** | Observes, doesn't influence | Facilitates, ensures voices heard | Performs estimation |
| **Sprint Planning** | Orders backlog, explains goal | Facilitates event | Creates Sprint Backlog |
| **Code Review** | Not involved | Monitors for bottlenecks | Performs reviews |
| **Definition of Done** | Provides input | Ensures transparency | Owns and enforces |
| **Sprint Review** | Demonstrates value delivered | Facilitates | Presents work, gathers feedback |

---

## Sources

### Primary Sources (Official/Peer-Reviewed)

1. [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html) — Official Scrum framework definition
2. [A Theory of Scrum Team Effectiveness (Verwijs & Russo, 2021)](https://dl.acm.org/doi/10.1145/3571849) — Peer-reviewed research on 2,000+ teams
3. [Mastering Scrum with Team Maturity (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0950584922001884) — Academic study on team composition
4. [Google re:Work - Project Aristotle](https://rework.withgoogle.com/intl/en/guides/understanding-team-effectiveness) — Team effectiveness research
5. [arXiv: A Theory of Scrum Team Effectiveness](https://arxiv.org/abs/2105.12439) — Preprint of effectiveness research

### Secondary Sources (Scrum.org)

6. [Product Backlog Refinement Explained (1/3)](https://www.scrum.org/resources/blog/product-backlog-refinement-explained-13)
7. [Product Backlog Refinement Explained (2/3)](https://www.scrum.org/resources/blog/product-backlog-refinement-explained-23)
8. [Refinement is a Team Responsibility](https://www.scrum.org/resources/blog/scrum-trenches-product-backlog-refinement-scrum-team-responsibility)
9. [Product Owner Anti-Patterns](https://www.scrum.org/resources/blog/anti-patterns-product-owner)
10. [Scrum Master Anti-Patterns](https://www.scrum.org/resources/blog/anti-patterns-scrum-master)
11. [Development Team Anti-Patterns](https://www.scrum.org/resources/blog/development-team-anti-patterns)
12. [27 Sprint Anti-Patterns](https://www.scrum.org/resources/blog/27-sprint-anti-patterns)
13. [20 Sprint Planning Anti-Patterns](https://www.scrum.org/resources/blog/20-sprint-planning-anti-patterns)
14. [Cross-Functional Teams in Scrum](https://www.scrum.org/resources/blog/unraveling-significance-cross-functional-scrum)
15. [Definition of Ready vs Done](https://www.scrum.org/resources/blog/what-difference-between-definition-done-dod-and-definition-ready-dor)
16. [Professional Tester in Agile](https://www.scrum.org/resources/blog/role-professional-tester-agile-world)
17. [Integrating UX Design into Scrum](https://www.scrum.org/resources/blog/integrating-ux-design-scrum-framework-stop-rework)
18. [Stakeholders in Sprint Review](https://www.scrum.org/resources/blog/scrum-who-are-key-stakeholders-should-be-attending-every-sprint-review)

### Industry Sources

19. [Atlassian - Scrum Roles](https://www.atlassian.com/agile/scrum/roles)
20. [Atlassian - Backlog Refinement](https://www.atlassian.com/agile/scrum/backlog-refinement)
21. [Mountain Goat Software - Planning Poker](https://www.mountaingoatsoftware.com/agile/planning-poker)
22. [Mountain Goat Software - Sprint Review Attendance](https://www.mountaingoatsoftware.com/blog/top-7-ways-to-get-stakeholders-to-attend-sprint-reviews)
23. [Age of Product - Development Team Anti-Patterns](https://age-of-product.com/development-team-anti-patterns/)
24. [Age of Product - Scrum Master Anti-Patterns](https://age-of-product.com/scrum-master-anti-patterns/)
25. [Age of Product - Product Backlog Anti-Patterns](https://age-of-product.com/28-product-backlog-anti-patterns/)
26. [Age of Product - Sprint Planning Anti-Patterns](https://age-of-product.com/scrum-sprint-planning-anti-patterns/)
27. [Growing Scrum Masters - PO Role in Refinement](https://www.growingscrummasters.com/blog/what-is-the-role-of-the-product-owner-in-backlog-refinement/)
28. [Growing Scrum Masters - SM Role in Refinement](https://www.growingscrummasters.com/blog/how-does-a-scrum-master-facilitate-backlog-refinement/)
29. [Agilemania - Scrum Master Anti-Patterns](https://agilemania.com/scrum-master-antipatterns)
30. [Geniusee - Product Owner Anti-Patterns](https://geniusee.com/single-blog/product-owner-anti-patterns)
31. [Medium - Product Owner Anti-Patterns](https://medium.com/hackernoon/product-owner-anti-patterns-22ed1f989867)
32. [Easy Agile - Sprint Anti-Patterns](https://www.easyagile.com/blog/agile-scrum-sprint-anti-patterns-team-collaboration)
33. [World of Agile - SM as Impediment Solver](https://worldofagile.com/blog/anti-pattern-scrum-master-solver-of-all-impediments/)
34. [Scrum Forum - Pull Requests](https://www.scrum.org/forum/scrum-forum/40055/pull-requests-reviews-team)
35. [QA Madness - Testing in Scrum](https://www.qamadness.com/software-testing-in-scrum/)
36. [NN/g - UX Responsibilities in Scrum](https://www.nngroup.com/articles/ux-scrum/)
37. [Planning Poker Live - Estimation Guide](https://planningpoker.live/knowledge-base/planning-poker-guide-agile-estimation-techniques)
38. [Eficode - Sprint Review Engagement](https://www.eficode.com/blog/revitalize-scrum-sprint-reviews-overcome-stakeholder-apathy)
39. [Scrum Alliance - Scrum Team](https://resources.scrumalliance.org/Article/scrum-team)
40. [Coursera - Scrum Roles](https://www.coursera.org/articles/scrum-roles-and-responsibilities)

---

## Research Gaps

The following areas have limited research coverage:

1. **Optimal team composition**: What mix of skills and experience levels produces best outcomes?

2. **Remote/hybrid team dynamics**: How do Scrum roles adapt to distributed teams?

3. **Scaling role interactions**: How do role responsibilities change in scaled frameworks (SAFe, LeSS)?

4. **AI impact on roles**: How will AI tools change the responsibilities of each role?

5. **Role transitions**: Best practices for transitioning from project management to Scrum Master or Product Owner roles.

---

_Generated by Claude Code research_
_Status: draft (pending review)_
