# Why QA Engineer Is Not a Formal Role in Scrum: A DORA-Aligned Analysis

**Date:** 2026-01-02
**Research Question:** Why is the role of QA Engineer not listed in Scrum as a key role for ticket refinement and peer review, as validated by DORA findings?

---

## Executive Summary

The QA Engineer role is intentionally absent from Scrum's formal role definitions—not because testing doesn't matter, but because quality is treated as a shared team responsibility rather than the domain of a specialist role. This report synthesizes research across first principles, best practices, prior art, expert consensus, academic research, and anti-patterns to explain why:

1. **Scrum's Whole-Team Quality Model**: The [Scrum Guide](https://scrumguides.org/scrum-guide.html) states that quality is embedded in the Definition of Done, which the entire Scrum Team owns. Testing is an activity, not a role.

2. **DORA's Validation**: [DORA research on test automation](https://dora.dev/capabilities/test-automation/) shows that "when developers are primarily responsible for creating and maintaining suites of automated tests... this drives improved performance."

3. **Shift-Left Paradigm**: Testing that happens at the end of a cycle—by a separate QA role—creates handoffs, bottlenecks, and delays. High-performing teams shift testing left into development activities.

The answer is not that testing doesn't matter—it matters profoundly. Rather, testing is more effective as a distributed team capability embedded throughout the development process than as a separate phase owned by a specialist role.

---

## 1. First Principles

### 1.1 The Agile Manifesto's Quality Emphasis

