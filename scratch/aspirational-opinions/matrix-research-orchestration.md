# Matrix Research Orchestration Guide

**Last updated:** 2025-12-28

A practical guide for running multi-agent research across a multidimensional matrix (e.g., Domain × Lifecycle Stage). Incorporates lessons from `scratch/multi-agent/` playbooks.

---

## The Problem

You have a research task spanning a matrix of cells:

```
              Capture  Sense  Explore  Shape  Formalize  Commit  Execute  Sustain  Close
Code             ○       ○       ○       ○        ○        ○       ○        ○       ○
Create           ○       ○       ○       ○        ○        ○       ○        ○       ○
Write            ○       ○       ○       ○        ○        ○       ○        ○       ○
Observe          ○       ○       ○       ○        ○        ○       ○        ○       ○
Learn            ○       ○       ○       ○        ○        ○       ○        ○       ○
```

Each cell requires phased research (key influencers → deep research → consolidation).

Running sequentially = too slow. You want **8 agents in parallel**.

---

## Core Principles (from Multi-Agent Playbook)

1. **Isolation by default** — one worktree + branch per agent
2. **Single source of truth** — one shared spec/instructions for all agents
3. **Explicit ownership** — each agent owns specific cells, no overlap
4. **One integration gate** — merges are centralized and deliberate
5. **Reproducibility** — every agent produces a structured handoff

---

## Architecture: The Matrix Worktree Farm

### Directory Structure

```
praxis-ai/
scratch/
  matrix-research/
    orchestrator/                   # Control plane
      agentctl.sh                   # Worktree management (from scratch/multi-agent/)
      matrix.yaml                   # Cell definitions + status
      agent-instructions.md         # Shared prompt template
      handoff-template.md           # Standardized handoff format
      status.sh                     # Progress dashboard
      advance-phase.sh              # Batch advance agents
    
    cells/                          # Research worktrees (created dynamically)
      code-capture/
      code-sense/
      ...
    
    output/                         # Final merged artifacts
      code/
        capture.md
        ...
```

---

## Step 1: Bootstrap Infrastructure

### 1.1 Create orchestrator directory

```bash
mkdir -p scratch/matrix-research/{orchestrator,cells,output}
```

### 1.2 Copy agentctl.sh (adapted for matrix use)

The existing `scratch/multi-agent/agentctl.sh` is excellent. Copy and adapt:

```bash
cp scratch/multi-agent/agentctl.sh scratch/matrix-research/orchestrator/
chmod +x scratch/matrix-research/orchestrator/agentctl.sh
```

**Adaptation for matrix:** Use cell names as `<agent>-<topic>` format:
```bash
# Creates worktree at ../praxis-ai-agent-code-capture
./agentctl.sh add code capture
```

### 1.3 Define the matrix

**`orchestrator/matrix.yaml`**
```yaml
dimensions:
  domain: [code, create, write, observe, learn]
  stage: [capture, sense, explore, shape, formalize, commit, execute, sustain, close]

# 45 cells total (5 × 9)
# Work in batches of 8

batch_1:
  - code-capture
  - code-sense
  - code-explore
  - create-capture
  - create-sense
  - create-explore
  - write-capture
  - write-sense

batch_2:
  - write-explore
  - observe-capture
  - observe-sense
  - observe-explore
  - learn-capture
  - learn-sense
  - learn-explore
  - code-shape
  # ... continue as cells complete

phases:
  - name: key_influencers
    stop_condition: All cells complete before proceeding
    
  - name: deep_research
    stop_condition: All cells complete before proceeding
    
  - name: consolidation
    stop_condition: Human review and approval
```

---

## Step 2: Agent Instructions Template

**`orchestrator/agent-instructions.md`**

```markdown
# Research Agent Instructions

## Your Assignment
- **Domain:** {{DOMAIN}}
- **Stage:** {{STAGE}}
- **Cell ID:** {{DOMAIN}}-{{STAGE}}

## Current Phase: {{PHASE}}

---

### Phase 1: Key Influencers
**Goal:** Identify 5-10 authoritative sources for this domain×stage intersection.

**Output:** `docs/key-influencers.md`

| Field | Description |
|-------|-------------|
| Name/Title | Source name |
| Authority | Why authoritative for this cell |
| Key concepts | What they contribute |
| Citation/URL | Reference |

**Stop when:** List complete. Produce handoff. Do NOT proceed to Phase 2 until instructed.

---

### Phase 2: Deep Research
**Goal:** Extract first principles from each key influencer.

**Output:** `docs/research-notes.md`

Contents:
- Source-by-source analysis
- Patterns across sources
- Contradictions or debates
- Preliminary principles

**Stop when:** All sources processed. Produce handoff.

---

### Phase 3: Consolidation
**Goal:** Synthesize into canonical opinion document.

**Output:** `docs/opinion.md`

Format:
```
# {{DOMAIN}} × {{STAGE}} Opinions

