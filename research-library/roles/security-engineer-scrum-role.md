# Security Engineer Role in Scrum Teams: Backlog Grooming, Ticket Refinement, and Peer Review

<!--
metadata:
  id: roles-security-engineer-scrum-2026-01-02
  title: Security Engineer Role in Scrum Teams: Backlog Grooming, Ticket Refinement, and Peer Review
  date: 2026-01-02
  status: draft
  topic: roles
  keywords: [security engineer, scrum, DevSecOps, backlog grooming, ticket refinement, peer review, security champion, shift left, threat modeling]
  consensus: high
  depth: standard
  sources_count: 12
-->

## Executive Summary

- Security Engineers in Scrum teams function as Development Team members who embed security practices throughout the SDLC, not as gatekeepers external to delivery teams
- The Security Champion model is the dominant pattern (high consensus across academic and industry sources), with champions acting as "satellite members" embedded in feature teams
- Shift-left security principles mandate security involvement from sprint planning onward, with 100x cost savings when vulnerabilities are caught in coding vs production
- Security requirements must be integrated during backlog refinement with clear acceptance criteria, not added during sprint planning when time is limited
- Peer review combines automated tools with manual security code review, focusing on OWASP Top 10, input validation, authentication, and authorization
- Threat modeling should occur in 15-30 minute time-boxed sessions during sprint planning using STRIDE or similar frameworks
- Key anti-pattern: treating security as a separate phase or external approval gate rather than embedded team capability
- Academic research identifies 14 steps and 32 actions for establishing sustainable security champion programs

## Consensus Rating

**High**: 8+ primary sources agree across academic research (SpringerLink, ACM), authoritative frameworks (OWASP SAMM, Microsoft STRIDE), and industry implementations (Atlassian, AWS, IBM). The Security Champion model embedded in feature teams is consistently endorsed as best practice for agile environments.

## First Principles

### Role Definition in Scrum Context

In traditional Scrum, teams consist of three roles: Scrum Master, Product Owner, and Development Team members. A Security Engineer operates as a specialized Development Team member, not a separate role outside the core structure. This positioning is critical—security engineers are delivery-focused contributors who happen to specialize in security, not external auditors or compliance officers.

Modern agile organizations face a structural tension: centralized security teams become bottlenecks when collaborating with fast-moving development teams. The solution, validated by both academic research and industry practice, is the Security Champion model. Champions are development team members who receive additional security training while maintaining their primary developer responsibilities. As the BSIMM (Building Security in Maturity Model) describes them, security champions are "satellite members" scattered across the organization who show above-average security interest.

### Shift-Left Security Philosophy

The foundational principle governing security in agile is "shift left"—moving security considerations from the end of the delivery pipeline to the beginning. This principle emerged in response to traditional waterfall approaches where security was often an afterthought or separate process occurring after development completion. Research shows vulnerabilities found in production can cost 100 times more to fix than those caught during the coding phase.

Shift-left aligns naturally with agile's iterative, feedback-driven approach. By integrating security from sprint planning through deployment, teams reduce attack surfaces, improve security posture, and build cross-functional collaboration between developers, security professionals, and QA teams. According to the State of DevOps Report 2020, 45% of companies with full security integration can remediate critical vulnerabilities within a day.

### DevSecOps Integration

DevSecOps extends DevOps philosophy to include security throughout the entire SDLC. Rather than treating security as a phase, DevSecOps integrates security testing and validation into the development process itself. Security controls and monitoring are implemented and maintained throughout the software lifecycle, making security a shared responsibility rather than a specialized function.

## Findings

### Security Champion Model: Academic Foundation

A 2023 systematic literature review published in SpringerLink examined approaches to establishing and maintaining security champions in agile organizations. Analyzing 11 primary studies, researchers developed a classification schema of 14 steps and 32 actions for establishing effective security champion programs. Key findings include:

