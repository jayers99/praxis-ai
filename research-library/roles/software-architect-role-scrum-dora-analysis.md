# Why Software Architect Is Not a Formal Role in Scrum: A DORA-Aligned Analysis

**Date:** 2026-01-02
**Research Question:** Why is the role of Software Architect not listed in Scrum as a key role for ticket refinement and peer review, as validated by DORA findings?

---

## Executive Summary

The Software Architect role is intentionally absent from Scrum's formal role definitions—not as an oversight, but as a deliberate design choice rooted in first principles of agile software development. This report synthesizes research across first principles, best practices, prior art, expert consensus, academic research, and anti-patterns to explain why:

1. **Scrum's Cross-Functional Model**: The [2020 Scrum Guide](https://scrumguides.org/scrum-guide.html) explicitly states: "Scrum recognizes no titles for Development Team members other than Developer, regardless of the work being performed by the person." Architecture is a team capability, not an individual role.

2. **DORA's Validation**: [DORA research on loosely coupled teams](https://dora.dev/capabilities/loosely-coupled-teams/) confirms that team autonomy—enabled by cross-functional ownership—is "the sole capability impacting all of DORA's performance metrics."

3. **Conway's Law Alignment**: Separating architects from delivery teams creates communication boundaries that manifest as architectural friction in the system itself.

The answer is not that architecture doesn't matter—it matters deeply. Rather, architecture work is better distributed across the team than concentrated in a single external role.

---

## 1. First Principles

### 1.1 The Agile Manifesto's Principle 11