## First Principles
1. [Principle]
   - Rationale:
   - Source(s):

## Aspirational Goals
- [Goal for this cell]

## Quality Gates
- [Checkpoint before progressing]

## Anti-Patterns
- [What to avoid]
```

**Stop when:** Draft complete. Await human review.

---

## Ownership Boundary
You own ONLY: `docs/` within your worktree.
Do NOT modify: root files, other cells, lockfiles.

## Handoff Format
Use the template in `../orchestrator/handoff-template.md` for all phase completions.
```

---

## Step 3: Handoff Template

**`orchestrator/handoff-template.md`** (adapted from `AGENT_HANDOFF_TEMPLATE.md`)

```markdown
# Handoff: {{DOMAIN}}-{{STAGE}}

## Summary
- **Phase completed:** [1/2/3]
- **What changed:** [brief description]

## Files Created/Modified
- `docs/key-influencers.md`
- `docs/research-notes.md`
- ...

## Key Findings (if applicable)
- [Notable discovery 1]
- [Notable discovery 2]

## Open Questions
- [Question 1]
- [Question 2]

## Ready For
- [ ] Phase 2 (Deep Research)
- [ ] Phase 3 (Consolidation)
- [ ] Human Review
- [ ] Integration/Merge
```

---

## Step 4: Batch Worktree Creation

**`orchestrator/create-batch.sh`**

```bash
#!/bin/bash
# Create worktrees for a batch of cells

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CELLS_DIR="$SCRIPT_DIR/../cells"

# Batch 1 cells
CELLS=(
  "code-capture"
  "code-sense"
  "code-explore"
  "create-capture"
  "create-sense"
  "create-explore"
  "write-capture"
  "write-sense"
)

cd "$SCRIPT_DIR/.."  # matrix-research directory

for cell in "${CELLS[@]}"; do
  domain=$(echo $cell | cut -d- -f1)
  stage=$(echo $cell | cut -d- -f2)
  
  echo "Creating worktree for $cell..."
  ./orchestrator/agentctl.sh add "$domain" "$stage" --dir "cells/$cell" 2>/dev/null || \
    echo "  (already exists or error)"
done

echo ""
echo "✓ Created worktrees for batch"
echo ""
echo "Next: Launch Claude in each cell directory"
```

---

## Step 5: Status Dashboard

**`orchestrator/status.sh`**

```bash
#!/bin/bash
# Check status of all cells

CELLS_DIR="../cells"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║            Matrix Research Status Dashboard               ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo ""

for cell in "$CELLS_DIR"/*/; do
  [ -d "$cell" ] || continue
  name=$(basename "$cell")
  
  # Check for phase completion markers
  if [ -f "$cell/docs/opinion.md" ]; then
    status="✓ Phase 3 Complete"
    color="\033[32m"  # green
  elif [ -f "$cell/docs/research-notes.md" ]; then
    status="◐ Phase 2 In Progress"
    color="\033[33m"  # yellow
  elif [ -f "$cell/docs/key-influencers.md" ]; then
    status="◔ Phase 1 Complete"
    color="\033[36m"  # cyan
  else
    status="○ Not Started"
    color="\033[90m"  # gray
  fi
  
  printf "${color}%-20s %s\033[0m\n" "$name" "$status"
done

echo ""
echo "╚═══════════════════════════════════════════════════════════╝"
```

---

## Step 6: Launching Agents

### Option A: tmux (recommended for 8 agents)