**Characterization**: Security champions are team-internal roles where agile team members continue as developers but receive additional security training. Organizations use various designations including "security champion," "security specialist," or "secure software engineer."

**Network Structure**: Champions are ideally networked with the company's central security team and other security champions across the organization. This creates a distributed security capability rather than a centralized bottleneck.

**Transition Timeline**: Case studies show a 3-year transition from initial state (central security team working with a few feature teams) to fully autonomous security champion teams. This underscores that implementing the model is a significant organizational change requiring sustained commitment.

**Critical Success Factor**: The main finding emphasizes that security champions require organizational support—they cannot succeed in isolation. Support includes training, time allocation, tooling, and executive backing.

### Backlog Grooming and Refinement

#### When Security Requirements Are Added

OWASP SAMM Agile Guidance explicitly states: "Picking specific requirements for a story is done during creation of the story and during backlog refinement, if necessary with the help of a security expert." Critically, doing this during sprint planning is not recommended because all available time is needed for planning work.

This timing is essential for several reasons:

1. **Planning Accuracy**: Security requirements affect story estimation and resource allocation. Adding them mid-sprint or during planning creates schedule disruption.
2. **Definition of Ready**: Stories cannot be considered "ready" without security considerations. The Definition of Ready should include that security requirements are identified and acceptance criteria updated.
3. **Cognitive Load**: Security thinking requires focused analysis. Cramming this into sprint planning alongside capacity planning and commitment decisions dilutes effectiveness.

#### Methods for Identifying Security Requirements

OWASP SAMM identifies several approaches for selecting appropriate security requirements during refinement:

**Trigger-Based Selection**: Using pick lists to determine whether specific requirements fit the story based on feature characteristics (e.g., handles PII, exposes API, processes payments).

**Expert Consultation**: Leveraging security expertise to efficiently select proper requirements. This is where embedded security champions prove valuable—they can participate in refinement sessions without requiring escalation to central teams.

**Abuse Stories**: Describing how the system can be attacked to help identify weaknesses and link to appropriate requirements. Abuse stories take the form "As an attacker..." and help teams think adversarially about their designs.

**OWASP ASVS Integration**: The OWASP Application Security Verification Standard provides a catalog of available security requirements and verification criteria. Teams select a manageable subset for each sprint, iterating to add more security functionality over time.

#### Security Acceptance Criteria

Security requirements must be written as clear, testable acceptance criteria within the development backlog. Examples include:

- "The API endpoint must only accept HTTPS traffic on port 443"
- "User passwords must meet minimum complexity requirements (12 characters, mixed case, numbers, special characters)"
- "All file uploads are scanned for malware before storage"
- "Session tokens expire after 30 minutes of inactivity"

This specificity ensures security is integrated into planning and estimation from the start, rather than being treated as a last-minute non-functional requirement that derails the project timeline.

#### Definition of Done vs. Acceptance Criteria

Security manifests differently in these two quality checkpoints:

**Definition of Done (DoD)**: Universal, repeatable security criteria that apply to all stories:
- Code scanning results checked and corrective actions taken
- Dependency analysis confirms no vulnerable libraries used
- Test coverage includes security test cases
- Security coding guidelines followed
- Peer review completed by developer with security expertise

**Acceptance Criteria**: Story-specific security requirements:
- Threat and risk analysis completed for the feature
- Specific mitigation requirements implemented (hardening, access controls, encryption)
- Security criteria from acceptance criteria met and verified

The general rule: consider only security criteria that are repeatable and can generally be agreed upon within a team or set of teams for the DoD. Feature-specific security needs belong in acceptance criteria.

### Ticket Refinement Best Practices

#### Breaking Down Security Work

Security tickets should follow the INVEST principle like any other user story:

- **Independent**: Can be implemented without dependencies on other incomplete work
- **Negotiable**: Details can be refined through conversation
- **Valuable**: Delivers tangible risk reduction or compliance value
- **Estimable**: Team can reasonably estimate effort
- **Small**: Completable within a sprint
- **Testable**: Clear verification criteria exist

