# Praxis Knowledge Distillation Pipeline (PKDP)

PKDP is a **risk-tiered pipeline** for turning raw, unstructured inputs into **validated, decision-grade knowledge artifacts** suitable for long-term retention.

It is intentionally **non-decisional**: the output is meant to populate the research-library with high-quality knowledge and open questions, not to commit you to a plan.

## Canonical stages

**RTC → IDAS → SAD → CCR → ASR → HVA**

- **RTC** — Raw Thought Capture
- **IDAS** — Inquiry-Driven Analytical Synthesis
- **SAD** — Specialist Agent Dispatch
- **CCR** — Critical Challenge Review
- **ASR** — Adjudicated Synthesis & Resolution
- **HVA** — Human Validation & Acceptance

## Risk tiers (validation depth)

Risk tiers govern **validation depth**, not authority.

- **Tier 0:** RTC → IDAS
- **Tier 1:** RTC → IDAS → SAD → ASR
- **Tier 2:** RTC → IDAS → SAD → CCR → ASR
- **Tier 3:** RTC → IDAS → SAD → CCR → ASR → HVA

## Files created in a project

PKDP state is stored next to your project configuration:

- `pipeline.yaml` — pipeline state (current stage, tier, timestamps)
- `pipeline-runs/<pipeline_id>/...` — outputs per pipeline run

Stage outputs are written to canonical filenames:

- `pipeline-runs/<id>/rtc-output.md`
- `pipeline-runs/<id>/idas-output.md`
- `pipeline-runs/<id>/sad-dispatch.md`
- `pipeline-runs/<id>/sad-responses/*.md`
- `pipeline-runs/<id>/ccr-consolidated.md`
- `pipeline-runs/<id>/ccr-critiques/*.md`
- `pipeline-runs/<id>/asr-synthesis.md`
- `pipeline-runs/<id>/hva-decision.md`

## CLI usage

PKDP is exposed via the `praxis pipeline` command group.

### Initialize a pipeline

```bash
praxis pipeline init --tier 2 --corpus path/to/corpus
```

- `--tier` is an integer `0–3`
- `--corpus` can be a file or directory
- Use `--force` to replace an existing active pipeline

### Check pipeline status

```bash
praxis pipeline status
```

### Run a stage (or all remaining stages)

```bash
praxis pipeline run --stage rtc
praxis pipeline run --all
```

Note: the stage executors generate **templates and placeholder files** that you (and your specialists/challengers) complete. PKDP does not treat AI output as authoritative.

### Make the HVA decision

```bash
praxis pipeline accept --rationale "ready to ingest"
praxis pipeline reject --rationale "insufficient evidence"
praxis pipeline refine --to idas --rationale "need clearer questions"
```

## Using PKDP with AI assistants

- Treat PKDP artifacts as **knowledge work**, not a plan-of-record.
- Keep provenance: preserve links, sources, and uncertainty.
- CCR is meant to be adversarial (challenge assumptions, find blind spots) without turning into scope-setting.
