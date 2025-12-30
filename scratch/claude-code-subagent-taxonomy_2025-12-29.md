# Claude Code Subagent Taxonomy: Effective Roles and Design Patterns

_Date: 2025-12-29_
_Timebox: 20 minutes_
_Seeds: none_

## Executive Summary

- **Optimal team size:** Research shows 3-4 specialized agents capture most utility gains, with coordination overhead growing super-linearly (exponent 1.724) beyond this threshold. The "Rule of 4" applies across domains.
- **Single responsibility is paramount:** Each subagent should have one clear goal, input, output, and handoff rule. Tool-heavy tasks suffer 2-6× efficiency penalty from excessive agent decomposition.
- **Context isolation is the killer feature:** Subagents prevent context bloat by maintaining separate windows and returning only relevant results to the orchestrator, not full conversation history.
- **Use subagents for stateful, multi-step work:** Reserve subagents for complex tasks requiring state management and multiple interactions. Use inline tools for discrete, stateless functions.
- **Human role analogs are durable:** Librarian, Reviewer, Architect, Product Manager, and Implementer map cleanly to well-understood engineering roles and withstand organizational change.
- **Tool scoping matters:** Read-only for reviewers/auditors (Read, Grep, Glob), research agents add WebSearch/WebFetch, implementers get Write/Edit/Bash.
- **Naming conventions should be role-based and action-oriented:** Prefer descriptive names that convey purpose (e.g., `research-librarian`, `code-reviewer`) over generic labels (`agent1`, `helper`).
- **Anti-patterns are well-documented:** Context stuffing, unchecked delegation, parallel subagents without shared context, and error amplification through cascading hallucinations.

## Design Principles for Subagents

### 1. Single Responsibility Principle
**Consensus: High** — Multiple independent sources (Claude Code official docs, academic research, industry practitioners) converge on this as foundational.