Large security initiatives should be decomposed into smaller, incremental improvements. For example, "Implement OAuth 2.0 authentication" might decompose into:
1. Research and select OAuth provider
2. Implement basic authorization code flow
3. Add token refresh capability
4. Implement PKCE for mobile clients
5. Add multi-factor authentication

#### Handling Uncertainty

Uncertain security tasks pose risks that can derail sprints. Best practices include:

**Flag High-Risk Tickets**: Clearly identify tickets with unknowns or technical challenges during refinement.

**Schedule Discovery Tickets**: Use smaller exploratory tickets to research and reduce uncertainty before committing to implementation work. These might be called "security spikes" following agile spike terminology.

**Time-Boxing**: Set explicit time limits for investigation work to prevent analysis paralysis.

### Threat Modeling in Sprint Planning

#### Timing and Session Structure

Threat modeling should occur in bite-sized chunks closely tied to current sprint work. The most effective approach: 15-30 minute time-boxed sessions during sprint planning to review new features or architecture changes through a security lens.

Martin Fowler's guide on agile threat modeling emphasizes: "Spending fifteen minutes examining the security implications of a new feature can yield more practical value than hours analyzing hypothetical scenarios for code that isn't written yet."

#### Integration Points

**Sprint Planning**: Identify potential security risks tied to user stories and include them in the sprint backlog. This ensures security is prioritized alongside functionality.

**Backlog Refinement**: Assess backlog items for security risks early, before they reach sprint planning.

**Retrospectives**: Review past sprints to address security issues and improve security practices continuously.

#### STRIDE Methodology

STRIDE, developed by Microsoft, is widely adopted for agile threat modeling because of its simplicity and relevance. Each category maps to a type of risk developers can relate to:

- **S**poofing: Can someone impersonate a user or system?
- **T**ampering: Can data be modified without authorization?
- **R**epudiation: Can actions be denied without proof?
- **I**nformation Disclosure: Can sensitive data be accessed inappropriately?
- **D**enial of Service: Can the system be made unavailable?
- **E**levation of Privilege: Can someone gain unauthorized access levels?

#### Core Questions

Every threat modeling session should address three fundamental questions:
1. What are we building?
2. What could go wrong?
3. What are we doing about it?

#### Team Collaboration

Threat modeling must be collaborative rather than performed in isolation. Involve developers, testers, architects, product owners, and security analysts to leverage diverse perspectives and expertise. A security expert should participate when drawing data flow diagrams and performing threat identification.

#### Actionable Outcomes

The primary outcome should be actionable security stories clearly documented with identified owners who add them to their respective backlogs. Avoid threat modeling sessions that produce only documentation without driving concrete work items.

#### Common Challenges

Although threat modeling is viewed as important, agile teams struggle to find time for it. Solutions:

- Use lightweight, focused sessions (15-30 minutes) assessing only critical features or epics
- Focus on high-impact, likely threats initially; expand scope as the team matures
- Avoid overcomplication that overwhelms teams and stalls progress
- Integrate into existing rhythms (sprint planning, design discussions, daily standups)

### Security Code Review and Peer Review

#### Hybrid Approach: Automated + Manual

The most efficient approach combines automated code review with manual peer review. Automated tools scan for common vulnerabilities and coding errors quickly, while manual reviews provide deep insights into business logic and complex security vulnerabilities that automated tools miss.

When automated scanning occurs early and continuously in the SDLC, reviewers can concentrate on:
- Validating effectiveness of security fixes
- Reviewing code architecture
- Identifying complex security flaws automated tools might miss

This practice reduces manual effort while ensuring high-impact vulnerabilities are addressed before they progress through the development lifecycle.

#### Focus Areas for Manual Security Review

**Input Validation**: User input is one of the most exploited attack vectors. Verify all inputs are:
- Sanitized to remove dangerous characters
- Validated for type, length, format, and range
- Escaped properly before use in queries or output
- Protected against SQL injection, XSS, and buffer overflows

