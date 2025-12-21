# Praxis Privacy Model

Version: 0.1  
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

**Intent**  
Content is safe for unrestricted publication and broad collaboration.

**Storage**
- Public GitHub repositories permitted

**AI / Tooling**
- Any AI tools permitted
- No secrets or proprietary data

**Artifacts**
- Full fidelity documentation allowed
- Real names and technologies acceptable

**Collaboration**
- Open, unrestricted

---

### 3.2 Public – Trusted Collaborators

**Intent**  
Content is broadly shareable but collaboration is intentionally limited.

**Storage**
- Public repositories allowed
- Write access restricted to named collaborators

**AI / Tooling**
- Any AI tools permitted
- Same content restrictions as Public

**Artifacts**
- Same as Public

**Collaboration**
- Read: public
- Write: trusted collaborators only

**Notes**
- This level controls *who may contribute*, not *what may be disclosed*

---

### 3.3 Personal

**Intent**  
Private to the author; low-to-moderate sensitivity.

**Storage**
- Private GitHub repositories allowed
- Mainstream cloud storage acceptable

**AI / Tooling**
- Consumer AI tools permitted
- No credentials, secrets, or regulated identifiers

**Artifacts**
- Real structure allowed
- Avoid sensitive logs, screenshots, or configs

**Collaboration**
- Optional, small trusted group

---

### 3.4 Confidential

**Intent**  
Sensitive material requiring deliberate containment and abstraction.

**Storage**
- Private repositories only
- Prefer restricted or self-hosted solutions
- Encrypted backups recommended

**AI / Tooling**
- Restricted AI usage
- Redacted or abstracted inputs only
- No raw logs, configs, or identifiers

**Artifacts**
- Sanitized architecture
- Tokenized names
- No environment-specific detail

**Collaboration**
- Explicitly named collaborators
- Intentional access review

---

### 3.5 Restricted

**Intent**  
Single-custodian, maximum secrecy. Exposure must be minimized by design.

**Storage**
- No GitHub (public or private)
- Local-only or encrypted vault storage
- Per-project encryption key
- Keys controlled solely by the author

**AI / Tooling**
- No external SaaS AI with raw content
- Local or offline models only
- Abstract summaries permitted, never source material

**Artifacts**
- Pattern-level abstraction only
- No real names, topologies, logs, or configs
- No screenshots of real systems

**Collaboration**
- None (unless explicit key-sharing model is defined)

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

## 7. Praxis Metadata Integration (Planned)

Each project should declare privacy explicitly, e.g.:

```yaml
privacy_level: confidential

