# Multi-Agent Orchestration: First Principles, Prior Art, and Best Practices

**Last updated:** 2025-12-28  
**Research source:** Web search across industry, academic, and practitioner sources

---

## TL;DR for Our Exercise

Our matrix research exercise (Domain × Stage cells, 8 parallel agents, phased execution) maps well to established patterns. The key applicable concepts are:

1. **Manager-Worker pattern** — We already use this (human as manager, Claude agents as workers)
2. **Barrier synchronization** — Phased stops where all agents must complete before proceeding
3. **Explicit ownership boundaries** — Each agent owns specific cells
4. **Structured handoffs** — Standardized output format for integration
5. **Blackboard pattern** — Shared documentation (orchestrator/) for coordination

---

## Part 1: Directly Applicable to Our Exercise

### 1.1 Coordination Patterns That Fit

| Pattern | How It Maps to Our Exercise | Implementation |
|---------|----------------------------|----------------|
| **Manager-Worker** | Human orchestrates, Claude agents execute | tmux + manual phase advancement |
| **Barrier Synchronization** | All agents must complete Phase 1 before any start Phase 2 | `status.sh` dashboard + manual gate |
| **Explicit Ownership** | Agent A owns `code-capture/`, Agent B owns `code-sense/` | File-level isolation via worktrees |
| **Blackboard** | Shared `orchestrator/` directory with instructions, templates | All agents read from common spec |
| **Handoff Protocol** | Structured output when stopping | `handoff-template.md` |

### 1.2 Best Practices We Should Follow

From OpenAI, Anthropic, and practitioner consensus:

1. **Narrow scope per agent**
   - Each agent gets ONE cell (one domain × one stage)
   - Single responsibility = easier debugging

2. **Clear, high-quality instructions**
   - Shared `agent-instructions.md` with explicit goals, non-goals, output format
   - Reduces ambiguity, improves consistency across agents

3. **Structured output enforcement**
   - All agents produce markdown with defined sections
   - Easier to merge and compare

4. **Phase-based checkpoints**
   - Stop at defined points (Key Influencers → Deep Research → Consolidation)
   - Human reviews before advancement
   - Prevents runaway agents and enables cross-agent learning

5. **Single source of truth**
   - One shared spec (agent-instructions.md)
   - No per-agent variations in goals

### 1.3 Principles Already in Our Playbook

We've already adopted these from prior work:

| Principle | Status |
|-----------|--------|
| Isolation by default (worktrees) | ✓ In playbook |
| Single authoritative spec | ✓ In playbook |
| Explicit ownership boundaries | ✓ In playbook |
| Centralized integration | ✓ In playbook |
| Reproducible handoffs | ✓ In playbook |

---

## Part 2: Potentially Useful for Future Enhancement

### 2.1 Framework Patterns Worth Knowing

| Framework | Core Idea | Potential Use |
|-----------|-----------|---------------|
| **CrewAI** | Role-based teams with defined goals/tools | Could formalize agent roles (Researcher, Synthesizer, Reviewer) |
| **LangGraph** | State-based workflows with checkpoints | Could model phase transitions as a graph |
| **AutoGen** | Conversational multi-agent collaboration | Useful if agents need to negotiate or debate findings |

### 2.2 Consensus Mechanisms

For future phases where agents might have conflicting findings:

| Mechanism | Description | When to Use |
|-----------|-------------|-------------|
| **Voting/Weighted consensus** | Agents vote on disputed findings | Consolidation phase disagreements |
| **Auction/Bidding** | Agents bid on task priority | Cell assignment when some are harder |
| **Iterative refinement** | Sequential agents build on previous output | Chain of reviewers |

### 2.3 Memory and Context Patterns

| Pattern | Description | Potential Use |
|---------|-------------|---------------|
| **RAG (Retrieval-Augmented)** | Agents query shared knowledge base | Cross-cell reference during consolidation |
| **Checkpoint memory** | State saved at phase boundaries | Resume after failures |
| **Conversation history** | Agents maintain context across turns | Multi-session research within a cell |

---

## Part 3: Advanced Concepts (Future Reference)

### 3.1 Protocols for Agent Communication

Emerging standards that may become relevant:

| Protocol | Purpose | Current Status |
|----------|---------|----------------|
| **A2A (Agent-to-Agent)** | Direct agent collaboration | Google/industry emerging |
| **MCP (Model Context Protocol)** | Connect agents to external tools/data | Anthropic standard |
| **ACP (Agent Communication Protocol)** | Multimodal data exchange | Emerging |
| **ANP (Agent Network Protocol)** | Decentralized discovery/trust | Research phase |