**Authentication and Authorization**: Review identity verification and access control mechanisms:
- Strong password policies enforced
- Session management secure (timeouts, secure flags, regeneration)
- Authorization checks present at all access points
- Principle of least privilege applied

**Cryptography**: Verify proper use of encryption:
- Strong algorithms used (no MD5, SHA-1, weak ciphers)
- Keys managed securely (not hardcoded)
- Sensitive data encrypted at rest and in transit
- Random number generation cryptographically secure

**Dependency Management**: Check that no vulnerable libraries are used, dependencies are up-to-date, and supply chain security practices are followed.

#### Review Team Composition

When selecting reviewers, consider:
- Experience with similar projects
- Understanding of security best practices
- Ability to think like potential attackers
- Complementary skills and perspectives

Code reviews should ideally include multiple developers, not just the code author. Including peers, senior developers, and occasionally security experts provides diverse insights and comprehensive feedback.

#### Review Size and Scope

Code under review should be relatively small and confined to a specific issue. This might mean splitting work into several pull requests and reviewing them independently. Small reviews are more thorough and less likely to miss subtle security issues.

#### Documentation and Metrics

Document findings, recommendations, and follow-up remediation actions. Establish metrics to assess effectiveness:
- Number of vulnerabilities identified and resolved
- Improvement in code quality scores
- Speed at which security issues are addressed post-review
- Trend in vulnerability density over time

#### Knowledge Sharing

Code reviews facilitate knowledge transfer about the codebase, solution approaches, and quality expectations. They enable junior developers to learn from senior colleagues, fostering a collaborative learning environment. This ensures no individual becomes a single point of failure.

Empower teams with security training, regular workshops, and knowledge-sharing sessions. Recognize and celebrate when team members identify and resolve complex security issues.

### Security Technical Debt Management

#### What Is Security Debt?

Security debt arises when teams cut corners on encryption, authentication, or vulnerability patching, leaving software exposed to cyber threats and compliance risks. Common sources include:

- Failing to prioritize security updates and patches
- Using outdated libraries or frameworks with known vulnerabilities
- Lack of automated security testing
- Hardcoded credentials or weak authentication
- Missing encryption for sensitive data

The cost of fixing a security incident far outweighs the effort required to prevent it through proper security practices.

#### Why Agile Teams Accumulate Security Debt

Agile emphasizes rapid iteration and frequent delivery, making it easier for technical debt—including security debt—to accumulate. The fast-paced approach helps teams deliver value quickly but often leads to trade-offs that require careful management.

Research shows variations in how practitioners perceive and manage security debt, with some prioritizing delivery speed over security while others consistently maintain security as a priority. Findings emphasize the need for:
- Stronger integration of security practices across the SDLC
- More consistent use of mitigation strategies
- Better balancing of deadlines, resources, and security-related tasks

#### Management Strategies

**Integrate into Sprint Planning**: Debt reduction should be a deliberate part of sprint planning. Allocate dedicated time and resources to addressing security debt to prevent it from snowballing. This enables incremental progress and measurement of debt reduction impact.

**Use Debt Sprints**: Periodically dedicate entire sprints or significant sprint capacity to refactoring and improving existing code instead of solely focusing on new features.

**Prioritize Based on Risk**: Align debt prioritization with business goals. Not all debt requires immediate elimination. Focus on debt that poses the greatest risk to scalability, security, or user experience.

**Automated Testing and CI/CD**: Nothing prevents bugs better than automated tests and continuous integration. When a new bug is found, write a test to reproduce it and fix the issue. If that bug resurfaces, automated tests catch it before customers do.

**Regular Refactoring**: Refactoring is a proactive strategy for maintaining code quality and preventing technical debt. In agile environments where requirements evolve frequently, refactoring ensures existing code remains clean, modular, and aligned with new needs.