The [Agile Manifesto's Principle 11](http://agilemanifesto.org/principles.html) states:

> "The best architectures, requirements, and designs emerge from self-organizing teams."

This principle fundamentally challenges the traditional model where architects design systems in isolation before handing specifications to developers. The manifesto's signatories—including Martin Fowler, Kent Beck, and other pioneers—embedded this belief at the foundation of agile methodology.

**Key insight:** Architecture is not prescribed top-down but emerges through the collaborative work of a self-organizing team. The team, not an external architect, owns the architecture.

### 1.2 Scrum's Three-Role Model

The [Scrum Guide](https://scrumguides.org/scrum-guide.html) defines exactly three roles:
- **Product Owner** - owns the "what" (product backlog, value maximization)
- **Scrum Master** - owns the "how of Scrum" (process facilitation, impediment removal)
- **Developers** - own the "how of building" (all technical work, including architecture)

From the 2020 Scrum Guide:

> "Within a Scrum Team, there are no sub-teams or hierarchies. It is a cohesive unit of professionals focused on one objective at a time, the Product Goal."

The absence of an architect role is not an oversight—it is a deliberate rejection of hierarchical specialization that creates dependencies.

### 1.3 Cross-Functional by Design

[Scrum.org's guidance on cross-functional teams](https://www.scrum.org/resources/blog/unraveling-significance-cross-functional-scrum) explains:

> "Scrum Teams are cross-functional, meaning the members have all the skills necessary to create value each Sprint."

Architecture skills are expected to exist **within** the team, not be provided by an external role. When teams lack these skills, the solution is capability building, not role specialization.

---

## 2. Best Practices

### 2.1 Embedded Architecture vs. External Architects

The [Scrum Alliance's guidance on software architecture](https://resources.scrumalliance.org/Article/software-architecture-scrum) recommends:

> "One option is the architect is part of the Scrum team, and this is the most embedded way that an architect would fit into a Scrum project. It may not even be an individual who has the title of 'architect', because the big idea behind Scrum teams is that team members have different skills."

**Best practice:** When architectural expertise is needed, embed the person with those skills as a Developer on the team, not as an external stakeholder.

### 2.2 Architecture as a Team Activity

[Xebia's analysis of architects in Scrum](https://xebia.com/blog/architects-scrum-4-what-is-the-role-of-the-architect-in-scrum/) advocates:

> "The most successful approach so far is to foster collaboration instead of delegation. This means guiding the few current 'architects' to work with the teams on their architecture challenges, but not for them."

The shift is from **architecture as specification** to **architecture as mentorship**—teaching teams to make good architectural decisions rather than making decisions for them.

### 2.3 Backlog Refinement Participants

According to [Scrum.org's guidance on refinement](https://www.scrum.org/resources/blog/scrum-trenches-product-backlog-refinement-scrum-team-responsibility):

> "Every member of the Scrum Team is responsible for Product Backlog refinement."

The participants in refinement are:
- Product Owner (required)
- Developers (required—all share responsibility for estimates and technical input)
- Scrum Master (optional, helps with facilitation)

Architecture considerations in refinement come from the Developers collectively, not from an external architect role.

### 2.4 Peer Review Ownership

[DORA's research on code review](https://dora.dev/research/2024/dora-report/) indicates that high-performing teams use peer review within the team, with practices including:

- Review depth and quality as a team metric
- Small batch sizes (smaller PRs = faster reviews, fewer defects)
- Collective ownership of code quality

Peer review is a team practice, not an architect gatekeeping function.

---

## 3. Prior Art

### 3.1 The Evolution of the Architect Role

Historically, the software architect emerged from civil engineering metaphors—someone who designs the building before construction begins. This model assumed:

1. Requirements are known upfront
2. Design can be separated from implementation
3. Specialists should control specialists

Agile methodologies challenge all three assumptions.

### 3.2 Conway's Law (1967)

[Melvin Conway's observation](https://martinfowler.com/bliki/ConwaysLaw.html) provides crucial context:

> "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations."

**Implication:** If architects sit outside delivery teams, communication boundaries will create architectural boundaries—often in unintended and undesirable ways. The [Inverse Conway Maneuver](https://learningloop.io/glossary/conways-law) suggests structuring teams to match desired architecture, which means embedding architectural capability within cross-functional teams.

### 3.3 Extreme Programming's Collective Ownership

The [collective code ownership model from XP](https://www.infoq.com/news/Collective-Code-Ownership-isnt/), as described by Martin Fowler, "abandons any notion of individual ownership of modules. The code base is owned by the entire team and anyone may make changes anywhere."

This directly contradicts models where an architect "owns" the system design and developers merely implement it.

---

## 4. Expert Consensus

### 4.1 Martin Fowler on Architecture and Teams

As one of the [Agile Manifesto signatories](https://en.wikipedia.org/wiki/Martin_Fowler_(software_engineer)) and author of the [Software Architecture Guide](https://martinfowler.com/architecture/), Fowler notes:

> "Pretty much all the practitioners I favor in Software Architecture are deeply suspicious of any kind of general law in the field. Good software architecture is very context-specific. But if there is one thing they all agree on, it's the importance and power of Conway's Law."

His guidance emphasizes that architecture must align with team organization—making embedded, collective ownership preferable to external architect roles.

### 4.2 DORA Research Team

The [DORA team's findings on loosely coupled teams](https://dora.dev/capabilities/loosely-coupled-teams/) represent years of research across tens of thousands of professionals:

> "When the architecture of the system is designed to enable teams to test, deploy, and change systems without dependencies on other teams, teams require little communication to get work done. In other words, both the architecture and the teams are loosely coupled."

External architect roles create dependencies that contradict this finding.

### 4.3 Scaled Agile Perspective

Notably, [SAFe (Scaled Agile Framework)](https://framework.scaledagile.com/agile-architecture) does define architect roles (System Architect, Solution Architect, Enterprise Architect). However, this is specifically for **enterprise scale** where multiple teams must coordinate. SAFe also emphasizes:

> "An effective approach to agile architecture requires a combination of intentional and emergent design."

Even at scale, architecture is not purely top-down—it balances central guidance with team-level emergence.

### 4.4 Academic Research Consensus

[Research published on ResearchGate](https://www.researchgate.net/publication/317888003_Investigating_the_Role_of_Architects_in_Scaling_Agile_Frameworks) found:

> "A review of about twenty scaling frameworks identified that for large teams the role of an architect is a necessity."

But critically:

> "Scaling agile methods at the enterprise level with some amount of architectural planning prevents excessive redesign efforts and functional redundancy."

The consensus is nuanced: single-team Scrum works without architects; scaled multi-team environments may need coordination roles—but these are coordination roles, not command-and-control roles.

---

## 5. Academic Research

### 5.1 Emergent vs. Intentional Architecture

[Research on emergent architecture](https://medium.com/@stefano.rossini.mail/agile-architecture-intentional-emergent-evolutionary-architectures-da77905098fc) distinguishes two approaches:

| Approach | Description | When to Use |
|----------|-------------|-------------|
| **Emergent** | Architecture evolves through refactoring and iteration | Small teams, uncertain requirements |
| **Intentional** | Architecture planned upfront for cross-team coordination | Large systems, known constraints |

The [Agile Manifesto's Principle 11](http://agilemanifesto.org/principles.html) favors emergence, while recognizing that "some amount of architecture planning and governance are required up front" for larger systems.

### 5.2 TDD and Refactoring as Architectural Tools

[Academic perspectives on emergent design](https://www.imagicle.com/en/blog/o/imagicle-why-choosing-emergent-design-for-agile-software-development/) emphasize:

> "TDD and refactoring are fundamental tools to allow the design to emerge. The tests are fundamental in order to refactor, which in turn is fundamental to be able to bring out the design while keeping the architecture both solid and extensible."

This research supports the idea that architecture emerges from engineering practices owned by the team, not from external specification.

### 5.3 The T-Shaped Developer Model

Research on team composition suggests the [T-shaped model](https://www.scrum.org/resources/blog/unraveling-significance-cross-functional-scrum):

- Deep expertise in one area (the vertical bar)
- Broad knowledge across many areas (the horizontal bar)

Architectural thinking is part of the "broad knowledge" expected of all developers, with some developers having deeper architectural expertise.

---

## 6. DORA Findings: The Empirical Evidence

### 6.1 Team Autonomy as Performance Driver

[DORA's research on loosely coupled teams](https://dora.dev/capabilities/loosely-coupled-teams/) provides the empirical foundation:

> "Teams with a loosely coupled architecture can make substantial modifications to their systems independently of other teams. This autonomy accelerates their pace, and it's the sole capability impacting all of DORA's performance metrics."

External architect roles create dependencies that reduce team autonomy and, according to DORA data, reduce delivery performance.

### 6.2 The Four Key Metrics

[DORA's four key metrics](https://dora.dev/research/2024/dora-report/) are:
1. **Deployment Frequency** - How often code deploys to production
2. **Lead Time for Changes** - Time from commit to production
3. **Change Failure Rate** - Percentage of deployments causing failures
4. **Time to Restore Service** - Time to recover from failures

All four metrics improve when teams can operate autonomously. External architect approval gates slow metrics 1-2; architect-imposed designs that teams don't understand worsen metrics 3-4.

### 6.3 Cross-Functional Teams and DORA

The [2021-2024 DORA reports](https://dora.dev/research/) consistently find:

> "Building cross-functional teams, with representation from across the organization (product, dev, test, and operations) enables teams to work independently and facilitates building around team boundaries."

Architecture capability should be represented **within** the cross-functional team, not provided by external stakeholders.

### 6.4 High-Trust, Low-Blame Cultures

DORA's cultural findings reinforce the case:

> "High-trust and low-blame cultures tend to have higher organizational performance."

External architect roles can create blame dynamics ("the team didn't follow the architecture") and reduce trust. Collective ownership creates shared accountability.

---

## 7. Anti-Patterns

### 7.1 The Ivory Tower Architect

The [Ivory Tower Architect anti-pattern](https://blog.alexewerlof.com/p/ivory-tower-architect) is extensively documented:

> "Ivory Tower Architect is a term of derision toward software architects who have become disconnected from anything related to actual implementation, coding, or related knowledge."

[O'Reilly's Software Architect's Handbook](https://www.oreilly.com/library/view/software-architects-handbook/9781788624060/d4ff9836-0ca4-4889-9e7c-71800c17156a.xhtml) warns:

> "If a software architect is working from an ivory tower, they may be creating an architecture based on a perfect-world environment that really doesn't reflect real scenarios."

**Symptoms:**
- Architects don't write code
- Architecture decisions made without team input
- Designs are rejected or worked around by teams
- Architecture diagrams don't match running systems

### 7.2 Centralized Architecture Teams

[Scrum Alliance's analysis](https://resources.scrumalliance.org/Article/software-architecture-scrum) identifies this pattern:

> "One of the recurring challenges many organizations face is that they tend to create architecture teams or areas, typically as a centralized service. This is obviously against the scrum principle about self-managed and cross-functional teams, as it is usually a decrease in scrum teams' autonomy."

Centralized architecture teams create bottlenecks and dependencies that slow delivery.

### 7.3 Silo Mentality

[Scrum.org's anti-pattern documentation](https://www.scrum.org/resources/blog/development-team-anti-patterns) describes:

> "The anti-pattern emerges when team members become siloed in their respective roles, leading to dependencies and delays."

When "the architect" handles all architecture work, other team members:
- Don't develop architectural thinking skills
- Create systems that conflict with architectural intent
- Defer decisions they should own

### 7.4 Micro-Management by External Roles

Another [documented anti-pattern](https://age-of-product.com/development-team-anti-patterns/):

> "The team are continually being micro-managed. Project/program managers, tech leads and architects are continually wandering in and assigning tasks and problems to people."

External architect roles often become micro-management vectors, especially for technical decisions the team should own.

### 7.5 Architecture as Gatekeeping

When architects control peer review or refinement:

- PRs wait for architect approval (slowing Lead Time)
- Teams can't refine tickets without architect availability
- Knowledge concentrates rather than spreads
- Truck factor approaches 1

---

## 8. Synthesis: Why This Matters for Ticket Refinement and Peer Review

### 8.1 Ticket Refinement

In Scrum, [refinement is a team activity](https://www.scrum.org/resources/blog/scrum-trenches-product-backlog-refinement-scrum-team-responsibility). The Developers (collectively) are responsible for:

- Understanding technical requirements
- Estimating effort
- Identifying architectural implications
- Breaking down work

When an external architect participates, they become either:
- **A stakeholder** (appropriate—provides input but doesn't own decisions)
- **A gatekeeper** (anti-pattern—blocks team autonomy)

The DORA-aligned approach: teams with architectural capability don't need external architects in refinement. They handle architectural concerns as part of their cross-functional responsibility.

### 8.2 Peer Review

DORA's research on [code review practices](https://dora.dev/research/2024/dora-report/) shows that high performers:

- Use peer review within the team
- Keep reviews fast (small batch sizes)
- Share code ownership collectively

External architect review gates:
- Slow Lead Time for Changes
- Create single points of failure
- Prevent collective ownership

The DORA-aligned approach: architectural concerns are part of normal peer review, conducted by team members with relevant knowledge. This may include someone with deep architectural expertise—but as a team member, not an external role.

---

## 9. When Architects ARE Needed

It would be incomplete to suggest architects never have value. The research indicates architects are valuable when:

### 9.1 Enterprise Scale (Multiple Teams)

[SAFe's architect roles](https://framework.scaledagile.com/agile-architecture) address coordination across multiple teams:

- System Architect: Coordinates within an Agile Release Train (5-12 teams)
- Solution Architect: Coordinates across Release Trains
- Enterprise Architect: Portfolio-level technology strategy

Even here, the role is **coordination, not command**—aligning teams, not dictating to them.

### 9.2 Greenfield Platform Decisions

When building new platforms with long-term strategic implications, some intentional architecture is appropriate. But this is:
- Time-bounded (upfront, then ongoing evolution)
- Collaborative (not isolation)
- Team-influenced (not top-down dictation)

### 9.3 Mentorship and Capability Building

The most effective "architect" role in agile is often:

> "Guiding the few current 'architects' to work with the teams on their architecture challenges, but not for them. The idea here is challenging that 'special' role to collaborate and add architectural knowledge to the team."

—[Scrum Alliance](https://resources.scrumalliance.org/Article/software-architecture-scrum)

This is architecture as teaching, not architecture as specification.

---

## 10. Conclusion

The Software Architect is not listed as a formal Scrum role for ticket refinement and peer review because:

1. **First Principles Forbid It**: The Agile Manifesto's Principle 11 asserts that "the best architectures emerge from self-organizing teams," not from external architects.

2. **Scrum's Design Excludes It**: The Scrum Guide explicitly rejects specialist titles within the Development Team. Architecture is a Developer responsibility, distributed across the team.

3. **DORA Data Validates It**: Team autonomy—enabled by cross-functional ownership—is "the sole capability impacting all of DORA's performance metrics." External architect dependencies reduce autonomy and thus reduce performance.

4. **Conway's Law Explains It**: Separating architects from teams creates organizational boundaries that manifest as architectural friction in the system.

5. **Anti-Patterns Warn Against It**: The Ivory Tower Architect, centralized architecture teams, and gatekeeping are well-documented failure modes.

The answer is not that architecture doesn't matter—it matters profoundly. Rather, architecture work is more effectively distributed as a team capability than concentrated in an external specialist role. High-performing teams, as DORA research consistently shows, own their own architectural decisions as part of their cross-functional responsibility.

---

## Sources

### Official Guides and Frameworks
- [The 2020 Scrum Guide](https://scrumguides.org/scrum-guide.html)
- [Principles behind the Agile Manifesto](http://agilemanifesto.org/principles.html)
- [12 Principles Behind the Agile Manifesto | Agile Alliance](https://agilealliance.org/agile101/12-principles-behind-the-agile-manifesto/)
- [SAFe Agile Architecture](https://framework.scaledagile.com/agile-architecture)

### DORA Research
- [DORA 2024 State of DevOps Report](https://dora.dev/research/2024/dora-report/)
- [DORA Capabilities: Loosely Coupled Teams](https://dora.dev/capabilities/loosely-coupled-teams/)
- [DORA Capabilities: Loosely Coupled Architecture](https://dora.dev/devops-capabilities/process/loosely-coupled-architecture/)
- [What are DORA Metrics | LinearB](https://linearb.io/blog/dora-metrics)
- [DORA Metrics | Atlassian](https://www.atlassian.com/devops/frameworks/dora-metrics)

### Expert Commentary
- [Martin Fowler: Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html)
- [Martin Fowler: Software Architecture Guide](https://martinfowler.com/architecture/)
- [Scaling Architecture Conversationally | Martin Fowler](https://martinfowler.com/articles/scaling-architecture-conversationally.html)

### Scrum and Agile Resources
- [Software Architecture in Scrum | Scrum Alliance](https://resources.scrumalliance.org/Article/software-architecture-scrum)
- [Product Backlog Refinement is a Scrum Team Responsibility | Scrum.org](https://www.scrum.org/resources/blog/scrum-trenches-product-backlog-refinement-scrum-team-responsibility)
- [Cross-Functional in Scrum | Scrum.org](https://www.scrum.org/resources/blog/unraveling-significance-cross-functional-scrum)
- [About Self-Organizing Teams | Scrum.org](https://www.scrum.org/resources/blog/about-self-organizing-teams)
- [Development Team Anti-Patterns | Scrum.org](https://www.scrum.org/resources/blog/development-team-anti-patterns)
- [What Is the Role of the Architect in Scrum? | Xebia](https://xebia.com/blog/architects-scrum-4-what-is-the-role-of-the-architect-in-scrum/)

### Anti-Patterns
- [Ivory Tower Architect | Alex Ewerlöf Notes](https://blog.alexewerlof.com/p/ivory-tower-architect)
- [Avoid Being an Ivory Tower Architect | InfoQ](https://www.infoq.com/news/2023/01/ivory-tower-architects/)
- [Ivory Tower Software Architects | O'Reilly](https://www.oreilly.com/library/view/software-architects-handbook/9781788624060/d4ff9836-0ca4-4889-9e7c-71800c17156a.xhtml)
- [Developer Anti-Patterns | Age of Product](https://age-of-product.com/development-team-anti-patterns/)

### Academic and Practitioner Research
- [Investigating the Role of Architects in Scaling Agile Frameworks | ResearchGate](https://www.researchgate.net/publication/317888003_Investigating_the_Role_of_Architects_in_Scaling_Agile_Frameworks)
- [Emergent Architecture | ScienceDirect](https://www.sciencedirect.com/topics/computer-science/emergent-architecture)
- [Agile Architecture: Intentional, Emergent & Evolutionary | Medium](https://medium.com/@stefano.rossini.mail/agile-architecture-intentional-emergent-evolutionary-architectures-da77905098fc)
- [Conway's Law | Wikipedia](https://en.wikipedia.org/wiki/Conway's_law)

### Additional Resources
- [The Role of an Architect on a Scrum Team | DZone](https://dzone.com/articles/role-of-architect-in-scrum-team)
- [SAFe vs Scrum: Key Differences | Monday.com](https://monday.com/blog/rnd/safe-vs-scrum/)
- [Self-Organizing Teams | agile42](https://www.agile42.com/en/blog/self-organizing-teams)
