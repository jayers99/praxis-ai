# Multi-Agent Development with Claude, Copilot, and Agentic Tools

*Last updated: 2025-12-28*

## Purpose

This document consolidates best practices and practical guidance for running **multiple AI agents in parallel** during software development. It focuses on **Claude Code** as the primary orchestrator, with comparisons to **GitHub Copilot** and **agentic frameworks (e.g., Antigravity)**, and formalizes the mental model of Claude as a **foreman** rather than an autonomous manager.

---

## Core Question

Can modern AI coding tools autonomously schedule, manage, and integrate multiple agents and git worktrees?

**Short answer:** No.

**Long answer:** Current tools can *procedurally orchestrate* work when explicitly instructed, but none own the execution loop end-to-end.

---

## Best Practices for Multi-Agent Work

### 1. Prefer Git Worktrees

- One worktree per agent
- One branch per agent
- Clean isolation with shared repository history

Example:

```bash
git worktree add ../proj-agent-a -b agent/a
git worktree add ../proj-agent-b -b agent/b

cd ../proj-agent-a && claude
cd ../proj-agent-b && claude
```

---

### 2. Enforce Explicit Ownership Boundaries

Define file- and responsibility-level ownership to avoid merge conflicts:

- Agent A owns `src/service_a/**`
- Agent B owns `src/service_b/**`
- Only one agent modifies lockfiles (`poetry.lock`, `package-lock.json`, etc.)

---

### 3. Maintain a Single Authoritative Spec

All agents work from:

- One shared spec
- Clear goals and non-goals

Each agent must produce a **handoff summary**:

- Summary of changes
- List of files touched
- How to run tests
- Assumptions and open questions

---

### 4. Isolate Runtime Resources

Common collision points:

- Ports
- Databases
- Containers
- Caches and virtual environments

Mitigations:

- Per-agent `PORT`
- Per-agent `COMPOSE_PROJECT_NAME`
- Per-worktree virtualenvs

---

### 5. Centralize Integration

Agents:

- Implement changes
- Run self-tests
- Stop

Integration:

- Happens once
- Intentionally
- Via a human or a dedicated integration agent

---

## Claude Code Capabilities

Claude **can**:

- Create and manage git worktrees (when instructed)
- Spawn sub-agents with scoped roles
- Follow explicit rules and ownership boundaries
- Review work against the original intent and spec

Claude **cannot**:

- Autonomously schedule work
- Persist orchestration state across sessions
- Continuously monitor repository state
- Enforce locks or merge policies without external tooling

---

## Tool Comparison

### Claude Code

**Role:** Foreman

- Strong task decomposition
- High adherence to rules and constraints
- Good spec-to-execution fidelity
- No autonomous control loop

### GitHub Copilot

**Role:** Worker / Pair Programmer

- Reactive and editor-local
- No awareness of agent lifecycles
- No orchestration or coordination capabilities

### Antigravity / Agentic Frameworks

**Role:** Research-Grade Coordinator

- Can model agent graphs and task flows
- Require significant glue code
- Fragile without strong guardrails
- Not production-hardened

---

## The Foreman Mental Model

A foreman:

- Reads and interprets the plan
- Breaks work into tasks
- Assigns tasks to specialists
- Enforces boundaries
- Reviews output before integration

Claude performs best when used explicitly in this role.

A foreman does *not*:

- Decide when work begins
- Run continuously or autonomously
- Merge code without oversight
- Hold final authority

That authority remains external (human, scripts, CI).

---

## Practical Architecture

```
Claude = Brain
Git + Shell = Hands
Human = Authority
```

This separation reflects the current state of AI-assisted development.

---

## Bottom Line

- No current AI tool fully owns the multi-agent execution loop
- Claude Code is the strongest procedural orchestrator available today
- True autonomy requires an external scheduler and policy engine

Until that exists, treat AI systems as **high-leverage foremen**, not managers.

---

## Optional Next Steps

- Create a reusable `MULTI_AGENT_PLAYBOOK.md`
- Add an `agentctl.sh` wrapper for worktree management
- Define and standardize an agent handoff template

---

*End of document.*