**Use Tracking Tools**: Tools such as SonarQube and Coverity measure technical debt and provide data to calculate the technical debt ratio, keeping development on schedule.

**Cross-Functional Collaboration**: Debt is not just a developer's problem. Product owners, designers, and stakeholders should align on trade-offs and repayment strategies.

## Dissenting Views

### The "Security as Enabler vs. Blocker" Debate

A significant tension exists in how security is perceived within agile teams. Some practitioners view security requirements as blockers that slow delivery and create friction. Others see security as an enabler that prevents costly rework and builds customer trust.

Research shows this divide correlates with organizational maturity. Organizations with mature DevSecOps practices consistently report security as enabling faster, more confident delivery because issues are caught early. Teams without mature practices more often experience security as a last-minute gate that rejects work and forces delays.

The consensus view supports security as enabler, but acknowledges this requires investment in:
- Training developers in secure coding
- Automating security checks in CI/CD
- Clear, reasonable security standards
- Partnership between security and development teams

### Shift-Left Limitations

While shift-left security has broad support, some practitioners note limitations:

**Upfront Inspection Burden**: In practice, shift-left has helped organizations release higher-quality software, but upfront inspections often slow production rather than speeding it up. Laborious component inspection can become a new form of waterfall thinking.

**Tool Overload**: Shifting left may lead to tool proliferation and increased complexity. Teams struggle to integrate and manage numerous security tools in their workflows.

**Skill Gaps**: Developers may lack security expertise to effectively perform security tasks. Training programs require time and resources.

**Emerging Alternative: Shift-Up**: Some sources advocate for "shift-up security," which builds on shift-left by embedding security practices across the entire SDLC with scalable automation, universal policies, and context-aware controls. This recognizes that some security verification is most effective in production or near-production environments.

**Balanced Approach**: Best practice emerging from cloud-native architectures: adopt both shift-left and shift-right strategies. Shift-left testing reduces defects and speeds time to market. Shift-right ensures reliability in production by testing under real-world conditions.

### Security Champion Challenges

While the security champion model has strong support, academic research identifies significant challenges:

**Lack of Organizational Support**: Security champions without adequate support from leadership and central security teams struggle to be effective. Support includes training budgets, time allocation, recognition programs, and executive sponsorship.

**Burnout Risk**: Champions maintain dual responsibilities (development + security), which can lead to overwork and burnout without proper workload management.

**Inconsistent Implementation**: Organizations vary widely in how they implement champion programs. Some provide extensive training and support; others simply designate someone as "security champion" without resources or authority.

**Network Effect Delays**: Case studies show 3-year transitions to mature champion programs. Organizations should set realistic expectations rather than expecting immediate results.

## Reusable Artifacts

### Security Backlog Refinement Checklist

**Pre-Refinement (Story Creation)**
- [ ] Identify if story handles sensitive data (PII, credentials, financial)
- [ ] Identify if story exposes new API endpoints or interfaces
- [ ] Identify if story changes authentication or authorization logic
- [ ] Identify if story processes user input or file uploads
- [ ] Draft initial abuse stories for adversarial scenarios

**During Refinement Session**
- [ ] Security champion or expert participates in session
- [ ] Select applicable OWASP ASVS requirements for story
- [ ] Add security acceptance criteria to story
- [ ] Flag high-risk or uncertain security aspects
- [ ] Estimate security testing effort as part of story estimate
- [ ] Verify story meets Definition of Ready including security criteria
- [ ] Create follow-up security spike tickets if needed

**Post-Refinement**
- [ ] Update Definition of Done if new repeatable security criteria identified
- [ ] Link story to relevant threat model documentation
- [ ] Tag story with security-related labels for filtering and reporting

### Threat Modeling Session Template

**Time Box**: 15-30 minutes

**Participants**: Developer(s), Security Champion/Engineer, Product Owner (optional)

**Agenda**:
1. **What are we building?** (5 min)
   - Brief description of feature
   - High-level data flow diagram (whiteboard or tool)
   - Identify trust boundaries and external interfaces

