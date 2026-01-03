# Multi-Agent Role Specialization as Context Memory Mitigation

**Research Report**
**Date:** 2026-01-02
**Status:** Draft → Revised (CCR feedback applied)

---

## Hypothesis Under Evaluation

> Groups of AI agents with narrowly defined roles—each having only the necessary background to complete a portion of a well-defined software feature ticket—can solve the problem of limited context memory by distributing cognitive load across specialized agents who hand off to an implementation agent.

**Example:** A crew of specialized AI agents (Python developer, QA engineer, architect) each with domain-specific memory and knowledge, collaborating on portions of an implementation ticket.

---

## Executive Summary

The hypothesis is **partially supported with significant caveats**. Multi-agent role specialization can mitigate context window limitations under specific conditions, but introduces coordination overhead that can negate the benefits. The evidence suggests this pattern works best for:

- **High-value, complex tasks** where the value justifies 15x token overhead
- **Well-shaped tickets** with clear boundaries and handoff points
- **Tasks exceeding ~30K tokens** where single-agent performance degrades
- **Parallelizable subtasks** that don't require tight coordination

It fails or underperforms when:
- Tasks require cross-cutting context that spans role boundaries
- Coordination overhead exceeds parallelization gains
- Handoff protocols lose critical information ("game of telephone")
- The orchestrator becomes its own context bottleneck

---

## Evidence Map

### Supporting Evidence

| Claim | Strength | Source |
|-------|----------|--------|
| Multi-agent outperforms single-agent on complex tasks | **Strong** | Anthropic: 90.2% improvement on research evaluations |
| Parallel context windows enable distributed reasoning | **Strong** | Anthropic, Google ADK |
| Role specialization reduces per-agent context requirements | **Moderate** | MetaGPT, CrewAI architecture |
| Context window performance degrades with length | **Strong** | Hong et al. (2025) "Context Rot" study |
| Subagents compress information before returning to coordinator | **Moderate** | Anthropic research system |

### Refuting Evidence

| Claim | Strength | Source |
|-------|----------|--------|
| Multi-agent uses 15x more tokens than single-agent | **Strong** | Anthropic measurements |
| 79% of multi-agent failures stem from specification/coordination | **Strong** | arXiv:2503.13657 |
| Coordination overhead scales non-linearly with agent count | **Strong** | Multiple sources |
| Handoffs are the primary failure point | **Strong** | Skywork AI, Google ADK |
| Simple memory (minimal context) outperforms complex memory | **Moderate** | Efficient Agents research |

---

## 1. Context Economics: Does Role Specialization Save Tokens?

### The Math

| Configuration | Token Usage | Performance |
|---------------|-------------|-------------|
| Single chat interaction | 1x baseline | Baseline |
| Single agent with tools | ~4x baseline | Higher than chat |
| Multi-agent system | ~15x baseline | 90.2% higher (Anthropic) |

**Key finding:** Multi-agent systems don't *save* tokens—they *spend more* to achieve better outcomes on complex tasks.

> "Multi-agent experiments were found to be much more cost-effective in long-context scenarios... Multi-agent systems begin to outperform single-agent baselines beyond the 30K token range."
> — [Snorkel AI](https://snorkel.ai/blog/multi-agents-in-the-context-of-enterprise-tool-use/)

**Important caveat:** The ~30K threshold is derived from specific benchmarks on specific models (circa 2025). This threshold is likely:
- **Model-dependent**: Different models have different context handling characteristics
- **Time-bound**: As context windows expand (Claude 3: 200K, GPT-4 Turbo: 128K), this crossover point may shift
- **Task-dependent**: Complex reasoning tasks may hit degradation earlier than retrieval tasks

**Recommendation:** Measure your own crossover point for your specific model, task type, and quality requirements rather than treating 30K as a universal constant.

### When It Works

The pattern succeeds when:

1. **Task value exceeds token cost**: High-stakes tasks where 15x tokens is acceptable
2. **Context exceeds single-window efficiency**: Beyond ~30K tokens, parallel windows win
3. **Subtasks are genuinely parallelizable**: Each agent explores different aspects simultaneously

> "Subagents facilitate compression by operating in parallel with their own context windows, exploring different aspects of the question simultaneously before condensing the most important tokens for the lead research agent."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)

