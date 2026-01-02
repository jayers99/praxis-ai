# Praxis Privacy Model

Version: 0.2
Status: Draft  
Scope: Cross-cutting control overlay for all Praxis domains and lifecycle stages

---

## 1. Purpose

Privacy in Praxis defines **how information may be stored, shared, processed, and externalized** throughout a project’s lifecycle.  
It is not a domain or stage; it is an **overlay** that constrains artifacts, tooling, collaboration, and AI usage.

Privacy is:

- Declared at project inception
- Enforceable through deterministic rules
- Reclassifiable mid-project with explicit migration steps

---

## 2. Privacy Levels (Canonical)

Praxis defines five privacy levels, ordered from least to most restrictive.

1. **Public**
2. **Public – Trusted Collaborators**
3. **Personal**
4. **Confidential**
5. **Restricted**

Each level defines the *maximum allowable exposure* for artifacts and workflows.

---

## 3. Privacy Level Definitions

### 3.1 Public

- **Intent**: Content is safe for unrestricted publication and broad collaboration.
- **Storage**: Public GitHub repositories permitted
- **AI / Tooling**: Any AI tools permitted; no secrets or proprietary data
- **Artifacts**: Full fidelity documentation allowed; real names and technologies acceptable
- **Collaboration**: Open, unrestricted

---

### 3.2 Public – Trusted Collaborators

- **Intent**: Content is broadly shareable but collaboration is intentionally limited.
- **Storage**: Public repositories allowed; write access restricted to named collaborators
- **AI / Tooling**: Any AI tools permitted; same content restrictions as Public
- **Artifacts**: Same as Public
- **Collaboration**: Read: public; write: trusted collaborators only
- **Notes**: This level controls *who may contribute*, not *what may be disclosed*

---

### 3.3 Personal

- **Intent**: Private to the author or trusted collaborators; low-to-moderate sensitivity.
- **Storage**: Private GitHub repositories allowed; mainstream cloud storage acceptable
- **AI / Tooling**: Consumer AI tools permitted; no credentials, secrets, or regulated identifiers
- **Artifacts**: Real structure allowed; avoid sensitive logs, screenshots, or configs
- **Collaboration**: Single user or small trusted group

---

### 3.4 Confidential

- **Intent**: Sensitive material requiring deliberate containment and abstraction.
- **Storage**: Private repositories only; prefer restricted or self-hosted solutions; encrypted backups recommended
- **AI / Tooling**: Restricted AI usage; redacted or abstracted inputs only; no raw logs, configs, or identifiers
- **Artifacts**: Sanitized architecture; tokenized names; no environment-specific detail
- **Collaboration**: Explicitly named collaborators; intentional access review

---

### 3.5 Restricted

- **Intent**: Single-custodian, maximum secrecy. Exposure must be minimized by design.
- **Storage**: No GitHub (public or private); local-only or encrypted vault storage; per-project encryption key; keys controlled solely by the author
- **AI / Tooling**: No external SaaS AI with raw content; local or offline models only; abstract summaries permitted, never source material
- **Artifacts**: Pattern-level abstraction only; no real names, topologies, logs, or configs; no screenshots of real systems
- **Collaboration**: None (unless explicit key-sharing model is defined)

---

## 4. Artifact Impact Rules

Privacy level defines the **maximum allowed specificity** across all artifacts.

Highest-impact artifacts:

- `README.md`
- `SOD.md`
- `architecture.md`
- ADRs
- Test data and logs

Rule of thumb:
> Higher privacy → more abstraction, less specificity

---

## 5. Lifecycle Integration

- Privacy level is declared at **Explore**
- Enforced during **Shape** and **Formalize**
- Must be honored during **Execute**
- Re-evaluated before **Commit**

---

## 6. Mid-Project Reclassification

### 6.1 Upgrade (less → more restrictive)

Required actions:

- Migrate storage to compliant location
- Sanitize or rewrite existing artifacts
- Rotate any exposed secrets or tokens
- Update collaboration and AI constraints

### 6.2 Downgrade (more → less restrictive)

Permitted only if:

- Sensitive material has been removed or rewritten
- Prior restricted artifacts are reviewed for safe disclosure

Downgrades are **discouraged by default**.

---

## 7. Pre-Project Capture (Observe Domain)

Raw captures in the Observe domain may occur *before* a project context exists—screenshots, brain dumps, web clippings collected in a scratch space.

### Default Handling

- All pre-project Observe artifacts default to **Personal** until explicitly classified
- AI processing of unclassified Observe artifacts is prohibited
- Promotion from Observe to another domain requires explicit privacy declaration
- Once assigned to a project, artifacts inherit the project's privacy level

### Rationale

Conservative defaults prevent accidental exposure. The cost of delayed AI processing is lower than the cost of leaked sensitive material. Users can always upgrade to a more restrictive level immediately upon capture if the material warrants it.

---

## 8. Praxis Metadata Integration

Each project declares privacy explicitly in `praxis.yaml`:

```yaml
domain: code
stage: formalize
privacy_level: confidential
environment: Home
```

### Validation Rules

| Rule | Severity | Trigger |
|------|----------|---------|
| Unknown privacy level | Error | Value not in allowed list |
| Privacy downgrade | Warning | `privacy_level` decreased from prior commit |
| Missing privacy declaration | Error | `privacy_level` field absent |

### Environment Override

The `PRAXIS_PRIVACY` environment variable can override the file-declared level for testing:

```bash
PRAXIS_PRIVACY=restricted praxis validate .
```

This is useful for CI pipelines that need to validate against stricter constraints.

---

## 9. AI Permission Modifiers by Privacy

Privacy level modifies the default AI permissions from the domain:

| Privacy Level | Effect on AI Permissions |
|---------------|--------------------------|
| Public | `generate`/`transform` → Ask, `publish` → Allowed |
| Public-Trusted | Default permissions (no modification) |
| Personal | Default permissions (no modification) |
| Confidential | All operations → Ask |
| Restricted | `generate`/`transform` → Blocked, `execute` → Blocked |

### Practical Impact

- **Public**: AI can suggest freely; publishing requires no special approval
- **Confidential**: Every AI operation requires explicit human approval
- **Restricted**: AI cannot generate or transform content; only suggest permitted

---

## 10. Summary

Privacy in Praxis is:

1. **Declared early** — no later than Explore stage
2. **Enforced consistently** — same rules across all domains
3. **Conservative by default** — unclassified material treated as Personal
4. **Upgrade-friendly** — moving to more restrictive is straightforward
5. **Downgrade-resistant** — moving to less restrictive requires explicit review

The privacy model ensures that sensitive material is protected throughout the lifecycle, regardless of domain or stage.

---

## References

- [Domains](domains.md) — Domain definitions and AI permissions
- [Lifecycle](lifecycle.md) — Stage definitions
- [SOD](sod.md) — Privacy and lifecycle interaction details