### 3.2 Fault Tolerance Patterns

For production multi-agent systems:

| Pattern | Description | Applicability |
|---------|-------------|---------------|
| **Byzantine Fault Tolerance** | Handle malicious/faulty agents | Not needed for our exercise |
| **Raft/Paxos consensus** | Distributed agreement | Overkill for 8 agents |
| **Circuit breakers** | Stop cascading failures | Future production use |

### 3.3 Scalability Considerations

What matters at different scales:

| Scale | Key Concerns | Our Status |
|-------|--------------|------------|
| 1-10 agents | Manual coordination feasible | ✓ Current scope |
| 10-50 agents | Need automated status tracking | Future |
| 50+ agents | Need distributed orchestration | Out of scope |

---

## Part 4: Anti-Patterns to Avoid

### 4.1 Known Failure Modes

| Anti-Pattern | Problem | Our Mitigation |
|--------------|---------|----------------|
| **Agents modifying shared resources** | Merge conflicts, data corruption | Worktree isolation |
| **Unbounded agent execution** | Agents run forever, drift from goal | Explicit phase stops |
| **Silent fallbacks** | Errors hidden, bad output propagates | Require explicit handoff with status |
| **Over-abstraction of instructions** | Agents interpret vaguely, inconsistent output | Concrete examples in instructions |
| **No checkpoint/review** | Bad work compounds across phases | Phase gates with human review |
| **Few-shot mimicry** | Agents copy examples even when inappropriate | Vary examples, emphasize principles |

### 4.2 Coordination Pitfalls

| Pitfall | Description | Avoidance |
|---------|-------------|-----------|
| **Manager bottleneck** | Central coordinator overwhelmed | Batch processing, 8-agent limit |
| **Cross-agent dependencies** | Agent A waits for Agent B | Cells are independent by design |
| **Inconsistent output formats** | Hard to merge/compare | Strict template enforcement |
| **Phase skipping** | Agent rushes ahead | Explicit stop conditions |

---

## Part 5: Mapping to Our Implementation

### Current Architecture Assessment

```
Our Model:

Human (Authority)
   │
   ├── orchestrator/           [Blackboard / Shared Spec]
   │     ├── agent-instructions.md
   │     ├── handoff-template.md
   │     └── status.sh
   │
   └── cells/                  [Isolated Workers]
         ├── code-capture/     → Claude Agent 1
         ├── code-sense/       → Claude Agent 2
         └── ...               → Claude Agents 3-8
```

### Pattern Correspondence

| Industry Pattern | Our Implementation |
|-----------------|-------------------|
| Manager-Worker | Human + Claude agents |
| Blackboard | `orchestrator/` directory |
| Barrier synchronization | Manual phase gates |
| Structured handoff | `handoff-template.md` |
| Ownership boundaries | Worktree isolation |
| Single spec | `agent-instructions.md` |

### What We Don't Need (Yet)

| Concept | Why Not Needed |
|---------|----------------|
| Consensus protocols | Agents don't need to agree; human arbitrates |
| Agent negotiation | Cells are independent |
| Distributed consensus (Raft/Paxos) | 8 agents, human-controlled |
| Real-time communication | Async, phased model |
| Fault tolerance (BFT) | Human oversight catches failures |

---

## Key Takeaways

### For Our Exercise

1. **We're using the right patterns** — Manager-Worker + Barrier + Blackboard
2. **Phase gates are industry best practice** — OpenAI and Anthropic both recommend checkpoints
3. **8 agents is the right scale** — Manageable without needing automation
4. **Worktree isolation is correct** — Standard approach for multi-agent dev work

### For Future Enhancement

1. Consider **CrewAI-style roles** if we want Researcher vs. Synthesizer specialization
2. **LangGraph** could formalize phase transitions as executable graphs
3. **MCP protocol** may standardize how agents access external tools
4. **Automated status tracking** needed if we scale beyond 10 agents

---

## Sources

### Industry Guidance
- OpenAI: Agent best practices (clear instructions, narrow scope, structured output)
- Anthropic: Manager-worker patterns, sub-agent spawning
- IBM: Multi-agent system architectures

### Framework Documentation
- LangGraph: Stateful workflows with checkpointing
- CrewAI: Role-based agent teams
- AutoGen (Microsoft): Conversational multi-agent systems

### Academic/Research
- arXiv: LLM-based multi-agent systems survey
- IEEE: Distributed consensus algorithms
- ResearchGate: Coordination mechanisms in MAS

### Practitioner Experience
- Medium: Framework comparisons (LangGraph vs CrewAI vs AutoGen)
- DataCamp: Multi-agent system tutorials
- Various: Production deployment lessons