```bash
#!/bin/bash
# orchestrator/launch-tmux.sh

SESSION="matrix-research"
CELLS_DIR="../cells"

# Kill existing session if present
tmux kill-session -t $SESSION 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION -n "agents"

# Get list of cells
CELLS=($(ls -d "$CELLS_DIR"/*/ 2>/dev/null | head -8 | xargs -n1 basename))

for i in "${!CELLS[@]}"; do
  cell="${CELLS[$i]}"
  if [ $i -gt 0 ]; then
    tmux split-window -t $SESSION
    tmux select-layout -t $SESSION tiled
  fi
  tmux send-keys -t $SESSION "cd $CELLS_DIR/$cell && echo 'Cell: $cell' && claude" Enter
done

echo "Launching tmux session..."
tmux attach -t $SESSION
```

### Option B: iTerm2 / Multiple terminals

Open 8 terminals, each running:
```bash
cd scratch/matrix-research/cells/code-capture && claude
```

### Initial Prompt to Each Agent

```
Read ../orchestrator/agent-instructions.md

You are assigned to: [Domain] × [Stage]

Execute Phase 1 (Key Influencers). Stop when complete and produce handoff using ../orchestrator/handoff-template.md
```

---

## Step 7: Phase Advancement

When all agents complete a phase:

**`orchestrator/advance-phase.sh`**

```bash
#!/bin/bash
# Create .next-phase marker in all cells

PHASE="${1:-2}"
CELLS_DIR="../cells"

echo "Advancing all cells to Phase $PHASE..."

for cell in "$CELLS_DIR"/*/; do
  [ -d "$cell" ] || continue
  name=$(basename "$cell")
  
  echo "Phase $PHASE" > "$cell/.next-phase"
  echo "  → $name"
done

echo ""
echo "Done. Instruct agents to:"
echo "  cat .next-phase && proceed to Phase $PHASE"
```

---

## Step 8: Merge & Consolidation

After all cells complete Phase 3:

```bash
#!/bin/bash
# orchestrator/merge-all.sh

# Return to main branch
git checkout aspirational-opinion-framework

for cell in ../cells/*/; do
  [ -d "$cell" ] || continue
  name=$(basename "$cell")
  domain=$(echo $name | cut -d- -f1)
  stage=$(echo $name | cut -d- -f2)
  branch="agent/$domain/$stage"
  
  echo "Merging $branch..."
  git merge --no-ff "$branch" -m "research: merge $name opinions"
  
  # Copy final output
  mkdir -p "../output/$domain"
  cp "$cell/docs/opinion.md" "../output/$domain/$stage.md" 2>/dev/null
done

echo "✓ All cells merged"
```

---

## Definition of Done (per cell)

From the Multi-Agent Playbook:

- [ ] Phase 3 (Consolidation) complete
- [ ] Handoff produced with all sections filled
- [ ] Files only in `docs/` within worktree
- [ ] No undocumented behavior changes
- [ ] Ready for merge

---

## Quick Reference

| Action | Command |
|--------|---------|
| Bootstrap | `mkdir -p scratch/matrix-research/{orchestrator,cells,output}` |
| Create batch | `./orchestrator/create-batch.sh` |
| Launch agents | `./orchestrator/launch-tmux.sh` |
| Check status | `./orchestrator/status.sh` |
| Advance phase | `./orchestrator/advance-phase.sh 2` |
| Merge results | `./orchestrator/merge-all.sh` |

---

## Foreman Mental Model

From `scratch/multi-agent/forman.md`:

```
Claude = Brain (interprets plan, assigns tasks, reviews)
Git + Shell = Hands (execution infrastructure)
Human = Authority (approves phase transitions, merges)
```

**Claude can:**
- Create worktrees (when instructed)
- Follow explicit rules and boundaries
- Spawn and scope sub-agents
- Review against original spec

**Claude cannot:**
- Autonomously schedule work
- Persist state across sessions
- Enforce locks without external tooling

Until full autonomy exists, treat Claude as a **high-leverage foreman**, not a manager.

---

## Limitations

1. **Manual phase advancement** — no auto-detection of completion
2. **No cross-agent learning mid-phase** — agents don't see each other's work
3. **tmux recommended** — for the multiplexed view
4. **Human integration required** — merges need oversight

---

## Sources

- `scratch/multi-agent/MULTI_AGENT_PLAYBOOK.md` — Principles and collision avoidance
- `scratch/multi-agent/AGENT_HANDOFF_TEMPLATE.md` — Handoff structure
- `scratch/multi-agent/agentctl.sh` — Worktree management
- `scratch/multi-agent/forman.md` — Foreman mental model