**Principle:** Each agent should have well-defined responsibilities. Avoid writing prompts that cover too many tasks simultaneously, such as generating content and validating it, in a single prompt. This creates role ambiguity, making debugging more challenging when failures occur. [[Source: Tweag]](https://www.tweag.io/blog/2025-10-23-agentic-coding-intro/)

**Evidence:**
- "Give each subagent one clear goal, input, output, and handoff rule." [[Source: PubNub]](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- "Create subagents with single, clear responsibilities rather than trying to make one subagent do everything. This improves performance and makes subagents more predictable." [[Source: Google Cloud Blog]](https://cloud.google.com/blog/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools)
- All elements of complexity (context length, ambiguity, reliability) are reduced as we limit and focus the responsibility of individual agents. [[Source: Cognizant]](https://www.cognizant.com/us/en/ai-lab/blog/single-agent-vs-multi-agent)

### 2. Context Isolation and Selective Information Return
**Consensus: High** — Core architectural pattern across all major implementations (Claude Code, Cursor, Google ADK).

**Principle:** Isolate per-subagent context. Let the orchestrator maintain the global plan and a compact state, not every detail. Subagents should return only essential results, not full conversation histories. [[Source: Claude Code Docs]](https://code.claude.com/docs/en/sub-agents)

**Evidence:**
- "Subagents maintain separate context from the main agent, preventing information overload and keeping interactions focused. This isolation ensures that specialized tasks don't pollute the main conversation context with irrelevant details." [[Source: VoltAgent]](https://github.com/VoltAgent/awesome-claude-code-subagents)
- "Context overflow can be avoided by designing your system to pass only essential context between agents rather than full conversation histories." [[Source: Google Cloud Blog]](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)
- "The 'context stuffing' anti-pattern should be replaced with a 'memory-based' workflow where agents recall exactly the snippets they need for the current step." [[Source: Medium]](https://medium.com/@armankamran/anti-patterns-in-multi-agent-gen-ai-solutions-enterprise-pitfalls-and-best-practices-ea39118f3b70)

### 3. Tool Specialization by Role
**Consensus: High** — Widely documented in Claude Code official documentation and practitioner guides.

**Principle:** Scope tools per agent based on their read/write/execute permissions. Different roles require different capabilities.

**Evidence:**
- Read-only agents (reviewers, auditors): Read, Grep, Glob — analyze without modifying
- Research agents (analysts, researchers): Read, Grep, Glob, WebFetch, WebSearch — gather information
- Code writers (developers, engineers): Read, Write, Edit, Bash, Glob, Grep — create and execute
[[Source: PubNub]](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)

### 4. Task Decomposability Determines Agent Count
**Consensus: Medium** — Emerging research consensus, but still task-dependent.

**Principle:** Favor single-agent systems or minimal-coordination multi-agent systems for tool-heavy tasks; scale agent teams only when task decomposability and low error rates are guaranteed. [[Source: arXiv]](https://arxiv.org/html/2512.08296v1)

**Evidence:**
- "The Rule of 4": Effective team sizes are currently limited to around three or four agents. Beyond this, communication overhead grows super-linearly (specifically, with an exponent of 1.724). [[Source: VentureBeat]](https://venturebeat.com/orchestration/research-shows-more-agents-isnt-a-reliable-path-to-better-enterprise-ai)
- "Task decomposability modulates optimal architectures: parallelizable tasks benefit greatly from multi-agent (+80.9%), while sequential planning suffers 39-70% degradation." [[Source: arXiv]](https://arxiv.org/html/2512.08296v1)
- Tool-heavy environments with more than 10 tools see 2-6× efficiency penalty from multi-agent systems due to coordination overhead. [[Source: Emergent Mind]](https://www.emergentmind.com/topics/quantitative-scaling-principles-for-agentic-systems)

### 5. Stateful vs. Stateless Determines Subagent vs. Tool
**Consensus: High** — Clear decision criteria from Google Cloud and official documentation.

**Principle:** Use tools for discrete, stateless, and reusable capabilities. Use subagents to manage complex, stateful, and context-dependent processes. [[Source: Google Cloud Blog]](https://cloud.google.com/blog/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools)

**When to use subagents:**
- Complex, multi-step tasks (data visualization: analyze → select chart type → generate)
- State and context management (hotel booking maintaining dates, location, rating preferences)
- Multiple back-and-forth interactions with user
- Specialized instructions with domain-specific best practices

**When to use inline tools:**
- Single, reusable functions (NL2SQL conversion)
- Transactional API-like operations with clear input/output
- Stateless operations

### 6. Human Role Analogs Provide Durable Abstractions
**Consensus: Medium-High** — Widely adopted in practice (CrewAI, MetaGPT, Claude Code examples), though less formally studied.

**Principle:** Model agents after well-understood human roles in software engineering teams. This leverages existing mental models and Conway's Law principles. [[Source: CrewAI, MetaGPT frameworks]](https://insights.daffodilsw.com/blog/5-agentic-ai-frameworks-developers-are-using-to-build-smarter-agents)

**Evidence:**
- MetaGPT "reimagines agentic AI development by simulating the structure of a real-world software company. Each agent is assigned a specific role such as product manager, software architect, programmer, or QA tester." [[Source: Daffodil Software]](https://insights.daffodilsw.com/blog/5-agentic-ai-frameworks-developers-are-using-to-build-smarter-agents)
- "The key thing to remember about Conway's Law is that the modular decomposition of a system and the decomposition of the development organization must be done together." [[Source: Martin Fowler]](https://martinfowler.com/bliki/ConwaysLaw.html)
- Architects represent "institutional knowledge (living documentation) of the system" and help new engineers learn the architecture. [[Source: Medium]](https://medium.com/draftkings-engineering/the-evolving-role-of-the-software-architect-b63c3d3104b3)

### 7. Explicit Descriptions for Orchestrator Routing
**Consensus: High** — Universal best practice across all frameworks.

**Principle:** Write descriptions that clearly indicate when to use the agent. Clear descriptions help the main AI choose the right agent for each task. [[Source: PubNub]](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)

**Evidence:**
- "Keep descriptions action-oriented ('Use after a spec exists; produce an ADR and guardrails')." [[Source: PubNub]](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." [[Source: Anthropic Engineering]](https://www.anthropic.com/engineering/multi-agent-research-system)

## Recommended Subagents

| Name | Primary Responsibility | Explicitly Does NOT Do | Typical Tools | When to Invoke | Consensus |
|------|----------------------|------------------------|---------------|----------------|-----------|
| **Research Librarian** | Gather, verify, and synthesize information from external sources | Generate code, modify files, make decisions | Read, Grep, WebSearch, WebFetch | Need to find authoritative sources, prior art, best practices, or verify claims | High |
| **Code Reviewer** | Analyze code for quality, security, style, and best practices | Implement fixes, run tests, commit changes | Read, Grep, Glob | Pull request review, pre-commit validation, security audit | High |
| **Architect** | Design system structure, evaluate tradeoffs, produce ADRs | Implement code, write tests, deploy | Read, Grep, Glob, (limited Write for ADRs) | New feature design, major refactoring, technology selection | Medium-High |
| **Implementer** | Write code, tests, and documentation for defined specs | Define requirements, make architectural decisions | Read, Write, Edit, Bash, Grep, Glob | After formalization/spec exists; execute against clear acceptance criteria | High |
| **Test Engineer** | Design and execute test strategies, identify edge cases | Implement production code, define features | Read, Write (tests only), Bash, Grep | Test generation, coverage analysis, regression detection | High |
| **Technical Writer** | Create, edit, and maintain documentation | Write code, run tests, make technical decisions | Read, Write (docs only), Grep | Documentation updates, API docs, user guides, README maintenance | Medium |
| **Security Auditor** | Identify vulnerabilities, compliance issues, and security risks | Fix security issues, implement mitigations | Read, Grep, Glob, specialized SAST tools | Security reviews, compliance checks, threat modeling | Medium-High |
| **Product Manager** | Clarify requirements, prioritize features, maintain specs | Implement solutions, review code | Read, Grep, (Write for specs/backlogs) | Requirement gathering, scope definition, backlog refinement | Medium |
| **Release Engineer** | Coordinate deployments, manage environments, orchestrate pipelines | Write application code, design features | Read, Bash (deployment scripts), limited Write | Deployment coordination, environment configuration, release validation | Medium |

### Notes on Consensus Strength

- **High consensus (Librarian, Reviewer, Implementer, Test Engineer):** These roles map directly to well-established human roles and are explicitly documented in multiple frameworks (Claude Code, CrewAI, MetaGPT, GitLab Duo).

- **Medium-High consensus (Architect, Security Auditor):** Widely adopted in practice but with more variation in scope and boundaries. Architect role particularly varies between "visionary designer" and "review/validation" modes.

- **Medium consensus (Technical Writer, Product Manager, Release Engineer):** Less frequently documented as standalone agents; more often bundled with other roles. Technical Writer role validated by Google Cloud case study. PM and Release Engineer less commonly separated in current implementations.

## Anti-Patterns: What NOT to Do

### 1. The Mega-Agent Anti-Pattern
**Problem:** Creating one massive "Do It All" agent that handles multiple concerns.

**Why it fails:** Single point of failure, context bloat, role ambiguity, difficult to debug.

**Solution:** Follow single-responsibility principle; decompose into focused agents. [[Source: SecureAgentOps]](https://www.secureagentops.com/)

### 2. Context Stuffing / Context Explosion
**Problem:** Passing full conversation histories between agents; subagents returning everything instead of summaries.

**Why it fails:**
- Cost/latency spirals (model cost and time-to-first-token grow with context size)
- Signal degradation ("lost in the middle" phenomenon)
- Context window exhaustion

**Solution:** Design agents to pass only essential context; use memory-based retrieval instead of full history dumps. [[Source: Google Cloud Blog, Medium]](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)

### 3. Unchecked Recursive Delegation
**Problem:** Agents granted autonomy to spawn sub-agents indefinitely without supervision.

**Why it fails:** Infinite loops, cost blowouts, context collapse, loss of control.

**Solution:** Implement delegation limits, supervising context, and explicit termination conditions. [[Source: Medium]](https://medium.com/@armankamran/anti-patterns-in-multi-agent-gen-ai-solutions-enterprise-pitfalls-and-best-practices-ea39118f3b70)

### 4. Parallel Subagents Without Shared Context
**Problem:** Multiple subagents working independently without awareness of each other's decisions.

**Why it fails:** "Very fragile" — when one agent diverges from the plan, others lack context to adapt, leading to inconsistent or conflicting outputs.

**Solution:** Ensure every agent action is informed by the context of all relevant decisions made by other parts of the system. Use a shared state manager or orchestrator. [[Source: Google Cloud Blog]](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)

### 5. Error Amplification Through Cascading
**Problem:** Hallucinations or errors from one agent are picked up and compounded by downstream agents.

**Why it fails:** "A misinterpreted RAG result by a researcher is confidently reformulated by a summarizer, making the final output dangerously misleading."

**Solution:** Implement validation checkpoints, fact-checking layers, and human-in-the-loop for critical paths. [[Source: Medium]](https://medium.com/@armankamran/anti-patterns-in-multi-agent-gen-ai-solutions-enterprise-pitfalls-and-best-practices-ea39118f3b70)

### 6. Generic "Helper" or Numbered Agents
**Problem:** Using vague names like "Agent 1," "Helper," "Assistant."

**Why it fails:** Unclear routing decisions, poor maintainability, role ambiguity.

**Solution:** Use role-based, action-oriented naming that clearly communicates purpose. [[Source: Camphouse, Microsoft Learn]](https://camphouse.io/blog/naming-conventions)

### 7. Too Many Agents (Beyond the Rule of 4)
**Problem:** Creating 6+ specialized agents for a single workflow.

**Why it fails:** Coordination overhead grows super-linearly (exponent 1.724); communication costs outpace reasoning value; context fragmentation.

**Solution:** Start with 2-3 agents; add more only when clear decomposition and low error rates are guaranteed. Most utility gains are captured by the first 3-4 agents. [[Source: VentureBeat, arXiv]](https://venturebeat.com/orchestration/research-shows-more-agents-isnt-a-reliable-path-to-better-enterprise-ai)

## Naming Conventions for Subagents

**Consensus: Medium-High** — Well-established in IT/DevOps naming conventions; less formally documented for AI agents specifically.

### Best Practices

1. **Role-based naming:** Use the primary function/responsibility as the name (e.g., `code-reviewer`, `research-librarian`, `security-auditor`).

2. **Action-oriented descriptors:** Names should suggest what the agent does (e.g., `test-engineer` not `testing-helper`).

3. **Avoid generic terms:** Never use `agent1`, `helper`, `assistant`, `team-a`. [[Source: Camphouse]](https://camphouse.io/blog/naming-conventions)

4. **Use consistent prefixes/suffixes if grouping:** For example, if you have domain-specific reviewers, use `backend-reviewer`, `frontend-reviewer`, `database-reviewer`. [[Source: Automic]](https://docs.automic.com/documentation/webhelp/english/ARA/24.3/DOCU/24.3/CDA%20Guides/Content/AWA/Objects/BestPractices/BP_ConsistentNamingConventionsObjects.htm)

5. **Reflect scope boundaries:** If an agent is limited to a specific domain, include it in the name (e.g., `api-architect` vs. `ui-architect`).

6. **Maintain a naming registry:** Document all agent names and their purposes in a shared location for team onboarding. [[Source: Camphouse]](https://camphouse.io/blog/naming-conventions)

### Examples of Good vs. Bad Names

| Bad | Good | Why |
|-----|------|-----|
| agent1 | code-reviewer | Descriptive, role-based |
| helper | research-librarian | Specific function |
| assistant | technical-writer | Clear responsibility |
| review-agent | security-auditor | More specific scope |
| builder | frontend-implementer | Domain + role clarity |

## Open Questions / Areas of Weak Consensus

### 1. How fine-grained should domain specialization be?
**Consensus: Low**

Current implementations vary widely:
- Some use broad agents (one "implementer" for all code)
- Others use highly specialized agents (separate agents for frontend, backend, database, API)

**Open question:** At what point does specialization improve vs. fragment the workflow? The research on coordination overhead suggests broader agents, but practitioner examples show heavy specialization (99 agents in one GitHub example).

**Evidence gaps:** No empirical studies comparing 4 broad agents vs. 8 specialized agents for the same workflow.

### 2. Should agents be stateless or maintain memory across invocations?
**Consensus: Low**

Conflicting guidance:
- Claude Code subagents appear stateless (invoked per-task, context isolated)
- Some frameworks advocate for persistent agent memory (learning from past interactions)

**Open question:** Does agent memory improve performance over time, or does it introduce staleness and inconsistency risks?

### 3. When should agents invoke other agents vs. returning to the orchestrator?
**Consensus: Low-Medium**

Two schools of thought:
- **Strict hierarchy:** All subagents return to main orchestrator; no peer-to-peer invocation
- **Flexible delegation:** Subagents can spawn their own subagents (with limits)

**Trade-offs:** Strict hierarchy is more predictable but less flexible; delegation can handle complexity but risks runaway behavior.

**Best practice (emerging):** Allow one level of delegation with explicit limits, but require orchestrator approval for deeper nesting. [[Source: Anthropic Engineering]](https://www.anthropic.com/engineering/multi-agent-research-system)

### 4. How to measure agent team effectiveness?
**Consensus: Low**

Current metrics are informal:
- Task completion rate
- Token usage
- Time to completion
- Human satisfaction

**Missing:** Standardized benchmarks for multi-agent systems across different domains; no widely accepted "SWE-bench for multi-agent workflows."

### 5. Should agents be user-scoped or project-scoped?
**Consensus: Low-Medium**

Claude Code supports both (`~/.claude/agents/` and `./.claude/agents/`), but best practices are unclear:
- User-scoped agents are portable across projects but may lack project-specific context
- Project-scoped agents are tailored but not reusable

**Emerging pattern:** Generic roles (reviewer, librarian) are user-scoped; domain-specific agents (e.g., "GraphQL API reviewer") are project-scoped.

### 6. How to version and maintain agent prompts over time?
**Consensus: Low**

No established practices for:
- Versioning agent definitions
- Testing agent changes before deployment
- Rolling back problematic agent updates
- A/B testing different agent configurations

**This is a significant gap** as organizations scale agent usage.

## Recommendations for Long-Term Maintainability

1. **Start small (2-3 agents), expand deliberately:** Most utility is captured by the first 3-4 agents. Add more only when you can clearly articulate the coordination overhead cost vs. specialization benefit.

2. **Prefer user-scoped generic roles:** Make broadly useful agents (Librarian, Reviewer, Implementer) available across all projects. Reserve project-scoped agents for highly specific needs.

3. **Document agent boundaries explicitly:** For each agent, write what it DOES and what it explicitly does NOT do. This prevents role creep and clarifies orchestrator routing.

4. **Establish tool budgets:** Limit which tools each agent can access. Treat tool permissions as security boundaries.

5. **Implement monitoring and audit trails:** Track which agents are invoked, how often, and at what cost. This data informs whether agents are properly scoped.

6. **Version agent definitions:** Store agent configs in version control; treat updates like code changes (review, test, deploy).

7. **Build a central agent registry:** Maintain a searchable catalog of available agents with descriptions, example invocations, and success metrics. This prevents duplicate agent creation.

8. **Use Conway's Law intentionally:** Organize agents to mirror your desired system architecture. If you want microservices, create service-specific agents. If you want modular monoliths, use broader domain agents.

## Source List

### Official Documentation and Primary Sources
- [Subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Building agents with the Claude Agent SDK - Anthropic Engineering](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [How we built our multi-agent research system - Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Where to use sub-agents versus agents as tools - Google Cloud Blog](https://cloud.google.com/blog/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools)
- [Architecting efficient context-aware multi-agent framework for production - Google Developers Blog](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)

### Research and Academic Sources
- [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering - arXiv](https://arxiv.org/abs/2405.15793)
- [Towards a Science of Scaling Agent Systems - arXiv](https://arxiv.org/html/2512.08296v1)
- [Quantitative Scaling for Agentic Systems - Emergent Mind](https://www.emergentmind.com/topics/quantitative-scaling-principles-for-agentic-systems)

### Industry Best Practices and Case Studies
- [Best practices for Claude Code subagents - PubNub](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [Supercharge Your Tech Writing with Claude Code Subagents - Google Cloud Community (Medium)](https://medium.com/google-cloud/supercharge-tech-writing-with-claude-code-subagents-and-agent-skills-44eb43e5a9b7)
- [Unleashing Claude Code's hidden power: A guide to subagents - AWS Builder Center](https://builder.aws.com/content/2wsHNfq977mGGZcdsNjlfZ2Dx67/unleashing-claude-codes-hidden-power-a-guide-to-subagents)

### Multi-Agent Frameworks and Patterns
- [5 Agentic AI Frameworks Developers Are Using - Daffodil Software](https://insights.daffodilsw.com/blog/5-agentic-ai-frameworks-developers-are-using-to-build-smarter-agents)
- [Introduction to Agentic Coding - Tweag](https://www.tweag.io/blog/2025-10-23-agentic-coding-intro/)
- [Single Agent vs. Multi-Agent - Cognizant AI Lab](https://www.cognizant.com/us/en/ai-lab/blog/single-agent-vs-multi-agent)

### Anti-Patterns and Research Findings
- ['More agents' isn't a reliable path to better enterprise AI systems - VentureBeat](https://venturebeat.com/orchestration/research-shows-more-agents-isnt-a-reliable-path-to-better-enterprise-ai)
- [Anti-Patterns in Multi-Agent Gen AI Solutions - Medium](https://medium.com/@armankamran/anti-patterns-in-multi-agent-gen-ai-solutions-enterprise-pitfalls-and-best-practices-ea39118f3b70)
- [DevSecOps for AI Agents - SecureAgentOps](https://www.secureagentops.com/)

### DevSecOps and Security-Specific Agents
- [GitLab Duo Agent Platform: What's next for intelligent DevSecOps](https://about.gitlab.com/blog/gitlab-duo-agent-platform-what-is-next-for-intelligent-devsecops/)
- [DevSecOps with Agentic AI - TestingXperts](https://www.testingxperts.com/blog/devsecops-with-agentic-ai/)

### Human Role Analogs and Organizational Design
- [The Evolving Role of the Software Architect - DraftKings Engineering (Medium)](https://medium.com/draftkings-engineering/the-evolving-role-of-the-software-architect-b63c3d3104b3)
- [Conway's Law - Martin Fowler](https://martinfowler.com/bliki/ConwaysLaw.html)
- [Conway's Law - Wikipedia](https://en.wikipedia.org/wiki/Conway's_law)

### Naming Conventions
- [Naming Conventions Best Practices - Camphouse](https://camphouse.io/blog/naming-conventions)
- [Best Practices: Naming Conventions - Automic](https://docs.automic.com/documentation/webhelp/english/ARA/24.3/DOCU/24.3/CDA%20Guides/Content/AWA/Objects/BestPractices/BP_ConsistentNamingConventionsObjects.htm)
- [Define your naming convention - Microsoft Learn](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)

### AI Coding Tool Comparisons
- [Cursor vs GitHub Copilot - Janea Systems](https://www.janeasystems.com/blog/your-next-developer-ai-agent-cursor-vs-copilot)
- [Discovering Agent Mode in Copilot and Cursor IDE - Jovylle Hub](https://hub.jovylle.com/posts/discovering-agent-mode-in-copilot-and-cursor-ide)

### Community Resources
- [awesome-claude-code-subagents - GitHub](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [ClaudeLog - Sub Agents](https://claudelog.com/mechanics/sub-agents/)
- [Claude Code customization guide - alexop.dev](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/)