2. **What could go wrong?** (15 min)
   - Apply STRIDE to each component and data flow:
     - Spoofing: Authentication weaknesses?
     - Tampering: Data integrity risks?
     - Repudiation: Audit/logging gaps?
     - Information Disclosure: Data exposure risks?
     - Denial of Service: Availability vulnerabilities?
     - Elevation of Privilege: Authorization bypasses?
   - Capture 3-5 highest priority threats

3. **What are we doing about it?** (10 min)
   - For each priority threat, identify mitigation:
     - Existing control already handles it
     - Add new security requirement to story
     - Create separate security story for backlog
     - Accept risk (document and track)
   - Assign owners for follow-up actions

**Outputs**:
- Updated acceptance criteria with security requirements
- New security stories in backlog
- Risk acceptance documentation (if applicable)
- Updated threat model documentation

### Security Code Review Checklist

**Before Review**
- [ ] Automated security scans completed (SAST, dependency check)
- [ ] Review scope is small and focused
- [ ] Reviewer has security context (related threats, requirements)

**Input Validation**
- [ ] All external inputs validated for type, length, format, range
- [ ] Inputs sanitized and escaped appropriately
- [ ] SQL parameterized or ORM used (no string concatenation)
- [ ] File upload types and sizes restricted
- [ ] Regular expressions validated for ReDoS vulnerabilities

**Authentication & Authorization**
- [ ] Authentication required for protected resources
- [ ] Authorization checks present at all access points
- [ ] Session management secure (timeouts, secure flags, regeneration)
- [ ] Password complexity requirements enforced
- [ ] Multi-factor authentication considered for sensitive operations

**Cryptography**
- [ ] Strong algorithms used (AES-256, SHA-256, RSA-2048+)
- [ ] No hardcoded keys or credentials
- [ ] Secure random number generation for tokens/IVs
- [ ] TLS/HTTPS enforced for sensitive data transmission
- [ ] Sensitive data encrypted at rest

**Error Handling & Logging**
- [ ] Error messages do not reveal sensitive information
- [ ] Security events logged (auth failures, access violations)
- [ ] Logs do not contain passwords or sensitive data
- [ ] Exceptions handled gracefully without exposing stack traces

**Dependencies & Configuration**
- [ ] No vulnerable dependencies identified by scans
- [ ] Dependencies pinned to specific versions
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Debug features disabled in production configuration
- [ ] Secrets managed via secure mechanism (vault, env vars)

**After Review**
- [ ] Findings documented with severity ratings
- [ ] Remediation actions assigned and tracked
- [ ] Knowledge shared with team (learning opportunity)
- [ ] Metrics updated (vulnerabilities found, time to remediate)

### Security Debt Tracking Template

| ID | Description | Risk Level | Affected Component | Created Date | Target Remediation | Owner | Status |
|----|-------------|-----------|-------------------|--------------|-------------------|-------|--------|
| SD-001 | Legacy auth uses MD5 hashing | High | User Service | 2025-10-15 | Q1 2026 Sprint 3 | J. Smith | Planned |
| SD-002 | No rate limiting on API | Medium | API Gateway | 2025-11-02 | Q1 2026 Sprint 5 | A. Johnson | Planned |
| SD-003 | Outdated OpenSSL version | High | All Services | 2025-12-01 | Q1 2026 Sprint 1 | Security Team | In Progress |

**Risk Levels**:
- **Critical**: Active exploit exists, immediate remediation required
- **High**: Significant vulnerability, remediate within 1 quarter
- **Medium**: Moderate risk, remediate within 2 quarters
- **Low**: Minor issue, remediate within 1 year or accept risk

## Sources

