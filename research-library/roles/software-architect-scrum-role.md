# Software Architect Role in Scrum Teams

A comprehensive analysis of the Software Architect role within Scrum and Agile teams, focusing on backlog grooming, ticket refinement, and peer review responsibilities.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [First Principles](#first-principles)
3. [Role Definition and Position](#role-definition-and-position)
4. [Best Practices](#best-practices)
5. [Backlog Grooming and Refinement](#backlog-grooming-and-refinement)
6. [Peer Review and Code Review](#peer-review-and-code-review)
7. [Prior Art and Expert Consensus](#prior-art-and-expert-consensus)
8. [Academic Research](#academic-research)
9. [Anti-Patterns](#anti-patterns)
10. [SAFe Framework Perspective](#safe-framework-perspective)
11. [Summary and Recommendations](#summary-and-recommendations)
12. [Sources](#sources)

---

## Executive Summary

The Software Architect role in Scrum presents a fundamental tension: the Scrum Guide does not explicitly define an "architect" role, yet the need for architectural guidance—especially at scale—is well-documented in industry practice and academic research. The resolution lies in viewing architecture as a **team responsibility** that may be concentrated in certain individuals, rather than an ivory tower function separated from development.

Modern consensus holds that architects in Agile contexts must be **hands-on, collaborative, and embedded** within the team. They guide rather than dictate, participate in ceremonies, and maintain a balance between intentional architectural planning and emergent design driven by the team.

---

## First Principles

### Agile Manifesto Alignment

The architect's role must align with core Agile principles:

1. **"The best architectures, requirements, and designs emerge from self-organizing teams"** (Principle 11 of the Agile Manifesto)
   - Architecture is a team responsibility, not solely the architect's domain
   - The architect facilitates emergence rather than prescribing solutions

2. **Working software over comprehensive documentation**
   - Architectural decisions should be validated through working code
   - Living architecture evolves with the system

3. **Responding to change over following a plan**
   - Architecture must support change while controlling complexity
   - Evolutionary architecture embraces iterative refinement

### Fundamental Responsibilities

At their core, Software Architects are responsible for:

- **Understanding the business and system needs** and translating them into technical solutions
- **Creating system designs** that can be built within time and budget constraints
- **Balancing goals and constraints** across the entire solution
- **Ensuring technical coherence** across teams and sprints
- **Extrapolating requirements** from short-term into the future while teams focus on delivery

### The Architecture Paradox

> "The architect must consider change and complexity while other developers focus on the next delivery."

This creates a productive tension: the architect holds the long view while respecting the team's autonomy in day-to-day decisions.

---

## Role Definition and Position

### Official Scrum Guide Position

The Scrum Guide does not explicitly name the role "Software Architect." Instead, Scrum uses the term "Developers" broadly:

> "Developers in Scrum are used not to exclude, but to simplify—it includes developers, researchers, analysts, scientists, and other specialists."

Those who participate in the development process from outside the Scrum Team are considered **Stakeholders**, which can include Business Analysts and Architects.

### Practical Team Positioning

In practice, architects in Scrum typically operate in one of three modes:

| Mode | Description | Pros | Cons |
|------|-------------|------|------|
| **Embedded Team Member** | Full Scrum Team member, participates in all ceremonies | Tight feedback loop, deep context | Risk of narrow focus |
| **Consulting Specialist** | Available to multiple teams, joins key sessions | Broad perspective, cross-team alignment | Less context on individual teams |
| **Pairing Partner** | Never owns stories independently, pairs with developers | Stays close to delivery without owning work | Scheduling challenges |

### Key Responsibilities

1. **Translate business requirements** into technical solutions
2. **Develop non-functional requirements** (NFRs)
3. **Document and communicate** technology, architecture, and design decisions
4. **Work with stakeholders** to find trade-offs between possible solutions
5. **Guide and mentor developers** on design patterns, best practices, and standards
6. **Participate actively** in Scrum ceremonies

---

## Best Practices

### Architecture as Team Responsibility

> "The best architectures, designs, and requirements emerge from self-organizing teams."

- **Foster collaboration instead of delegation**—guide architects to work *with* teams on architecture challenges, not *for* them
- A self-managing team should debate and agree on future-state architecture together
- The architect acts as guide and mentor, respecting developers' autonomy and encouraging self-organization

### Active Participation

Architects should be present and active:

- **Daily stand-ups**: Share blockers, provide technical context
- **Sprint Planning**: Help estimate, identify dependencies, assess achievability
- **Sprint Reviews**: Validate architectural decisions against delivered increments
- **Backlog Refinement**: Provide technical guidance, identify enablers

### Maintaining Hands-On Skills

> "Non-coding architects, sometimes called 'PowerPoint architects' or 'astronaut architects,' may use archibabble and talkitecture to convince non-technical stakeholders of their expertise while delegating the unsolved, real problems to developers."

Best practice is for architects to:

- **Write code** regularly, even if not owning full stories
- **Pair with developers** on complex implementations
- **Participate in code reviews** to stay connected to the codebase
- **Build prototypes** to validate architectural decisions

### Balancing Big Picture and Details

When pairing or performing code reviews, the architect should:

- Drive the **essence of the need**, not every detail
- Guide toward **architectural direction** and enforce coding standards
- Allow **some poetic license**—there are many valid ways to code even simple logic
- Focus on **systemic concerns**: scalability, security, maintainability

---

## Backlog Grooming and Refinement

### Architect's Role in Refinement

Backlog refinement (formerly "grooming") is the ongoing process of reviewing, ranking, and editing the product backlog to ensure items are ready for development.

**Key participants** typically include:
- Product Owner
- Development Team
- Scrum Master
- **Architects** (part of the "product ownership circle")

The architect contributes to refinement by:

1. **Identifying architectural enablers** that need to precede features
2. **Flagging technical risks** and constraints early
3. **Defining non-functional requirements** (NFRs) for stories
4. **Helping split large stories** along technical and value dimensions
5. **Ensuring Definition of Ready** includes necessary technical criteria

### Story Splitting Guidance

Architects should guide teams toward **vertical slicing** rather than horizontal/layered splits:

| Approach | Description | Architect's Role |
|----------|-------------|------------------|
| **Vertical Slice** | Thin end-to-end functionality | Ensure each slice is technically complete |
| **Horizontal Slice** | Layer-by-layer (UI, API, DB) | **Discourage**—fails "Independent" and "Valuable" criteria |
| **INVEST Criteria** | Independent, Negotiable, Valuable, Estimable, Small, Testable | Help assess technical feasibility |

The **SPIDR technique** (Mike Cohn) offers five patterns for splitting:
- **S**pike
- **P**ath
- **I**nterface
- **D**ata
- **R**ules

### Technical Debt in Refinement

Architects play a crucial role in surfacing technical debt:

- **Distinguish** between actual technical debt, desired architectural changes, and new features
- **Estimate tech stories** in backlog grooming using the same scale as feature work
- **Advocate** for allocating 15-20% of sprint capacity to debt reduction
- **Help the team understand background** and moderate technical discussions

> "All tasks related to dealing with technical debt should be part of the Product Backlog—there is no shadow accounting in Scrum."

### Non-Functional Requirements (NFRs)

Architects are often responsible for establishing NFRs:

| NFR Category | Architect's Contribution |
|--------------|-------------------------|
| Performance | Define response time, throughput targets |
| Scalability | Establish capacity requirements |
| Security | Specify authentication, authorization, compliance |
| Availability | Set uptime guarantees, fault tolerance expectations |
| Maintainability | Define code quality, testability standards |

NFRs should be:
- **Bounded** with specific context
- **Independent** for isolated testing
- **Negotiable** for economic trade-offs
- **Testable** with objective measures

---

## Peer Review and Code Review

### Architect's Role in Code Review

Code reviews provide architects a mechanism to:

- Stay **involved in the source code**
- **Mentor and coach** team members
- **Promote best practices** and standards
- Ensure **architectural alignment** of implementations

### Architecture-Level Code Review

> "First and most important should be an architecture-focused code review. This level of review should be done mainly by the most experienced programmers who understand the project's architecture."

Architecture-level reviewers focus on:

- **Scalability and reusability** of proposed changes
- **Application security** concerns
- **Consistency** with established patterns
- **Technical debt** implications
- **Non-functional requirement** adherence

### Best Practices for Architect Code Reviews

1. **Avoid unidirectional reviewing**—seniors should also be reviewed by juniors
2. **Review small chunks**—limit to code that can be understood in 20 minutes
3. **Focus on architecture, not syntax**—let automated tools catch trivial issues
4. **Be a reviewer, not a rewriter**—it's code review, not code rewrite
5. **Establish consistent standards**—reduce variation between reviewers
6. **Review frequently**—don't let changes accumulate

### Code Review Anti-Patterns to Avoid

| Anti-Pattern | Description | Remedy |
|--------------|-------------|--------|
| **Rewriting code** | Taking over and rewriting someone's work | Suggest, don't rewrite; respect author ownership |
| **Reviewing huge chunks** | Large PRs reviewed in one session | Request smaller, focused PRs |
| **Infrequent reviews** | Reviews happen only occasionally | Make code review a daily practice |
| **Excessive reviewers** | Too many reviewers cause bottlenecks | Define practical reviewer count by complexity |
| **Inconsistent standards** | Each reviewer has different pet peeves | Document and align on review criteria |
| **Lack of automation** | Manual review of trivial issues | Use linters, formatters, static analysis |

---

## Prior Art and Expert Consensus

### Martin Fowler on Evolutionary Architecture

Martin Fowler, co-author of the Agile Manifesto and author of foundational software architecture texts, advocates for **evolutionary architecture**:

> "Good architecture is something that supports its own evolution, and is deeply intertwined with programming."

Key principles from Fowler's work:

1. **Architecture should evolve** through constant effort working closely with programming
2. **Continuous Delivery** enables practical evolutionary architecture
3. **Refactoring is essential**—good architecture isn't achieved the first time
4. **Start with a monolith**—microservices built from scratch often fail

### The Rise of Continuous Architecture

Modern approaches gaining traction:

- **Continuous Architecture**: Shorter feedback loops during design
- **Evolutionary Architecture**: Fitness functions validate architectural qualities
- **Architecture Decision Records (ADRs)**: Lightweight documentation of decisions

### Industry Consensus

The software industry has converged on several key points:

1. **Architects must code**—non-coding architects become disconnected
2. **Architecture is a team sport**—not an individual's exclusive domain
3. **Emergent design needs guidance**—pure emergence doesn't scale
4. **Intentional + Emergent balance**—the "meet-in-the-middle" approach
5. **Architects should be present daily** on agile teams

---

## Academic Research

### Scaling Agile Frameworks

Research investigating architects in scaled agile frameworks (ResearchGate: "Investigating the Role of Architects in Scaling Agile Frameworks") finds:

> "For large teams, the role of an architect is a necessity."

Key findings:
- Some architectural planning prevents excessive redesign and functional redundancy
- Effective evolution requires trade-offs between emergent and intentional design
- Close collaboration between agile and architecture teams is critical

### Emergent vs. Intentional Architecture

Academic literature (ScienceDirect, SpringerLink) explores the tension:

| Approach | Definition | When Appropriate |
|----------|------------|------------------|
| **Emergent** | Architecture evolves through refactoring and TDD | Small projects, single teams |
| **Intentional** | Planned strategies for cross-team alignment | Large solutions, multiple ARTs |
| **Hybrid** | "Meet-in-the-middle"—balance both approaches | Most real-world scenarios |

> "Projects that apply only Principle 11 result in architectures that usually require significant refactoring as new requirements emerge. For larger systems, some architecture planning and governance are required up front."

### Team Boundaries and Architecture

Research highlights a key limitation of pure emergence:

> "It is not possible for individual teams to understand the whole system landscape and avoid unnecessary or conflicting design decisions. Teams alone may not be able to see the big picture."

---

## Anti-Patterns

### Ivory Tower Architect

**Description**: Architect disconnected from actual implementation, making pronouncements no one follows.

**Symptoms**:
- Creates architecture based on perfect-world assumptions
- Doesn't work closely with developers
- Engages in "high visibility, low value work"
- Relies on politics rather than technical skills to stay relevant

**Remedy**: Embed in team, write code, pair with developers

### Architecture Astronaut

**Description**: So focused on abstraction that practical implementation suffers.

> "Architecture Astronauts find it very hard to write code or design programs, because they won't stop thinking about Architecture. They're astronauts because they are above the oxygen level."

**Symptoms**:
- Over-engineering and premature abstraction
- "Archibabble and talkitecture"
- Designs that never get implemented
- Technology selection for resume building

**Remedy**: Ground decisions in working software, prototype first

### PowerPoint Architect

**Description**: Produces slides and diagrams but never code.

**Symptoms**:
- Can't explain implementation details
- Delegates all "hard problems" to developers
- Out of touch with modern tooling and practices

**Remedy**: Require hands-on coding time, participate in code reviews

### Bottleneck Architect

**Description**: All technical decisions must flow through a single person.

**Symptoms**:
- Long wait times for architectural guidance
- Teams blocked on architect availability
- Architect becomes exhausted and decisions suffer

**Remedy**: Distribute architectural knowledge, empower team decisions

### Cherry-Picking Reviews

**Description**: Architect only reviews "interesting" work.

**Symptoms**:
- Critical but mundane code goes unreviewed
- Team feels architect is disconnected
- Architectural drift in "boring" areas

**Remedy**: Balanced review distribution, systematic approach

### Big Design Up Front (BDUF)

**Description**: Extensive architecture planning before any code is written.

**Symptoms**:
- Lengthy design phases delay delivery
- Designs become obsolete before implementation
- Poor fit with emergent requirements

**Remedy**: Iterative architecture, last responsible moment decisions

### No Architect at Scale

**Description**: Assuming pure team-based architecture works for large systems.

**Symptoms**:
- Conflicting technical decisions across teams
- Redundant implementations
- Integration failures
- Accumulated technical debt

**Remedy**: Introduce coordinating architect role while preserving team autonomy

---

## SAFe Framework Perspective

SAFe (Scaled Agile Framework) is notable for explicitly naming architect roles:

### Three Architect Levels

| Role | Level | Focus |
|------|-------|-------|
| **Enterprise Architect** | Portfolio | Broadest view, thinnest depth |
| **Solution Architect** | Large Solution | Cross-ART coordination |
| **System Architect** | ART/Team | Deepest technical knowledge |

### System Architect in SAFe

Primary responsibilities:
- Define solution's architectural and technical orientations
- Establish non-functional requirements and enablers
- Build technological hypotheses and evaluate alternatives
- Maintain the **Architectural Runway**
- Participate in PI Planning, System Demo, SoS

### Key SAFe Principles for Architects

1. **Not an ivory tower role**—integrated part of Agile Release Trains
2. **Hands-on and in service**—to customer, organization, and teams
3. **Coaching and connecting**—not prescriptive and controlling
4. **Intentional architecture**—grows incrementally, not Big Design Up Front

---

## Summary and Recommendations

### For Organizations

1. **Don't eliminate the architect role**—redistribute it appropriately
2. **Embed architects in teams** rather than creating separate architecture groups
3. **Measure architect effectiveness** by team outcomes, not document output
4. **Invest in architectural runway** to enable future delivery

### For Architects

1. **Stay hands-on**—write code, pair, review PRs
2. **Attend all ceremonies**—be a true team member
3. **Balance long-term vision with sprint delivery**
4. **Facilitate rather than dictate**—enable team decisions
5. **Document decisions lightly**—ADRs over comprehensive specs

### For Scrum Teams

1. **View architecture as shared responsibility**
2. **Include architects in refinement** for technical guidance
3. **Use Definition of Ready** to capture architectural criteria
4. **Allocate capacity** for technical debt and enablers
5. **Leverage architects in code review** for mentoring

### Key Metrics

| Metric | Purpose |
|--------|---------|
| Architectural decision cycle time | How fast can the team get guidance? |
| Technical debt ratio | Is architecture enabling sustainable pace? |
| Cross-team integration success | Are teams aligned architecturally? |
| Architectural runway health | Is there capacity for future features? |

---

## Sources

### Role Definition and Best Practices
- [Role of an Agile Architect in a Scrum Team - Premier Agile](https://premieragile.com/where-does-an-architect-fit-in-scrum/)
- [The Role of an Architect on a Scrum Team - American Technology](https://blog.american-technology.net/the-role-of-an-architect-on-a-scrum-team/)
- [Software Architecture in Scrum - Scrum Alliance](https://resources.scrumalliance.org/Article/software-architecture-scrum)
- [The role of software architects in Agile teams - Anders Tornblad](https://atornblad.se/agile-software-architecture)
- [Role of the Agile Architect](https://www.agilearchitect.org/agile/role.htm)
- [Architects & Scrum: What Is The Role Of The Architect In Scrum? - Xebia](https://xebia.com/blog/architects-scrum-4-what-is-the-role-of-the-architect-in-scrum/)
- [Agile architecture - Where does an architect fit in a Scrum sprint? - Equinox](https://www.equinox.co.nz/blog/agile-architecture-where-architect-fit-scrum-sprint)

### Backlog Refinement
- [What is Backlog Refinement? - Atlassian](https://www.atlassian.com/agile/scrum/backlog-refinement)
- [What is Backlog Refinement (or Backlog Grooming)? - Agile Alliance](https://agilealliance.org/glossary/backlog-refinement/)
- [Backlog grooming - Atlassian](https://www.atlassian.com/agile/project-management/backlog-grooming)
- [Product Backlog Refinement (Grooming) in Agile - Agile Academy](https://www.agile-academy.com/en/product-owner/product-backlog-refinement-grooming/)

### Story Splitting
- [The Humanizing Work Guide to Splitting User Stories](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/)
- [Best Ways to Split User Stories for Product Backlog Refinement - KnowledgeHut](https://www.knowledgehut.com/blog/agile/best-ways-to-split-user-stories-for-efficient-product)
- [SPIDR – five simple techniques for a perfectly split user story - itemis](https://blogs.itemis.com/en/spidr-five-simple-techniques-for-a-perfectly-split-user-story)
- [User Story Splitting - Vertical Slice vs Horizontal Slice - Visual Paradigm](https://www.visual-paradigm.com/scrum/user-story-splitting-vertical-slice-vs-horizontal-slice/)

### Code Review
- [Code review antipatterns - Simon Tatham](https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/code-review-antipatterns/)
- [Anti-patterns for code review - AWS DevOps Guidance](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-code-review.html)
- [Rules to Better Architecture and Code Review - SSW](https://www.ssw.com.au/rules/rules-to-better-architecture-and-code-review/)
- [What are code reviews and how they actually save time - Atlassian](https://www.atlassian.com/agile/software-development/code-reviews)
- [A complete guide to code reviews - Swarmia](https://www.swarmia.com/blog/a-complete-guide-to-code-reviews/)

### Scrum Anti-Patterns
- [Developer Anti-Patterns — Scrum Anti-Patterns Guide 2022 - Age of Product](https://age-of-product.com/development-team-anti-patterns/)
- [27 Sprint Anti-Patterns - Scrum.org](https://www.scrum.org/resources/blog/27-sprint-anti-patterns)
- [The Ultimate List of Scrum Anti-Patterns (and How to Fix Them) - LinearB](https://linearb.io/blog/the-ultimate-list-of-scrum-anti-patterns-and-how-to-fix-them)

### Architect Anti-Patterns
- [Ivory Tower Architect - Alex Ewerlöf Notes](https://blog.alexewerlof.com/p/ivory-tower-architect)
- [Ivory tower software architects - Software Architect's Handbook (O'Reilly)](https://www.oreilly.com/library/view/software-architects-handbook/9781788624060/d4ff9836-0ca4-4889-9e7c-71800c17156a.xhtml)
- [Architects, Anti-Patterns, and Organizational Fuckery - charity.wtf](https://charity.wtf/2023/03/09/architects-anti-patterns-and-organizational-fuckery/)
- [Architecture Astronauts - Frontend at Scale](https://frontendatscale.com/issues/41/)

### Emergent and Evolutionary Architecture
- [Foreword to Building Evolutionary Architectures - Martin Fowler](https://martinfowler.com/articles/evo-arch-forward.html)
- [Software Architecture Guide - Martin Fowler](https://martinfowler.com/architecture/)
- [Agile Architecture Part 2: Intentional, Emergent & Evolutionary Architectures - Stefano Rossini](https://medium.com/@stefano.rossini.mail/agile-architecture-intentional-emergent-evolutionary-architectures-da77905098fc)
- [Emergent Architecture: Architecture in the Age of Agile - Steve Cornish](https://medium.com/@steve.cornish/emergent-architecture-architecture-in-the-age-of-agile-9f21ba654845)
- [Balancing Emergent Design and Intentional Architecture - Dilanka Muthukumarana](https://dilankam.medium.com/balancing-emergent-design-and-intentional-architecture-in-agile-software-development-889b07d5ccb9)

### Academic Research
- [Investigating the Role of Architects in Scaling Agile Frameworks - ResearchGate](https://www.researchgate.net/publication/317888003_Investigating_the_Role_of_Architects_in_Scaling_Agile_Frameworks)
- [Software Architecture: Past, Present, Future - SpringerLink](https://link.springer.com/chapter/10.1007/978-3-319-73897-0_10)
- [Emergent Architecture - ScienceDirect](https://www.sciencedirect.com/topics/computer-science/emergent-architecture)
- [Anti-patterns in Modern Code Review: Symptoms and Prevalence - IEEE Xplore](https://ieeexplore.ieee.org/document/9425884/)

### SAFe Framework
- [System Architect - Premier Agile](https://premieragile.com/scaled-agile-system-architect/)
- [Solution Architect - Scaled Agile Framework](https://framework.scaledagile.com/solution-architect)
- [Agile Architecture - Scaled Agile Framework](https://framework.scaledagile.com/agile-architecture)
- [The architect role within SAFe in a nutshell - Highberg](https://highberg.com/insights/the-architect-role-within-safe-in-a-nutshell)
- [The Vital Role of System Architects in Agile Development - Lean Wisdom](https://www.leanwisdom.com/blog/role-of-system-architects-in-agile-development/)

### Technical Debt and NFRs
- [What is Tech Debt? Signs & How to Effectively Manage It - Atlassian](https://www.atlassian.com/agile/software-development/technical-debt)
- [Technical Debt & Scrum: Who Is Responsible? - Scrum.org](https://www.scrum.org/resources/blog/technical-debt-scrum-who-responsible)
- [Nonfunctional Requirements - Scaled Agile Framework](https://scaledagileframework.com/nonfunctional-requirements/)
- [The Role of Architects in Managing Non-Functional Requirements - Architecture & Governance Magazine](https://www.architectureandgovernance.com/applications-technology/the-role-of-architects-in-managing-non-functional-requirements/)

### Hands-On Coding
- [Should software architect responsibilities include coding? - TechTarget](https://www.techtarget.com/searchapparchitecture/opinion/Should-software-architect-responsibilities-include-coding)
- [Architects Should Code: The Architect's Misconception - InfoQ](https://www.infoq.com/articles/architects-should-code-bryson/)
- [Balancing Architecture and Hands-On Coding - Developer to Architect](https://developertoarchitect.com/lessons/lesson103.html)

---

*Report generated: January 2026*
*Research methodology: Web search aggregation of industry sources, expert blogs, framework documentation, and academic publications*