While the [Agile Manifesto](http://agilemanifesto.org/principles.html) doesn't directly address testing roles, several principles embed quality expectations:

> "Continuous attention to technical excellence and good design enhances agility." (Principle 9)

> "Working software is the primary measure of progress." (Principle 7)

These principles imply that quality is built in continuously—not verified at the end by a separate role. The manifesto's emphasis on "working software" means every increment must be tested before it can be called "done."

### 1.2 Scrum's Three-Role Model

The [Scrum Guide](https://scrumguides.org/scrum-guide.html) defines exactly three roles:
- **Product Owner** - owns the "what" (product backlog, value maximization)
- **Scrum Master** - owns the "how of Scrum" (process facilitation, impediment removal)
- **Developers** - own the "how of building" (all technical work, including testing)

From [Scrum.org's guidance on QA](https://www.scrum.org/resources/blog/yds-where-does-quality-assurance-qa-fit-scrum-team):

> "Quality is owned by everyone in the Scrum Team and is part of the work that needs to be done in order to satisfy the Definition of Done. Scrum does not have any job titles listed in the Guide anywhere."

The absence of a QA role is not an oversight—it is a deliberate design choice to avoid the quality-as-gatekeeper anti-pattern.

### 1.3 Definition of Done as Quality Enforcement

In Scrum, quality is enforced through the Definition of Done (DoD), not through a separate QA role. [Agile Pain Relief explains](https://agilepainrelief.com/glossary/quality-assurance-in-scrum/):

> "In Scrum, QA is an activity inside the team, not a role. A specific team member may perform it. However, the team is accountable as a whole."

The DoD typically includes testing criteria. When the team says an item is "Done," it means tested, not "ready for QA."

### 1.4 W. Edwards Deming's Quality Principle

The foundational principle that "quality is everyone's responsibility" predates agile. [Deming](https://www.zenergytechnologies.com/blog/testing/quality-testing), the legendary quality guru, established:

> "Quality is everyone's responsibility."

This principle, central to manufacturing quality movements and later adopted by software development, rejects the idea that quality can be "inspected in" by a separate function at the end.

---

## 2. Best Practices

### 2.1 Shift-Left Testing

[Shift-left testing](https://www.theknowledgeacademy.com/blog/shift-left-testing-in-agile/) is the industry-standard approach for modern software development:

> "Shift-left testing is a software testing approach that shifts all testing activities to earlier development stages rather than leaving until the very final stages."

Key principles include:
- Testing begins when requirements are written, not after code is complete
- Developers write tests alongside (or before) code
- Defects found early cost 15-100x less to fix than those found in production

[IBM research](https://abstracta.us/blog/devops/shift-left-testing/) shows:

> "Fixing a bug during testing costs 15x less than fixing it in production."

### 2.2 Test-Driven Development (TDD)

[TDD](https://agilealliance.org/glossary/tdd/), developed by Kent Beck, makes testing an integral part of development:

> "Test-driven development (TDD) is a way of writing code that involves writing an automated unit-level test case that fails, then writing just enough code to make the test pass."

With TDD, the question "who does the testing?" is answered: the developer who writes the code writes the tests. Testing is not a separate activity for a separate role.

### 2.3 The Three Amigos / Power of Three

[Lisa Crispin and Janet Gregory's work](https://agiletester.ca/) describes the "Three Amigos" or "Power of Three" pattern:

Before any story is implemented, three perspectives collaborate:
1. **Developer** - "How will we build this?"
2. **Tester** (someone with testing mindset) - "What could go wrong? How will we verify this?"
3. **Product Owner/Business Analyst** - "What does the user need?"

Note that "Tester" here is a perspective, not necessarily a dedicated role. Any Developer can bring the testing perspective.

### 2.4 Continuous Testing in CI/CD

[DORA's research on continuous integration](https://dora.dev/capabilities/continuous-integration/) establishes:

> "Developers should be able to get feedback from automated tests in less than ten minutes both on local workstations and from the continuous integration system."

This implies:
- Tests must be automated (manual QA handoffs don't meet this standard)
- Developers must be able to run and fix tests themselves
- Testing is embedded in the development workflow, not a separate phase

---

## 3. Prior Art

### 3.1 The Evolution of QA

Historically, Quality Assurance emerged from manufacturing, where inspectors at the end of an assembly line would catch defects. This model was adopted by software development in the waterfall era:

1. **Requirements Phase** → 2. **Design Phase** → 3. **Development Phase** → 4. **Testing Phase** → 5. **Release**

The "Testing Phase" was owned by a separate QA team. This created several problems:
- Defects found late are expensive to fix
- Developers don't learn from their mistakes (feedback loop is too long)
- QA becomes a bottleneck before every release

### 3.2 The Agile Testing Quadrants

[Lisa Crispin and Janet Gregory's Agile Testing Quadrants](https://ucsb-cs48.github.io/topics/testing_agile_testing_crispin_and_gregory/) provide a framework for understanding testing activities:

| Quadrant | Purpose | Who Does It |
|----------|---------|-------------|
| Q1 | Unit tests, component tests (technology-facing, support team) | Developers |
| Q2 | Functional tests, acceptance tests (business-facing, support team) | Developers + Testers |
| Q3 | Exploratory testing, usability testing (business-facing, critique product) | Testers, UX, Users |
| Q4 | Performance testing, security testing (technology-facing, critique product) | Specialists (as needed) |

The quadrants show that testing is distributed across the team, with different types of testing performed by different people. There's no single "QA role" that owns all testing.

### 3.3 Extreme Programming (XP) Practices

XP, one of the original agile methodologies, includes several testing practices:

- **Test-First Programming** (now TDD) - Developers write tests before code
- **Pair Programming** - Two developers work together, catching defects in real-time
- **Continuous Integration** - Tests run automatically on every commit
- **Collective Code Ownership** - Anyone can improve any code, including tests

None of these practices require a separate QA role. Testing is embedded in development.

---

## 4. Expert Consensus

### 4.1 Lisa Crispin and Janet Gregory

As the foremost experts on agile testing, [Crispin and Gregory](https://agiletester.ca/) advocate for the "Whole Team Approach":

> "As Lisa Crispin and Janet Gregory say in their book Agile Testing, 'The fact is, it's all about quality — and if it's not, we question whether it's really an "agile" team.'"

Their [Agile Testing Fellowship](https://agiletestingfellow.com/) teaches:

> "Testing is an activity that happens throughout. It is not a phase that happens at the end. Start thinking about the risks at the very beginning, and how we are going to mitigate those with testing."

### 4.2 DORA Research Team

[DORA's test automation research](https://dora.dev/capabilities/test-automation/) is unequivocal:

> "DORA's research shows that when developers are primarily responsible for creating and maintaining suites of automated tests, and when it is easy for developers to fix acceptance test failures, this drives improved performance."

Note the emphasis: **developers** are primarily responsible for automated tests, not a separate QA team.

### 4.3 Scrum.org Guidance

[Scrum.org's official position](https://www.scrum.org/resources/blog/yds-where-does-quality-assurance-qa-fit-scrum-team) on QA in Scrum:

> "The Scrum framework is suitable for any business. Therefore, QA, Tester, UX, UI, and some other roles are not part of Scrum because it would be limiting. However, Scrum says developers bring all required skills to achieve the product goals."

People with testing expertise are valuable—but they are Developers on the Scrum Team, not a separate role.

### 4.4 The Quality Coach Evolution

Industry thought leaders describe an evolution from "QA Engineer" to ["Quality Coach"](https://www.functionize.com/blog/the-new-role-of-qa):

> "The new role of QA involves a broadening of implications; the role can now be seen as an organization-wide gatekeeper for quality. It involves quality coaching and quality enablement for the whole team and often for the whole company."

This evolution reflects the shift from "doing testing" to "enabling the team to do testing."

---

## 5. Academic Research

### 5.1 Cost of Defects

Multiple studies establish that defects found later cost exponentially more to fix:

- [IBM Systems Sciences Institute](https://abstracta.us/blog/devops/shift-left-testing/) found fixing a bug during testing costs 15x less than fixing it in production
- Studies show production defects can cost 30-100x more than those caught during development

This research supports the shift-left approach: testing by a separate QA role at the end of the cycle is economically inefficient.

### 5.2 DORA's Multi-Year Research

[DORA's research program](https://dora.dev/capabilities/test-automation/) has studied over 39,000 professionals:

> "Not only does this help teams build (and learn how to build) high quality software faster, DORA's research shows that it also drives improved software stability, reduced team burnout, and lower deployment pain."

Key findings on test automation:
- Developers should write tests
- Tests should provide feedback in under 10 minutes
- Test automation drives all four DORA metrics

### 5.3 The 2015 State of DevOps Report

[DORA's 2015 research](https://dora.dev/capabilities/continuous-integration/) established:

> "Teams perform better when developers merge their work into trunk at least daily."

Frequent integration requires automated testing. If testing is a separate phase owned by a separate role, daily integration becomes impossible.

---

## 6. DORA Findings: The Empirical Evidence

### 6.1 Test Automation as a Core Capability

[DORA identifies test automation](https://dora.dev/capabilities/test-automation/) as one of the key technical capabilities that drives software delivery performance:

> "The use of comprehensive automated test suites primarily created and maintained by developers. Effective test suites are reliable—that is, tests find real failures and only pass releasable code."

Critical insight: **developers** create and maintain the tests, not a separate QA team.

### 6.2 Change Failure Rate

[Change Failure Rate](https://incident.io/hubs/dora/dora-metrics-change-failure-rate) measures "the percentage of deployments that result in a failure in production."

From [DORA metrics research](https://getdx.com/blog/dora-metrics/):

> "A change failure rate above 40% can indicate poor testing procedures."

Teams with high change failure rates often have:
- Insufficient automated testing
- Testing that happens too late (after development is "done")
- Manual testing bottlenecks

The solution is not more QA resources—it's earlier, automated testing owned by developers.

### 6.3 Continuous Delivery Prerequisites

[DORA's continuous delivery research](https://dora.dev/capabilities/continuous-delivery/) lists prerequisites:

> "Test automation: The use of comprehensive automated test suites primarily created and maintained by developers."

> "Trunk-based development: Characterized by fewer than three active branches... branches and forks having very short lifetimes (e.g., less than a day) before being merged into mainline."

Both prerequisites are incompatible with a separate QA phase. If code must wait for QA before merging, branches cannot be short-lived. If tests are owned by QA, developers cannot get fast feedback.

### 6.4 The Four Key Metrics and Testing

| Metric | How Testing Relates |
|--------|---------------------|
| **Deployment Frequency** | Manual QA creates bottlenecks that reduce deployment frequency |
| **Lead Time for Changes** | QA handoffs add wait time to lead time |
| **Change Failure Rate** | Automated testing by developers reduces failures |
| **Mean Time to Restore** | Teams that own their tests can diagnose and fix issues faster |

All four metrics are optimized when testing is embedded in development, not separated into a QA phase.

---

## 7. Anti-Patterns

### 7.1 The Handoff Anti-Pattern

[From QualityNexus analysis](https://medium.com/qualitynexus/anti-patterns-in-team-setups-that-silence-qa-49dbd83fb53a):

> "Devs push a ticket to QA like a delivery: 'Here, go test this.' No shared responsibility, no collaboration, just handoff. This delays feedback, breeds tension, and turns QA into a bottleneck."

The handoff model creates:
- Loss of context (developer moves on while QA investigates)
- Delayed feedback (defects found days after code was written)
- Finger-pointing ("that's a QA problem" vs. "that's a dev problem")

### 7.2 The Two-Sprint Anti-Pattern

[Scrum.org warns](https://www.scrum.org/forum/scrum-forum/45299/how-sprint-plan-when-qa-always-lags-behind-development):

> "You are in effect encouraging 2 separate overlapping sprints where one team codes and another team tests. This goes against the Scrum framework's practice of delivering increments that meet the Definition of Done at the end of every Sprint."

When QA is a separate phase, teams often:
- Code in Sprint N, test in Sprint N+1
- Never deliver truly "Done" increments
- Create inventory (untested code) that hides risk

### 7.3 QA as Bottleneck

[Analysis from Inbank](https://medium.com/inbank-product-and-engineering/merging-product-engineering-and-qa-d5ce2b2e639e):

> "Having a separate QA person in the team will inevitably slow down the team's release frequency. First, it allows the team to invest less in test automation. Second, even if the QA person is writing acceptance tests then this still means introducing additional handoff in the development cycle."

Their research found:

> "Teams were able to reduce their cycle time by up to 45% by investing in acceptance test automation and removing handoffs in testing."

### 7.4 QA Exclusion from Planning

[The World Quality Report](https://www.softwaretestpro.com/three-tips-for-dissolving-qa-and-testing-bottlenecks-on-agile-teams/) found:

> "Over 1,660 executives from 32 countries... the most common challenge cited in this report is the lack of early involvement of their QA and testing teams in the inception phase or sprint planning."

When QA is excluded from planning:
- Testing is an afterthought
- Requirements lack testability criteria
- Defects are found late

### 7.5 The "QA Will Catch It" Mindset

When a separate QA role exists, developers may abdicate responsibility for quality:
- "I don't need to test this thoroughly—QA will find any bugs"
- "Writing tests isn't my job—that's what testers are for"
- "Ship it to QA and move on to the next story"

This mindset undermines quality at its source.

### 7.6 The "Waterscrumfall" Pattern

[Scrum.org discussion](https://www.scrum.org/forum/scrum-forum/32563/qa-separate-development) identifies:

> "A separate QA function is often symptomatic of waterscrumfall... a stage-gated organization pretending to be agile."

Organizations that claim to be agile but maintain separate QA teams often have:
- Sprint ceremonies without true iterative development
- "Done" that doesn't mean releasable
- Quality gates that create bottlenecks

---

## 8. The Transformation: From QA Role to Quality Capability

### 8.1 People with Testing Expertise Still Valuable

The absence of a "QA Engineer" role doesn't mean testing expertise is unwanted. [Scrum.org clarifies](https://www.scrum.org/resources/blog/yds-where-does-quality-assurance-qa-fit-scrum-team):

> "If you don't need independent quality assurance, then the Development Team is responsible for everything. You may have a QA specialist, but they reside on the Development Team and help the team design test cases, execute manual tests, perform exploratory tests, automate tests, and so on."

The key distinction:
- **QA as Role** (anti-pattern): A separate person/team responsible for testing
- **QA as Capability** (best practice): Testing expertise embedded in the team

### 8.2 The Quality Angel Concept

[Scrum.org's "Quality Angel" metaphor](https://www.scrum.org/resources/blog/quality-angels-your-scrum-team):

> "A Quality Assurance specialist should be called a Quality Angel instead. The angel who spreads their wings and reminds the Scrum Team of what quality is and how to take care of it."

The Quality Angel:
- Coaches the team on testing practices
- Helps define the Definition of Done
- Champions quality as a team value
- Does NOT own testing as a separate responsibility

### 8.3 From Quality Assurance to Quality Engineering

[The industry evolution](https://www.cprime.com/resources/blog/the-devops-qa-role-automated-testing-in-the-devops-lifecycle/):

> "DevOps QA should shift from quality assurance to quality assistance."

> "To align with DevOps and support current and future technologies, the QA role is being transformed into Quality Engineering (QE). The Quality Engineering role is more demanding than QA was, as it is more fundamentally focused on quality."

Quality Engineering encompasses:
- Test automation expertise (coding tests, not just running them)
- CI/CD pipeline development
- Quality coaching for the whole team
- Quality culture advocacy

### 8.4 The Quality Coach Role

[Modern QA evolution](https://www.functionize.com/blog/the-new-role-of-qa):

> "Viewing QA as a quality coach role can help you understand how QA managers can participate in enabling quality for the whole team and, by extension, the whole organization."

The Quality Coach:
- Teaches developers to write better tests
- Advocates for quality practices
- Identifies systemic quality issues
- Enables the team rather than gatekeeping releases

---

## 9. Synthesis: Why This Matters for Ticket Refinement and Peer Review

### 9.1 Ticket Refinement

In Scrum, [refinement is a team activity](https://www.scrum.org/resources/blog/scrum-trenches-product-backlog-refinement-scrum-team-responsibility). Testing considerations should be part of refinement:

- What are the acceptance criteria?
- How will we verify this works?
- What edge cases should we consider?
- What tests will we write?

These questions should be asked by the Developers (including anyone with testing expertise), not deferred to a separate QA role.

The [Three Amigos](https://agiletester.ca/) approach ensures testing perspectives are represented in refinement—but by team members, not by an external QA role.

### 9.2 Peer Review

DORA's research on [code review and quality](https://dora.dev/research/2024/dora-report/) shows that high performers:

- Use peer review within the team
- Include test coverage in review criteria
- Review tests alongside code

When tests are written by developers:
- Peer review naturally includes test review
- Reviewers can verify test coverage
- Tests are treated as first-class code

When QA is separate:
- Code reviews don't include test review (tests don't exist yet)
- Developers ship code without verifying test coverage
- Testing quality isn't part of the review process

---

## 10. When Testing Specialists ARE Needed

### 10.1 Complex Testing Domains

Some testing activities benefit from specialist expertise:

| Domain | Why Specialists Help |
|--------|---------------------|
| **Performance Testing** | Requires specialized tools and expertise |
| **Security Testing** | Penetration testing requires deep security knowledge |
| **Accessibility Testing** | Requires expertise in assistive technologies |
| **Compliance Testing** | Regulated industries need domain expertise |

These specialists may be embedded in teams or work across teams—but they're addressing specific needs, not owning all testing.

### 10.2 Exploratory Testing

[Quadrant 3 testing](https://ucsb-cs48.github.io/topics/testing_agile_testing_crispin_and_gregory/) includes exploratory testing, which benefits from:

- A testing mindset (adversarial thinking)
- Domain knowledge
- Creativity in finding edge cases

Someone with testing expertise can excel at exploratory testing. However, this person is a Developer on the team, not a separate QA role.

### 10.3 Large-Scale Coordination

At enterprise scale, some organizations have:
- Test automation architects (designing test frameworks)
- Quality coaches (enabling multiple teams)
- Test environment managers (coordinating shared resources)

These are coordination roles, not quality ownership roles. The teams still own their testing.

---

## 11. Conclusion

The QA Engineer is not listed as a formal Scrum role for ticket refinement and peer review because:

1. **First Principles Reject It**: "Quality is everyone's responsibility" (Deming). Quality cannot be delegated to a separate role—it must be built in by those who build the product.

2. **Scrum's Design Excludes It**: The Scrum Guide defines three roles. Testing is part of the Developers' responsibility, embedded in the Definition of Done. There are no sub-teams or hierarchies.

3. **DORA Data Validates It**: "When developers are primarily responsible for creating and maintaining suites of automated tests... this drives improved performance." Separate QA roles create handoffs that hurt all four DORA metrics.

4. **Shift-Left Demands It**: Defects found late cost 15-100x more than those found early. Testing at the end (by a separate role) is economically inefficient.

5. **Anti-Patterns Warn Against It**: The handoff model, QA bottleneck, two-sprint testing, and "QA will catch it" mindset are well-documented failure modes.

The answer is not that testing doesn't matter—it matters profoundly. Rather, testing is more effective as a distributed team capability embedded throughout the development process than as a separate phase owned by a specialist role.

People with testing expertise remain valuable—but as Developers on the team who elevate the team's testing capability, not as gatekeepers who test at the end.

---

## Sources

### Official Guides and Frameworks
- [The 2020 Scrum Guide](https://scrumguides.org/scrum-guide.html)
- [Principles behind the Agile Manifesto](http://agilemanifesto.org/principles.html)
- [What is TDD? | Agile Alliance](https://agilealliance.org/glossary/tdd/)

### DORA Research
- [DORA Capabilities: Test Automation](https://dora.dev/capabilities/test-automation/)
- [DORA Capabilities: Continuous Delivery](https://dora.dev/capabilities/continuous-delivery/)
- [DORA Capabilities: Continuous Integration](https://dora.dev/capabilities/continuous-integration/)
- [DORA 2024 State of DevOps Report](https://dora.dev/research/2024/dora-report/)
- [DORA Metrics | Atlassian](https://www.atlassian.com/devops/frameworks/dora-metrics)
- [DORA Metrics Guide | GetDX](https://getdx.com/blog/dora-metrics/)
- [DORA Change Failure Rate | incident.io](https://incident.io/hubs/dora/dora-metrics-change-failure-rate)

### Expert Resources
- [Agile Testing - Lisa Crispin & Janet Gregory](https://agiletester.ca/)
- [Agile Testing Fellowship](https://agiletestingfellow.com/)
- [Agile Testing: A Practical Guide | O'Reilly](https://www.oreilly.com/library/view/agile-testing-a/9780321616944/)

### Scrum and Agile Testing
- [Where Does QA Fit on a Scrum Team? | Scrum.org](https://www.scrum.org/resources/blog/yds-where-does-quality-assurance-qa-fit-scrum-team)
- [Quality Angels in your Scrum Team | Scrum.org](https://www.scrum.org/resources/blog/quality-angels-your-scrum-team)
- [Quality Assurance in Scrum | Agile Pain Relief](https://agilepainrelief.com/glossary/quality-assurance-in-scrum/)
- [How Does QA Fit With Scrum? | LinkedIn](https://www.linkedin.com/pulse/how-does-quality-assurance-fit-scrum-david-pereira)
- [Software Testing in Scrum | QA Madness](https://www.qamadness.com/software-testing-in-scrum/)

### Shift-Left Testing
- [Shift Left Testing in Agile | Knowledge Academy](https://www.theknowledgeacademy.com/blog/shift-left-testing-in-agile/)
- [Shift Left Testing | Abstracta](https://abstracta.us/blog/devops/shift-left-testing/)
- [Shift Left Testing | Katalon](https://katalon.com/resources-center/blog/shift-left-testing-approach)
- [Shift Left Testing | GitHub](https://github.com/resources/articles/security/what-is-shift-left-testing)

### Anti-Patterns
- [QA Bottlenecks in Agile Teams | SoftwareTestPro](https://www.softwaretestpro.com/three-tips-for-dissolving-qa-and-testing-bottlenecks-on-agile-teams/)
- [Anti-Patterns That Silence QA | Medium QualityNexus](https://medium.com/qualitynexus/anti-patterns-in-team-setups-that-silence-qa-49dbd83fb53a)
- [Merging Product Engineering and QA | Medium Inbank](https://medium.com/inbank-product-and-engineering/merging-product-engineering-and-qa-d5ce2b2e639e)
- [QA Separate from Development | Scrum.org](https://www.scrum.org/forum/scrum-forum/32563/qa-separate-development)
- [Sprint Planning When QA Lags | Scrum.org](https://www.scrum.org/forum/scrum-forum/45299/how-sprint-plan-when-qa-always-lags-behind-development)

### Role Transformation
- [The DevOps QA Role | Cprime](https://www.cprime.com/resources/blog/the-devops-qa-role-automated-testing-in-the-devops-lifecycle/)
- [The New Role of QA | Functionize](https://www.functionize.com/blog/the-new-role-of-qa)
- [Quality Engineering in DevOps | Celsior](https://celsiortech.com/role-of-quality-engineering-within-devops-and-ci-cd/)

### Testing Practices
- [Test-Driven Development | Wikipedia](https://en.wikipedia.org/wiki/Test-driven_development)
- [Introduction to TDD | Agile Data](https://agiledata.org/essays/tdd.html)
- [Agile Testing Quadrants | UCSB](https://ucsb-cs48.github.io/topics/testing_agile_testing_crispin_and_gregory/)
- [Whole Team Approach | TrustEd Institute](https://trustedinstitute.com/concept/agile-project-management/agile-testing-quality-assurance/whole-team-approach/)
- [Quality is Everyone's Responsibility | Zenergy](https://www.zenergytechnologies.com/blog/testing/quality-testing)

### Additional Resources
- [DORA Metrics in Testing | mabl](https://www.mabl.com/articles/using-dora-metrics-in-software-development-and-testing)
- [Who Is Responsible for Testing in Scrum? | Kaizenko](https://www.kaizenko.com/who-is-responsible-for-testing/)
- [My Experience as QA in Scrum | InfoQ](https://www.infoq.com/articles/experience-qa-scrum/)