### When It Fails

**Coordination overhead negates gains:**

> "Two agents require one exchange; ten agents may need 45. With each exchange, costs rise, delays mount, and the chance of errors multiplies."
> — [orq.ai](https://orq.ai/blog/why-do-multi-agent-llm-systems-fail)

**Handoff latency accumulates:**

> "Handoff latency ranges from 100ms to 500ms per interaction. A workflow requiring 10 agent handoffs adds 1-5 seconds of pure coordination overhead."
> — [Galileo AI](https://galileo.ai/blog/multi-agent-coordination-strategies)

---

## 2. Handoff Fidelity: What Gets Lost?

### The "Game of Telephone" Problem

> "Subagent output to a filesystem to minimize the 'game of telephone'... prevents information loss during multi-stage processing."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)

When agents pass information through conversation, each hop degrades signal quality. Anthropic's solution: **bypass the coordinator entirely** by having subagents write directly to persistent storage.

### What Gets Preserved vs. Lost

| Preserved (with good architecture) | Lost (without safeguards) |
|-----------------------------------|---------------------------|
| Structured outputs (JSON schemas) | Free-text nuance |
| Explicit research plans | Implicit reasoning |
| Artifacts in external storage | Intermediate reasoning chains |
| Lightweight references | Full context history |
| Citations and provenance | Turn-by-turn dialogue |

### Google's ADK Solution: Narrative Casting

> "Prior Assistant messages are re-cast as narrative context... tool calls from other agents are marked or summarized. This builds a fresh Working Context from the sub-agent's point of view while preserving factual history."
> — [Google Developers Blog](https://developers.googleblog.com/en/architecting-efficient-context-aware-multi-agent-framework-for-production/)

**Key techniques:**
- **Action attribution**: Mark who did what to prevent confusion
- **Selective event filtering**: Drop irrelevant events before the model sees them
- **Artifact externalization**: Large payloads stay external; agents see summaries

### Best Practice: Structured Handoff Schema

```json
{
  "schemaVersion": "1.0",
  "summary": "Concise task outcome",
  "citations": ["source1", "source2"],
  "evidence_map": {
    "claim": "supporting/refuting evidence"
  },
  "open_questions": ["unresolved item"],
  "confidence": 0.85,
  "tool_state": {},
  "trace_id": "uuid"
}
```

> "Treat inter-agent transfer like a public API: constrain model outputs at generation time using JSON Schema-based structured outputs."
> — [Skywork AI](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)

---

## 3. Coordination Costs: Does the Orchestrator Become a Bottleneck?

### Yes, Without Careful Design

> "The current synchronous execution model creates constraints: lead agents 'waiting for each set of subagents to complete before proceeding' creates bottlenecks in information flow."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)

### Orchestration Patterns Compared

| Pattern | Context Handling | Coordination Overhead |
|---------|-----------------|----------------------|
| **Agents as Tools** | Minimal context passed to subagent | Low—fire and forget |
| **Agent Transfer** | Full context inheritance | High—full handoff |
| **Shared Memory** | External store, agents query as needed | Medium—query overhead |

### Scaling Behaviors

| Framework | Scaling Strategy | Trade-off |
|-----------|-----------------|-----------|
| **CrewAI** | Horizontal agent replication, task parallelization | Simpler but less flexible |
| **LangGraph** | Distributed graph execution, parallel nodes | More control but state management complexity |
| **AutoGen** | Conversation sharding | Context coherence challenges |

---

## 4. Framework Evidence

### CrewAI: Role-Based Teams

> "CrewAI uses structured, role-based memory with RAG support for contextual agent behavior... Each task is a fresh prompt that includes relevant prior outputs."
> — [DataCamp](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)

**Strengths:** Well-established memory concept, seamless state management
**Weaknesses:** Doesn't maintain long conversation buffers; persistence requires explicit saves

### MetaGPT: Company-Like Structure

> "MetaGPT models multi-agent systems as company-like structures, assigning roles like CEO, CTO, or Engineer and simulating collaboration within a corporate-style framework."
> — [ioni.ai](https://ioni.ai/post/multi-ai-agents-in-2025-key-insights-examples-and-challenges)

**Use case:** Structured software engineering workflows (requirements → design → code → review)

### AutoGen: Conversational Orchestration

> "AutoGen treats workflows as conversations between agents... focuses on conversation-based memory, maintaining dialogue history for multi-turn interactions."
> — [Amplework](https://www.amplework.com/blog/langgraph-vs-autogen-vs-crewai-multi-agent-framework/)

**Best for:** Dynamic multi-agent conversations, creative problem-solving

---

## 5. Failure Modes

### Primary Failure Categories

From [arXiv:2503.13657](https://arxiv.org/abs/2503.13657) analysis of 1600+ traces across 7 frameworks:

| Category | % of Failures |
|----------|---------------|
| Specification problems | 41.77% |
| Coordination failures | 36.94% |
| Task verification | ~21% |

**Combined: 79% of failures stem from specification/coordination—not individual agent capability.**

### Cross-Cutting Concerns

> "While it's tempting to treat each failure mode in multi-agent LLM systems as isolated, beneath the surface lies a network of cross-cutting issues that amplify risk."
> — [orq.ai](https://orq.ai/blog/why-do-multi-agent-llm-systems-fail)

**The cascade problem:**

> "A single misinterpreted message or misrouted output early in the workflow can cascade through subsequent steps, leading to major downstream failures."
> — [Galileo AI](https://galileo.ai/blog/multi-agent-coordination-strategies)

### Specific Failure Patterns

| Pattern | Description | Mitigation |
|---------|-------------|------------|
| **Infinite handoff loops** | Agents bounce tasks back and forth | Explicit termination conditions |
| **Resource contention** | Agents compete for shared tools/APIs | Rate limiting, queuing |
| **Context drift** | Gradual performance decay over time | Regular context reset |
| **Siloed context** | Agents lack full picture | Shared memory stores |
| **Action confusion** | Agent thinks it did what another did | Action attribution |

### 5.6 Security Considerations

Multi-agent systems introduce attack surfaces not present in single-agent systems:

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Prompt injection propagation** | A compromised subagent can poison the orchestrator's context | Input validation, sandboxing, output filtering |
| **Trust boundary violations** | Agents may implicitly trust outputs from other agents | Explicit trust policies, verification layers |
| **Audit trail complexity** | Distributed responsibility obscures accountability | Trace IDs, action attribution, centralized logging |
| **Credential leakage** | Agents with tool access may expose secrets in handoffs | Credential isolation, minimal privilege per agent |
| **State poisoning** | Malicious inputs corrupt shared memory stores | Write validation, memory integrity checks |

**Recommendations:**
1. **Define trust boundaries explicitly**: Which agents can invoke which tools? Which can write to shared state?
2. **Implement output validation**: Don't blindly trust subagent outputs; validate against schemas
3. **Maintain audit trails**: Every handoff should include trace_id, timestamp, and agent attribution
4. **Apply least privilege**: Each agent should have only the tools/access required for its role
5. **Monitor for anomalies**: Detect unusual patterns (excessive handoffs, tool abuse, context inflation)

---

## 6. The Alternative: Context Engineering

Some researchers argue against multi-agent entirely:

> "Multi-agent systems are inherently fragile because they introduce coordination complexity that often outweighs their benefits. Some researchers advocate for context engineering—the art of providing a single, highly capable agent with all the information it needs to succeed."
> — [Augment Code](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them)

**Counter-evidence:**

> "Simple Memory, which retains only the agent's observations and actions, minimizes the context window size, resulting in the lowest computational cost. Surprisingly, this configuration also yields the best performance."
> — [Efficient Agents (arXiv)](https://arxiv.org/html/2508.02694v1)

This suggests that **minimal, focused context** may outperform both bloated single-agent and complex multi-agent approaches.

---

## 7. Synthesis: When Role Specialization Works

### Decision Tree: Should I Use Multi-Agent?

```
START: Is the task complex enough to justify coordination overhead?
│
├─ NO → Use single agent
│
└─ YES → Does the task exceed ~30K tokens of context?
         │
         ├─ NO → Can you reduce context via summarization/RAG?
         │       │
         │       ├─ YES → Use single agent with context engineering
         │       └─ NO → Consider multi-agent (but measure ROI)
         │
         └─ YES → Can the task be decomposed into independent subtasks?
                  │
                  ├─ NO → Multi-agent may not help (tight coupling)
                  │
                  └─ YES → Does task value justify 15x token cost?
                           │
                           ├─ NO → Accept single-agent quality degradation
                           │       or reduce scope
                           │
                           └─ YES → Is the ticket "well-shaped"?
                                    │
                                    ├─ NO → Shape the ticket first
                                    │
                                    └─ YES → Use multi-agent with
                                             structured handoffs
```

**Default position:** Start with single-agent. Escalate to multi-agent only when you have measured evidence that single-agent is insufficient.

### What Is a "Well-Shaped Ticket"?

A ticket is "well-shaped" for multi-agent execution when it meets these criteria:

| Criterion | Description | How to Verify |
|-----------|-------------|---------------|
| **Past Formalize stage** | Has explicit formalization artifacts | `docs/sod.md` or equivalent exists |
| **Clear acceptance criteria** | Testable conditions for "done" | Given-When-Then scenarios defined |
| **Bounded scope** | Single feature, not epic | Can be completed in one sprint |
| **Decomposable** | Natural subtask boundaries exist | Can identify 2-4 distinct work units |
| **Explicit interfaces** | Inputs/outputs for each subtask | API contracts or data schemas defined |
| **Low cross-cutting concerns** | Subtasks don't require full codebase context | Each subtask touches ≤3 files |

**Mapping to Praxis Lifecycle:**
- **Pre-Formalize (Capture → Shape)**: NOT suitable for multi-agent—scope is still fluid
- **Formalize → Commit**: Suitable IF acceptance criteria are complete
- **Execute**: Ideal—scope is locked, artifacts exist
- **Sustain**: May work for well-isolated maintenance tasks

**Red flags (ticket is NOT well-shaped):**
- "Refactor the authentication system" (unbounded)
- "Improve performance" (no acceptance criteria)
- "Add feature X and also fix Y" (multiple concerns)
- "Make it work like the old system" (implicit requirements)

### Model Selection Guidance

Different agent roles have different requirements. Match models to roles:

| Role | Recommended Model Tier | Rationale |
|------|------------------------|-----------|
| **Orchestrator** | Fast, cheap (e.g., Haiku, GPT-4o-mini) | Routing decisions, not deep reasoning |
| **Architect** | Capable (e.g., Sonnet, GPT-4o) | System design requires nuance |
| **Developer** | Capable to Frontier (e.g., Sonnet, Opus) | Code generation quality matters |
| **QA/Reviewer** | Capable (e.g., Sonnet, GPT-4o) | Pattern matching, not generation |
| **Research** | Frontier (e.g., Opus, o1) | Deep reasoning, synthesis |

**Token economics example:**

| Configuration | Model Cost | Est. Tokens | Total |
|---------------|------------|-------------|-------|
| Single Opus agent | High | 50K | $$$ |
| Haiku orchestrator + 3 Sonnet specialists | Mixed | 75K (15x overhead) | $$ |
| All Opus multi-agent | High | 75K | $$$$ |

**Recommendation:** Use the cheapest model that meets quality requirements for each role. Don't use frontier models for routing.

### Optimal Conditions

| Factor | Favorable | Unfavorable |
|--------|-----------|-------------|
| **Task complexity** | High (exceeds single-agent capacity) | Low (simple tasks) |
| **Context size** | >30K tokens | <30K tokens |
| **Subtask independence** | High (parallel execution) | Low (tight coupling) |
| **Handoff structure** | Well-defined boundaries | Fuzzy boundaries |
| **Value of task** | High (justifies 15x tokens) | Low |
| **Failure tolerance** | Some tolerance | Zero tolerance |

### Architecture Recommendations

1. **Use structured handoffs**: JSON Schema-based, validated, versioned
2. **Externalize artifacts**: Don't pass large payloads through context
3. **Minimize agent count**: Start with 2-3, add only when proven necessary
4. **Treat coordination as distributed systems**: Contracts, monitoring, circuit breakers
5. **Preserve provenance**: Track who did what for debugging
6. **Implement direct-to-storage writes**: Bypass coordinator for subagent outputs

### The "Crew" Model Assessment

Your proposed model (Python dev + QA engineer + architect):

| Aspect | Assessment |
|--------|------------|
| **Role separation** | Good—clear boundaries between concerns |
| **Handoff structure** | Needs explicit schema definition |
| **Context reduction** | Moderate—each role still needs domain context |
| **Coordination risk** | Medium—three agents = three potential failure points |
| **Best fit** | Shaped, medium-complexity tickets with clear interfaces |

---

## 8. Verdict

### Hypothesis Status: **Partially Supported**

**What the evidence supports:**
- Role specialization *can* reduce per-agent context requirements
- Parallel context windows enable better performance on complex tasks
- Multi-agent outperforms single-agent beyond ~30K token threshold

**What the evidence refutes:**
- This approach *saves* tokens (it uses 15x more)
- Coordination is free (79% of failures are specification/coordination)
- More agents = better results (coordination overhead scales non-linearly)

### Refined Hypothesis

> For well-shaped software implementation tickets exceeding single-agent context efficiency (~30K tokens), a small crew (2-4) of specialized AI agents with structured handoff protocols can outperform single-agent approaches—provided coordination overhead is managed through artifact externalization, schema-based handoffs, and minimal agent count.

**Critical success factors:**
1. Ticket is well-shaped (clear boundaries, acceptance criteria)
2. Handoffs use structured schemas, not free text
3. Subagents write outputs to storage, not through coordinator
4. Agent count is minimized (2-4, not 10+)
5. Task value justifies 15x token cost

---

## Sources

### Primary Research
- [Anthropic - How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Google Developers - Architecting efficient context-aware multi-agent framework](https://developers.googleblog.com/en/architecting-efficient-context-aware-multi-agent-framework-for-production/)
- [arXiv:2503.13657 - Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)
- [arXiv - Efficient Agents: Building Effective Agents While Reducing Cost](https://arxiv.org/html/2508.02694v1)
- [arXiv - A Survey of AI Agent Protocols](https://arxiv.org/abs/2504.16736)

### Framework Comparisons
- [DataCamp - CrewAI vs LangGraph vs AutoGen](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [Amplework - Top Multi-Agent Tools Compared](https://www.amplework.com/blog/langgraph-vs-autogen-vs-crewai-multi-agent-framework/)
- [Turing - A Detailed Comparison of Top 6 AI Agent Frameworks](https://www.turing.com/resources/ai-agent-frameworks)
- [Iterathon - Agent Orchestration 2026 Guide](https://iterathon.tech/blog/ai-agent-orchestration-frameworks-2026)

### Failure Analysis
- [orq.ai - Why Multi-Agent LLM Systems Fail](https://orq.ai/blog/why-do-multi-agent-llm-systems-fail)
- [Galileo AI - Multi-Agent Coordination Strategies](https://galileo.ai/blog/multi-agent-coordination-strategies)
- [Augment Code - Why Multi-Agent LLM Systems Fail](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them)
- [Maxim AI - Multi-Agent System Reliability](https://www.getmaxim.ai/articles/multi-agent-system-reliability-failure-patterns-root-causes-and-production-validation-strategies/)

### Best Practices
- [Skywork AI - Multi-Agent Orchestration Best Practices](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)
- [Vellum - How to Build Multi Agent AI Systems](https://www.vellum.ai/blog/multi-agent-systems-building-with-context-engineering)
- [Factory.ai - The Context Window Problem](https://factory.ai/news/context-window-problem)

### Industry Analysis
- [ioni.ai - Multi-AI Agents in 2025](https://ioni.ai/post/multi-ai-agents-in-2025-key-insights-examples-and-challenges)
- [Classic Informatics - LLMs and Multi-Agent Systems](https://www.classicinformatics.com/blog/how-llms-and-multi-agent-systems-work-together-2025)
- [Snorkel AI - Evaluating multi-agent systems](https://snorkel.ai/blog/multi-agents-in-the-context-of-enterprise-tool-use/)

---

## Related Research

See also: [agile-shared-responsibility-ai-context-memory.md](agile-shared-responsibility-ai-context-memory.md) — explores the broader question of how AI agent memory constraints interact with agile shared responsibility models.

---

## CCR Review (Red Team Critique)

**Reviewer:** Red Team
**Date:** 2026-01-02
**Verdict:** SUGGEST → REVISED

**Revisions Applied (2026-01-03):**
- ✅ Added "What Is a Well-Shaped Ticket?" with operational criteria (Section 7)
- ✅ Added Model Selection Guidance table (Section 7)
- ✅ Added Decision Tree: "Should I Use Multi-Agent?" (Section 7)
- ✅ Added Security Considerations section (Section 5.6)
- ✅ Contextualized 30K threshold with model/time caveats (Section 1)

### Strengths

1. **Honest evidence mapping** — Presents both supporting and refuting evidence with clear source attribution, including the "15x token overhead" and "79% coordination failures" statistics
2. **Practical threshold identification** — The ~30K token threshold for multi-agent efficiency is useful and actionable
3. **Failure mode taxonomy** — Section 5 provides concrete failure patterns with mitigations
4. **Structured handoff schema example** — Gives implementers something concrete to work from
5. **Nuanced verdict** — "Partially Supported" conclusion demonstrates intellectual honesty
6. **Strong source diversity** — Citations span academic papers, vendor research, and practitioner blogs

### Challenges (Assumptions Questioned)

1. **30K Token Threshold Without Context** — Cited from single source (Snorkel AI); may be model-dependent and time-bound. Does it scale with expanding context windows?

2. **15x Token Overhead Accepted Uncritically** — This measurement comes from Anthropic's specific architecture. Different patterns (agents-as-tools vs. full transfer) have vastly different token economics.

3. **"Well-Shaped Tickets" Undefined** — Document uses this phrase repeatedly but never defines it operationally. Critical gap for applying the guidance.

4. **"Company-Like Structure" Analogy May Mislead** — Human org structures evolved under constraints that don't apply to AI agents. May import dysfunctions without benefits.

5. **"Context Rot" Study Cited Without Scrutiny** — What is context rot specifically? If it's lost-in-the-middle effects, prompt engineering might address it without multi-agent distribution.

### Blind Spots

1. **Model Selection Absent** — Which models are best suited for orchestrator vs. specialist roles? Different economics possible.
2. **Security and Trust Boundaries Ignored** — Prompt injection propagation, inter-agent trust, audit trail complexity
3. **Human-in-the-Loop Integration Not Addressed** — Where do code reviews fit? How does Praxis HVA interact?
4. **Testing/Debugging Complexity** — How do you debug failures spanning multiple agents with separate contexts?
5. **State Persistence Across Sessions** — What happens when workflow is interrupted?
6. **"Crew" Assessment Too Shallow** — Missing: role context contents, specific handoff schemas, loop behavior
7. **No Comparison to RAG/Other Strategies** — Multi-agent is one approach; no comparison to retrieval augmentation, summarization, or memory stores

### Risks

1. **Premature Optimization** — Teams may build multi-agent for tasks that don't need it
2. **Complexity Debt** — Schema versioning, contract changes, debugging burden
3. **Framework Lock-In** — Premature adoption without understanding migration costs
4. **Over-Engineering Handoff Schemas** — Protocol may become as complex as the task
5. **Coordinator Single Point of Failure** — Centralized coordination centralizes failure

### Suggested Revisions

**High Priority:**
1. Define "well-shaped ticket" operationally — map to Praxis lifecycle stages
2. Add model selection guidance — orchestrator vs. specialist recommendations
3. Include decision tree — "Should I use multi-agent?"
4. Address security considerations — trust boundaries, prompt injection, audit
5. Contextualize 30K threshold — note it's model/time-specific

**Medium Priority:**
6. Expand "Crew" model with concrete examples
7. Add comparison to RAG and other strategies
8. Address testing and debugging guidance
9. Discuss human integration points

### Consensus Assessment

| Claim | Strength | Notes |
|-------|----------|-------|
| Multi-agent uses significantly more tokens | Strong | Multiple sources |
| Coordination failures are dominant failure mode | Strong | arXiv study with 1600+ traces |
| 30K token threshold | Moderate | Single source; may be model-specific |
| "Well-shaped tickets" as success criteria | Speculative | Undefined term |
| 15x token overhead as universal | Overfit | Architecture-dependent |

---

*CCR performed by Red Team role, 2026-01-02*