1. [Cybersecurity Jobs in 2026: Top Roles, Responsibilities, and Skills | Splunk](https://www.splunk.com/en_us/blog/learn/cybersecurity-jobs-skills-responsibilities.html) — authority: secondary — Overview of cybersecurity engineer responsibilities in modern contexts
2. [Common DevOps Roles and Responsibilities Today | Splunk](https://www.splunk.com/en_us/blog/learn/devops-roles-responsibilities.html) — authority: secondary — Security engineer role within DevOps teams
3. [What Is DevSecOps? Definition and Best Practices | Microsoft Security](https://www.microsoft.com/en-us/security/business/security-101/what-is-devsecops) — authority: primary — Microsoft's authoritative definition and best practices
4. [What is DevSecOps? | AWS](https://aws.amazon.com/what-is/devsecops/) — authority: primary — AWS official guidance on DevSecOps principles
5. [8 Best Practices for Code Review Quality and Security | Legit Security](https://www.legitsecurity.com/aspm-knowledge-base/best-practices-for-code-review) — authority: secondary — Comprehensive security code review practices
6. [Security code review - best practices | Checkmarx](https://checkmarx.com/learn/developers/secure-code-review-6-best-practices-every-developer-should-follow/) — authority: secondary — Developer-focused secure code review guidance
7. [7 Best Practices for Security Code Reviews | Codacy](https://blog.codacy.com/security-code-review-best-practices) — authority: secondary — Practical security review implementation
8. [Shift-Left Security in Agile Development | DevOps Security Hub](https://medium.com/@devopshub/shift-left-security-in-agile-development-f099ad6c5922) — authority: secondary — Shift-left integration with agile methodologies
9. [What is Shift Left Security? | Orca Security](https://orca.security/resources/blog/what-is-shift-left-security/) — authority: secondary — Shift-left security concepts and benefits
10. [Establishing a Security Champion in Agile Software Teams: A Systematic Literature Review | SpringerLink](https://link.springer.com/chapter/10.1007/978-3-031-28073-3_53) — authority: primary — Academic systematic literature review on security champions
11. [Security Champions Without Support: Results from a Case Study | ACM](https://dl.acm.org/doi/fullHtml/10.1145/3617072.3617115) — authority: primary — Academic case study on security champion implementation
12. [SAMM Agile Guidance | OWASP](https://owaspsamm.org/guidance/agile/) — authority: primary — OWASP authoritative guidance on security in agile
13. [C1: Define Security Requirements | OWASP Top 10 Proactive Controls](https://top10proactive.owasp.org/archive/2018/c1-security-requirements/) — authority: primary — OWASP security requirements framework
14. [Threat Modeling Guide for Software Teams | Martin Fowler](https://martinfowler.com/articles/agile-threat-modelling.html) — authority: primary — Authoritative guide on agile threat modeling
15. [Threat Modeling in Agile Development | Security Compass](https://www.securitycompass.com/blog/threat-modeling-in-agile-development/) — authority: secondary — Practical threat modeling integration
16. [Definition of done, ready — and security | Medium](https://medium.com/@gaurav.bhorkar/dod-dor-and-security-aff3ab1c4728) — authority: secondary — Security in Definition of Done
17. [What is an Abuser Story (Software) | Rietta](https://rietta.com/what-is-an-abuser-story-software/) — authority: secondary — Abuse story concept and usage
18. [What Is Technical Debt? | IBM](https://www.ibm.com/think/topics/technical-debt) — authority: primary — IBM's authoritative overview of technical debt
19. [Say 'bye' to tech debt: Agile solutions for clean development | Atlassian](https://www.atlassian.com/agile/software-development/technical-debt) — authority: secondary — Agile technical debt management
20. [Managing Security in Software Or: How I Learned to Stop Worrying and Manage the Security Technical Debt | ResearchGate](https://www.researchgate.net/publication/334084753_Managing_Security_in_Software_Or_How_I_Learned_to_Stop_Worrying_and_Manage_the_Security_Technical_Debt) — authority: primary — Academic research on security technical debt

---
_Generated by researcher v2.0_
_Status: draft (pending review)_
